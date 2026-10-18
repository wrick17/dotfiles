#!/usr/bin/env python3
"""Seed independent Claude account files; preserve account edits on later runs."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import shlex


AI = Path(__file__).resolve().parent


def provision(config, profile, default_model):
    config = config.expanduser().absolute()
    if config.is_symlink():
        raise ValueError("Account directory must be independent, not a symlink")
    config.mkdir(parents=True, exist_ok=True)
    backup = Path.home() / ".local/state/claude-account-backups" / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-" + config.name
    )
    replacements = {}
    for scope in ("common", "work", "personal"):
        source = AI / "skills" / scope
        for skill in source.iterdir():
            if skill.is_dir():
                local = str(config / "skill-library" / scope / skill.name)
                replacements[str(skill.resolve())] = local
                try:
                    relative = skill.resolve().relative_to((AI / "skills").resolve())
                except ValueError:
                    continue
                replacements["~/skills/" + str(relative)] = local
                replacements[str(Path.home() / "skills" / relative)] = local
        for prefix in ("~/skills/", str(Path.home() / "skills") + "/", str(AI / "skills") + "/"):
            replacements[prefix + scope] = str(config / "skill-library" / scope)
    for prefix in ("~/dotfiles/ai/", str(AI) + "/", str(Path.home() / "dotfiles/ai") + "/"):
        for scope in ("common", "work", "personal"):
            replacements[prefix + scope] = str(config / "rules" / scope)
    replacements = sorted(replacements.items(), key=lambda pair: len(pair[0]), reverse=True)

    def localize(text):
        for old, new in replacements:
            text = text.replace(old, new)
        return text

    def save(path):
        if not path.exists() and not path.is_symlink():
            return
        backup.mkdir(parents=True, exist_ok=True, mode=0o700)
        target = backup / path.relative_to(config)
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        shutil.copy2(path, target, follow_symlinks=False) if not path.is_dir() or path.is_symlink() else shutil.copytree(path, target, symlinks=True)
        if not target.is_symlink() and target.is_file():
            target.chmod(0o600)

    def write(path, text):
        if path.is_file() and not path.is_symlink() and path.stat().st_nlink == 1 and path.read_text() == text:
            return
        save(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_name(path.name + ".isolation-tmp")
        with temp.open("x", encoding="utf-8") as stream:
            os.chmod(temp, 0o600)
            stream.write(text)
        temp.replace(path)

    def snapshot(source, target):
        if source.is_dir():
            if target.is_symlink():
                save(target)
                target.unlink()
            target.mkdir(parents=True, exist_ok=True)
            for child in source.iterdir():
                if child.name not in (".git", "__pycache__", ".DS_Store"):
                    snapshot(child, target / child.name)
        elif not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                text = source.read_text()
            except UnicodeDecodeError:
                shutil.copy2(source, target)
            else:
                target.write_text(localize(text))
                target.chmod(source.stat().st_mode & 0o777)

    for scope in ("common", profile):
        snapshot(AI / scope, config / "rules" / scope)
        snapshot(AI / "skills" / scope, config / "skill-library" / scope)

    skills = config / "skills"
    if skills.is_symlink():
        raise ValueError("Skill directory must be independent, not a symlink")
    skills.mkdir(exist_ok=True)
    if not any(skills.iterdir()):
        for scope in ("common", profile):
            for skill in (AI / "skills" / scope).iterdir():
                if (skill / "SKILL.md").is_file() and not skill.name.startswith("ponytail"):
                    snapshot(skill, skills / skill.name)
    # Materialize existing links, including nested links, without touching plugins.
    def materialize(path):
        if path.is_symlink():
            source = path.resolve(strict=True)
            save(path)
            path.unlink()
            snapshot(source, path)
        elif path.is_dir():
            for child in path.iterdir():
                materialize(child)

    materialize(skills)

    entry = config / "CLAUDE.md"
    text = entry.read_text() if entry.exists() else "# Global Claude Code instructions\n\n@rules/" + profile + "/claude.md\n"
    write(entry, localize(text))

    settings_path = config / "settings.json"
    settings = json.loads(settings_path.read_text()) if settings_path.exists() else {}
    settings.setdefault("model", default_model)
    hooks = settings.setdefault("hooks", {})
    pre = hooks.setdefault("PreToolUse", [])
    if not any(h.get("command") == "rtk hook claude" for group in pre for h in group.get("hooks", [])):
        pre.append({"matcher": "Bash", "hooks": [{"type": "command", "command": "rtk hook claude"}]})
    if profile == "work":
        hook = config / "hooks/claude-session-rules.sh"
        snapshot(AI / "work/claude-session-rules.sh", hook)
        command = "CLAUDE_CONFIG_DIR=" + shlex.quote(str(config)) + " bash " + shlex.quote(str(hook))
        session = hooks.setdefault("SessionStart", [])
        found = False
        for group in session:
            for item in group.get("hooks", []):
                if "claude-session-rules.sh" in item.get("command", ""):
                    item["command"] = command
                    found = True
        if not found:
            session.append({"hooks": [{"type": "command", "command": command, "timeout": 10}]})
    write(settings_path, json.dumps(settings, indent=2) + "\n")
    print("Provisioned " + str(config))
    if backup.exists():
        print("Backup: " + str(backup))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    parser.add_argument("--profile", choices=("work", "personal"), required=True)
    parser.add_argument("--default-model", required=True)
    args = parser.parse_args()
    provision(args.config, args.profile, args.default_model)
