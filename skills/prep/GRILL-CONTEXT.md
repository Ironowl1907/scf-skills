# Prep: Grill the Context

Compile **all context and reference material** the task the confirmed Task Brief needs. Then write the Context section.

## Input

Read Dossier's Task Brief section, written by the brief grilling.
Every Decision Log entry is a settled branch.

## Grilling session

**Discover first, then confirm.** Start from the brief's problem, outcome, and acceptance criteria. Search the repository, its docs, and its git history yourself. Relevance not certain? Present as relevance question ("I found X; is it relevant, and why?"), with recommendation. Never ask the User to point you to things you can find yourself.

**Ask directly only about what you cannot discover:** tacit constraints, external specs and APIs, prior art that exists only in someone's head.

Follow the grilling protocol. Seed the tree with these branches. Expand each until all are fully settled:

1. **Codebase**: modules, areas, and file paths involved, and why each matters to this task.
2. **Conventions and prior art**: established patterns, ADRs, similar past work to follow or reuse.
3. **Related work**: tickets, PRs, branches that overlap with or affect this task. Include linked ClickUp tasks if a ClickUp tool is available.
4. **External references**: third-party docs, APIs, specs.
5. **Constraints**: technical, security, performance, deadline.

Record facts and pointers, not designs. Question drifts toward *how* to implement? Note it belongs to later steps. Move on.

## Completion rule

Session done only when every branch is settled and no open questions remain.

## Writing the file

1. Fill the Dossier's Context section with the predefined structure. Fill every subsection. Write "None" only where something does not apply.
2. Append this session's decisions to the Decision Log. Continue its Q<n> numbering.
3. File paths encouraged here.
4. Write content in the User's language. Keep template section headings and field labels unchanged, so later steps can locate them.
5. Write the completed Dossier to the Draft File.
6. Run the Dossier Validator on it. Warnings or errors raised? Do not proceed. Fix the Dossier structure and rerun until all validation requirements pass.
7. Show the User the complete Dossier file as it will be written. Wait for confirmation.
8. User confirms? Write it to the Output File path. Then delete the Draft File.
