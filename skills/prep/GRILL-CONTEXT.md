# Prep: Grill the Context

Compile **all the context and reference material** needed for the task described in the confirmed Task Brief, then write the Context section.

## Input

Read the Dossier's Brief section. It must be filled in and confirmed.
If it isn't, stop and let the user know, then abort your task.
Treat every entry already in the Decision Log as a settled branch.

## Grilling session

**Discover first, then confirm.** Starting from the brief's problem, outcome, and acceptance criteria, search the repository, its docs, and its git history yourself. State what you find to the developer as relevance questions ("I found X; is it relevant, and why?"), with your recommendation for each. Don't ask the developer to point you to things you can find yourself.

**Ask directly only about what can't be discovered:** tacit constraints, external specs and APIs, deadlines, people who own or know the area, and prior art that exists only in someone's head.

Follow the grilling protocol, seeding the tree with these branches and expanding each one until they are all fully settled:

1. **Codebase**: the modules, areas, and file paths involved, and why each one matters to this task.
2. **Conventions and prior art**: established patterns, ADRs, and similar past work to follow or reuse.
3. **Related work**: tickets, PRs, and branches that overlap with or affect this task (including linked ClickUp tasks, if a ClickUp tool is available).
4. **External references**: third-party docs, APIs, and specs.
5. **Constraints**: technical, security, performance, and deadline constraints.
6. **People to consult**: owners, reviewers, and domain experts.

Record facts and pointers, not designs. If a question drifts toward *how* to implement the task, note that it belongs to later steps and move on.

## Writing the file

Once the developer confirms, fill in the Dossier's Context section, using the predefined structure, filling in every subsection (write "None" where something genuinely doesn't apply). Append this session's decisions to the Decision Log, and update the status line to `Completed`. On a re-run, update entries in place. File paths are encouraged here. Write the file's contents in the developer's language.
