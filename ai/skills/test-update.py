#!/usr/bin/env python3
"""Check the vendored-skill three-way merge and the host-name lint on a disposable fixture."""

from importlib.machinery import SourceFileLoader
from pathlib import Path
import subprocess
import tempfile
import unittest

update = SourceFileLoader("update", str(Path(__file__).with_name("update"))).load_module()


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, text=True, capture_output=True).stdout.strip()


class UpdateTest(unittest.TestCase):
    def test_merge_keeps_local_edits_and_applies_upstream(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            update.ROOT, update.SOURCES = root, root / ".sources"
            repo = update.SOURCES / "up"
            (repo / "skills/s").mkdir(parents=True)
            git(repo, "init", "-q", "-b", "main")
            (repo / "skills/s/SKILL.md").write_text("one\ntwo\nthree\nfour\n")
            (repo / "skills/s/old.md").write_text("old\n")
            git(repo, "add", "-A")
            git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base")
            base = git(repo, "rev-parse", "HEAD")

            vendored = root / "common/s"
            vendored.mkdir(parents=True)
            (vendored / "SKILL.md").write_text("ONE local\ntwo\nthree\nfour\n")
            (vendored / "old.md").write_text("old\n")

            (repo / "skills/s/SKILL.md").write_text("one\ntwo\nthree\nFOUR upstream\n")
            (repo / "skills/s/old.md").unlink()
            (repo / "skills/s/new.md").write_text("new\n")
            git(repo, "add", "-A")
            git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "change")
            head = git(repo, "rev-parse", "HEAD")

            spec = {"repo": "up", "path": "skills/s", "base": base}
            self.assertEqual(update.merge_skill("s", spec, head), [])
            self.assertEqual((vendored / "SKILL.md").read_text(), "ONE local\ntwo\nthree\nFOUR upstream\n")
            self.assertFalse((vendored / "old.md").exists())
            self.assertEqual((vendored / "new.md").read_text(), "new\n")
            self.assertEqual(spec["base"], head)

            (vendored / "SKILL.md").write_text("ONE local\ntwo\nthree\nFOUR mine\n")
            (repo / "skills/s/SKILL.md").write_text("one\ntwo\nthree\nFOUR again\n")
            git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qam", "clash")
            notes = update.merge_skill("s", spec, git(repo, "rev-parse", "HEAD"))
            self.assertIn("conflict markers", notes[0])

    def test_lint_flags_hosts_but_not_css_cursor(self):
        self.assertTrue(update.BANNED.search("Spawn a Task subagent with subagent_type"))
        self.assertTrue(update.BANNED.search("use grok-4.7 for explorers"))
        self.assertFalse(update.BANNED.search(update.CSS_CURSOR.sub("", "a { cursor: pointer; }")))


if __name__ == "__main__":
    unittest.main()
