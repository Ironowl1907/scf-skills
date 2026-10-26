---
name: impl-proposal
description: Step 3 (Implementation Proposal) of the team's 8-step AI collaboration framework. Takes in the curated Input, drafts an implementation design, settles each decision with the User, and produces a step-by-step implementation recipe that Step 4 can follow. Must only be invoked manually by the User.
---

# Implementation Proposal

Turn Input into **recipe**: ordered steps an agent or human developer follows to the letter, no decisions left. Proposal settles **how** task is done. Never **what** task is, never **which** consequences to address. User decides those.

## References

- [Design Drafting](DRAFT-DESIGN.md)
- [Design Grilling](GRILL-DESIGN.md)
- [Caveman Protocol](references/caveman.md)
- [Grilling Protocol](references/grilling.md)
- [Impact Lenses](references/impact-lenses.md)
- [Dossier Renderer](scripts/dossier-renderer)
- [Dossier Validator](scripts/dossier-validator)
- [Dossier Structure](assets/impl-proposal.json)
- Draft File: `.ai/tasks/<task_name>/03-impl-proposal.draft.md`
- Output File: `.ai/tasks/<task_name>/03-impl-proposal.md`
- Overturn Report: `.ai/tasks/<task_name>/03-impl-proposal.overturn.md`
- Preview File: `.ai/tasks/<task_name>/03-impl-proposal.preview.md`

## Input

Invoking message holds task: usually acceptance criteria, scope boundaries, things to watch, dangers to prevent.
- Take Input as-is, whatever its state.
- Info missing or wrong? User can clarify. Ask only most important questions, only if needed.
- Never ask what Input or its references already answer.

## Process

Follow Caveman Protocol in every User interaction and every file written.

1. **Read Input** per Input section.
2. **Read and run `DRAFT-DESIGN.md`.** Finds viable designs and decisions they rest on.
3. **Read and run `GRILL-DESIGN.md`.** Settles every decision with User, builds recipe, writes output Dossier after User confirms.
4. **Finish**: give User output file path. Say Implementation Proposal complete. Next step: Implementation.

Each step blocked until previous step completes.

## Overturning

Skill never corrects its Input. User settles every gap: on the spot, or by re-running earlier steps. Overturn may be suggested when:

1. **Gap in Input**: key info missing, ambiguous, contradictory, or contradicted by system, and it changes design.
2. **Unmeetable target**: target can be neither met nor certified with evidence. Includes target conflicting with another target or with scope boundary.
3. **Unavoidable unanalyzed impact**: every viable design introduces same impact, and Input does not account for it. Some viable design avoids it? Prefer that design. Not an Overturn.

Overturn vs ordinary work:
- Codebase facts: yours to find.
- Choices between viable designs: User decides in `GRILL-DESIGN.md`.
- Only missing or wrong Input info is an Overturn.

User has final say. User settles gap on the spot? Continue normally. Record settlement in Decision Log.

User accepts Overturn:

1. Stop immediately.
2. Offer to save session work to file of User's choosing. User accepts? Show complete content. Write only after User confirms.
3. Show Overturn Report complete content. Write only after User confirms. Per gap, state: what is missing or contradicted, where it belongs in Input, evidence, skill(s) to re-run in order, question each skill must settle.
4. Delete Draft File and Preview File, if present.
5. Give User paths of files written. Tell User to come back once gaps amended.

## Output

Output Dossier at Output File path. Structure: Dossier Structure. Written once, at end of `GRILL-DESIGN.md`, after it passes Dossier Validator and User confirms. Format: caveman style, within schema constraints.
