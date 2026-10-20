# Implementation Proposal: Grill the Design

Settle with the user **every real design decision**, turn the settled design into a recipe, and write the output dossier.

## Input

The Draft File, and the rest of the Input Data. Treat all of that data as settled branches.

## Grilling session

Run **one** grilling session (it may span several rounds), following the Grilling Protocol. Seed the tree with one branch per decision in the Draft File, with the decisions others depend on (the overall approach) before those that refine it (names, shapes, placement).

For each decision, ask a single question that presents the options, the evidence, and each option's consequence, and give your recommendation. The user accepts or amends it.

Keep the tree tight:

- If the user proposes a new option, test it as in `DRAFT-DESIGN.md` before adding it as a branch.
- If the chosen option would worsen or widen a deferred impact, say so with the evidence.
- If an answer can only be given by changing an input dossier, or rests on a fact that belongs in one, clarify with the user. You may also suggest an overturn.
- If a question drifts toward test suites, documentation, or PR text, drop it and move on.

Update the Draft File after every round.

## Building the recipe

Once every decision is settled, build the proposal from the Dossier Structure.

**Design Summary**: in 2–5 sentences, the chosen design and why it meets every target without worsening any deferred impact.

**Recipe**: one `S<n>` entry per step, listed in execution order. Step 4 executes them top to bottom.

- **Action**: exactly one of `Create`, `Modify`, `Delete`, or `Run`.
- **Touches**: the exact file paths and symbols. For `Create`, the new path and the symbols it defines. For `Run`, the files, data, or systems the command changes. `None` for steps that don't introduce changes (e.g. `cat`).
- **Behavior**: what holds once the step is done, including the edge cases the analysis raised. For `Run`, the exact command, the directory it runs from, and its expected outcome.
- **Contract**: `Literal, below` when the step creates or changes a contract: signatures, schemas, configuration keys, migration, messages, endpoints, etc. Otherwise `None`.

**Literal blocks**: after a step's last field, leave a blank line and write each literal as a fenced code block indented exactly two spaces on every line, fences included. When a step has more than one literal, precede each with an indented one-line label naming its file and symbol. Give the final content of each contract as it must read after the step: the whole signature, schema, or block, never a diff. The indentation is mandatory: the Dossier Validator doesn't recognize code fences, so an unindented literal line starting with `## ` or `### ` is parsed as a heading, and every step after it silently escapes validation.

**Checks**: one `CH<n>` entry per check:

- **Method**: something exact, observable from outside the component. Never "read the code" or similar.
- **Expected**: a pass condition an observer can decide unambiguously.
- **Verifies**: the AC / obligations it verifies, or `None`.

## Completion rule

Keep working until all of the following hold:

1. **Every step names the exact files and symbols it touches**
2. **Every step gives literal content for every contract it creates or changes**
3. **Every step has at least one check**, and every check's Method is observable from outside the component.
4. **No step leaves a choice open.** Wording such as "e.g.", "as appropriate", "optionally", "consider", "TBD" is prohibited.
5. **The recipe is followable by both an agent and a human developer.**
6. **Every target traces.** Every AC / obligation can be traced to from at least one step's Check, unless they are outright unmet.

Then write the proposal to the Preview File and validate it (see below). Show the user the complete dossier as it will be written and ask them to confirm it. Do not write the Output File until they confirm.

## Writing the file

Run the scripts with the skill's directory as the working directory. Both need Python 3.8+ and the standard library only. Exit codes are 0 for ok, 1 for invalid, and 2 for usage errors.

1. **Render the template**: `python3 scripts/dossier-renderer assets/impl-proposal.json`. Fill it in at the Preview File. Keep the section headings, field labels, and the fixed values `None`, `Literal, below`, `Create`, `Modify`, `Delete`, and `Run` unchanged. Write all other content in the user's language. Remove the template's comments.
2. **Validate**: `python3 scripts/dossier-validator <Preview File> assets/impl-proposal.json`. Fix every error and re-run until it exits with 0. The validator checks structure only: the completion rule's checks remain yours.
3. **Write**: once the user confirms, move the Preview File to the Output File path. Do not record processed question ids from input dossiers.
4. **Clean up**: delete the Draft File, the Preview File, and the Overturn Report, if any. Never modify the input dossiers.
