---
name: hill-climb
description: Improve a target round by round until an Opus and Sol council scores every rubric category at the bar. Use when the user asks to hill climb, or to keep iterating on a UI, code, docs, or an eval score until judges agree it is good.
---

# Hill climb

A hill climb repeats one round: score the target, fix what the scores point at, score again. Two judges form the council: Opus and Sol. The climb ends at a pass (every judge clears the bar in every category in the same round) or at a plateau.

## Set up

1. Name the target and its capture: what is being improved, and how judges see it. Examples: screenshots of named screens in light and dark mode, a diff plus the touched files, a rendered doc.
2. Write the rubric: 4 to 8 categories for this target, each with one line on what a 10 looks like. A UI rubric might use hierarchy, typography, color and contrast, spacing and layout, consistency, iconography, and state clarity. A code rubric might use correctness, simplicity, naming, error handling, and test coverage.
3. Collect the anchors: the baseline (the target before any change) and every reference the user names, such as competitor products or a previous version. Capture each anchor the same way as the target, once, and reuse it every round. A target scored on its own drifts upward; scored beside anchors, it stays honest.
4. Find the metric: a command that prints a number, such as tests passed, an eval score, bundle size, or latency. When one exists, give it a threshold; it gates the pass alongside the council. When none exists, the council decides alone.
5. Set the bar: 9/10 in every category from both judges, unless the user names another. The plateau limit is 3 rounds.
6. Work on a dedicated branch or worktree, so the baseline stays reachable for anchoring and rollback.

## Each round

1. Capture the target fresh and run the metric.
2. Convene the council: start one fresh Opus judge and one fresh Sol judge in parallel, read-only, through the orchestration layer in the `delegation` skill. Give both the same judge brief. A fresh judge each round keeps earlier scores out of its context.
3. Add the round to the score table: one row per judge, one column per category, for the target and each anchor, plus the metric.
4. Check the exits in order:
   - **Pass**: both judges rate every target category at or above the bar, and the metric meets its threshold. Stop.
   - **Plateau**: neither judge's lowest target category score has risen for 3 rounds in a row. Stop.
   - Otherwise, continue.
5. Merge the findings. Keep findings both judges raise, and findings from one judge that come with a concrete fix. Rank them by how much they lift the lowest categories. Record disagreements.
6. Fix: send the ranked findings to an Opus worker under the `delegation` skill. Opus applies them and runs the build-and-load checks. The scope stays inside the target; a fix never adds features. Revert any fix that drops the metric before the next round.

## Judge brief

Send each judge:

- The rubric with its category definitions.
- The target and every anchor, labelled "Target", "Baseline", and "Reference: <name>".
- The task: score each labelled item 1 to 10 in each category, to one decimal place; list the findings that cost the target points, each with a concrete fix; name the strongest item in each category and why.
- The limit: read-only, with no edits, commits, or messages.

The brief carries no bar, round number, earlier scores, or goal score. A judge that knows the number aims for it.

## Raising the bar

After a pass, the user may set a higher bar, such as 9.5 and then 10. Continue on the same branch, or fork a new worktree so the passing version stays mergeable. Keep the round numbering and the score table running.

A metric climb can turn into a squeeze after a pass: keep the passing state, then shrink a second number (description size, tokens, runtime) while the first metric holds its threshold. The council still judges each round.

## Report

End with:

- The score table across all rounds, for the target and each anchor.
- The exit reached. For a plateau, list the findings still holding the target below the bar.
- Before and after captures of the target, with each visible change pointed out.
- Disagreements between the judges that remain.
