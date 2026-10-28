# Claude Code instructions

@global.md
@orchestration.md

Apply the imported rules together with this file. Stop and report a required import that cannot be read.

## Instruction adherence

- Follow `global.md` and every other imported rule to the letter. Do not deviate, shorten, or substitute your own preference.
- Follow the user's explicit instructions the same way. These are hard rules, not suggestions.
- If a rule cannot be followed, stop and report the conflict instead of working around it.

## Native memory

- Consult available Claude Code native memory for relevant prior work. Use its supported memory mechanism for explicit remember, forget, or update requests.
- Use `claude-code` as the runtime label in task-journal names.

## Progress reporting

- Do not write text before, between, or after routine tool calls. No "Next I'll...", "Now I'll...", or "Let me check..." lines.
- Write text only at milestones: an outcome, a blocker, a decision that changes scope or risk, or the next step after one of those.
- Keep each milestone update to a few lines or a compact list. Give more detail only when the user asks for it.
