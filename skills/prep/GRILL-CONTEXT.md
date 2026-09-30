---
name: prep-grill-context
description: Second grilling session of the Preparation step (step 1 of the team's AI collaboration framework). Starting from a confirmed Task Brief, it explores the codebase and grills the developer until all the context and reference material the task needs has been compiled, then writes the Context section of `.ai/tasks/<task_name>/01-brief-and-context.md`. Invoked by the `prep` skill, or directly by the developer to re-run context gathering.
---

# Prep: Grill the Context

Compile **all the context and reference material** needed for the task described in the confirmed Task Brief, then write the Context section.

## Input & References

- [brief-and-context.md](references/brief-and-context.md): The base structure for the output file

Read `.ai/tasks/<task_name>/01-brief-and-context.md`. Its Task Brief must be filled in and confirmed.
If it isn't, stop and tell the developer to run `prep-grill-task` first.
Treat every entry already in the Decision Log as a settled branch.

## Grilling protocol

*Adapted from Matt Pocock's `grilling` skill (github.com/mattpocock/skills).*

Interview the developer relentlessly. Map the conversation as a **design tree**: every item of context branches into the
questions that depend on it.
Work in **rounds**. The **frontier** is every question whose prerequisites are already settled. Ask the whole frontier
in one round: number each question, continuing from the last number in the Decision Log, and give your recommended answer
to each. Then wait for the developer's answers.

```
**Q<n>** - **<question title>**: <question body; may include multiple choices and/or paragraphs>

Recommendation: <your recommended answer>
```

Each set of answers reshapes the tree. Recompute the frontier and ask the next round. A question that depends on another
question still open in the current round belongs to a *later* round.

**Facts are your job; decisions are the developer's.** If you can dispatch sub-agents, send them to explore in parallel.
Otherwise, ask the questions that don't depend on exploration first, and explore while the developer answers.

The session is done only when **every acceptance criterion maps to at least one context entry, or to an explicit "no prior
art"**, every branch has been visited, and no open questions remain.

Then summarize the Context section and ask the developer to confirm it. Do not write anything until they confirm.

## How to gather context

**Discover first, then confirm.** Starting from the brief's problem, outcome, and acceptance criteria, search the repository,
its docs, and its git history yourself. Put what you find to the developer as relevance questions ("I found X; is it relevant,
and why?"), with your recommendation for each. Don't ask the developer to point you to things you can find yourself.

**Ask directly only about what can't be discovered:** tacit constraints, external specs and APIs, deadlines, people who 
own or know the area, and prior art that exists only in someone's head.

Cover these branches:

1. **Codebase**: the modules, areas, and file paths involved, and why each one matters to this task.
2. **Conventions and prior art**: established patterns, ADRs, and similar past work to follow or reuse.
3. **Related work**: tickets, PRs, and branches that overlap with or affect this task (including linked ClickUp tasks, if a ClickUp tool is available).
4. **External references**: third-party docs, APIs, and specs.
5. **Constraints**: technical, security, performance, and deadline constraints.
6. **People to consult**: owners, reviewers, and domain experts.

Record facts and pointers, not designs. If a question drifts toward *how* to implement the task, note that it belongs to
later steps and move on.

## Writing the file

Once the developer confirms, append to the file `.ai/tasks/*/01-brief-and-context.md` the Context section, using the
predefined structure, filling in every subsection (write "None" where something genuinely doesn't apply). Append this 
session's decisions to the Decision Log, and update the status line to `Completed`. On a re-run, update entries in place.
File paths are encouraged here. Write the file's contents in the developer's language.

