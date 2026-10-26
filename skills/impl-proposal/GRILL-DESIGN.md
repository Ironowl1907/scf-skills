# Implementation Proposal: Grill the Design

Goal: settle **every real design decision** with User. Turn settled design into recipe. Write output Dossier.

## Input

Draft File plus Input. All of it settled branches.

## Grilling session

Run **one** grilling session per Grilling Protocol. Several rounds allowed. Seed tree with one branch per Draft File decision. Decisions others depend on (overall approach) first. Refinements (names, shapes, placement) after.

Per decision: one question. Show options, evidence, consequence of each option, your recommendation. User accepts or amends.

Keep tree tight:

- User proposes new option? Test it per `DRAFT-DESIGN.md` first. Then add as branch.
- Chosen option worsens or widens accepted or deferred impact? Say so, with evidence.
- Answer needs Input change, or rests on fact that belongs in Input? Clarify with User. May suggest Overturn.
- Question drifts toward test suites, documentation, or PR text? Drop it. Move on.

Update Draft File after every round.

## Building the recipe

Every decision settled: build proposal from Dossier Structure.

**Design Summary**: 2–5 sentences. Chosen design, and why it meets every target without worsening any accepted or deferred impact.

**Targets**: one `T<n>` entry per Draft File target.

- **Source**: where Input states target. Include its id there, if any.
- **Statement**: target, plus any condition under which it applies and any verification it requires.

**Recipe**: one `S<n>` entry per step, in execution order. Step 4 runs them top to bottom.

- **Action**: exactly one of `Create`, `Modify`, `Delete`, `Run`.
- **Touches**: exact file paths and symbols. `Create`: new path plus symbols it defines. `Run`: files, data, or systems the command changes. `None` for steps that change nothing (e.g. `cat`).
- **Behavior**: what holds once step done, including edge cases Input and Draft File raised. `Run`: exact command, directory it runs from, expected outcome.
- **Contract**: `Literal, below` when step creates or changes a contract: signatures, schemas, configuration keys, migrations, messages, endpoints, etc. Otherwise `None`.

**Literal blocks**: after step's last field, leave blank line. Write each literal as fenced code block, indented exactly two spaces on every line, fences included. Step has more than one literal? Precede each with indented one-line label naming its file and symbol. Give final content of each contract as it must read after step: whole signature, schema, or block. Never a diff. Indentation mandatory: Dossier Validator does not recognize code fences. Unindented literal line starting with `## ` or `### ` parses as heading. Every step after it then silently escapes validation.

**Checks**: one `V<n>` entry per check.

- **Method**: exact command or action, observable from outside component. Never "read the code" or similar.
- **Expected**: pass condition an observer can decide unambiguously.
- **Verifies**: target ids it verifies, or `None`.

**Certifications**: one `C<n>` entry per target that already holds with no change: claim, plus evidence that proves it.

**Traceability**: one line per target. Target stays unmet only if User declined Overturn for it. Its line then reads `T<n> — Met by: None — Checks: None`.

**Decision Log**: one entry per question settled in grilling session, or gap User settled on the spot. Number from Q1. Never carry over question ids from Input.

## Completion rule

Keep working until all hold:

1. **Every step names exact files and symbols it touches.**
2. **Every step gives literal content for every contract it creates or changes.**
3. **Every step has at least one check.** Every check's Method observable from outside component.
4. **No step leaves a choice open.** Prohibited wording: "e.g.", "as appropriate", "optionally", "consider", "TBD".
5. **Recipe followable by both agent and human developer.**
6. **Every target traces.** Every target traced to from at least one step's Check, unless User declined Overturn for it.

Then write proposal to Preview File. Validate it (see below). Show User complete Dossier exactly as it will be written. Ask User to confirm. Write nothing to Output File before confirmation.

## Writing the file

Run scripts with skill directory as working directory. Both need Python 3.8+, standard library only. Exit codes: 0 ok, 1 invalid, 2 usage error.

1. **Render template**: `python3 scripts/dossier-renderer assets/impl-proposal.json`. Fill it in at Preview File. Overwrite any file already at that path. Keep unchanged: section headings, field labels, fixed values `None`, `Literal, below`, `Create`, `Modify`, `Delete`, `Run`. Write all other content in User's language. Remove template comments.
2. **Validate**: `python3 scripts/dossier-validator <Preview File> assets/impl-proposal.json`. Fix every error. Re-run until exit 0. Validator checks structure only. Completion rule checks stay yours.
3. **Write**: User confirms? Move Preview File to Output File path.
4. **Clean up**: delete Draft File, plus Preview File if it remains. Never delete Overturn Report or Session Save File. Never modify any Input file.
