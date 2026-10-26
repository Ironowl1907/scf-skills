# SCF Skill Conventions

Conventions shared by the Systemic Context Framework skills. New skills MUST follow them; existing skills that deviate MUST be updated to match.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 when, and only when, they appear in all capitals, as shown here.

## Terminology

- **User**: the person invoking a skill.
- **Agent**: the AI model executing a skill. Skills MUST address the Agent as 'you'.
- **Input**: all of the curated information the User provides to the Agent.
- **Dossier**: the primary output file of a step. MUST be capitalized.
- **Gap**: missing or contradictory information in the Input.
- **Overturn**: sending the User back to one or more earlier steps to resolve a gap.
- **Overturn report**: the file listing the gaps behind an Overturn.

## 0. General principles

### Decision making

- The User MAY make any choice, whatever the consequences, and is solely responsible for their AI-assisted work.
- Before the User decides, the Agent MUST make sure the User is fully informed. For a risky choice, the Agent MUST state the risks explicitly.
- The Agent MUST NOT override a User's decision, even one it believes is a mistake.

### Token usage and cognitive load

- The Agent MUST NOT ask the User to confirm what can be derived from established facts (the Input, explicit User instructions, etc.).
  - Good: "Follow these guidelines" -> the Agent follows them.
  - Bad: "Follow these guidelines" -> "Should I conform to guideline 1.2? What about 1.3?"
- All Agent output, files included, MUST follow the Caveman protocol.

### Runs

- Every run is a first run: a skill MUST NOT distinguish a re-run from a first run.
- The User MAY supply any file as input, including a previously generated Dossier or Overturn report. The User MAY instead run a skill without those files and just base their answers on them.
- A skill MAY produce material to help the User with a later run (see Overturning).

> **Rationale**: in testing, iterative re-runs proved ineffective and a major source of hallucination.

### Input

- The Input is curated by the User, and may or may not contain all the necessary information that a skill needs.
- The Input MUST be read as-is and MUST NOT be rejected by the Agent.
- The User's own words take priority over anything and everything else (e.g. for settling gaps or amending information).

## 1. Skill layout

- All skills MUST follow the [Agent Skills](https://agentskills.io/specification) specification.
- The `description` MUST state the skill's step number and name in the framework and what it takes in and produces. It MUST end with the exact sentence "Must only be invoked manually by the User."
- All skill files MUST be written in English and MUST be agent-agnostic. Optional capabilities MUST be phrased conditionally ("If you can dispatch sub-agents, …").

## 2. `SKILL.md` as a lean orchestrator

- `SKILL.md` MUST contain only orchestration; detailed procedures MUST live in sub-procedure files.
- Its sections MUST appear in this order: **References**, **Input**, **Process**, **Overturning** (OPTIONAL), **Output**.
- The last Process step MUST tell the User the output file's path, that the process is complete, and what to do next.
- The Process list MUST be followed with: "Each step is blocked until the one before it has run to completion."

## 3. References section

The References section MUST list:

- every bundled file, in order: sub-procedures, references, scripts, and assets, as relative Markdown links;
- the default path of every file the skill writes under `.ai/tasks/<task_name>/`, in alphabetical order.

## 4. Sub-procedures

- Sub-procedures MUST live at the skill root and MUST be named in uppercase verb-noun or verb-only form (`GRILL-BRIEF.md`, `RED-TEAM.md`).
- Each sub-procedure MUST contain, in this order, as applicable: **Input**, the procedure, (e.g. **Grilling session**, **Procedure**), **Completion rule**, **Writing the file**.

## 5. Shared references

- All shared references MUST be byte-identical copies across skills. Some examples are `grilling.md` and `impact-lenses.md`.
- Each skill MUST only bundle the shared files it uses. This is handled automatically by a script.
- The canonical copy lives in this repository's `shared/` folder.

## 6. Dossiers and files


- Each Dossier's structure MUST be defined in a JSON file in `assets/`. A script in `scripts/` generates the blank template from it.
- The Agent MUST run the validator script before showing the completed Dossier to the User.
- By default, all files for a task MUST live in `.ai/tasks/<task_name>/` and MUST be named `NN-<name>[.<suffix>].md` (e.g. `02-analysis.md`, `03-impl-proposal.overturn.md`, etc.).
- The User MAY change any output file path.

- Content MAY be written in the User's language of choice; section headings and labels MUST be kept untouched.
- Temporary working files MUST sit next to the Dossier as `NN-<name>.<suffix>.md` and MUST be deleted when the step completes. The Overturn report is not a temporary file and MUST NOT be deleted.
- Before writing any file, the Agent SHOULD show the User its complete content as it will be written. In that case, the Agent MUST NOT write it until the User confirms. This is especially true for deliverables.
- A skill MUST NOT modify another step's files.

## 7. Decision Log

- Every Dossier MUST end with a Decision Log. Each entry MUST be formatted as `**Q<n>** — <question title>: <decision>`
- Each Dossier MUST start numbering at Q1.

## 8. Overturning

- When the Agent finds a gap in the Input, it MAY suggest an Overturn to the User.
- The User MAY instead settle the gap on the spot. The skill then continues normally.
- If the User accepts the Overturn, the Agent MUST write an Overturn report to `.ai/tasks/<task_name>/NN-<name>.overturn.md` for the User to act on, and end the run.
- For each gap, the report MUST state: what is missing or contradicted, the evidence, the skill(s) to run in order, and the question each skill needs to settle.
