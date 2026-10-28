#!/usr/bin/env python3
"""Seed independent Claude account files; import shared rules and link the user's own skills from dotfiles; preserve account edits on later runs."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import shlex


AI = Path(__file__).resolve().parent


def skills_in(owner, scope):
    folder = AI / "skills" / owner / scope
    return sorted(s for s in folder.iterdir() if s.is_dir()) if folder.is_dir() else []


def provision(config, profile, default_model, refresh=False):
    config = config.expanduser().absolute()
    if config.is_symlink():
        raise ValueError("Account directory must be independent, not a symlink")
    config.mkdir(parents=True, exist_ok=True)
    backup = Path.home() / ".local/state/claude-account-backups" / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "-" + config.name
    )
    replacements = {}
    for scope in ("common", "work", "personal"):
        for skill in skills_in("third-party", scope):
            local = str(config / "skill-library" / scope / skill.name)
            replacements[str(skill.resolve())] = local
            try:
                relative = skill.resolve().relative_to((AI / "skills").resolve())
            except ValueError:
                continue
            replacements["~/skills/" + str(relative)] = local
            replacements[str(Path.home() / "skills" / relative)] = local
        for prefix in ("~/skills/", str(Path.home() / "skills") + "/", str(AI / "skills") + "/"):
            replacements[prefix + "third-party/" + scope] = str(config / "skill-library" / scope)
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
        library = config / "skill-library" / scope
        if refresh and library.is_dir():
            save(library)
            shutil.rmtree(library)
        snapshot(AI / "skills/third-party" / scope, library)

    skills = config / "skills"
    if skills.is_symlink():
        raise ValueError("Skill directory must be independent, not a symlink")
    skills.mkdir(exist_ok=True)
    if not any(skills.iterdir()):
        for scope in ("common", profile):
            for skill in skills_in("third-party", scope):
                if (skill / "SKILL.md").is_file() and not skill.name.startswith("ponytail"):
                    snapshot(skill, skills / skill.name)
    # Materialize third-party links, including nested links, without touching plugins or the user's own skills.
    mine = (AI / "skills/mine").resolve()

    def materialize(path):
        if path.is_symlink() and path.resolve().is_relative_to(mine):
            return
        if path.is_symlink():
            source = path.resolve(strict=True)
            save(path)
            path.unlink()
            snapshot(source, path)
        elif path.is_dir():
            for child in path.iterdir():
                materialize(child)

    materialize(skills)

    # --refresh-third-party replaces account copies of third-party skills with the current dotfiles version.
    if refresh:
        for scope in ("common", profile):
            for skill in skills_in("third-party", scope):
                target = skills / skill.name
                if target.is_dir() and not target.is_symlink():
                    save(target)
                    shutil.rmtree(target)
                    snapshot(skill, target)

    # The user's own skills stay live: link each one so dotfiles edits apply at once.
    for scope in ("common", profile):
        for skill in skills_in("mine", scope):
            target = skills / skill.name
            if target.is_symlink() and target.resolve() == skill.resolve():
                continue
            if target.exists() or target.is_symlink():
                save(target)
                target.unlink() if target.is_symlink() or not target.is_dir() else shutil.rmtree(target)
            target.symlink_to(skill)

    # Rules load straight from dotfiles; drop rule snapshots left by older runs.
    entry = config / "CLAUDE.md"
    text = entry.read_text() if entry.exists() else "# Global Claude Code instructions\n\n@rules/" + profile + "/claude.md\n"
    write(entry, text.replace("@" + str(config / "rules") + "/", "@rules/").replace("@rules/", "@" + str(AI) + "/"))
    rules = config / "rules"
    if rules.exists() or rules.is_symlink():
        save(rules)
        rules.unlink() if rules.is_symlink() else shutil.rmtree(rules)

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
    parser.add_argument("--refresh-third-party", action="store_true", help="replace account copies of third-party skills, backing them up first")
    args = parser.parse_args()
    provision(args.config, args.profile, args.default_model, args.refresh_third_party)
