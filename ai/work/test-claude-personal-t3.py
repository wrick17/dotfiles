#!/usr/bin/env python3
"""Check the T3 Personal launcher with synthetic credentials and mocked Keychain and exec."""

import contextlib
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch


sys.dont_write_bytecode = True  # the launcher has no .py suffix, so its cache would land beside it
loader = importlib.machinery.SourceFileLoader("launcher", str(Path(__file__).with_name("claude-personal-t3")))
module = importlib.util.module_from_spec(importlib.util.spec_from_loader("launcher", loader))
loader.exec_module(module)

TOKEN = "synthetic-access-token"
HOME = Path("/synthetic/home")


class Replaced(Exception):
    """Stands in for exec replacing the process."""


def keychain(**fields):
    credentials = {"accessToken": TOKEN, "expiresAt": (time.time() + 3600) * 1000,
                   "scopes": ["user:inference"], "subscriptionType": "max"}
    credentials.update(fields)
    return subprocess.CompletedProcess([], 0, stdout=json.dumps({"claudeAiOauth": credentials}))


@patch("pathlib.Path.home", return_value=HOME)
class LauncherTest(unittest.TestCase):
    def launch(self, arguments, run, environment=None):
        stdout = io.StringIO()
        with patch.object(sys, "argv", ["claude-personal-t3", *arguments]), \
                patch.dict(os.environ, environment or {}, clear=True), \
                patch("subprocess.run", side_effect=run) as security, \
                patch("os.execv", side_effect=Replaced) as execv, \
                patch("os.execve", side_effect=Replaced) as execve, \
                contextlib.redirect_stdout(stdout), contextlib.suppress(Replaced):
            module.main()
        self.assertEqual(stdout.getvalue(), "")
        return security, execv, execve

    def test_help_and_version_pass_through_without_keychain(self, home):
        for arguments in (["--version"], ["--help"], ["-h"]):
            security, execv, execve = self.launch(arguments, AssertionError)
            executable = str(HOME / ".local/bin/claude")
            execv.assert_called_once_with(executable, [executable, *arguments])
            security.assert_not_called()

    def test_personal_login_reaches_cli_only_through_descriptor(self, home):
        inherited = {"PATH": "/usr/bin", "ANTHROPIC_API_KEY": "work-key", "CLAUDE_CODE_OAUTH_TOKEN": "work-token",
                     "ANTHROPIC_BEDROCK_BASE_URL": "https://proxy", "CLAUDE_CODE_USE_BEDROCK": "1",
                     "CLAUDE_CONFIG_DIR": str(HOME / ".claude")}
        security, _, execve = self.launch(["-p", "hi"], [keychain()], inherited)
        service = "Claude Code-credentials-" + hashlib.sha256(str(HOME / ".plaude").encode()).hexdigest()[:8]
        self.assertEqual(security.call_args.args[0][-2:], [service, "-w"])
        executable, argv, environment = execve.call_args.args
        self.assertEqual(executable, str(HOME / ".local/bin/claude"))
        self.assertEqual(argv[1], "--managed-settings")
        self.assertEqual(json.loads(argv[2]), {"model": "claude-opus-5-5",
                                               "availableModels": ["opus", "sonnet", "haiku"]})
        self.assertEqual(argv[3:], ["-p", "hi"])
        self.assertEqual(environment["CLAUDE_CONFIG_DIR"], str(HOME / ".plaude"))
        self.assertEqual(environment["PATH"], "/usr/bin")
        self.assertEqual(environment["CLAUDE_CODE_SUBSCRIPTION_TYPE"], "max")
        for name in ("ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_BEDROCK_BASE_URL",
                     "CLAUDE_CODE_USE_BEDROCK"):
            self.assertNotIn(name, environment)
        self.assertFalse(any(TOKEN in value for value in [*argv, *environment.values()]))
        descriptor = int(environment["CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR"])
        self.assertTrue(os.get_inheritable(descriptor))
        with os.fdopen(descriptor) as pipe:
            self.assertEqual(pipe.read(), TOKEN)

    def test_missing_or_expired_login_fails_before_launch(self, home):
        failures = {"keychain miss": subprocess.CalledProcessError(44, "security"),
                    "no token": keychain(accessToken=""),
                    "expired": keychain(expiresAt=(time.time() - 60) * 1000)}
        for name, result in failures.items():
            with self.subTest(name):
                with self.assertRaises(SystemExit) as failure:
                    self.launch([], [result])
                self.assertIn("regular personal CLI", str(failure.exception.code))
                self.assertNotIn(TOKEN, str(failure.exception.code))


if __name__ == "__main__":
    unittest.main()
