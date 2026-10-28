#!/usr/bin/env python3
"""Check account independence and preservation using a disposable fixture."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("provision", Path(__file__).with_name("provision-claude.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


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
            (own / "SKILL.md").write_text("Live edit")
            for config in accounts:
                self.assertEqual((config / "skills/own/SKILL.md").read_text(), "Live edit")
            self.assertIn("Keep my account rule", (personal / "CLAUDE.md").read_text())
            self.assertEqual(json.loads((personal / "settings.json").read_text())["model"], "sonnet")
            self.assertNotEqual((accounts[0] / "skills/test/SKILL.md").read_text(), "Personal edit")
            left = {p.stat().st_ino for p in accounts[0].rglob("*") if p.is_file() and not {"plugins", "own"} & set(p.parts)}
            right = {p.stat().st_ino for p in accounts[1].rglob("*") if p.is_file() and not {"plugins", "own"} & set(p.parts)}
            self.assertFalse(left & right)


if __name__ == "__main__":
    unittest.main()
