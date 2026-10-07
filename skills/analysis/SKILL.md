---
name: analysis
description: Step 2 (Analysis & Design) of the team's 8-step AI collaboration framework. Takes in the task dossier produced by Step 1 (prep), red-teams every impact that fulfilling the task would have on the rest of the system, and interviews the user on what must be done about each impact and why, producing an analysis dossier for Step 3. Must only be invoked manually by the user.
---

# Analysis

Determine what fulfilling one task **does to the system around it**, and settle with the user **what must be done about it, and why**. Analysis finds the **problems** that need fixing, never **how** to fix them.

## References

- [Red-Team Procedure](RED-TEAM.md)
- [Impact Grilling](GRILL-IMPACT.md)
- [Impact Lenses](references/impact-lenses.md)
- [Grilling Protocol](references/grilling.md)
- [Dossier Template](assets/analysis.md)
- Working File: `ai/tasks/<task_name>/02-analysis.candidates.md`
- Input File: `.ai/tasks/<task_name>/01-brief-and-context.md`
- Output File: `.ai/tasks/<task_name>/02-analysis.md`

## Input

The user's invoking message identifies the task by `<task_name>`, by ClickUp ID/URL, or by the path to its input dossier.

- Resolve it to exactly one input dossier under `.ai/tasks/`. For a ClickUp ID, match the directory whose name starts with that ID. If nothing or more than one thing matches, list what you found and ask. Never guess.
- The input dossier is valid only if its status line reads `Completed` and its Task Brief and Context sections are filled in. If it isn't valid, or doesn't exist, stop: tell the user to run (or finish) `prep` for this task, then abort.
- Read the whole input dossier. Every entry in its Decision Log is a settled branch: never re-ask it.

## Process

1. **Resolve and validate the input** as described above.
2. **Check for an existing output dossier and working file.** If an output dossier exists, this is a re-run: read it and treat every entry in its Decision Log as settled. Compare its `Processed questions` line with the input dossier's Decision Log: if its Decision Log goes beyond the recorded Q<n>, context has changed since the last run, so re-examine every impact those entries touch. Only grill what is new, changed, or what the user says has changed. If a working file exists, delete it. Chances are the context it relied on has changed.
3. **Read and execute `RED-TEAM.md`.** It produces the candidate impacts.
4. **Read and execute `GRILL-IMPACT.md`.** It settles every candidate with the user and writes the output dossier once they confirm it.
5. **Finish**: tell the user the output file's path, that Analysis is complete, and that the next step is Implementation Proposal.

Each step is blocked until the one before it has run to completion. Do not declare Analysis complete while an overturn is pending.

## Overturning

Analysis never edits the input dossier; its gaps are fixed by re-running `prep`. Overturn when any of the following is true:

1. **The Task Brief is ambiguous or contradictory** in a way that yields materially different impacts depending on the reading.
2. **Settling an impact would change the Task Brief**: adding, removing, or altering an acceptance criterion, the expected outcome, or a scope boundary.
3. **The system contradicts the dossier**: the repository, its docs, or its history contradict a Context entry or a settled Decision Log entry.
4. **A non-discoverable fact is missing**: the analysis depends on something you cannot find yourself (an external spec, a tacit constraint, an external consumer, a deadline) and the Context doesn't contain it. This applies even when the user could answer on the spot: facts about the task and its context belong in the input dossier, not here.

Distinguish overturns from ordinary work: facts about the codebase are yours to find; dispositions of impacts are the user's decisions in `GRILL-IMPACT.md`; only a missing or wrong *task definition* or *non-discoverable context* is an overturn.

When an overturn is found:

1. Finish the current red-team pass if the remaining analysis doesn't depend on the gap. If it does depend on it, stop immediately.
2. Do not create or update the output dossier, write the gap report to the working file.
3. Report every gap to the user, each with: what is missing or contradicted, the evidence, the input dossier section it belongs to (Task Brief, Context, or Decision Log), and the question `prep` needs to settle.
4. Tell the user to re-run `prep` for this task with that report, and to only then invoke `analysis` again.

## Output

The output dossier at the Output File path, built from the Dossier Template and written once, at the end of `GRILL-IMPACT.md`, after the user confirms it.
