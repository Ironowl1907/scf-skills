---
name: prep
description: Step 1 (Preparation) of the team's 8-step AI collaboration framework. Takes a task and runs two grilling sessions in order — prep-grill-task, then prep-grill-context — producing `.ai/tasks/<task_name>/01-brief-and-context.md`.
disable-model-invocation: true
---

# Prep

Compile everything the later steps of the framework need to know about **one task**:
a shared understanding of what the task is, and the context and reference material
needed to do it. Preparation records *what* and *with what*, never *how*. Do not
propose designs, implementations, or tests; those belong to later steps.

## Input

The developer's invoking message contains the task: a free-text user story, and/or a ClickUp task ID/URL.

- **ClickUp ID/URL**: if a ClickUp tool is available, fetch the task (title, description, acceptance criteria, comments, linked tasks, attachments). If no ClickUp tool is available, say which tool is missing, ask the developer to paste the story, and continue from the pasted text. Never guess a ticket's contents.
- **Free text**: a document or paragraph/s. Use as-is.

## Process

1. **Resolve the input** as described above.
2. **Check for an existing file** at `.ai/tasks/*/01-brief-and-context.md` matching this task (same ClickUp ID or same slug). If one exists, this is a re-run: read it, and treat every entry in its Decision Log as a settled branch. Only grill what is missing or what the developer says has changed.
3. **Read and execute `GRILL-BRIEF.md`** with the resolved story. It proposes the `<task_name>`, creates the file, and writes the Task Brief once the developer confirms it.
4. **Read and execute `GRILL-CONTEXT.md`** on the same task. It writes the Context section once the developer confirms it.
5. **Finish**: tell the developer the file's path and that Preparation is complete, and say that the next step is Analysis & Design.

Each step is blocked from execution until the one before it has run to completion.
Do not declare Preparation complete until both sessions are confirmed.

## Output

A single file: `.ai/tasks/<task_name>/01-brief-and-context.md`, written incrementally by the two sub-skills.
