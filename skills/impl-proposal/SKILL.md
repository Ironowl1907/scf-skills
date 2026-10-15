---
name: impl-proposal
description: Step 3 (Implementation Proposal) of the team's 8-step AI collaboration framework. Takes in the task dossiers produced by Step 1 (prep) and Step 2 (analysis), drafts a design that meets every acceptance criterion and obligation without worsening any deferred impact, settles each design decision with the user, and produces a step-by-step implementation recipe that Step 4 can follow without making any decision. Must only be invoked manually by the user.
---

# Implementation Proposal

Turn one task's brief, context, and analysis into a **recipe**: an ordered list of steps that an agent or a human developer can follow to the letter without making any decision. The proposal settles **how** the task is done. It never changes **what** the task is or **which** impacts must be addressed: those belong to the input dossiers, and gaps in them are overturned, never patched here.

## References

- [Design Drafting](DRAFT-DESIGN.md)
- [Design Grilling](GRILL-DESIGN.md)
- [Grilling Protocol](references/grilling.md)
- [Impact Lenses](references/impact-lenses.md)
- [Dossier Structure](assets/impl-proposal.json)
- [Dossier Renderer](scripts/dossier-renderer)
- [Dossier Validator](scripts/dossier-validator)
- Input Files: `.ai/tasks/<task_name>/01-brief-and-context.md`, `.ai/tasks/<task_name>/02-analysis.md`
- Output File: `.ai/tasks/<task_name>/03-impl-proposal.md`
- Draft File: `.ai/tasks/<task_name>/03-impl-proposal.draft.md`
- Preview File: `.ai/tasks/<task_name>/03-impl-proposal.preview.md`
- Overturn Report: `.ai/tasks/<task_name>/03-impl-proposal.overturn.md`

## Input

The user's invoking message identifies the task by `<task_name>`, by ClickUp ID/URL, or by the path to its directory or to one of its dossiers.

- Resolve it to exactly one `.ai/tasks/<task_name>/` directory. For a ClickUp ID, match the directory whose name starts with that ID. If nothing or more than one thing matches, list what you found and ask. Never guess.
- If `01-brief-and-context.md` is missing, stop: tell the user to run `prep`, then `analysis`, and abort. If only `02-analysis.md` is missing, stop: tell the user to run `analysis`, and abort.
- Otherwise read both input dossiers in full, as-is. Do not validate them in any way: not their status line, structure, or completeness. Their content may differ from the usual shape produced by `prep` and `analysis`. Missing or wrong information surfaces while drafting, and is handled by Overturning.
- Every entry in either input's Decision Log is a settled branch: never re-ask it.

Terms used throughout this skill:

- **AC<n>** is the n-th acceptance criterion in the Task Brief of `01-brief-and-context.md`, counted by position.
- **O<n>** and **I<n>** are the obligations and impacts of `02-analysis.md`, by their ids.
- **Targets** are every AC<n> and every O<n>: what the recipe must cover.
- A **deferred impact** is an impact in `02-analysis.md` whose disposition is Defer.
- An **unanalyzed impact** is an impact, in the sense of the Impact Lenses, that `02-analysis.md` does not record, or records at a smaller extent or severity than the design would cause.

## Process

1. **Resolve and read the input** as described above.
2. **Check for existing working files and output.**
   - If an Overturn Report exists, read it: each gap it lists must now be settled in the inputs. If one still isn't, overturn again with that gap.
   - If an output dossier exists, this is a re-run: read it, treat every entry in its Decision Log as settled, and keep its ids stable. Re-runs do not detect upstream changes on their own: only regrill what the user says has changed, what an Overturn Report targeted, or what the current inputs visibly contradict.
   - If a Draft File exists, carry forward the decisions it records as settled branches, unless the inputs have changed in a way that touches them. Then delete it and any Preview File.
3. **Read and execute `DRAFT-DESIGN.md`.** It finds the viable designs and the decisions they rest on.
4. **Read and execute `GRILL-DESIGN.md`.** It settles every decision with the user, builds the recipe, and writes the output dossier once they confirm it.
5. **Finish**: tell the user the output file's path, that Implementation Proposal is complete, and that the next step is Implementation.

Do not declare Implementation Proposal complete while an overturn is pending.
Each step is blocked until the one before it has run to completion.

## Overturning

This skill never edits the input dossiers; their gaps are fixed by re-running the skills that own them. Overturn when one of the following holds, and in no other case:

1. **Gap in `01-brief-and-context.md`**: the Task Brief or Context is missing, ambiguous, contradictory, or contradicted by the system, in a way that changes the design. Also when an acceptance criterion can be neither met nor certified. Re-run `prep`, then `analysis`.
2. **Gap in `02-analysis.md`**: an impact, obligation, disposition, or cross-reference is missing, ambiguous, undecidable, or contradicted by the system, in a way that changes the design. Re-run `analysis`.
3. **Unmeetable obligation**: an obligation can be neither met by any recipe step nor certified with evidence. Re-run `analysis`. If the cause lies in the Task Brief (for example, the obligation conflicts with an acceptance criterion or a scope boundary), re-run `prep`, then `analysis`.
4. **Worsened deferred impact**: the settled design would worsen or widen a deferred impact in any way: more severe, more likely, reaching more consumers or areas, or harder to address later. Re-run `analysis`.
5. **Unavoidable unanalyzed impact**: every viable design introduces the same unanalyzed impact. Re-run `analysis`. If some viable design avoids it, choose that design instead; that is not an overturn.

Distinguish overturns from ordinary work: facts about the codebase are yours to find; choices between viable designs are the user's decisions in `GRILL-DESIGN.md`; only missing or wrong information in the input dossiers is an overturn. An answer the user can give only by changing an input dossier is an overturn too.

When an overturn is found:

1. Finish the current drafting or grilling pass if the remaining work doesn't depend on the gap. If it does, stop immediately.
2. Do not create or update the output dossier. Keep the Draft File updated with every decision and finding the gap doesn't block.
3. Write every gap to the Overturn Report, each with: what is missing or contradicted, the evidence, the target dossier and section (Task Brief, Context, Impacts, Obligations, or Decision Log), the skill(s) to re-run in order, and the question that skill needs to settle.
4. Report the gaps to the user, and tell them to re-run the named skill(s) in order, passing them the Overturn Report, and only then to invoke `impl-proposal` again.

## Output

The output dossier at the Output File path, structured by the Dossier Structure, written once at the end of `GRILL-DESIGN.md`, after it passes the Dossier Validator and the user confirms it.
