# SCF Skill Conventions

Conventions shared by the Systemic Context Framework skills. New skills follow them; existing skills that deviate are updated to match.

## 1. Skill layout

- All skills must follow the [Agent Skills](https://agentskills.io/specification) specification.
- The `description` states the skill's step number and name in the framework, what it takes in and produces, and ends with: "Must only be invoked manually by the user."
- All skill files are written in English and are agent-agnostic. Optional capabilities are phrased conditionally ("If you can dispatch sub-agents, …").

## 2. `SKILL.md` as a lean orchestrator

- `SKILL.md` holds only orchestration; the detailed procedures live in sub-procedure files.
- Its sections appear in this order: **References**, **Input**, **Process**, **Overturning** (optional), **Output**.
- The Process list ends with: "Each step is blocked until the one before it has run to completion."
- The last Process step tells the user the output file's path, that the step is complete, and which step comes next.

## 3. References section

- Lists every bundled file as a relative Markdown link (sub-procedures, `references/…`, `assets/…`).
- Lists every path the skill reads or writes under `.ai/tasks/<task_name>/` by default: input file(s), output file, and other files.

## 4. Sub-procedures

- Live at the skill root, named in uppercase verb-noun form (`GRILL-BRIEF.md`, `RED-TEAM.md`, `GRILL-IMPACT.md`).
- Each contains, as applicable: **Input**, the procedure itself (e.g. **Grilling session**, **Procedure**), a **Completion** [rule], and **Writing the file**.

## 5. Shared references

- All shared references are byte-identical copies across skills. The only examples of this at the time of writing are `grilling.md` and `impact-lenses.md`

## 6. Dossiers and files

- The Dossiers' structure is defined in a JSON file that lives in `assets/`. A template is generated off it with a script to be filled in, and the completed Dossier is then re-validated using a different script.
- All files for a task live in `.ai/tasks/<task_name>/`, named `NN-<name>.md`, where `NN` is the step number (`01-brief-and-context.md`, `02-analysis.md`, etc.).
- Content may be written in the user's language of choice, but section headings and labels must stay untouched.
- A skill never modifies another step's dossier.
- Temporary working files sit next to the dossier as `NN-<name>.<suffix>.md` and are deleted when the step completes.
- The user is shown the complete file as it will be written and asked for confirmation. Nothing is written before the user confirms.

## 7. Decision Log

- Every dossier ends with a Decision Log whose entries read `**Q<n>** — <question title>: <decision>`.
- Each dossier restarts the numbering at Q1; it never continues an input dossier's numbering.
- Every entry in any Decision Log a skill reads is a settled branch and is never re-asked.
- On a re-run, the dossier is updated in place, existing IDs stay stable, and new decisions are appended rather than rewriting the log. Decisions reopened by an Overturn can be superseded, but are never overwritten or deleted.
- A dossier that consumes others records the last question IDs it processed from them (`Processed <input dossier; e.g. 01-brief-and-context> questions through Q<n>`), so a script can detect upstream changes when on a re-run.

## 8. Overturning

- When a skill finds a gap in its upstream dossiers, it does not create or update its own output dossier. It may, though, create and update working files as necessary to preserve information that's not blocked by the reported gap.
- It writes the gap report to a dedicated file: `.ai/tasks/<task_name>/NN-<name>.overturn.md`.
- Each gap in the report states: what is missing or contradicted, the evidence, the target dossier and section, the skill(s) to re-run (in order), and the question that skill needs to settle.
- The skill tells the user to re-run the named skill(s) in order, passing them the report, and to only then invoke it again.
- A run that completes successfully deletes any existing working files for its step.
