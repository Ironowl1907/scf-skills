---
name: analysis
description: Step 2 (Analysis & Design) of the team's 8-step AI collaboration framework. Takes in the task dossier produced by Step 1 (prep), red-teams every impact that fulfilling the task would have on the rest of the system, and interviews the user on what must be done about each impact and why, producing an analysis dossier for Step 3. Must only be invoked manually by the User.
---

# Analysis

Determine what fulfilling one task **does to the system around it**, and settle with the user **what must be done about it, and why**. Analysis finds the **problems** that need fixing, never **how** to fix them.

## References

- [Red-Team Procedure](RED-TEAM.md)
- [Impact Grilling](GRILL-IMPACT.md)
- [Impact Lenses](references/impact-lenses.md)
- [Grilling Protocol](references/grilling.md)
- [Dossier Template](assets/analysis.json)
- [Template Generator Script](scripts/dossier-renderer)
- [Validation Script](scripts/dossier-validator)
- [Caveman Protocol](references/caveman.md)
- Input File: `.ai/tasks/<task_name>/01-brief-and-context.md`
- Output File: `.ai/tasks/<task_name>/02-analysis.md`
- Draft File: `.ai/tasks/<task_name>/02-analysis.draft.md`
- Candidates File: `.ai/tasks/<task_name>/02-analysis.candidates.md`
- Overturn Report: `.ai/tasks/<task_name>/02-analysis.overturn.md`

## Input

The user's invoking message identifies the task by `<task_name>`, by ClickUp ID/URL, or by the path to its input dossier.

- Resolve it to exactly one input dossier under `.ai/tasks/`. For a ClickUp ID, match the directory whose name starts with that ID. If nothing or more than one thing matches, list what you found and ask. Never guess.
- Read the input dossier as-is, whatever its state. Missing or contradictory information in it is a gap (see Overturning).
- Read the whole input dossier. Every entry in its Decision Log is a settled branch: never re-ask it.
- Any other file the user supplies (e.g. a previously generated dossier or overturn report) is read as-is, like the rest of the input.

## Process

Strictly adhere to the Caveman Protocol across all user interactions, questioning/grilling cycles, confirmations, and generated dossier content.

1. **Resolve and read the input** as described above.
2. **Generate the Draft File** by using the Template Generator Script.
3. **Read and execute `RED-TEAM.md`.** It produces the candidate impacts.
4. **Read and execute `GRILL-IMPACT.md`.** It settles every candidate with the user, validates the Dossier using the Validation Script, and writes the output dossier once they confirm it.
5. **Finish**: tell the user the output file's path, that Analysis is complete, and that the next step is Implementation Proposal.

Each step is blocked until the one before it has run to completion.
Do not declare Analysis complete while an overturn is pending.

## Overturning

Analysis never edits the input dossier; its gaps are fixed by re-running `prep`. You may suggest an Overturn when any of the following is true:

1. **The Task Brief is ambiguous or contradictory** in a way that yields materially different impacts depending on the reading.
2. **Settling an impact would change the Task Brief**: adding, removing, or altering an acceptance criterion, the expected outcome, or a scope boundary.
3. **The system contradicts the dossier**: the repository, its docs, or its history contradict a Context entry or a settled Decision Log entry.
4. **A non-discoverable fact is missing**: the analysis depends on something you cannot find yourself (an external spec, a tacit constraint, an external consumer, a deadline) and the Context doesn't contain it.

Distinguish overturns from ordinary work: facts about the codebase are yours to find; dispositions of impacts are the user's decisions in `GRILL-IMPACT.md`; only a missing or wrong *task definition* or *non-discoverable context* is an overturn.

When a gap is found:

1. Finish the current red-team pass if the remaining analysis doesn't depend on the gap. If it does depend on it, stop immediately.
2. Present every gap to the user and suggest an Overturn. The user may instead settle a gap on the spot; the skill then continues normally.
3. If the user accepts the Overturn, do not create or update the output dossier; write the gap report to the Overturn Report file. For each gap, state: what is missing or contradicted, the evidence, the target dossier and section it belongs to (Task Brief, Context, or Decision Log), the skill(s) to run in order, and the question each skill needs to settle. Show the user the complete report as it will be written and write it only once they confirm.
4. Tell the user to re-run `prep` for this task with that report, and to only then invoke `analysis` again. End the run.

## Output

The output dossier at the Output File path, built from the Dossier Template and written once, at the end of `GRILL-IMPACT.md`, after the user confirms it.
Formatted strictly in caveman style while adhering to schema constraints.
