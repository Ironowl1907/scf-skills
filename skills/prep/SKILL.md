---
name: prep
description: Step 1 (Preparation) of the team's 8-step AI collaboration framework. Takes in a task and interviews the user to produce a confirmed task brief and context/reference dossier. Must only be invoked manually by the User.
---

# Prep

Compile everything the later steps of the framework need to know about **one task**: a shared understanding of what the task is, and the context and reference material needed to do it. Preparation records *what* and *with what*, never *how*. Do not propose designs, implementations, or tests; those belong to later steps.

## References

- [Brief Grilling](GRILL-BRIEF.md)
- [Context Grilling](GRILL-CONTEXT.md)
- [Grilling Protocol](references/grilling.md)
- [Caveman Protocol](references/caveman.md)
- [Template Generator Script](scripts/dossier-renderer)
- [Validation Script](scripts/dossier-validator)
- [Dossier Template](assets/brief-and-context.json)
- Output File: `.ai/tasks/<task_name>/01-brief-and-context.md`
- Draft File: `.ai/tasks/<task_name>/01-brief-and-context.draft.md`

## Input

The user's invoking message contains the task: a free-text user story, and/or a ClickUp task ID/URL:
- **ClickUp ID/URL**: if a ClickUp tool is available, fetch the task (title, description, acceptance criteria, comments, linked tasks, attachments). If no ClickUp tool is available, say which tool is missing, ask the user to paste the story, and continue from the pasted text. Never guess a ticket's contents.
- **Free text and other files**: Documents, paragraphs, and any other material. Use as-is.

## Process

Strictly adhere to the Caveman Protocol across all user interactions, questioning/grilling cycles, confirmations, and generated dossier content.

1. **Resolve the input** as described above.
2. **Generate the Draft File** by using the Template Generator Script.
3. **Read and execute the brief grilling** with the resolved story. It proposes the `<task_name>`, creates the file, and writes the Task Brief once the user confirms it.
4. **Read and execute the context grilling** on the same task. It validates the completed Dossier using the Validation Script, then writes the Context section once the user confirms it.
5. **Finish**: tell the user the file's path and that Preparation is complete, and say that the next step is Analysis & Design.

Each step is blocked until the one before it has run to completion.

## Output

A dossier file under the Output File Directory, written incrementally by the two sub-skills, and formatted strictly in caveman style while adhering to schema constraints.
