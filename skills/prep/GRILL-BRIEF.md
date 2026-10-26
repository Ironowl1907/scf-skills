# Prep: Grill the Task

Goal: **shared understanding of task** with user. Zero ambiguity, zero assumptions. Then write Task Brief.

## Input

Resolved story plus anything user supplies. Read as-is.

## Grilling session

Follow grilling protocol. Seed tree with these branches. Expand each until all fully settled:

1. **Problem and who has it**: whose problem, why it matters now.
2. **Expected outcome**: what "done" looks like for end user.
3. **Acceptance criteria**: each concrete, verifiable. Rewrite vague criteria ("should be fast", "handle errors") until measurable or observable.
4. **Scope boundaries**: what is explicitly in scope, what is out.
5. **Dependencies and blockers**: other tasks, teams, services, decisions this task relies on.
6. **Ambiguities in story wording**: terms, actors, behaviors open to more than one interpretation.

First round: also propose short `<task_name>`. Ticket exists: `<ClickUp-ID>-<kebab-case-slug>`. No ticket: `<kebab-case-slug>` only.

## Completion rule

Session done only when **no open questions and no unconfirmed assumptions remain**:
- every branch visited
- every acceptance criterion verifiable
- every assumption confirmed or replaced by decision

Never write unresolved items as open questions. Keep grilling until resolved.

Then show user complete dossier file exactly as it will be written. Ask user to confirm. Write nothing before confirmation.

## Writing the file

User confirms: fill Task Brief sections. Append session decisions to Decision Log, starting at Q1. Leave Context section and field labels untouched. Write all other content in user's language.
