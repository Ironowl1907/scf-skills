---
task_name: impl-skill
description: Develop Step 4 (Agentic Implementation) skill (`skills/impl`) for the SCF framework.
---

## 1. Task Brief

### Problem Statement
SCF framework has Steps 1–3 (`prep`, `analysis`, `impl-proposal`), but lacks Step 4 (`impl`) to execute implementations strictly from User-supplied Input without inventing design decisions or assuming contracts.

### Expected Outcome
Working `skills/impl` skill conforming to `CONVENTIONS.md` that executes code changes strictly per Input (`03-impl-proposal.md`, partial Dossiers, or direct prompt), runs associated checks, handles gaps via the Overturn protocol (Overturn recommended, settle on the spot, or ignore with explicit risk and continue), outputs a validated `.ai/tasks/<task_name>/04-impl.md` Dossier, and is wired into repo scripts and docs.

### Acceptance Criteria
1. `skills/impl/SKILL.md` exists and follows `CONVENTIONS.md` layout: YAML frontmatter (naming Step 4, what it takes in and produces, ending with `"Must only be invoked manually by the User."`), and sections `References`, `Input`, `Process`, `Overturning`, `Output` in order.
2. `skills/impl` accepts `03-impl-proposal.md` Recipe/Checks, partial earlier Dossiers, or free-text prompt as Input without rejecting it.
3. `skills/impl` forbids asking design questions, inventing behaviors, or assuming unstated API contracts; it executes only unambiguous instructions present at prompt-time.
4. When a Recipe with `S<n>` steps and `V<n>` checks is provided, `skills/impl` executes steps in order and runs their `V<n>` checks.
5. On any Gap (missing contract, ambiguous instruction, contradiction with codebase, or failed check despite exact adherence), `skills/impl` presents three options: (1) Overturn (Recommended, writing `.ai/tasks/<task_name>/04-impl.overturn.md`), (2) Settle on the spot, or (3) Ignore gap and continue (stating risk explicitly, skipping blocked step/target or leaving existing code untouched, and recording in Dossier).
6. `skills/impl` defines its Dossier schema in `skills/impl/assets/impl.json`, bundles `dossier-renderer` and `dossier-validator`, validates `.ai/tasks/<task_name>/04-impl.md` before User confirmation, and includes a Decision Log starting at `Q1`.
7. `sync-refs.sh`, `symlinks/`, `package_skills.sh` compatibility, and `README.md` status table are updated to include `impl`.

### Out of Scope
- Modifying existing steps (`prep`, `analysis`, `impl-proposal`) unless required by shared script wiring.
- Steps 5–8 (`audit`, `test`, `docs`, `integration`).
- Conducting design grilling or automated test suite generation beyond checks specified in Input.

## 2. Context

### Codebase
- `CONVENTIONS.md` — Normative specification for all SCF skills (layout, sections, sub-procedures, Dossier validation, Decision Log, Overturn protocol, Caveman voice).
- `skills/impl-proposal/SKILL.md` — Step 3 orchestrator and Overturn pattern reference.
- `skills/impl-proposal/GRILL-DESIGN.md` — Defines the Step 3 Recipe (`S<n>`), Checks (`V<n>`), Certifications (`C<n>`), Targets (`T<n>`), and literal contract block conventions consumed by `impl`.
- `skills/impl-proposal/assets/impl-proposal.json` — JSON schema of Step 3 output Dossier (`03-impl-proposal.md`).
- `skills/analysis/SKILL.md` — Step 2 orchestrator and Overturn report structure reference.
- `skills/prep/SKILL.md` — Step 1 orchestrator reference.
- `shared/dossier-renderer` — Renders blank Dossier markdown from `assets/*.json`.
- `shared/dossier-validator` — Validates filled Dossier markdown against `assets/*.json`.
- `shared/caveman.md` — Shared Caveman protocol reference to bundle into `skills/impl/references/caveman.md`.
- `sync-refs.sh` — Script copying shared scripts and references into each skill; must include `./skills/impl/references/` for `caveman.md`.
- `package_skills.sh` — Runs `sync-refs.sh` and packages `skills/*` into `export/*.zip`.
- `symlinks/` — Contains convenience symlinks and `<skill>-tree.txt` snapshots for each skill.
- `README.md` — Roadmap and skill status table (`impl` currently marked "En desarrollo").

### Conventions & Prior Art
- `CONVENTIONS.md` Sections 0–8 — Lean `SKILL.md` orchestrator, uppercase verb-noun sub-procedures at skill root, relative Markdown links in `References`, alphabetical `.ai/tasks/<task_name>/04-impl*.md` paths, and confirmation before writing deliverables.
- `skills/impl-proposal/` & `skills/analysis/` — Prior art for sub-procedure decomposition, Dossier Validator invocation, preview/draft cleanup, and Overturn reporting.
- `shared/dossier-validator` schema format — JSON `version`, `metadata`, `sections` (`string`, `ordered_list`, `bullet_list`, `entries` with `heading_schema` and `fields`).

### Related Work
- Branch `implementation-skill` — Active git branch for Step 4 skill development.

### External References
- [Agent Skills Specification](https://agentskills.io/specification) — Standard required by `CONVENTIONS.md` Section 1.

### Constraints
- All skill files written in English, agent-agnostic, and adhering to Caveman protocol.
- `skills/impl/references/` bundles only `caveman.md` (no `grilling.md` or `impact-lenses.md`).
- Scripts require Python 3.8+ standard library only.
- Semilinear git history (rebase workflow).

## 3. Decision Log
- **Q1** — Task Name: `impl-skill`.
- **Q2** — Problem and Expected Outcome: Develop Step 4 (`impl`) skill executing Input strictly without design questions or assumed contracts, handling gaps via Overturn protocol.
- **Q3** — Output Dossier Requirement: Produce `.ai/tasks/<task_name>/04-impl.md` validated against `skills/impl/assets/impl.json`, in addition to code changes and optional `04-impl.overturn.md`.
- **Q4** — Handling Partial / Free-Text Input Without Recipe: Execute unambiguous instructions; treat any missing contract, target ambiguity, or open implementation choice as a Gap.
- **Q5** — Ignoring a Gap vs Settling on the Spot: Offer (1) Overturn (Recommended), (2) Settle on the spot, or (3) Ignore gap and continue (explicitly state risk, skip blocked step/target or leave untouched, record in Dossier).
- **Q6** — Checks Execution: Execute Recipe steps in order and run associated checks; treat check failure despite exact adherence as a Gap.
- **Q7** — Scope Boundaries & Dependencies: Include `skills/impl/` plus updates to `sync-refs.sh`, `symlinks/`, and `README.md`; no external blockers.
- **Q8** — Shared References for `impl`: Bundle only `caveman.md` in `skills/impl/references/`.
- **Q9** — Test Directory Relevance: `test/` is irrelevant and out of scope.
- **Q10** — Tacit Constraints & External Specs: Follow `CONVENTIONS.md`, Agent Skills spec, Python 3.8+ stdlib, and semilinear git workflow on `implementation-skill`.
