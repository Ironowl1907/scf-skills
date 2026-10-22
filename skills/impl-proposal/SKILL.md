---
name: impl-proposal
description: Step 3 (Implementation Proposal) of the team's 8-step AI collaboration framework. Takes in the curated Input, drafts an implementation design, settles each decision with the User, and produces a step-by-step implementation recipe that Step 4 can follow. Must only be invoked manually by the User.
---

# Implementation Proposal

Turn the Input into a **recipe**: an ordered list of steps that an agent or a human developer can follow to the letter without making any decision. The proposal settles **how** the task is done. Never **what** the task is or **which** consequences to address. That is the User's job to decide.

## References

- [Design Drafting](DRAFT-DESIGN.md)
- [Design Grilling](GRILL-DESIGN.md)
- [Grilling Protocol](references/grilling.md)
- [Impact Lenses](references/impact-lenses.md)
- [Dossier Structure](assets/impl-proposal.json)
- [Dossier Renderer](scripts/dossier-renderer)
- [Dossier Validator](scripts/dossier-validator)
- [Caveman Protocol](references/caveman.md)
- Draft File: `.ai/tasks/<task_name>/03-impl-proposal.draft.md`
- Output File: `.ai/tasks/<task_name>/03-impl-proposal.md`
- Overturn Report: `.ai/tasks/<task_name>/03-impl-proposal.overturn.md`
- Preview File: `.ai/tasks/<task_name>/03-impl-proposal.preview.md`

## Input

The user's invoking message details the task at hand, usually including a mix of acceptance criteria, scope boundaries, things to look out for and dangers to prevent. You must take the input as-is, whatever it's state may be. The user is able to clarify when information is missing or wrong, so do ask only the most important questions if you find it necessary, but never re-ask anything that you can find out from the input or its references.

## Process

Follow the Caveman Protocol in every interaction with the User and in every file you write.

1. **Read the input** as described above.
2. **Read and execute `DRAFT-DESIGN.md`.** It finds the viable designs and the decisions they rest on.
3. **Read and execute `GRILL-DESIGN.md`.** It settles every decision with the user, builds the recipe, and writes the output dossier once they confirm it.
4. **Finish**: tell the user the output file's path, that Implementation Proposal is complete, and that the next step is Implementation.

Each step is blocked until the one before it has run to completion.

## Overturning

This skill never corrects its Input; the User settles every gap, either on the spot or by re-running earlier steps. You may suggest an Overturn in the following cases:

1. **Gap in the Input**: a key piece of information is missing, ambiguous, contradictory, or contradicted by the system, in a way that changes the design.
2. **Unmeetable target**: a target can be neither met nor certified with evidence. This also holds if, for example, the target conflicts with another target or with a scope boundary.
3. **Unavoidable unanalyzed impact**: every viable design introduces the same impact the Input does not account for. If some viable design avoids it, prefer that design instead; that is not an Overturn.

Distinguish Overturns from ordinary work: facts about the codebase are yours to find; choices between viable designs are the User's decisions in `GRILL-DESIGN.md`; only missing or wrong information in the Input is an Overturn. The User always has the final say: if they settle a gap on the spot instead, continue normally and record the settlement in the Decision Log.

If the User accepts an Overturn:

1. Stop immediately.
2. Offer to save this session's work to a file of the User's choosing. If they accept, show its complete content and write it once they confirm.
3. Show the Overturn Report's complete content and write it once the User confirms. For each gap, it states: what is missing or contradicted, where it belongs in the Input, the evidence, the skill(s) to re-run in order, and the question each skill needs to settle.
4. Delete the Draft File and the Preview File, if any.
5. Tell the User the paths of the files written, and to come back once the gaps have been amended.

## Output

The output dossier at the Output File path, structured by the Dossier Structure, written once at the end of `GRILL-DESIGN.md`, after it passes the Dossier Validator and the User confirms it. Written in caveman style, within the schema's constraints.
