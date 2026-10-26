# Implementation Proposal: Grill the Design

Settle with the User **every real design decision**, turn the settled design into a recipe, and write the output dossier.

## Input

The Draft File and the Input. Treat all of it as settled branches.

## Grilling session

Run **one** grilling session (it may span several rounds), following the Grilling Protocol. Seed the tree with one branch per decision in the Draft File, with the decisions others depend on (the overall approach) before those that refine it (names, shapes, placement).

For each decision, ask a single question that presents the options, the evidence, and each option's consequence, and give your recommendation. The User accepts or amends it.

Keep the tree tight:

- If the User proposes a new option, test it as in `DRAFT-DESIGN.md` before adding it as a branch.
- If the chosen option would worsen or widen an accepted or deferred impact, say so with the evidence.
- If an answer can only be given by changing the Input, or rests on a fact that belongs in it, clarify with the User. You may also suggest an Overturn.
- If a question drifts toward test suites, documentation, or PR text, drop it and move on.

Update the Draft File after every round.

## Building the recipe

Once every decision is settled, build the proposal from the Dossier Structure.

**Design Summary**: in 2–5 sentences, the chosen design and why it meets every target without worsening any accepted or deferred impact.

**Targets**: one `T<n>` entry per target in the Draft File.

- **Source**: where the Input states the target, with its id there if it has one.
- **Statement**: the target, including any condition under which it applies and any verification it requires.

**Recipe**: one `S<n>` entry per step, listed in execution order. Step 4 executes them top to bottom.

- **Action**: exactly one of `Create`, `Modify`, `Delete`, or `Run`.
- **Touches**: the exact file paths and symbols. For `Create`, the new path and the symbols it defines. For `Run`, the files, data, or systems the command changes. `None` for steps that don't introduce changes (e.g. `cat`).
- **Behavior**: what holds once the step is done, including the edge cases the Input and the Draft File raised. For `Run`, the exact command, the directory it runs from, and its expected outcome.
- **Contract**: `Literal, below` when the step creates or changes a contract: signatures, schemas, configuration keys, migration, messages, endpoints, etc. Otherwise `None`.

**Literal blocks**: after a step's last field, leave a blank line and write each literal as a fenced code block indented exactly two spaces on every line, fences included. When a step has more than one literal, precede each with an indented one-line label naming its file and symbol. Give the final content of each contract as it must read after the step: the whole signature, schema, or block, never a diff. The indentation is mandatory: the Dossier Validator doesn't recognize code fences, so an unindented literal line starting with `## ` or `### ` is parsed as a heading, and every step after it silently escapes validation.

**Checks**: one `V<n>` entry per check:

- **Method**: something exact, observable from outside the component. Never "read the code" or similar.
- **Expected**: a pass condition an observer can decide unambiguously.
- **Verifies**: the target ids it verifies, or `None`.

**Certifications**: one `C<n>` entry per target that already holds with no change: the claim, and the evidence that proves it.

**Traceability**: one line per target. A target stays unmet only if the User declined the Overturn for it; its line then reads `T<n> — Met by: None — Checks: None`.

**Decision Log**: one entry per question settled in the grilling session or gap the User settled on the spot, numbered from Q1. Never carry over question ids from the Input.

## Completion rule

Keep working until all of the following hold:

1. **Every step names the exact files and symbols it touches**
2. **Every step gives literal content for every contract it creates or changes**
3. **Every step has at least one check**, and every check's Method is observable from outside the component.
4. **No step leaves a choice open.** Wording such as "e.g.", "as appropriate", "optionally", "consider", "TBD" is prohibited.
5. **The recipe is followable by both an agent and a human developer.**
6. **Every target traces.** Every target is traced to from at least one step's Check, unless the User declined the Overturn for it.

Then write the proposal to the Preview File and validate it (see below). Show the User the complete dossier as it will be written and ask them to confirm it. Do not write the Output File until they confirm.

## Writing the file

Run the scripts with the skill's directory as the working directory. Both need Python 3.8+ and the standard library only. Exit codes are 0 for ok, 1 for invalid, and 2 for usage errors.

1. **Render the template**: `python3 scripts/dossier-renderer assets/impl-proposal.json``. Fill it in at the Preview File, overwriting any file already at that path. Keep the section headings, field labels, and the fixed values `None`, `Literal, below`, `Create`, `Modify`, `Delete`, and `Run` unchanged. Write all other content in the User's language. Remove the template's comments.
2. **Validate**: `python3 scripts/dossier-validator <Preview File> assets/impl-proposal.json`. Fix every error and re-run until it exits with 0. The validator checks structure only: the completion rule's checks remain yours.

3. **Write**: once the User confirms, move the Preview File to the Output File path.
4. **Clean up**: delete the Draft File, and the Preview File if it remains. Never delete the Overturn Report or the Session Save File, and never modify any file in the Input.
