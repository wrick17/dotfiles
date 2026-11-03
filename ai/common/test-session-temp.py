#!/usr/bin/env python3
"""Check session-temp.sh ownership cleanup against a disposable temp root."""

import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import time
import unittest


SCRIPT = Path(__file__).with_name("session-temp.sh")
DEAD_PID = 999999  # above macOS and Linux default pid_max, so never a running process
OLD_START = "Mon Jan 1 00:00:00 2026"


def start_time(pid):
    # The form the script stores: C locale, UTC, single-spaced.
    out = subprocess.run(["ps", "-o", "lstart=", "-p", str(pid)], capture_output=True, text=True,
                         env={**os.environ, "LC_ALL": "C", "TZ": "UTC"}).stdout
    return " ".join(out.split())


class SessionTempTest(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)  # background deletes may still run
        self.addCleanup(folder.cleanup)
        self.base = Path(folder.name)
        self.claude = self.base / f"claude-{os.getuid()}" / "project"
        self.claude.parent.mkdir(mode=0o700)  # Claude creates its root at startup
        self.config = self.base / "config"
        (self.config / "sessions").mkdir(parents=True)
        # HOME too, so the script's default ~/.claude registry is the fixture's, not the machine's.
        (self.base / "home").mkdir()
        self.env = {**os.environ, "SESSION_TEMP_BASE": str(self.base), "CLAUDE_CONFIG_DIR": str(self.config),
                    "HOME": str(self.base / "home")}
        # Register the machine's running claude processes, as Claude does, so they do not look like booting resumes.
        listing = subprocess.run(["ps", "-axo", "pid=,comm="], capture_output=True, text=True).stdout
        for line in listing.splitlines():
            pid, _, comm = line.strip().partition(" ")
            if comm.strip().rsplit("/", 1)[-1] == "claude":
                self.register(int(pid), "other")

    def register(self, pid, session_id, start=None, config=None):
        entry = {"pid": pid, "sessionId": session_id, "procStart": start or start_time(pid)}
        ((config or self.config) / "sessions" / f"{pid}.json").write_text(json.dumps(entry))

    def hook(self, runtime, environment=None, **event):
        result = subprocess.run(["bash", str(SCRIPT), runtime], input=json.dumps(event), capture_output=True, text=True,
                                env={**self.env, **(environment or {})})
        self.assertEqual(result.returncode, 0)
        return result.stdout

    def owner(self, runtime):
        """A command named after the runtime, which the script takes as the owning agent process."""
        owner = self.base / "bin" / runtime
        if not owner.exists():
            owner.parent.mkdir(exist_ok=True)
            owner.symlink_to("/bin/bash")
        return str(owner)

    def as_owner(self, runtime, *events):
        """Run events in order from one long-lived owner process."""
        steps = []
        for index, event in enumerate(events):
            (self.base / f"event{index}.json").write_text(json.dumps(event))
            steps.append(f"bash {shlex.quote(str(SCRIPT))} {runtime} < {shlex.quote(str(self.base / f'event{index}.json'))}")
        command = "; ".join(steps) + "; :"  # the trailing no-op stops bash from exec-ing the last step
        result = subprocess.run([self.owner(runtime), "-c", command], capture_output=True, text=True, env=self.env)
        self.assertEqual(result.returncode, 0)
        return result.stdout

    def session(self, name, pid=None, start="", config=None):
        folder = self.claude / name
        folder.mkdir(parents=True)
        if pid is not None:
            (folder / ".session-owner").write_text(f"{pid}\n{start}\n{config or self.config}\n")
        return folder

    def sweep(self, environment=None):
        self.hook("claude", environment, hook_event_name="SessionStart", session_id="current", source="startup")

    def test_session_end_deletes_only_the_folder_its_owner_claimed(self):
        # Claude creates its folder lazily, so SessionStart creates it from the cwd slug.
        own = self.base / f"claude-{os.getuid()}" / "-work-my-app" / "current"
        start = {"hook_event_name": "SessionStart", "session_id": "current", "source": "startup", "cwd": "/work/my.app"}
        end = {"hook_event_name": "SessionEnd", "session_id": "current"}
        self.as_owner("claude", start, {**end, "reason": "clear"})
        self.assertTrue((own / ".session-owner").exists())
        self.as_owner("claude", start, {**end, "reason": "prompt_input_exit"})
        self.assertFalse(own.exists())
        unmarked = self.session("unmarked")
        self.hook("claude", hook_event_name="SessionEnd", session_id="unmarked", reason="other")
        self.assertTrue(unmarked.exists())

    def test_session_start_reclaims_only_folders_of_dead_owners_in_any_locale(self):
        me = os.getpid()
        dead = self.session("dead", DEAD_PID, OLD_START)
        reused = self.session("reused", me, OLD_START)
        live = self.session("live", me, start_time(me))
        # A new live process resumed this session under another known account dir and has not claimed it yet.
        other = self.base / "other-config"
        (other / "sessions").mkdir(parents=True)
        for entry in (self.config / "sessions").iterdir():  # so only the missing resume entry can tell
            (other / "sessions" / entry.name).write_bytes(entry.read_bytes())
        resumed = self.session("resumed", DEAD_PID, OLD_START, other)
        self.register(me, "resumed")
        unmarked = self.session("unmarked")
        outside = self.base / "outside" / "victim"  # a slug dir symlinked out of the root
        outside.mkdir(parents=True)
        (outside / ".session-owner").write_text(f"{DEAD_PID}\n{OLD_START}\n{self.config}\n")
        (self.claude.parent / "link").symlink_to(outside.parent)
        self.session("current")
        # The live marker was written in C/UTC; a hook in another locale and zone must still match it.
        self.sweep({"LC_ALL": "fr_FR.UTF-8", "TZ": "Asia/Tokyo"})
        self.assertFalse(dead.exists())
        self.assertFalse(reused.exists())
        for kept in (live, resumed, unmarked, outside / ".session-owner", self.claude / "current"):
            self.assertTrue(kept.exists(), kept)

    def test_unregistered_claude_process_blocks_the_sweep(self):
        dead = self.session("dead", DEAD_PID, OLD_START)
        self.session("current")
        booting = subprocess.Popen([self.owner("claude"), "-c", "sleep 30; :"])
        self.addCleanup(booting.wait)
        self.addCleanup(booting.kill)
        self.register(booting.pid, "other", OLD_START)  # stale entry from an earlier process with this PID
        self.sweep()
        self.assertTrue(dead.exists())
        booting.kill()
        booting.wait()
        self.sweep()
        self.assertFalse(dead.exists())

    def test_session_end_returns_fast_for_a_large_folder(self):
        events = [self.base / "start.json", self.base / "end.json"]
        events[0].write_text(json.dumps({"hook_event_name": "SessionStart", "session_id": "big", "cwd": "/work/big"}))
        events[1].write_text(json.dumps({"hook_event_name": "SessionEnd", "session_id": "big", "reason": "other"}))
        script = shlex.quote(str(SCRIPT))
        owner = subprocess.Popen([self.owner("claude"), "-c", f"bash {script} claude < {events[0]}; read -r go; bash {script} claude < {events[1]}; :"],
                                 stdin=subprocess.PIPE, env=self.env, text=True)
        self.addCleanup(owner.kill)
        folder = self.base / f"claude-{os.getuid()}" / "-work-big" / "big"
        while not (folder / ".session-owner").exists():
            self.assertIsNone(owner.poll())
            time.sleep(0.05)
        for index in range(20000):
            (folder / str(index)).touch()
        began = time.monotonic()
        owner.communicate("go\n", timeout=10)
        self.assertLess(time.monotonic() - began, 2.5)  # a synchronous rm of 20,000 files took 4.2 s
        self.assertFalse(folder.exists())

    def test_sweep_touches_only_its_own_trash(self):
        root = self.claude.parent
        dead = self.session("dead", DEAD_PID, OLD_START)
        self.session("current")
        # Unmarked folders that only look like trash, including the name a fixed trash path would use.
        lookalikes = [root / ".trash-valuable", root / ".trash.valuable", root / ".trash-dead", root / ".trash"]
        for folder in lookalikes:
            folder.mkdir()
            (folder / "keep").touch()
        leftover = root / ".trash.leftover"  # a container from a delete that did not finish
        leftover.mkdir()
        (leftover / ".session-temp-trash").touch()
        self.sweep()
        self.assertFalse(dead.exists())
        for _ in range(100):  # deletes run in the background; wait for them before checking what stayed
            if not leftover.exists():
                break
            time.sleep(0.05)
        time.sleep(0.5)
        self.assertFalse(leftover.exists())
        for folder in lookalikes:
            self.assertEqual([entry.name for entry in folder.iterdir()], ["keep"], folder)

    def test_unsafe_session_id_deletes_nothing(self):
        self.session("current", DEAD_PID, OLD_START)
        self.hook("claude", hook_event_name="SessionEnd", session_id="../project", reason="other")
        self.assertTrue((self.claude / "current").exists())

    def test_codex_start_names_the_folder_and_end_deletes_it(self):
        output = self.as_owner("codex", {"hook_event_name": "SessionStart", "session_id": "019a-codex", "source": "startup"},
                               {"hook_event_name": "SessionEnd", "session_id": "019a-codex", "reason": "other"})
        folder = self.base / f"codex-{os.getuid()}" / "019a-codex"
        self.assertIn(f"Session temp folder: {folder}", output)
        self.assertFalse(folder.exists())


if __name__ == "__main__":
    unittest.main()
