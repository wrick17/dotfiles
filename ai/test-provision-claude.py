#!/usr/bin/env python3
"""Check account independence and preservation using a disposable fixture."""

import contextlib
import importlib.machinery
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("provision", Path(__file__).with_name("provision-claude.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
loader = importlib.machinery.SourceFileLoader("apply", str(Path(__file__).with_name("apply")))
apply = importlib.util.module_from_spec(importlib.util.spec_from_loader("apply", loader))
loader.exec_module(apply)


class ProvisionTest(unittest.TestCase):
    @patch("pathlib.Path.home")
    def test_materialize_and_preserve_independent_accounts(self, home):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            home.return_value = root / "home"
            module.AI = root / "ai"
            source = module.AI
            for scope in ("common", "work", "personal"):
                (source / scope).mkdir(parents=True)
                (source / "skills/third-party" / scope).mkdir(parents=True)
                (source / "skills/mine" / scope).mkdir(parents=True)
            (source / "work/claude.md").write_text("@../common/claude.md\n@instructions.md\n")
            (source / "work/instructions.md").write_text("Use ~/skills/third-party/work/test/SKILL.md\n")
            (source / "common/claude.md").write_text("@global.md\n")
            (source / "common/global.md").write_text("Use ~/skills/third-party/common/test/SKILL.md\n")
            (source / "work/claude-session-rules.sh").write_text("#!/bin/bash\nexit 0\n")
            upstream = root / "upstream"
            upstream.mkdir()
            (upstream / "SKILL.md").write_text("# Skill\n[reference](reference.md)\n")
            (upstream / "reference.md").symlink_to(source / "common/global.md")
            (source / "skills/third-party/common/test").symlink_to(upstream)
            own = source / "skills/mine/common/own"
            own.mkdir()
            (own / "SKILL.md").write_text("# Own\n")
            accounts = [root / "work", root / "max"]
            for config in accounts:
                (config / "skills").mkdir(parents=True)
                (config / "skills/test").symlink_to(upstream)
                (config / "skills/own").mkdir()
                (config / "skills/own/SKILL.md").write_text("Stale own copy")
                (config / "CLAUDE.md").write_text("@" + str(config / "rules/work/claude.md") + "\nKeep my account rule\n")
                (config / "rules/common").mkdir(parents=True)
                (config / "rules/common/global.md").write_text("Stale snapshot")
                (config / "settings.json").write_text(json.dumps({"distinct": config.name}))
                (config / ".claude.json").write_text("auth sentinel")
                (config / "plugins").mkdir()
                (config / "plugins/sentinel").symlink_to(upstream)
                module.provision(config, "work", "opus" if config.name == "max" else "haiku")
                self.assertIn("Keep my account rule", (config / "CLAUDE.md").read_text())
                self.assertIn("@" + str(source / "work/claude.md") + "\n", (config / "CLAUDE.md").read_text())
                self.assertFalse((config / "rules").exists())
                self.assertEqual((config / "skills/own").resolve(), own.resolve())
                self.assertFalse(any(p.is_symlink() for p in (config / "skills").rglob("*") if "own" not in p.parts))
                self.assertEqual((config / ".claude.json").read_text(), "auth sentinel")
                self.assertTrue((config / "plugins/sentinel").is_symlink())
                settings = json.loads((config / "settings.json").read_text())
                self.assertEqual(settings["distinct"], config.name)
                self.assertIn(str(config / "hooks"), settings["hooks"]["SessionStart"][0]["hooks"][0]["command"])
            personal = accounts[1]
            (personal / "skills/test/SKILL.md").write_text("Personal edit")
            settings = json.loads((personal / "settings.json").read_text())
            settings["model"] = "sonnet"
            (personal / "settings.json").write_text(json.dumps(settings))
            (upstream / "SKILL.md").write_text("Updated shared source")
            for config in accounts:
                module.provision(config, "work", "opus")
            self.assertEqual((personal / "skills/test/SKILL.md").read_text(), "Personal edit")
            module.provision(personal, "work", "opus", refresh=True)
            self.assertEqual((personal / "skills/test/SKILL.md").read_text(), "Updated shared source")
            (own / "SKILL.md").write_text("Live edit")
            (personal / "skills/renamed").symlink_to(source / "skills/mine/work/renamed")
            module.provision(personal, "work", "opus")
            self.assertFalse((personal / "skills/renamed").is_symlink())
            for config in accounts:
                self.assertEqual((config / "skills/own/SKILL.md").read_text(), "Live edit")
            self.assertIn("Keep my account rule", (personal / "CLAUDE.md").read_text())
            self.assertEqual(json.loads((personal / "settings.json").read_text())["model"], "sonnet")
            self.assertNotEqual((accounts[0] / "skills/test/SKILL.md").read_text(), "Personal edit")
            left = {p.stat().st_ino for p in accounts[0].rglob("*") if p.is_file() and not {"plugins", "own"} & set(p.parts)}
            right = {p.stat().st_ino for p in accounts[1].rglob("*") if p.is_file() and not {"plugins", "own"} & set(p.parts)}
            self.assertFalse(left & right)
            # core.hooksPath is set only when it would not disable hooks already active in .git/hooks.
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            git_config = ["git", "-C", str(root), "config", "--get", "core.hooksPath"]
            active = root / ".git/hooks/pre-commit"
            active.write_text("#!/bin/sh\n")
            active.chmod(0o755)
            module.provision(personal, "work", "opus")
            self.assertEqual(subprocess.run(git_config, capture_output=True, text=True).stdout, "")
            active.unlink()
            module.provision(personal, "work", "opus")
            self.assertEqual(subprocess.run(git_config, capture_output=True, text=True).stdout.strip(), "ai/git-hooks")

    def test_apply_saves_accounts_and_registers_session_temp_once(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()  # provision-claude.py resolves its path; macOS temp dirs sit behind /var -> /private/var
            ai = root / "repo/ai"
            for scope in ("common", "work", "personal"):
                (ai / "skills/third-party" / scope).mkdir(parents=True)
                (ai / "skills/mine" / scope).mkdir(parents=True)
                (ai / scope).mkdir()
            (ai / "work/claude-session-rules.sh").write_text("#!/bin/bash\nexit 0\n")
            # A copy, not a link: provision-claude.py resolves its own path to find the fixture ai/ (no .git, so git config is untouched).
            shutil.copy(Path(__file__).with_name("provision-claude.py"), ai)
            work, personal = root / "work", root / "personal"
            env = {"HOME": str(root / "home"), "CODEX_HOME": str(root / "no-codex"), "AGENT_MEMORY_SOURCE": str(root / "no-memory")}

            def run(*argv):
                with patch.object(apply, "AI", ai), patch.object(apply, "ACCOUNTS", root / "config/ai-accounts"), \
                        patch("sys.argv", ["apply", *argv]), patch.dict(os.environ, env), contextlib.redirect_stdout(io.StringIO()), \
                        contextlib.redirect_stderr(io.StringIO()):
                    return apply.main()

            self.assertEqual(run(), 2)
            self.assertEqual(run("--since", "HEAD"), 0)  # git hook mode only warns
            self.assertEqual(run("--account", str(work), "work", "haiku", "--account", str(personal), "personal", "opus"), 0)
            self.assertEqual(len((root / "config/ai-accounts").read_text().splitlines()), 2)
            self.assertEqual(run(), 0)
            self.assertEqual(run(), 0)
            command = "bash " + str(ai / "common/session-temp.sh") + " claude"
            expected = {"SessionStart": {"type": "command", "command": command, "timeout": 30, "async": True},
                        "SessionEnd": {"type": "command", "command": command, "timeout": 30}}
            # An entry from before the flag existed gains it on the next run.
            settings = json.loads((personal / "settings.json").read_text())
            settings["hooks"]["SessionStart"][0]["hooks"][0].pop("async")
            (personal / "settings.json").write_text(json.dumps(settings))
            self.assertEqual(run(), 0)
            for config in (work, personal):
                hooks = json.loads((config / "settings.json").read_text())["hooks"]
                for event in ("SessionStart", "SessionEnd"):
                    entries = [h for g in hooks[event] for h in g["hooks"] if "session-temp.sh" in h["command"]]
                    self.assertEqual(entries, [expected[event]])
            rules = [h for g in json.loads((work / "settings.json").read_text())["hooks"]["SessionStart"] for h in g["hooks"]
                     if "claude-session-rules.sh" in h["command"]]
            self.assertEqual(len(rules), 1)
            # An empty path means the cwd, which under a git hook is this repo, so it is refused when saved and when read.
            with self.assertRaises(SystemExit):
                run("--account", "", "work", "opus")
            (root / "config/ai-accounts").write_text("'' work opus\n")
            self.assertEqual(run(), 1)
            self.assertFalse((ai.parent / "settings.json").exists())
            self.assertEqual(run("--account", str(personal), "personal", "opus"), 0)
            self.assertEqual((root / "config/ai-accounts").read_text().split(), [str(personal), "personal", "opus"])


    def test_agent_memory_hooks_replace_legacy_and_keep_foreign(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            ai = root / "ai"
            for scope in ("common", "personal"):
                (ai / "skills/third-party" / scope).mkdir(parents=True)
                (ai / "skills/mine" / scope).mkdir(parents=True)
            config, codex = root / "account", root / "codex"
            config.mkdir()
            codex.mkdir()
            bin = str(root / "home/.agent-memory/bin/agent-memory")
            legacy = "/usr/bin/env CLAUDE_CONFIG_DIR=" + str(config) + " /old/node " + bin + ".mjs hook claude-code"
            foreign = {"type": "command", "command": "ponytail hook", "timeout": 7}
            (config / "settings.json").write_text(json.dumps({"hooks": {
                "SessionStart": [{"hooks": [foreign]}, {"hooks": [{"type": "command", "command": legacy, "timeout": 10}]}],
                "Stop": [{"hooks": [{"type": "command", "command": legacy, "async": True}]}],
                "PostToolUse": [{"matcher": "^mcp__t3", "hooks": [foreign, {"type": "command", "command": legacy}]}]}}))
            installed = {"Stop": [{"hooks": [{"type": "command", "command": bin + " hook claude-code", "async": True}]}],
                         "SessionStart": [{"hooks": [{"type": "command", "command": bin + " hook claude-code", "timeout": 3}]}],
                         "PostToolUseFailure": [{"hooks": [{"type": "command", "command": bin + " hook claude-code", "timeout": 5}]}]}
            with patch.object(module, "AI", ai), patch.dict(os.environ, {"HOME": str(root / "home"), "CODEX_HOME": str(codex)}), \
                    contextlib.redirect_stdout(io.StringIO()):
                for _ in range(2):
                    module.provision(config, "personal", "opus", agent_memory=("/abs/node", installed))
                first = (config / "settings.json").read_text()
                module.provision(config, "personal", "opus", agent_memory=("/abs/node", installed))
                self.assertEqual((config / "settings.json").read_text(), first)
                module.provision(config, "personal", "opus")  # skipped step: agent-memory entries stay
                self.assertEqual((config / "settings.json").read_text(), first)

                hooks = json.loads(first)["hooks"]
                prefix = "/usr/bin/env CLAUDE_CONFIG_DIR=" + str(config) + " /abs/node "
                mine = {e: [h for g in gs for h in g["hooks"] if "agent-memory" in h["command"]] for e, gs in hooks.items()}
                self.assertEqual({e: hs for e, hs in mine.items() if hs},
                                 {e: [{**g[0]["hooks"][0], "command": prefix + bin + " hook claude-code"}] for e, g in installed.items()})
                self.assertEqual(hooks["SessionStart"][0], {"hooks": [foreign]})
                self.assertEqual(hooks["PostToolUse"], [{"matcher": "^mcp__t3", "hooks": [foreign]}])
                # A current install names its stable bin/node link: only the account env is added, never a second Node.
                current = bin[:-len("agent-memory")] + "node " + bin + " hook claude-code"
                stable = {e: [{"hooks": [{**g[0]["hooks"][0], "command": current}]}] for e, g in installed.items()}
                module.provision(config, "personal", "opus", agent_memory=("/abs/node", stable))
                hooks = json.loads((config / "settings.json").read_text())["hooks"]
                mine = [h["command"] for gs in hooks.values() for g in gs for h in g["hooks"] if "agent-memory" in h["command"]]
                self.assertEqual(mine, ["/usr/bin/env CLAUDE_CONFIG_DIR=" + str(config) + " " + current] * len(installed))
                module.provision(config, "personal", "opus", agent_memory=("/abs/node", installed))  # back to the old form for the checks below

                (root / "agent.json").write_text(json.dumps({"server": "s", "token_file": "t", "facts": {"timeout_ms": 2000}, "inject": {"enabled": False}}))
                (root / "agent.json").chmod(0o600)
                self.assertTrue(apply.enable_agent_memory(root / "agent.json"))
                self.assertFalse(apply.enable_agent_memory(root / "agent.json"))
                self.assertEqual(json.loads((root / "agent.json").read_text()), {"server": "s", "token_file": "t", "inject": {"enabled": False},
                                 "facts": {"timeout_ms": 2000, "inject": True, "synthesis": True}, "loop_guard": {"enabled": True}})
                self.assertEqual((root / "agent.json").stat().st_mode & 0o777, 0o600)
                (root / "agent.json").chmod(0o644)  # flags already on: the mode is still made private
                self.assertFalse(apply.enable_agent_memory(root / "agent.json"))
                self.assertEqual((root / "agent.json").stat().st_mode & 0o777, 0o600)

                # Codex: the hand-written tables go, the managed block is written once, everything else stays byte for byte.
                kept = 'model = "x"\n\n[hooks]\n[hooks.state."a:session_start:0:0"]\ntrusted_hash = "h"\n\n[[hooks.Stop]]\n[[hooks.Stop.hooks]]\ntype = "command"\ncommand = "rtk hook codex-other"\n\n[agents]\nmax = 10\n\n'
                old = ('# Agent Memory capture hooks (owner go-live).\n[[hooks.SessionEnd]]\n[[hooks.SessionEnd.hooks]]\ntype = "command"\n'
                       'command = "/usr/bin/env CLAUDE_CONFIG_DIR=/p /old/node ' + bin + '.mjs hook codex"\ntimeout = 3\n')
                (codex / "config.toml").write_text(kept + old)
                toml = '[[hooks.SessionEnd]]\n[[hooks.SessionEnd.hooks]]\ntype = "command"\ncommand = "' + bin + ' hook codex"\ntimeout = 3\n'
                if sys.version_info < (3, 11):  # no tomllib: the Codex step only warns and leaves the file alone
                    self.assertTrue(apply.write_codex_hooks("/abs/node", toml).startswith("Warning:"))
                    self.assertEqual((codex / "config.toml").read_text(), kept + old)
                    self.skipTest("the Codex TOML cases need Python 3.11 or newer")
                apply.write_codex_hooks("/abs/node", toml)
                text = (codex / "config.toml").read_text()
                self.assertEqual(apply.write_codex_hooks("/abs/node", toml), "Codex: Agent Memory hooks unchanged")
                self.assertEqual(text, kept + "\n" + apply.BEGIN + toml.replace('command = "', 'command = "/abs/node ') + apply.END)
                block = "\n" + apply.BEGIN + toml.replace('command = "', 'command = "/abs/node ') + apply.END
                # A current install names its stable bin/node link: the block replaces the old one and keeps the command as printed.
                stable = toml.replace('command = "', 'command = "' + bin[:-len("agent-memory")] + 'node ')
                apply.write_codex_hooks("/abs/node", stable)
                self.assertEqual((codex / "config.toml").read_text(), kept + "\n" + apply.BEGIN + stable + apply.END)
                # Headers with trailing comments end the old table: neither [agents] nor the unrelated hook after it is removed.
                after = ('[agents] # worker limits\nmax = 10\n\n[[hooks.Stop]]\n[[hooks.Stop.hooks]] # unrelated hook\n'
                         'type = "command"\ncommand = "rtk hook codex-other"\n')
                for tail in (after, after.replace("[agents] # worker limits\nmax = 10\n\n", "")):
                    (codex / "config.toml").write_text('model = "x"\n\n' + old + tail)
                    apply.write_codex_hooks("/abs/node", toml)
                    self.assertEqual((codex / "config.toml").read_text(), 'model = "x"\n\n' + tail + block)
                # An edit that would change anything but agent-memory hooks, or a file that is not TOML, keeps the file as it was.
                # A file whose only hooks were agent-memory ones loses its emptied [hooks] table.
                (codex / "config.toml").write_text(old)
                apply.write_codex_hooks("/abs/node", toml)
                self.assertEqual((codex / "config.toml").read_text(), block)
                # A nested-array line looks like a header to the text edit, so the edit is refused instead of breaking the file.
                for broken in ('[[hooks.Stop]]\n[[hooks.Stop.hooks]]\ncommand = "' + bin + ' hook codex"\nargs = [\n["a"]\n]\n',
                               old + "[broken\n"):
                    (codex / "config.toml").write_text(broken)
                    self.assertTrue(apply.write_codex_hooks("/abs/node", toml).startswith("Warning:"))
                    self.assertEqual((codex / "config.toml").read_text(), broken)

    @unittest.skipUnless((Path.home() / "Projects/personal/memory/local/agent-memory.mjs").is_file() and apply.find_node(), "needs the memory checkout and Node 24")
    def test_apply_installs_agent_memory_from_checkout(self):
        """Runs the real client's install into a disposable home, so the parsed output contract is checked against the client."""
        source = Path.home() / "Projects/personal/memory"
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            ai = root / "repo/ai"
            for scope in ("common", "personal"):
                (ai / "skills/third-party" / scope).mkdir(parents=True)
                (ai / "skills/mine" / scope).mkdir(parents=True)
            shutil.copy(Path(__file__).with_name("provision-claude.py"), ai)
            home, account = root / "home", root / "account"
            (home / ".codex").mkdir(parents=True)
            # The fake HOME hides fnm's default dirs, so put the real Node 24 first on PATH.
            path = str(Path(apply.find_node()).parent) + os.pathsep + os.environ.get("PATH", "")
            env = {"HOME": str(home), "CODEX_HOME": str(home / ".codex"), "AGENT_MEMORY_SOURCE": str(source), "PATH": path}
            with patch.object(apply, "AI", ai), patch.object(apply, "ACCOUNTS", root / "config/ai-accounts"), \
                    patch.object(apply, "load_launchd", lambda plist: "launchd skipped in test"), patch.dict(os.environ, env), \
                    patch("sys.argv", ["apply", "--account", str(account), "personal", "opus"]), contextlib.redirect_stdout(io.StringIO()), \
                    contextlib.redirect_stderr(io.StringIO()):
                os.environ.pop("AGENT_MEMORY_HOME", None)
                self.assertEqual(apply.main(), 0)
                codex_file = home / ".codex/config.toml"
                settings, codex = (account / "settings.json").read_text(), codex_file.exists() and codex_file.read_text()
                self.assertEqual(apply.main(), 0)
                self.assertEqual((account / "settings.json").read_text(), settings)
                self.assertEqual(codex_file.exists() and codex_file.read_text(), codex)
            config = home / ".agent-memory/config.json"
            self.assertEqual(config.stat().st_mode & 0o777, 0o600)
            self.assertIn("server", json.loads(config.read_text()))
            bin = str(home / ".agent-memory/bin/agent-memory")
            hooks = json.loads(settings)["hooks"]
            events = {e for e, gs in hooks.items() for g in gs for h in g["hooks"] if bin + " hook claude-code" in h["command"]}
            self.assertEqual(events, {"Stop", "SessionEnd", "SessionStart", "PreCompact", "PostToolUse", "PostToolUseFailure"})
            start = [h for g in hooks["SessionStart"] for h in g["hooks"] if "agent-memory" in h["command"]]
            self.assertEqual(start[0]["timeout"], 3)
            # Every command runs through the client's stable bin/node link, never with a second Node in front.
            node = str(home / ".agent-memory/bin/node")
            commands = {h["command"] for gs in hooks.values() for g in gs for h in g["hooks"] if "agent-memory" in h["command"]}
            self.assertEqual(commands, {"/usr/bin/env CLAUDE_CONFIG_DIR=" + str(account) + " " + node + " " + bin + " hook claude-code"})
            if sys.version_info >= (3, 11):
                self.assertEqual(codex.count('command = "' + node + " " + bin + ' hook codex"'), 5)  # Stop, SessionEnd, SessionStart, PreCompact, PostToolUse
                self.assertEqual(codex.count(" hook codex"), 5)
            else:
                self.assertFalse(codex)  # no tomllib: the Codex step is skipped, the rest still applies


if __name__ == "__main__":
    unittest.main()
