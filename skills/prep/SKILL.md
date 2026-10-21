---
name: prep
description: Step 1 (Preparation) of the team's 8-step AI collaboration framework. Takes in a task and interviews the user to produce a confirmed task brief and context/reference dossier. Must only be invoked manually by the user.
---

# Prep

Compile everything the later steps of the framework need to know about **one task**: a shared understanding of what the task is, and the context and reference material needed to do it. Preparation records *what* and *with what*, never *how*. Do not propose designs, implementations, or tests; those belong to later steps.

## References

- [Brief Grilling](GRILL-BRIEF.md)
- [Context Grilling](GRILL-CONTEXT.md)
- [Grilling Protocol](references/grilling.md)
- [Dossier Template](assets/brief-and-context.json)
- [Template Generator Script](scripts/dossier_renderer)
- [Validation Script](scripts/dossier_validator)
- [Caveman Protocol](references/caveman.md)
- Input File (if the user mentions an overturn): `.ai/tasks/<task_name>/NN-<name>.overturn.md`
- Output File: `.ai/tasks/<task_name>/01-brief-and-context.md`

## Input

The user's invoking message contains the task: a free-text user story, and/or a ClickUp task ID/URL:
- **ClickUp ID/URL**: if a ClickUp tool is available, fetch the task (title, description, acceptance criteria, comments, linked tasks, attachments). If no ClickUp tool is available, say which tool is missing, ask the user to paste the story, and continue from the pasted text. Never guess a ticket's contents.
- **Free text**: a document or paragraph(s). Use as-is.
- **Overturn report**: if the user passes a downstream step's overturn report, read it. Every gap that targets this skill's dossier must be settled in this run.

## Process

1. **Resolve the input** as described above.
2. **Generate the Dossier template** by using the Template Generator Script.
3. **Check for an existing dossier file** matching this task (same ClickUp ID or same slug). If one exists, this is a re-run: read it, and treat every entry in its Decision Log as a settled branch. Only grill what is missing or what the user says has changed.
4. **Read and execute the brief grilling** with the resolved story. It proposes the `<task_name>`, creates the file, and writes the Task Brief once the user confirms it.
5. **Read and execute the context grilling** on the same task. It writes the Context section once the user confirms it.
6. **Validate the Dossier** using the Validation Script. Do not proceed if warnings or errors are raised; iterate on the dossier structure until all validation requirements pass.
7. **Finish**: tell the user the file's path and that Preparation is complete, and say that the next step is Analysis & Design.

## Communication Style
Strictly adhere to [Caveman Protocol](references/caveman.md) across all user interactions, questioning/grilling cycles, confirmations, and generated dossier content.

Each step is blocked until the one before it has run to completion.

## Output

A dossier file under the Output File Directory, written incrementally by the two sub-skills.
Formatted strictly in caveman style while adhering to schema constraints.
