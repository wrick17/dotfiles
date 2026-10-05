---
name: rtk
description: Use when running shell commands in Codex or Claude Code. Route commands through RTK for compact output, with unfiltered passthrough when required.
---

# RTK

RTK is a CLI proxy that reduces command output before it reaches the agent's context.

- Use `rtk <command> <args>` for supported commands. Check `rtk --help` when unsure which wrapper exists.
- Use `rtk proxy <command> <args>` for unsupported commands or when exact, complete output is required. Use this for instruction files, structured output, and commands whose output feeds another command or parser.
- Preserve the original arguments, environment, working directory, and shell quoting. For pipelines or compound commands, use `rtk proxy sh -c '<original command>'`, or the original shell if its syntax requires it.
- RTK changes output handling; existing authorization, account-routing, and safety rules still apply.

```sh
rtk ls
rtk npm run build
rtk pytest -q
rtk proxy cat ai/global.md
rtk proxy rg -n 'pattern' src
```

Use `rtk --version` to check availability. Use `rtk gain` or `rtk gain --history` when reviewing recorded output savings.
