#!/usr/bin/env bash
# One temp folder per agent session. Registered for SessionStart and SessionEnd:
#   bash session-temp.sh <claude|codex>   (hook JSON on stdin)
# SessionStart marks the session's folder with its owner process (PID and start time) and deletes
# other folders whose owner is provably gone (crash fallback). SessionEnd deletes the folder only
# when this same owner claimed it. Unmarked folders are never touched. Always exits 0.
set -u

runtime=${1:-}
uid=$UID
case $runtime in
  # SESSION_TEMP_BASE exists only so tests can point at a throwaway root.
  claude) root=${SESSION_TEMP_BASE:-${CLAUDE_CODE_TMPDIR:-/tmp}}/claude-$uid ;;
  codex) root=${SESSION_TEMP_BASE:-/tmp}/codex-$uid ;;
  *) exit 0 ;;
esac
marker=.session-owner
# Claude's account dir; recorded in the marker so a sweep can read that account's live-session registry.
config=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
# ps prints lstart in the caller's locale and time zone; pin both so every session writes and compares one form.
export LC_ALL=C TZ=UTC
LSTART='^[A-Z][a-z]{2} [A-Z][a-z]{2} [0-9]{1,2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}$'

# A non-whitespace separator, so empty fields do not collapse.
IFS=$'\x1f' read -r event sid reason cwd < <(jq -r '[.hook_event_name, .session_id, .reason, .cwd] | map(. // "" | tostring) | join("\u001f")' 2>/dev/null) || exit 0
# session_id becomes a path component, so allow only a plain safe name.
[[ $sid =~ ^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$ ]] || exit 0

