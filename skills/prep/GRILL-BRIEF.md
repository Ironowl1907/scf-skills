---
name: prep-grill-task
description: First grilling session of Preparation (step 1 of the team's AI collaboration framework). Interviews the developer relentlessly about a single task until there is a shared, unambiguous understanding of it, then writes the Task Brief of `.ai/tasks/<task_name>/01-brief-and-context.md`. Invoked by `prep`, or directly by the developer to re-run the task-understanding session.
---

# Prep: Grill the Task

Reach a **shared understanding of the task** with the developer, with nothing left ambiguous, then write the Task Brief.

## Grilling protocol

*Adapted from Matt Pocock's `grilling` skill (github.com/mattpocock/skills).*

Interview the developer relentlessly. Map the conversation as a **design tree**: every decision branches into the decisions that depend on it.

Work in **rounds**. The **frontier** is every decision whose prerequisites are already settled. Ask the whole frontier in one round: number each question, and give your recommended answer to each. Then wait for the developer's answers.

```
❓ **Q1** - **<question title>**: <question body; may include multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - ...
```

Each set of answers reshapes the tree. Recompute the frontier and ask the next round. A question that depends on another question still open in the current round belongs to a *later* round. Keep numbering questions across rounds.

**Facts are your job; decisions are the developer's.** Never ask for something you could look up in the repository, its docs, its git history, or the ticket. If you can dispatch sub-agents, send them to find facts in parallel. Otherwise, ask the questions that don't depend on those facts first, and investigate while the developer answers. Only questions that depend on a pending lookup wait for it.

## Design tree: root branches

Seed the tree with these branches and expand each one until it is fully settled:

1. **Problem and who has it**: whose problem this is, and why it matters now.
2. **Expected outcome**: what "done" looks like, from the user's perspective.
3. **Acceptance criteria**: each one concrete and verifiable. Rewrite vague criteria ("should be fast", "handle errors") until they are measurable or observable.
4. **Scope boundaries**: what is explicitly in scope and what is out of scope.
5. **Dependencies and blockers**: other tasks, teams, services, or decisions this task relies on.
6. **Ambiguities in the story's wording**: terms, actors, or behaviors the story leaves open to more than one interpretation.

In the first round, also propose the `<task_name>`: `<ClickUp-ID>-<kebab-case-slug>` when there is a ticket, otherwise just `<kebab-case-slug>`.

## Completion rule

The session is done only when **no open questions and no unconfirmed assumptions remain**: every branch has been visited, every acceptance criterion is verifiable, and every assumption has been either confirmed or replaced by a decision. Unresolved items are never written down as open questions. Keep grilling until they are resolved.

Then summarize the brief and ask the developer to confirm it. Do not write anything until they confirm.

## Writing the file

Once the developer confirms, create `.ai/tasks/<task_name>/01-brief-and-context.md` from the template below, if it doesn't already exist. Fill in the Task Brief and append this session's decisions to the Decision Log. On a re-run, update the brief in place and append new decisions instead of rewriting the log. Leave the Context section untouched. Write the file's contents in the developer's language.

