# Prep: Grill the Task

Reach a **shared understanding of the task** with the user, leaving no room for ambiguity or assumptions of any kind, then write the Task Brief.

## Input

The resolved story, plus any other file the user supplied (e.g. a previously generated dossier or an overturn report), read as-is.

## Grilling session

Follow the grilling protocol, seeding the tree with these branches and expanding each one until they are all fully settled:

1. **Problem and who has it**: whose problem this is, and why it matters now.
2. **Expected outcome**: what "done" looks like, from the end user's perspective.
3. **Acceptance criteria**: each one concrete and verifiable. Rewrite vague criteria ("should be fast", "handle errors") until they are measurable or observable.
4. **Scope boundaries**: what is explicitly in scope and what is out of scope.
5. **Dependencies and blockers**: other tasks, teams, services, or decisions this task relies on.
6. **Ambiguities in the story's wording**: terms, actors, or behaviors the story leaves open to more than one interpretation.

In the first round, also propose the `<task_name>`: `<ClickUp-ID>-<kebab-case-slug>` when there is a ticket, otherwise just `<kebab-case-slug>`.

## Completion rule

The session is done only when **no open questions and no unconfirmed assumptions remain**: every branch has been visited, every acceptance criterion is verifiable, and every assumption has been either confirmed or replaced by a decision. Unresolved items are never written down as open questions. Keep grilling until they are resolved.

Then show the user the complete dossier file as it will be written and ask them to confirm it. Do not write anything until they confirm.

## Writing the file
Once the user confirms, write the dossier at the Output File path, creating it from the Dossier Template. Set the Status to `Context Pending`, fill in the Task Brief section and append this session's decisions to the Decision Log, starting at Q1. Leave the Context section untouched and keep the template's section headings and field labels unchanged so later steps can locate them; write all other content in the user's language.
