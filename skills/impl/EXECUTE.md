# Implementation: Execute

Apply Input changes **to the letter**, verify implementation works, write output Dossier. Zero design invention.

You are executor, not designer:

- Execute only unambiguous instructions present in Input.
- Preserve unrelated code, comments, and formatting untouched.
- Never invent APIs, signatures, schemas, error handling, or fallbacks not in Input.
- Literal contract block given? Write exact contract content as specified.

## Input

Input, read as-is. All of it: settled branches.

## Procedure

1. **Derive execution plan from Input.**
   - Input has `03-impl-proposal.md` Recipe? Use its `S1…S<n>` steps and `V1…V<n>` checks in exact order.
   - Input is partial Dossier or free text without Recipe? Break explicit instructions into ordered `S1…S<n>` steps (`Create`, `Modify`, `Delete`, `Run`). Use stated checks as `V1…V<n>`; if none stated, define lightweight smoke/I/O checks (`V1…V<n>`) to verify implemented changes work.
   - Task name missing from Input? Propose `<task_name>` in kebab-case and confirm with User before writing `.ai/tasks/<task_name>/` files.
2. **Audit each step before touching workspace.**
   - Verify target file paths and symbols exist (for `Modify`/`Delete`) or path is clear (for `Create`).
   - Verify contract, signature, schema, and behavior have zero open choices.
   - Verify system does not contradict step assumptions.
   - Any check fails? Raise gap per `SKILL.md` Overturning before editing blocked target.
3. **Execute steps top to bottom.**
   - Apply each `S<n>` action (`Create`, `Modify`, `Delete`, `Run`) strictly as written.
   - Record step status (`Done` or `Skipped`) and concrete outcome.
4. **Verify implementation (Checks).**
   - After each step (or when step's prerequisites finish), run its `V<n>` checks.
   - When Input lacks explicit `V<n>` checks or extra verification is needed, run ad-hoc checks (CLI runs, direct input/output checks, or existing commands) to confirm the implemented thing works.
   - Scope boundary: testing here only confirms implemented changes work. Creating or committing test suites, test files, or test harnesses is out of scope (belongs to Step 6 `test`). Leave no temporary test files in workspace.
   - Compare actual output against expected behavior.
   - Check passes? Record `Pass` and observed output in `3. Check Results`.
   - Check fails despite exact adherence to step? Do not guess a fix. Raise gap per `SKILL.md` Overturning.
5. **Handle gaps strictly per Overturning.**
   - User chooses **Overturn**: follow `SKILL.md` Overturn exit flow immediately.
   - User **settles on the spot**:
     - User supplies exact contract, disambiguation, or fix: apply it, re-run affected step/check, log `**Q<n>**` in Decision Log.
     - User chooses to skip blocked step/check or proceed despite failed check: state explicit risk first. Once User confirms, leave blocked target untouched (mark step `Skipped` or check `Fail`/`Skipped`), log `**Q<n>**` with risk and decision in Decision Log, and continue.

## Completion rule

Execution done only when all hold:

1. **Every `S<n>` step is `Done`, or `Skipped` via User decision logged in `4. Decision Log`.**
2. **Every `V<n>` check is `Pass`, or `Fail`/`Skipped` via User decision logged in `4. Decision Log`.**
3. **Every gap settled on the spot has entry in `4. Decision Log` starting at `Q1`.**
4. **No Overturn pending.**

Then write Dossier to Preview File, validate it, show User complete Preview File content, and ask User to confirm. Write nothing to Output File before confirmation.

## Writing the file

Run scripts with skill directory as working directory. Both need Python 3.8+, standard library only. Exit codes: 0 ok, 1 invalid, 2 usage error.

1. **Render template**: `python3 scripts/dossier-renderer assets/impl.json`. Fill it in at Preview File. Overwrite any file at that path. Keep unchanged: section headings, field labels, fixed values `Create`, `Modify`, `Delete`, `Run`, `Done`, `Skipped`, `Pass`, `Fail`, `None`. Write all other content in User's language. Remove template comments.
   - No checks in run? Omit `### V<n>` headings under `## 3. Check Results`.
   - No decisions logged? Write `- None` under `## 4. Decision Log`. Number logged decisions from `Q1`; never carry over question ids from Input.
2. **Validate**: `python3 scripts/dossier-validator <Preview File> assets/impl.json`. Fix every error. Re-run until exit 0.
3. **Write**: show complete Preview File to User. User confirms? Move Preview File to Output File path.
4. **Clean up**: delete Preview File if it remains. Never delete Overturn Report. Never modify any Input file.
