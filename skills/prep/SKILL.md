---
name: prep
description: Step 1 (Preparation) of the team's 8-step AI collaboration framework. Takes in a task and interviews the User to produce a confirmed task brief and context/reference Dossier. Must only be invoked manually by the User.
---

# Prep

Compile what later framework steps need about **one task**: shared understanding of task, plus context and reference material to do it. Record *what* and *with what*. Never *how*. No designs, implementations, or tests: later steps own those.

## References

- [Brief Grilling](GRILL-BRIEF.md)
- [Context Grilling](GRILL-CONTEXT.md)
- [Grilling Protocol](references/grilling.md)
- [Caveman Protocol](references/caveman.md)
- [Dossier Renderer](scripts/dossier-renderer)
- [Dossier Validator](scripts/dossier-validator)
- [Dossier Structure](assets/impl-proposal.json)
- Draft File: `.ai/tasks/<task_name>/01-brief-and-context.draft.md`
- Output File: `.ai/tasks/<task_name>/01-brief-and-context.md`

## Input

Invoking message holds task: free-text user story, ClickUp task ID/URL, or both.
- **ClickUp ID/URL**: ClickUp tool available? Fetch task: title, description, acceptance criteria, comments, linked tasks, attachments. No ClickUp tool? Name missing tool. Ask User to paste story. Continue from pasted text. Never guess ticket contents.
- **Free text and other files**: documents, paragraphs, any other material. Use as-is.

## Process

Follow Caveman Protocol strictly in all User interaction, grilling cycles, confirmations, and Dossier content.

1. **Resolve Input** per Input section.
2. **Read and run brief grilling** on resolved story. It proposes `<task_name>`, creates Draft File, fills Task Brief after User confirms.
3. **Read and run context grilling** on same task. It validates completed Dossier with Validation Script, then writes Context section after User confirms.
4. **Finish**: give User file path. Say Preparation complete. Next step: Analysis & Design.

Each step blocked until previous step completes.

## Output

Dossier file in Output File directory. Two sub-procedures write it incrementally. Format: strict caveman style, within schema constraints.
