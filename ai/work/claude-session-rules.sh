#!/usr/bin/env bash
# Work-only SessionStart hook: check that the active CLAUDE.md's imports resolve, and remind
# the session to follow them. The rules load through the @imports, so this script
# never re-injects them. Provision an independent copy for each account on a
# work machine. Personal machines do not install it.
# Always exits 0 so a broken rule import never blocks the session.

root="${CLAUDE_HOOK_GLOBAL_MD:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}/CLAUDE.md}"
files=()
missing=()

resolve() {
  case "$2" in
    "~/"*) printf '%s\n' "$HOME/${2#"~/"}" ;;
    /*) printf '%s\n' "$2" ;;
    *) printf '%s\n' "$(dirname "$1")/$2" ;;
  esac
}

visit() {
  local file="$1" depth="$2" target line seen
  local targets=()
  # Claude Code expands @imports up to four hops; it never follows Markdown links.
  [ "$depth" -gt 4 ] && return
  for seen in ${files[@]+"${files[@]}"}; do [ "$seen" = "$file" ] && return; done
  if [ ! -r "$file" ]; then
    missing+=("$file")
    return
  fi
  files+=("$file")
  while IFS= read -r line; do
    case "$line" in
      @*)
        target="${line#@}"
        target="${target%%[[:space:]]*}"
        [ -n "$target" ] && targets+=("$target")
        ;;
    esac
  done < "$file"
  for target in ${targets[@]+"${targets[@]}"}; do
    visit "$(resolve "$file" "$target")" $((depth + 1))
  done
}

visit "$root" 0

cfg="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
account=$(jq -r '.oauthAccount.emailAddress // "none recorded"' "$cfg/.claude.json" 2>/dev/null)
echo "Claude account for this session: $account (config dir: $cfg)."
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  echo "WARNING: ANTHROPIC_API_KEY is set and can override subscription login. Tell the user before doing task work."
fi
if [ ${#missing[@]} -gt 0 ]; then
  echo ""
  echo "MISSING REQUIRED IMPORT, cannot be read:"
  for file in "${missing[@]}"; do echo "- $file"; done
  echo "Stop and report this to the user before doing task work."
fi
cat <<EOF
The rules from $root are already loaded through its @imports. Follow them; do not re-read them.

Before acting on any non-trivial task:
1. Apply the memory and journal rules from those files. Recall prior context and open or resume the task journal before the first action.
2. Load each skill the rules require before applying it.
3. Apply the orchestration rules before choosing between doing work in the main thread and delegating it.
Do not skip these steps because a task looks small. The rule files decide what counts as trivial.
EOF
exit 0