# Process launches cost 65-250 ms each here (more while Claude starts), so the hot paths use builtins and globs.
# One process snapshot screens PIDs cheaply. It can be stale,
# so anything that leads to a delete is re-checked with owner_dead. Arrays are indexed by PID because
# bash 3.2 has no associative arrays; read collapses lstart's padding, so markers store that single-spaced form.
load_procs() {
  local pid ppid a b c d e comm
  while read -r pid ppid a b c d e comm; do
    [[ $pid =~ ^[0-9]+$ ]] || continue
    parent[pid]=$ppid started[pid]="$a $b $c $d $e" name[pid]=${comm##*/}
  done < <(ps -axo pid=,ppid=,lstart=,comm= 2>/dev/null)
  # An enumeration that misses this very process is not trustworthy.
  [ -n "${started[$$]:-}" ]
}

# The digit check also keeps marker text out of the arithmetic array index.
start_time() { [[ $1 =~ ^[0-9]+$ ]] && [ -n "${started[$1]:-}" ] && printf '%s' "${started[$1]}"; }

# The agent process may sit above a shell wrapper, so walk up to the first ancestor named after the runtime.
owner_pid() {
  local p=$PPID i
  for i in 1 2 3 4 5 6; do
    [ "$p" -gt 1 ] 2>/dev/null || return 1
    [ "${name[p]:-}" = "$runtime" ] && { printf '%s' "$p"; return 0; }
    p=${parent[p]:-0}
  done
  return 1
}

# Sets m_pid, m_start and m_config; fails unless the marker is a regular file with a valid PID and start time.
read_marker() {
  m_pid= m_start= m_config=
  [ -f "$1" ] && [ ! -L "$1" ] || return 1
  { read -r m_pid; read -r m_start; read -r m_config; } 2>/dev/null <"$1"
  [[ $m_pid =~ ^[0-9]+$ ]] && [[ $m_start =~ $LSTART ]]
}

# Fresh check: dead only if ps reports no such process, or one that started at another time (PID reuse).
owner_dead() {
  local out rc a b c d e
  out=$(ps -o lstart= -p "$1" 2>/dev/null)
  rc=$?
  read -r a b c d e <<<"$out"
  if [ -z "$a" ]; then [ "$rc" -eq 1 ]; else [ "$a $b $c $d $e" != "$2" ]; fi
}

# Claude registers each live process in <config>/sessions/<pid>.json (pid, sessionId, procStart) about a
# second after it starts, seconds before SessionStart, and creates the folder only later. A crashed session
# can be resumed by a new process, under any known config dir, before that process's SessionStart claims the
# folder. So keep the folder if any known registry names the session for a running process, or if any running
# claude process lacks an entry matching its PID and start time (it may be booting that resume, or its entry
# is stale from a reused PID). Any doubt keeps the folder. $1 is the session id.
claude_in_use() {
  local d f files=() reg out p s rs a b c e g comm self=
  local -a fresh registered
  for d in "${configs[@]}"; do
    [[ $d == /* ]] || continue
    for f in "$d"/sessions/*.json; do [ -f "$f" ] && files+=("$f"); done
  done
  if [ ${#files[@]} -gt 0 ]; then
    reg=$(jq -r '[.pid, .procStart, .sessionId] | map(. // "" | tostring) | join("\u001f")' "${files[@]}" 2>/dev/null) || return 0
  fi
  out=$(ps -axo pid=,lstart=,comm= 2>/dev/null) || return 0
  while read -r p a b c e g comm; do
    [[ $p =~ ^[0-9]+$ ]] || continue
    [ "$p" = "$$" ] && self=1
    fresh[p]="$a $b $c $e $g"
  done <<<"$out"
  [ -n "$self" ] || return 0
  while IFS=$'\x1f' read -r p s rs; do
    read -r a b c e g <<<"$s"
    s="$a $b $c $e $g"
    # An entry counts only for the process that wrote it: same PID and the same start time.
    [[ $p =~ ^[0-9]+$ ]] && [[ $s =~ $LSTART ]] && [ "${fresh[p]:-}" = "$s" ] || continue
    registered[p]=1
    [ "$rs" = "$1" ] && return 0
  done <<<"${reg:-}"
  while read -r p a b c e g comm; do
    [[ $p =~ ^[0-9]+$ ]] && [ "${comm##*/}" = claude ] && [ -z "${registered[p]:-}" ] && return 0
  done <<<"$out"
  return 1
}

# Codex keeps no live-session registry, so a new codex process resuming a crashed session cannot be told
# apart; skip the Codex sweep while any codex process other than this hook's owner runs.
codex_in_use() {
  local out p comm self= own
  own=$(owner_pid)
  out=$(ps -axo pid=,comm= 2>/dev/null) || return 0
  while read -r p comm; do
    [ "$p" = "$$" ] && self=1
    [ "${comm##*/}" = codex ] && [ "$p" != "$own" ] && return 0
  done <<<"$out"
  [ -z "$self" ]
}

# Delete in the background so a big folder cannot outlast the hook timeout (Codex SessionEnd allows 3 s).
# The rm gets no lock fd and no stdout/stderr, so it neither holds the lock nor keeps the hook's pipes open.
delete_later() { nohup rm -rf -- "$@" </dev/null >/dev/null 2>&1 9>&- & }

# Delete only a real directory strictly inside root, reached without a symlink (globs follow them). It is
# renamed (atomic) into a fresh mktemp container, so the move can never land inside an existing folder,
# and the container carries a trash marker so the sweep removes only containers this script made.
trash_marker=.session-temp-trash
remove_dir() {
  local trash
  case $1 in
    "$root"/?*) [ -d "$1" ] && [ ! -L "$1" ] && [ ! -L "${1%/*}" ] || return 1 ;;
    *) return 1 ;;
  esac
  trash=$(mktemp -d "$root/.trash.XXXXXXXX" 2>/dev/null) || return 1
  : >"$trash/$trash_marker"
  mv -- "$1" "$trash/d" 2>/dev/null
  delete_later "$trash"
}

