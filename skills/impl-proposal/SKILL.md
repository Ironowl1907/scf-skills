---
name: impl-proposal
description: Step 3 (Implementation Proposal) of the team's 8-step AI collaboration framework. Drafts an implementation design, settles each decision with the user, and produces a step-by-step implementation recipe that Step 4 can follow. Must only be invoked manually by the user.
---

# Implementation Proposal

Turn the user's input into a **recipe**: an ordered list of steps that an agent or a human developer can follow to the letter without making any decision. The proposal settles **how** the task is done. Never **what** the task is or **which** consequences to address. That is the user's job to decide.

## References

- [Design Drafting](DRAFT-DESIGN.md)
- [Design Grilling](GRILL-DESIGN.md)
- [Grilling Protocol](references/grilling.md)
- [Impact Lenses](references/impact-lenses.md)
- [Dossier Structure](assets/impl-proposal.json)
- [Dossier Renderer](scripts/dossier-renderer)
- [Dossier Validator](scripts/dossier-validator)
- Output File: `.ai/tasks/<task_name>/03-impl-proposal.md`
- Draft File: `.ai/tasks/<task_name>/03-impl-proposal.draft.md`
- Preview File: `.ai/tasks/<task_name>/03-impl-proposal.preview.md`
- Overturn Report: `.ai/tasks/<task_name>/03-impl-proposal.overturn.md`

## Input

The user's invoking message details the task at hand, usually including a mix of acceptance criteria, scope boundaries, things to look out for and dangers to prevent. You must take the input as-is, whatever it's state may be. The user is able to clarify when information is missing or wrong, so do ask only the most important questions if you find it necessary, but never re-ask anything that you can find out from the input or its references.

## Process

1. **Resolve and read the input** as described above.
2. **Delete existing working files and output**: They are likely from an older run and will contaminate the context.
3. **Read and execute `DRAFT-DESIGN.md`.** It finds the viable designs and the decisions they rest on.
4. **Read and execute `GRILL-DESIGN.md`.** It settles every decision with the user, builds the recipe, and writes the output dossier once they confirm it.
5. **Finish**: tell the user the output file's path, that Implementation Proposal is complete, and that the next step is Implementation.

Each step is blocked until the one before it has run to completion.

## Overturning

This skill never corrects its input; gaps are fixed by the user by optionally re-running the previous skills. You may suggest an Overturn in the following cases:

1. **Gap in the task's brief and/or context**: A key piece of information is missing, ambiguous, contradictory, or contradicted by the system, in a way that changes the design. Also when an acceptance criterion can be neither met nor certified.
2. **Gap in the analysis**: a key impact or obligation is missing, ambiguous, or contradicted by the system, in a way that changes the design.
3. **Unmeetable obligation**: an obligation can be neither met nor certified with evidence. This also holds if, for example, the obligation conflicts with an acceptance criterion or a scope boundary.
4. **Unavoidable unanalyzed impact**: every viable design introduces the same unanalyzed impact. If some viable design avoids it, choose that design instead; that is not an overturn.

Distinguish overturns from ordinary work: facts about the codebase are yours to find; choices between viable designs are the user's decisions in `GRILL-DESIGN.md`; only missing or wrong information in the input data is an overturn. The user always has the final say in this.

If the user agrees to an overturn:

1. Stop immediately.
2. Let the user decide whether to save this session's work in the corresponding files.
3. Write an Overturn Report containing: everything that's missing or contradicted, the evidence, the section, the skill(s) to optionally re-run in order, and the question to settle.
4. Give the report to the user, and tell them to come back once the gaps have been ammended.

## Output

The output dossier at the Output File path, structured by the Dossier Structure, written once at the end of `GRILL-DESIGN.md`, after it passes the Dossier Validator and the user confirms it.
