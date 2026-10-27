# Implementation: Execute

Apply Input changes **to the letter**, run checks, write output Dossier. Zero design invention.

## Input

Input, read as-is. All of it: settled branches.

## Stance

You are executor, not designer.

- Execute only unambiguous instructions present in Input.
- Preserve unrelated code, comments, and formatting untouched.
- Never invent APIs, signatures, schemas, error handling, or fallbacks not in Input.
- Literal contract block given? Write exact contract content as specified.

## Procedure

1. **Derive execution plan from Input.**
   - Input has `03-impl-proposal.md` Recipe? Use its `S1…S<n>` steps and `V1…V<n>` checks in exact order.
   - Input is partial Dossier or free text without Recipe? Break explicit instructions into ordered `S1…S<n>` steps (`Create`, `Modify`, `Delete`, `Run`) and any stated checks into `V1…V<n>`.
   - Task name missing from Input? Propose `<task_name>` in kebab-case and confirm with User before writing `.ai/tasks/<task_name>/` files.
2. **Audit each step before touching workspace.**
   - Verify target file paths and symbols exist (for `Modify`/`Delete`) or path is clear (for `Create`).
   - Verify contract, signature, schema, and behavior have zero open choices.
   - Verify system does not contradict step assumptions.
   - Any check fails? Raise gap per `SKILL.md` Overturning before editing blocked target.
3. **Execute steps top to bottom.**
   - Apply each `S<n>` action (`Create`, `Modify`, `Delete`, `Run`) strictly as written.
   - Before writing deliverable or new file, show complete content to User and wait for confirmation when required by conventions.
   - Record step status (`Done` or `Skipped`) and concrete outcome.
4. **Run checks.**
   - After each step (or when step's prerequisites finish), run its linked `V<n>` checks using exact `Method`.
   - Compare actual output against `Expected`.
   - Check passes? Record `Pass` and observed output.
   - Check fails despite exact adherence to step? Do not guess a fix. Raise gap per `SKILL.md` Overturning (Overturn recommended, settle on the spot, or ignore with explicit risk).
5. **Handle gaps strictly per Overturning.**
   - User chooses **Overturn**: follow `SKILL.md` Overturn exit flow immediately.
   - User chooses **Settle on the spot**: apply User's exact instruction, re-run affected step/check, log `**Q<n>**` in Decision Log.
   - User chooses **Ignore gap and continue**: state explicit risk before User confirms. Leave blocked target untouched (or skip blocked step/check), record `G<n>` in `4. Ignored Gaps` and `**Q<n>**` in Decision Log, continue.

## Completion rule

Execution done only when all hold:

1. **Every `S<n>` step is `Done`, or `Skipped` via confirmed Option 3 (Ignore gap).**
2. **Every `V<n>` check is `Pass`, or accounted for in `4. Ignored Gaps` (`Fail`/`Skipped` via Option 3).**
3. **Every settled or ignored gap has entry in `5. Decision Log` starting at `Q1`.**
4. **No Overturn pending.**

Then write Dossier to Preview File, validate it, show User complete Preview File content, and ask User to confirm. Write nothing to Output File before confirmation.

## Writing the file

Run scripts with skill directory as working directory. Both need Python 3.8+, standard library only. Exit codes: 0 ok, 1 invalid, 2 usage error.

1. **Render template**: `python3 scripts/dossier-renderer assets/impl.json`. Fill it in at Preview File. Overwrite any file at that path. Keep unchanged: section headings, field labels, fixed values `Create`, `Modify`, `Delete`, `Run`, `Done`, `Skipped`, `Pass`, `Fail`, `None`. Write all other content in User's language. Remove template comments.
   - No checks in run? Omit `### V<n>` headings under `## 3. Check Results`.
   - No ignored gaps? Omit `### G<n>` headings under `## 4. Ignored Gaps`.
   - No decisions logged? Write `- None` under `## 5. Decision Log`. Number logged decisions from `Q1`; never carry over question ids from Input.
2. **Validate**: `python3 scripts/dossier-validator <Preview File> assets/impl.json`. Fix every error. Re-run until exit 0.
3. **Write**: show complete Preview File to User. User confirms? Move Preview File to Output File path.
4. **Clean up**: delete Preview File if it remains. Never delete Overturn Report. Never modify any Input file.
