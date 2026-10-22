# Prep: Grill the Context

Compile **all the context and reference material** needed for the task described in the confirmed Task Brief, then write the Context section.

## Input

Read the Dossier's Task Brief section, as written by the brief grilling.
Treat every entry already in the Decision Log as a settled branch.
If an overturn report was passed, grill every gap in it that targets the Context.

## Grilling session

**Discover first, then confirm.** Starting from the brief's problem, outcome, and acceptance criteria, search the repository, its docs, and its git history yourself. State what you find to the user as relevance questions ("I found X; is it relevant, and why?"), with your recommendation for each. Don't ask the user to point you to things you can find yourself.

**Ask directly only about what can't be discovered:** tacit constraints, external specs and APIs, deadlines, and prior art that exists only in someone's head.

Follow the grilling protocol, seeding the tree with these branches and expanding each one until they are all fully settled:

1. **Codebase**: the modules, areas, and file paths involved, and why each one matters to this task.
2. **Conventions and prior art**: established patterns, ADRs, and similar past work to follow or reuse.
3. **Related work**: tickets, PRs, and branches that overlap with or affect this task (including linked ClickUp tasks, if a ClickUp tool is available).
4. **External references**: third-party docs, APIs, and specs.
5. **Constraints**: technical, security, performance, and deadline constraints.

Record facts and pointers, not designs. If a question drifts toward *how* to implement the task, note that it belongs to later steps and move on.

## Completion rule

The session is done only when every branch has been settled and no open questions remain.

## Writing the file

Fill in the Dossier's Context section using the predefined structure, filling in every subsection (write "None" where something genuinely doesn't apply). Append this session's decisions to the Decision Log, continuing its Q<n> numbering. File paths are encouraged here. Write the file's contents in the user's language, but keep the template's section headings and field labels unchanged so later steps can locate them.

Write this completed Dossier to the Draft File and run the Validation Script on it. Do not proceed if warnings or errors are raised; iterate on the dossier structure until all validation requirements pass. Then show the user the complete dossier file as it will be written and wait for their confirmation. Once the user confirms, write it to the Output File path and delete the Draft File.
