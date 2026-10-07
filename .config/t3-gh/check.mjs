// Run with node for terminal behavior, or T3's binary with ELECTRON_RUN_AS_NODE=1
// for native app behavior. Supply the expected GitHub login as the argument.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { homedir } from 'node:os';

const expected = process.argv[2];
assert.ok(expected, 'Supply the expected GitHub login');
const env = { ...process.env };
delete env.GH_TOKEN;
delete env.GITHUB_TOKEN;
delete env.GH_DEBUG;
const run = (binary, args) => {
  const result = spawnSync(binary, args, { env, encoding: 'utf8' });
  assert.equal(result.status, 0, `${binary} failed`);
  return result.stdout.trim();
};
const shim = `${homedir()}/.config/t3-gh/bin/gh`;
const resolved = run('/bin/zsh', ['-ilc', 'command -v gh']);
assert.equal(resolved.split('\n').at(-1), shim, 'Fresh login shell must find the shim');
const status = JSON.parse(run(shim, ['auth', 'status', '--hostname', 'github.com', '--json', 'hosts']));
assert.equal(status.hosts['github.com'].find((account) => account.active && account.state === 'success')?.login, expected);
assert.equal(run(shim, ['api', 'user', '--jq', '.login']), expected);
console.log(`PASS: fresh login shell, gh discovery, and GitHub API identify ${expected}`);
