---
name: analysis
description: Step 2 (Analysis & Design) of team's 8-step AI collaboration framework. Takes task Dossier from Step 1 (prep). Red-teams every impact the task has on rest of system. Interviews User on what must be done about each impact, and why. Produces analysis Dossier for Step 3. Must only be invoked manually by the User.
---

# Analysis

Find what fulfilling one task **does to system around it**. Settle with User **what must be done about it, and why**. Analysis finds **problems** to fix, never **how** to fix them.

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

User's invoking message names task by `<task_name>`, ClickUp ID/URL, or Input File path.

- Resolve it to exactly one Input File under `.ai/tasks/`. ClickUp ID: match directory whose name starts with that ID. Nothing matches, or more than one? List findings and ask. Never guess.
- Read Input File as-is, whatever its state. Missing or contradictory info in it is a gap (see Overturning).
- Read whole Input File. Every entry in its Decision Log is settled branch: never re-ask it.
- Read any other file User supplies as-is, like rest of Input. Example: previous Dossier or Overturn Report.

## Process

Strictly follow Caveman Protocol in all User interaction, grilling rounds, confirmations, and Dossier content.

1. **Resolve and read Input** as above.
2. **Generate Draft File** with Template Generator Script.
3. **Read and execute `RED-TEAM.md`.** It produces candidate impacts.
4. **Read and execute `GRILL-IMPACT.md`.** It settles every candidate with User and validates Dossier with Validation Script. It writes Output File once User confirms.
5. **Finish**: tell User Output File path, that Analysis is complete, and that next step is Implementation Proposal.

Each step is blocked until the one before it has run to completion.
Do not declare Analysis complete while overturn is pending.

## Overturning

Analysis never edits Input File. Re-running `prep` fixes its gaps. You may suggest Overturn when any of these is true:

1. **Task Brief is ambiguous or contradictory**: different readings yield materially different impacts.
2. **Settling an impact would change Task Brief**: add, remove, or alter acceptance criterion, expected outcome, or scope boundary.
3. **System contradicts Dossier**: repository, its docs, or its history contradict Context entry or settled Decision Log entry.
4. **Non-discoverable fact is missing**: analysis depends on something you cannot find yourself, and Context lacks it. Examples: external spec, tacit constraint, external consumer, deadline.

Overturn vs ordinary work:

- Codebase facts: yours to find.
- Impact dispositions: User decisions in `GRILL-IMPACT.md`.
- Overturn: only missing or wrong *task definition* or *non-discoverable context*.

Gap found:

1. Remaining analysis does not depend on gap? Finish current red-team pass. Depends on it? Stop immediately.
2. Present every gap to User and suggest Overturn. User may settle gap on the spot instead. Skill then continues normally.
3. User accepts Overturn? Do not create or update Output File. Write gap report to Overturn Report. Per gap, state:
   - what is missing or contradicted;
   - evidence;
   - target Dossier and section (Task Brief, Context, or Decision Log);
   - skill(s) to run, in order;
   - question each skill must settle.

   Show User complete report as it will be written. Write it only after User confirms.
4. Tell User: re-run `prep` for this task with that report, and only then invoke `analysis` again. End run.

## Output

Output File, built from Dossier Template. Written once, at end of `GRILL-IMPACT.md`, after User confirms it.
Strictly caveman style, within schema constraints.
