---
name: opus-auth-recovery
description: Recover personal Opus logout, expired-login, or Claude authentication failures through Terra, pc auth login, and the user's Google session in Helium. Applies to ~/.plaude and the personal T3 Claude provider, not Office login or usage limits.
---

# Opus auth recovery

Restore the personal Claude login and resume the interrupted work. The user authorizes this recovery, including selecting their existing Google account and pressing Claude Code's Authorize button. Ask only when account identity is ambiguous or a password, MFA, CAPTCHA, or other user-only action is required.

## Route to Terra

Load `delegation` and `browser-work`. Terra owns recovery even when Opus was doing the interrupted work. If the current agent is Terra, do it directly; otherwise delegate one bounded recovery task to the latest available Terra through the session's orchestration tools. Discover the live provider/model identifiers and pass this skill's path, the sanitized failure, the failed personal provider, and the interrupted task's checkpoint. If Terra is unavailable, report that blocker without switching models unasked.

Confirm an authentication failure before starting. Examples include logout, expired OAuth login, `invalid_grant`, or the personal launcher's "cannot read a current personal Claude login" error. Usage limits, billing failures, policy restrictions, and network outages need their own handling.

## Recover, at most three complete cycles

A cycle includes CLI login, browser authorization, CLI verification, and Opus retries. Stop on the first verified Opus success. If a cycle fails, start the next from CLI login, up to three cycles total. Keep one login process active at a time; stop an abandoned process and close only its recovery-created tabs before restarting. Report the sanitized failure and cycle count if all three fail. A user-only authentication challenge pauses recovery for the user's action instead of consuming the remaining cycles blindly.

1. Read `~/dotfiles/.alias.zsh` and `~/dotfiles/ai/common/open-helium.sh`. Verify the effective `pc` alias in interactive zsh matches the dotfiles alias and selects `~/.plaude` with Helium as `BROWSER`. If overridden, load the dotfiles alias into the recovery shell only, leaving persistent shell configuration alone. Use the alias itself, not bare `claude`, `cc`, or `setup-token`.

   ```sh
   rtk proxy zsh -ic 'pc auth login'
   ```

   Run with a PTY and retain its session so the CLI can complete the browser callback or request a code. Keep OAuth URLs, codes, tokens, and credentials out of chat, memory, and saved logs. Do not read or export Keychain secrets.

2. Use the existing Helium profile and Google session. This workflow explicitly requires Helium and DevTools MCP. Discover the available tools rather than opening a different browser. Follow `browser-work` for task grouping and tab ownership; the CLI opens its own login tab, so identify that newly created tab from before/after page lists. Preserve all pre-existing tabs and sessions. If DevTools cannot reach Helium, report the blocker without restarting the browser or changing its profile/debug settings.

3. Inspect and interact with the login page through `chrome-devtools-mcp`. Choose Continue with Google if needed, then select the user's already signed-in personal Google account. Use the intended personal Claude account, not the Office account. Complete the expected Claude Code consent page, headed "Claude Code would like to connect to your Claude chat account", by clicking **Authorize**. Validate the live page and expected Google/Claude origins; use current accessible elements rather than screenshot coordinates. This routine authorization needs no additional confirmation.

4. Wait for the same `pc auth login` process to finish successfully. If the normal flow presents a one-time code instead of completing a callback, submit it only to that waiting CLI session. Verify with `pc auth status` through the same interactive zsh and alias. Record only the logged-in result and config-directory match. A successful browser page alone does not establish CLI success.

5. Retry Opus through the same personal T3 provider that failed. Use a fresh, harmless request and check actual assistant/provider model evidence when available; requested model metadata alone does not prove Opus answered. Allow up to three Opus attempts per cycle, since the provider may need a fresh session to pick up the renewed login. Stop obsolete failed probes before replacing them. Do not replay partially completed mutating work as a probe. If all attempts fail with authentication errors, begin the next full recovery cycle. If the failure changes to a non-authentication issue, report it instead of repeating login.

## Finish

Close only recovery-created tabs and stop abandoned login/probe processes. Preserve the user's Helium session, account separation, and existing personal launcher. Report cycles and Opus attempts, CLI verification, actual Opus success or the remaining blocker, without sensitive output. Once Opus responds, return control to the original task owner and resume from its checkpoint without repeating completed side effects. If recovery fails after three complete cycles, flag it to the user and retain the checkpoint.