session_dir() {
  if [ "$runtime" = codex ]; then
    printf '%s' "$root/$sid"
  else
    # Claude's folder is <root>/<project slug>/<session id>; skip anything reached through a symlink.
    local d
    for d in "$root"/*/"$sid"; do
      [ -d "$d" ] && [ ! -L "$d" ] && [ ! -L "${d%/*}" ] && [ -O "$d" ] && { printf '%s' "$d"; return; }
    done
  fi
}

# Claude creates its folder lazily, after SessionStart, so create it now to mark it. Claude's project slug
# is the cwd with every character other than A-Z, a-z, 0-9 replaced by '-'.
create_claude_dir() {
  local slug
  [[ $cwd == /* ]] || return 1
  slug=${cwd//[^A-Za-z0-9]/-}
  # shortcut: Claude shortens slugs over 200 chars with a hash; such sessions get no folder or marker here and are never reclaimed.
  [ ${#slug} -le 200 ] || return 1
  mkdir -p -m 700 "$root/$slug/$sid" 2>/dev/null
  [ ! -L "$root/$slug" ] && printf '%s' "$root/$slug/$sid"
}

# Refuse a root that is a symlink or belongs to someone else (shared /tmp).
root_ok() { [ -d "$root" ] && [ ! -L "$root" ] && [ -O "$root" ]; }

# Claims, sweeps and deletes run under one kernel flock on fd 9, so a sweeper cannot delete a folder
# that a resumed session is claiming. The lock lives as long as this shell's fd 9 and ends with the
# process, so a killed hook leaves no stale lock. macOS has no flock command; perl provides flock(2).
# $1 is the longest wait in seconds.
lock() {
  { exec 9>>"$root/.session-temp.lock"; } 2>/dev/null || return 1
  perl -MFcntl=:flock -e 'open(my $f, ">&=", 9) or exit 1; $SIG{ALRM} = sub { exit 1 }; alarm $ARGV[0]; flock($f, LOCK_EX) or exit 1' "$1" 2>/dev/null
}

case $event in
  SessionStart)
    [ "$runtime" = codex ] && mkdir -p -m 700 "$root" 2>/dev/null
    root_ok || exit 0
    locked=
    lock 2 && locked=1
    if [ "$runtime" = codex ]; then
      mkdir -m 700 "$root/$sid" 2>/dev/null
      [ -d "$root/$sid" ] && printf 'Session temp folder: %s\nPut every temporary file in this folder (use mktemp -d inside it for scratch work). Never use fixed paths such as /tmp/<name>. The folder is deleted when the session ends.\n' "$root/$sid"
    fi
    # Without the lock or a trustworthy process list, skip claiming and cleanup.
    [ -n "$locked" ] && load_procs || exit 0
    dir=$(session_dir)
    [ -z "$dir" ] && [ "$runtime" = claude ] && dir=$(create_claude_dir)
    if [ -n "$dir" ] && [ -d "$dir" ] && [ ! -L "$dir" ]; then
      # Keep a live owner's marker (resume, compact, or a repeat start in the same process).
      if ! read_marker "$dir/$marker" || owner_dead "$m_pid" "$m_start"; then
        # No identifiable owner means no marker, so the folder is never reclaimed by mistake.
        if pid=$(owner_pid) && start=$(start_time "$pid"); then
          printf '%s\n%s\n%s\n' "$pid" "$start" "$config" >"$dir/$marker.$$" && mv -f "$dir/$marker.$$" "$dir/$marker"
        fi
      fi
    fi
    # Crash fallback for other sessions: keep anything not provably dead.
    markers=() configs=("$config" "$HOME/.claude")
    if [ "$runtime" = claude ]; then set -- "$root"/*/*/"$marker"; else set -- "$root"/*/"$marker"; fi
    for m in "$@"; do
      [ -O "$m" ] && read_marker "$m" || continue
      markers+=("$m")
      [[ $m_config == /* ]] && configs+=("$m_config")
    done
    for m in ${markers[@]+"${markers[@]}"}; do
      d=${m%/*}
      [ "${d##*/}" = "$sid" ] && continue
      read_marker "$m" || continue
      [ "$(start_time "$m_pid")" = "$m_start" ] && continue
      owner_dead "$m_pid" "$m_start" || continue
      if [ "$runtime" = claude ]; then claude_in_use "${d##*/}" && continue; else codex_in_use && continue; fi
      remove_dir "$d"
    done
    # Trash containers left by a delete that did not finish belong to no session; anything else stays.
    for t in "$root"/.trash.*; do
      [ -d "$t" ] && [ ! -L "$t" ] && [ -O "$t" ] && [ -f "$t/$trash_marker" ] && [ ! -L "$t/$trash_marker" ] && delete_later "$t"
    done
    ;;
  SessionEnd)
    # After /clear or /resume the same process keeps running and may still use the old folder;
    # the crash fallback reclaims it once that process exits.
    case $reason in clear | resume) exit 0 ;; esac
    # A short lock wait keeps SessionEnd inside Codex's 3 s cap; a skipped delete is left to the crash fallback.
    root_ok && lock 1 && load_procs || exit 0
    dir=$(session_dir)
    [ -n "$dir" ] && read_marker "$dir/$marker" || exit 0
    # Only the process that claimed the folder deletes it.
    if pid=$(owner_pid) && [ "$pid" = "$m_pid" ] && [ "$(start_time "$pid")" = "$m_start" ]; then
      remove_dir "$dir"
    fi
    ;;
esac
exit 0
