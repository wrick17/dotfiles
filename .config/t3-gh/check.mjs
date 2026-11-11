// Run with node for terminal behavior, or T3's binary with ELECTRON_RUN_AS_NODE=1
// for native app behavior. Checks that the gh shim picks the account per repo.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync } from 'node:fs';
import { homedir, tmpdir } from 'node:os';
import { join } from 'node:path';

const PERSONAL = 'wrick17';
const WORK = 'pratyush-poddar_seq';
const env = { ...process.env };
for (const name of ['GH_TOKEN', 'GITHUB_TOKEN', 'GH_DEBUG', 'GH_REPO', 'GH_SHIM_PRINT_LOGIN']) delete env[name];
const run = (binary, args, opts = {}) => {
  const result = spawnSync(binary, args, { env, encoding: 'utf8', ...opts });
  assert.equal(result.status, 0, `${binary} ${args.join(' ')} failed: ${result.stderr.trim()}`);
  return result.stdout.trim();
};
const shim = `${homedir()}/.config/t3-gh/bin/gh`;
const dotfiles = `${homedir()}/dotfiles`;
const resolved = run('/bin/zsh', ['-ilc', 'command -v gh']);
assert.equal(resolved.split('\n').at(-1), shim, 'Fresh login shell must find the shim');

const scratch = mkdtempSync(join(process.env.TMPDIR || tmpdir(), 'gh-check-'));
try {
  const repo = (name, remotes) => {
    const dir = join(scratch, name);
    run('git', ['init', '-q', dir]);
    for (const [remote, url] of remotes) run('git', ['-C', dir, 'remote', 'add', remote, url]);
    return dir;
  };
  const workRepo = repo('work', [['origin', 'git@github.com:Sequoia-Engineering/example.git']]);
  const forkRepo = repo('fork', [
    ['origin', 'git@personal:wrick17/example.git'],
    ['upstream', 'git@github.com:Sequoia-Engineering/example.git'],
  ]);
  run('git', ['-C', forkRepo, 'config', 'remote.upstream.gh-resolved', 'base']);
  const outside = join(scratch, 'outside');
  mkdirSync(outside);
  const workToken = run('/opt/homebrew/bin/gh', ['auth', 'token', '--hostname', 'github.com', '--user', WORK]);

  // Live calls: the API reports which account the token belongs to.
  const live = [
    ['personal repo', dotfiles, {}, PERSONAL],
    ['work repo', workRepo, {}, WORK],
    ['outside any repo', outside, {}, WORK],
    ['personal repo with GITHUB_TOKEN=work', dotfiles, { GITHUB_TOKEN: workToken }, PERSONAL],
  ];
  for (const [name, cwd, extraEnv, expected] of live) {
    assert.equal(run(shim, ['api', 'user', '--jq', '.login'], { cwd, env: { ...env, ...extraEnv } }), expected, name);
    console.log(`PASS: ${name} -> ${expected}`);
  }
  // gh api has no -R, so prove the -R route with a call only the repo admin (wrick17) can make.
  run(shim, ['secret', 'list', '-R', 'wrick17/dotfiles'], { cwd: outside });
  console.log(`PASS: -R wrick17/dotfiles outside -> ${PERSONAL} (admin-only call succeeded)`);
  const admin = run(shim, ['api', 'https://api.github.com/repos/wrick17/dotfiles', '--jq', '.permissions.admin'], { cwd: workRepo });
  assert.equal(admin, 'true', 'full API URL from work repo');
  console.log(`PASS: api full URL from work repo -> ${PERSONAL} (read-only, admin permission seen)`);

  // Resolver-only: the shim prints the login it would use and exits without a token.
  const resolve = [
    ['--body URL in work repo', workRepo, {}, ['pr', 'create', '--body', 'https://github.com/wrick17/dotfiles'], WORK],
    ['gh-resolved upstream beats personal origin', forkRepo, {}, ['run', 'list'], WORK],
    ['GH_REPO=work with repos/wrick17 endpoint', outside, { GH_REPO: 'Sequoia-Engineering/example' }, ['api', 'repos/wrick17/dotfiles'], PERSONAL],
    ['GH_REPO=personal outside', outside, { GH_REPO: 'wrick17/dotfiles' }, ['api', 'user'], PERSONAL],
    ['-R is case-insensitive', outside, {}, ['pr', 'list', '-R', 'WRICK17/dotfiles'], PERSONAL],
    ['repo view URL', workRepo, {}, ['repo', 'view', 'https://github.com/wrick17/dotfiles'], PERSONAL],
    ['pr view -c URL', workRepo, {}, ['pr', 'view', '-c', 'https://github.com/wrick17/dotfiles/pull/1'], PERSONAL],
    ['pr merge -s URL', workRepo, {}, ['pr', 'merge', '-s', 'https://github.com/wrick17/dotfiles/pull/1'], PERSONAL],
    ['repo fork --remote OWNER/REPO', workRepo, {}, ['repo', 'fork', '--remote', 'wrick17/dotfiles'], PERSONAL],
    ['search repo: qualifier', workRepo, {}, ['search', 'issues', 'repo:wrick17/dotfiles bug'], PERSONAL],
  ];
  for (const [name, cwd, extraEnv, args, expected] of resolve) {
    const login = run(shim, args, { cwd, env: { ...env, ...extraEnv, GH_SHIM_PRINT_LOGIN: '1' } });
    assert.equal(login, expected, name);
    console.log(`PASS: ${name} -> ${expected}`);
  }
} finally {
  rmSync(scratch, { recursive: true, force: true });
}
