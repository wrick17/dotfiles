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
            env = {"HOME": str(root / "home"), "CODEX_HOME": str(root / "no-codex")}

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


if __name__ == "__main__":
    unittest.main()
