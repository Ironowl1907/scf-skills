---
name: analysis
description: Step 2 (Analysis & Design) of the team's 8-step AI collaboration framework. Consumes the confirmed task dossier produced by Step 1 (prep), red-teams every impact that fulfilling the task would have on the rest of the system, and settles with the developer what must be done about each impact and why, producing an analysis dossier for Step 3. Must only be invoked manually by the user.
metadata:
  disable-model-invocation: "true"
---

# Analysis

Determine **what fulfilling one task does to the system around it**, and settle with the developer **what must be done about it, and why**. You play Red Team: assume nothing is safe until you have checked it, and look for every contract, consumer, dependency, data guarantee, and security or performance property the task can break or strain.

## Scope rule

Analysis owns the *what* and the *why* at the system level. The *how* belongs to Step 3 (Implementation Proposal).

**Rule of thumb: if it can be verified from outside the component, it is in scope.**

- In scope: API and event contracts, observable behavior, data guarantees, security properties, performance budgets, compatibility during rollout, and which parts of the system must take on new or changed responsibilities (e.g. "the backend must now validate X", "a new frontend component is needed to show Y").
- Out of scope: internal structure, algorithms, class or function design, library choices, file-by-file edit plans, and test design.

If a finding drifts into *how*, restate it as the externally verifiable requirement behind it. If no such requirement exists, it belongs to Step 3: drop it.

## References

- [Red-Team Procedure](RED-TEAM.md)
- [Impact Grilling](GRILL-IMPACT.md)
- [Impact Lenses](references/impact-lenses.md)
- [Grilling Protocol](references/grilling.md)
- [Dossier Template](assets/analysis.md)
- Input File: `.ai/tasks/<task_name>/01-brief-and-context.md`
- Output File: `.ai/tasks/<task_name>/02-analysis.md`

## Input

The developer's invoking message identifies the task by `<task_name>`, by ClickUp ID/URL, or by the path to its input dossier.

- Resolve it to exactly one input dossier under `.ai/tasks/`. For a ClickUp ID, match the directory whose name starts with that ID. If nothing or more than one thing matches, list what you found and ask. Never guess.
- The input dossier is valid only if its status line reads `Completed` and its Task Brief and Context sections are filled in. If it isn't valid, or doesn't exist, stop: tell the developer to run (or finish) `prep` for this task, then abort.
- Read the whole input dossier. Every entry in its Decision Log is a settled branch: never re-ask it.

## Process

1. **Resolve and validate the input** as described above.
2. **Check for an existing output dossier.** If one exists, this is a re-run: read it and treat every entry in its Decision Log as settled. Compare its `Input` line with the input dossier's Decision Log: entries newer than the one recorded mean the brief or context changed since the last run, so re-examine every impact those entries touch. Only grill what is new, changed, or what the developer says has changed.
3. **Read and execute `RED-TEAM.md`.** It produces the candidate impacts. Nothing is written to disk in this step.
4. **Read and execute `GRILL-IMPACT.md`.** It settles every candidate with the developer and writes the output dossier once they confirm it.
5. **Finish**: tell the developer the output file's path, that Analysis is complete, and that the next step is Implementation Proposal.

Each step is blocked until the one before it has run to completion. Do not declare Analysis complete while an overturn is pending.

## Overturning

Analysis never edits the input dossier; its gaps are fixed by re-running `prep`. Overturn when any of the following is true:

1. **The Task Brief is ambiguous or contradictory** in a way that yields materially different impacts depending on the reading.
2. **Settling an impact would change the Task Brief**: adding, removing, or altering an acceptance criterion, the expected outcome, or a scope boundary.
3. **The system contradicts the dossier**: the repository, its docs, or its history contradict a Context entry or a settled Decision Log entry.
4. **A non-discoverable fact is missing**: the analysis depends on something you cannot find yourself (an external spec, a tacit constraint, an external consumer, a deadline) and the Context doesn't contain it. This applies even when the developer could answer on the spot: facts about the task and its context belong in the input dossier, not here.

Distinguish overturns from ordinary work: facts about the codebase are yours to find; dispositions of impacts are the developer's decisions in `GRILL-IMPACT.md`; only a missing or wrong *task definition* or *non-discoverable context* is an overturn.

When an overturn is found:

1. Finish the current red-team pass if the remaining analysis doesn't depend on the gap, so the developer re-runs `prep` once, not once per gap. If it does depend on it, stop immediately.
2. Do not create or update the output dossier.
3. Report every gap to the developer, each with: what is missing or contradicted, the evidence, the input dossier section it belongs to (Task Brief, Context, or Decision Log), and the question `prep` needs to settle.
4. Tell the developer to re-run `prep` for this task with that report, then invoke `analysis` again.

## Output

The output dossier at the Output File path, built from the Dossier Template and written once, at the end of `GRILL-IMPACT.md`, after the developer confirms it.
