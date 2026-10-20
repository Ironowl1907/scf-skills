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
- **Contract**: `Literal, below` when the step creates or changes a contract: a signature, schema, configuration key, migration, message (user-facing text, error or log format, event), file format, CLI command, endpoint, etc. Otherwise `None`.
- **Behavior**: what holds once the step is done, including the edge cases the analysis raised. For `Run`, the exact command, the directory it runs from, and its expected outcome.
- **Checks**: the checks that verify the step.

**Literal blocks**: after a step's last field, leave a blank line and write each literal as a fenced code block indented exactly two spaces on every line, fences included. When a step has more than one literal, precede each with an indented one-line label naming its file and symbol. Give the final content of each contract as it must read after the step: the whole signature, schema, or block, never a diff. The indentation is mandatory: the Dossier Validator doesn't recognize code fences, so an unindented literal line starting with `## ` or `### ` is parsed as a heading, and every step after it silently escapes validation.

**Checks**: one `V<n>` entry per check.

- **Method**: an exact command or action observable from outside the component: a CLI invocation, a request, a UI action, a file comparison, a script run. Never "read the code" or "inspect the implementation".
- **Expected**: a pass condition an observer can decide unambiguously.
- **Verifies**: the AC and obligation ids it verifies, or `None` for a check that only confirms its own step.
- Every obligation's Verification is realized by at least one check that lists it.

**Certifications**: one `C<n>` entry per target, or part of one, that already holds with no change: the **Claim**, and the **Evidence** proving it (paths, symbols, lines, references). A conditional obligation whose condition doesn't hold under the chosen design is certified as not applicable, with the design decision and the system as evidence. A certification only stands if no recipe step changes its evidence. A certified obligation still needs a check that realizes its Verification.

**Traceability**: one line per target, every AC in order and then every obligation in order, each reading `<id> — Met by: <step or certification ids> — Checks: <check ids>`.

**Decision Log**: one entry per question settled in this session, numbered from Q1 (never continuing an input dossier's numbering), including options ruled out for introducing unanalyzed impacts.

## Completion rule

Reject the proposal and keep working until all of the following hold:

1. **Every step names the exact files and symbols it touches, and its place in the order**: its position in the list, and a Depends on that cites only earlier steps.
2. **Every step gives literal content for every contract it creates or changes**, and the expected behavior for everything else.
3. **Every step has at least one check**, and every check's Method is observable from outside the component.
4. **No step leaves a choice open.** Reject wording such as "e.g.", "such as", "or similar", "as appropriate", "if needed", "optionally", "consider", "TBD", "unknown", or "to be confirmed" wherever it leaves a choice to the reader.
5. **The recipe is followable by both an agent and a human developer.** Every tool, command, and access it needs is named in the step that needs it, and no step relies on capabilities only one of them has.
6. **Every target traces.** Every AC and obligation has exactly one Traceability line, with at least one step or certification and at least one check. Every obligation's Verification is realized by a check that lists it.
7. **Every reference resolves.** Every id cited exists. Every check is cited by at least one step or Traceability line. Every step and certification is cited by at least one Traceability line, or is a prerequisite (Depends on) of a step that is.
8. **No overturn is pending.** The design worsens no deferred impact and introduces no unanalyzed impact.

Then write the proposal to the Preview File and validate it (see below). Show the user the complete dossier as it will be written and ask them to confirm it. Do not write the Output File until they confirm. If they amend it, apply the amendment, re-check the completion rule, re-validate, and show it again.

## Writing the file

Run the scripts with the skill's directory as the working directory, always passing the JSON path (both scripts require it, despite their docstrings). Both need Python 3.8+ and the standard library only. Exit codes are 0 for ok, 1 for invalid, and 2 for usage errors.

1. **Render the template**: `python3 scripts/dossier-renderer assets/impl-proposal.json`. Fill it in at the Preview File. Keep the section headings, field labels, and the fixed values `None`, `Literal, below`, `Create`, `Modify`, `Delete`, and `Run` unchanged. Write all other content in the user's language. Remove the template's comments.
2. **Validate**: `python3 scripts/dossier-validator <Preview File> assets/impl-proposal.json`. Fix every error and re-run until it exits with 0. The validator checks structure only: the completion rule's checks remain yours.
3. **Write**: once the user confirms, move the Preview File to the Output File path. Do not record processed question ids from the input dossiers.
4. **On a re-run**, update the dossier in place and keep existing ids stable. New entries take the next free number, and steps are placed at their position in the execution order, so list order, not number, gives the order. Retired ids are never reused. Append new decisions instead of rewriting the log.
5. **Clean up**: delete the Draft File, the Preview File, and the Overturn Report, if any. Never modify the input dossiers.
