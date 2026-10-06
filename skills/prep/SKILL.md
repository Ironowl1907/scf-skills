---
name: prep
description: Step 1 (Preparation) of the team's 8-step AI collaboration framework. Takes in a task and interviews the developer to produce a confirmed task brief and context/reference dossier. Must only be invoked manually by the user.
metadata:
  disable-model-invocation: "true"
---

# Prep

Compile everything the later steps of the framework need to know about **one task**: a shared understanding of what the task is, and the context and reference material needed to do it. Preparation records *what* and *with what*, never *how*. Do not propose designs, implementations, or tests; those belong to later steps.

## References

- [Brief Grilling](GRILL-BRIEF.md)
- [Context Grilling](GRILL-CONTEXT.md)
- [Grilling Protocol](references/grilling.md)
- [Dossier Template](assets/brif-and-context.md)
- Output File Directory: `.ai/tasks/<task_name>/01-brief-and-context.md`

## Input

The developer's invoking message contains the task: a free-text user story, and/or a ClickUp task ID/URL:
- **ClickUp ID/URL**: if a ClickUp tool is available, fetch the task (title, description, acceptance criteria, comments, linked tasks, attachments). If no ClickUp tool is available, say which tool is missing, ask the developer to paste the story, and continue from the pasted text. Never guess a ticket's contents.
- **Free text**: a document or paragraph/s. Use as-is.

## Process

1. **Resolve the input** as described above.
2. **Check for an existing dossier file** matching this task (same ClickUp ID or same slug). If one exists, this is a re-run: read it, and treat every entry in its Decision Log as a settled branch. Only grill what is missing or what the developer says has changed. If there's no pre-existing file, create it using the Dossier Template.
4. **Read and execute the brief grilling** with the resolved story. It proposes the `<task_name>`, creates the file, and writes the Task Brief once the developer confirms it.
5. **Read and execute the context grilling** on the same task. It writes the Context section once the developer confirms it.
6. **Finish**: tell the developer the file's path and that Preparation is complete, and say that the next step is Analysis & Design.

Each step is blocked from execution until the one before it has run to completion.
Do not declare Preparation complete until both sessions are confirmed.

## Output

A dossier file under the Output File Directory, written incrementally by the two sub-skills.
