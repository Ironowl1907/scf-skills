# scf-step3-impl-proposal-skill

Source: free text · Status: Completed

## 1. Task Brief

### Problem Statement
The team's Systemic Context Framework (SCF) has 8 steps. Steps 1 (Preparation, `prep`) and 2 (Analysis & Design, `analysis`) exist as skills, but Step 3 (Implementation Proposal) does not. Without it, nothing turns the confirmed task brief and the settled obligations into a concrete, executable plan. Step 4 (or the developer) is left to make design decisions outside the framework's human validation loop.

### Expected Outcome
The developer manually invokes an `impl-proposal` skill on a task whose `01` and `02` dossiers exist. The skill designs the implementation together with the developer through a grilling session. It then writes `03-impl-proposal.md`: a recipe concrete enough that an agent (Step 4) or a developer implementing by hand can follow it without making any decision. When the inputs are insufficient, it writes an overturn report instead and tells the developer which skill(s) to re-run, and in what order.

### Acceptance Criteria
1. The skill is a directory named `impl-proposal/` whose `SKILL.md` frontmatter contains only fields defined by the Agent Skills specification: `name: impl-proposal`, which matches the directory, and a `description` of at most 1024 characters. `SKILL.md` is under 500 lines, and every file reference in it is one level deep and resolves to an existing file.
2. The directory mirrors the existing skills' layout: a `SKILL.md` orchestrator and its sub-procedure file(s) at the root, `references/grilling.md` identical to the existing grilling protocol, and the dossier template in `assets/`.
3. Every skill file is written in English. None names a model, a vendor, or a vendor-specific tool. Optional capabilities (e.g. sub-agents) are phrased conditionally ("if you can…").
4. The `description` contains the sentence "Must only be invoked manually by the user.", and the frontmatter has no non-standard keys.
5. The skill resolves its input (`<task_name>`, ClickUp ID/URL, or dossier path) to exactly one directory under `.ai/tasks/`. If zero or several directories match, it lists what it found and asks.
6. The skill stops and tells the user to run or finish `prep` when `01-brief-and-context.md` is missing, its status isn't `Completed`, or its Task Brief or Context sections are unfilled. It stops and tells the user to run `analysis` when `02-analysis.md` is missing or any of its template sections is unfilled.
7. When `01`'s Decision Log goes beyond the Q<n> in `02`'s `Processed questions` line, the skill raises an overturn pointing to a re-run of `analysis`.
8. The skill reads both input dossiers in full before designing anything, and treats every Decision Log entry in `01`, `02` (and `03` on a re-run) as settled.
9. The skill runs a grilling session that follows the grilling protocol. Every design decision with real alternatives is put to the user with a recommendation, and the complete proposal is shown and confirmed before anything is written.
10. The output is written to `.ai/tasks/<task_name>/03-impl-proposal.md` from the template. Headings and field labels stay in English, and all other content is in the user's language.
11. Every implementation step states: the exact file path(s); the action on each (create / modify / delete); the exact signatures, contracts, or schemas it introduces or changes, where applicable; its position in the execution order; and how to verify it. The proposal contains no complete code.
12. No decision is left to Step 4: the output contains no open alternatives, placeholders, or hedging terms ("TBD", "choose", "consider", "e.g.", "as appropriate", "if needed", or equivalents in the output language).
13. Traceability runs in both directions:
    - Every step cites the acceptance criteria (from `01`) and obligations (from `02`) it serves.
    - Every acceptance criterion and every obligation is covered by at least one step.
    - A conditional obligation can instead be covered by a recorded, traceable reason why its condition does not arise. That reason is either a design decision enforced by at least one step, or a concrete explanation that cites evidence.
14. Every Accepted or Deferred impact from `02` is listed as acknowledged, with no action. If the design would raise its severity or widen its reach, the skill raises an overturn pointing to a re-run of `analysis` instead.
15. The output records the last question ID of both `01`'s and `02`'s Decision Logs.
16. Overturns are routed as follows:
    - Gaps in the task definition, missing non-discoverable context, or a system that contradicts `01`: re-run `prep`, then `analysis`.
    - A stale `02`, an impact the design introduces or worsens, an obligation that can't be satisfied or that conflicts with another, or a system that contradicts `02`: re-run `analysis` only.
    - The skill never adds impacts or obligations itself.
17. On an overturn, the skill does not create or update `03-impl-proposal.md`. It writes `.ai/tasks/<task_name>/03-impl-proposal.overturn.md`, listing for each gap: what is missing or contradicted, the evidence, the target dossier and section, the skill(s) to re-run, and the question to settle. It then tells the user to re-run the named skill(s) in order, passing them the report.
18. A run that completes successfully deletes any existing `03-impl-proposal.overturn.md`.
19. On a re-run, the skill treats its own Decision Log as settled. It compares the recorded last-question IDs with the current `01` and `02` Decision Logs and re-examines only the steps affected by new entries. It updates the proposal in place, keeps step IDs stable, and appends new decisions to the log.
20. Each step's verification is derived from the Verification field of the obligations it serves. The proposal specifies no test suites.
21. On completion, the skill tells the user the output path and says: "Implementation Proposal is complete. Next step: Agentic Implementation (Step 4, optional); if implementing manually, follow the proposal and continue with Audit (Step 5)."
22. The `assets/` dossier template is reviewed and approved by the user before delivery.
23. The `impl-proposal/` skill directory is delivered as a single zip archive.

### Out of Scope
- Building the Step 4 (Agentic Implementation) skill.
- Fixing the defects found in `prep` and `analysis` (the broken `assets/brif-and-context.md` link, the typos in `RED-TEAM.md`).
- Changing the formats of `01-brief-and-context.md` or `02-analysis.md`.
- Making `prep` or `analysis` read the overturn report automatically.
- Specifying test suites (Step 6).
- A `<skill>-tree.txt` file.

## 2. Context

### Codebase
- No source repository — the `impl-proposal/` directory is delivered as a zip archive and the user places it (Q21).
- `prep/` (all files) — upstream skill (Step 1); produces `01-brief-and-context.md`; layout reference.
- `analysis/` (all files) — closest analogue and primary reference: input resolution and validation wording, the `Processed questions` staleness check, the Overturning section, working-file handling, a template with numbered IDs and two-way cross-references.
- `prep/assets/brief-and-context.md` — input contract for `01`: the `Status:` line, Task Brief subsections (numbered Acceptance Criteria), Context subsections, Decision Log.
- `analysis/assets/analysis.md` — input contract for `02`: the `Processed questions through Q<n>` line; impact fields `I<n>` (Severity, Condition, Disposition); obligation fields `O<n>` (Requirements, Applies, Verification, Source); Decision Log.
- `references/grilling.md` — Grilling Protocol; copied verbatim (the `prep` and `analysis` copies are byte-identical).
- `analysis/references/impact-lenses.md` — defines what counts as an impact; the reference for detecting impacts the design introduces or worsens (AC 14, AC 16).

### Conventions & Prior Art
- `CONVENTIONS.md` (maintained by the user, outside this task's deliverable) — governing conventions: lean `SKILL.md` orchestrator (References, Input, Process, Overturning, Output); uppercase verb-noun sub-procedures at the root; References list every bundled file and every task path; `**Q<n>** — <title>: <decision>` Decision Log restarting at Q1 per dossier; working files `NN-<name>.<suffix>.md` deleted on completion; numbered `##` template sections with fixed English labels; confirmation before writing; the overturn report goes in a dedicated `NN-<name>.overturn.md` file.
- `analysis` overturn handling (gap report written to its working file) — superseded by `CONVENTIONS.md`; `analysis` will be aligned separately, outside this task.

### Related Work
- None. The Step 4 skill does not exist yet and will later be built to consume the `03` format (Q19).

### External References
- Agent Skills specification — https://agentskills.io/specification (source: `agentskills/agentskills`, `docs/specification.mdx`) — frontmatter fields, naming rules, the 500-line guideline, one-level-deep file references; governs AC 1 and AC 4.
- `skills-ref validate` CLI (`agentskills/agentskills`) — verification tool for AC 1.
- SCF diagrams (`SCF_simplified_diagram.png`, `SCF_context_levels_diagram.png`) — framework reference: Step 3 "IA genera plan → Dev revisa", Step 4 optional, Step 5 Audit, HITL at the centre.

### Constraints
- Agnosticism toward specific clients is best-effort; there is no target client list.
- The skill is expected to be forked and adapted per team; team-specific values (paths, file names, fixed phrases) must be easy to locate and change.
- No deadline or approval constraints.

## 3. Decision Log

- **Q1** — Task name: `scf-step3-impl-proposal-skill`.
- **Q2** — Skill name: `impl-proposal`.
- **Q3** — Recipe consumer: primarily an agent executing Step 4; must stay readable enough for a developer to implement by hand when Step 4 is skipped.
- **Q4** — Interaction model: grilling session; design decisions with alternatives go to the user with a recommendation; full proposal confirmed before writing.
- **Q5** — Detail level: exact paths, actions, signatures/contracts/schemas, order and per-step verification; no full code; nothing left for Step 4 to decide.
- **Q6** — Traceability: bidirectional between steps and ACs/obligations; every AC and obligation covered, except conditional obligations whose condition is prevented from arising.
- **Q7** — Output path: `.ai/tasks/<task_name>/03-impl-proposal.md`.
- **Q8** — Input validity: `02` valid if it exists with every section filled in; stale if `01`'s Decision Log goes beyond its `Processed questions` line; `03` records both inputs' last question IDs.
- **Q9** — Overturn routing: task-definition/context gaps → `prep` then `analysis`; analysis-level problems → `analysis` only; Step 3 never adds impacts or obligations; a report is always filed.
- **Q10** — Language: skill files in English; output content in the user's language, headings and labels in English.
- **Q11** — Manual-only invocation: stated in the `description`, as in the existing skills; no non-standard frontmatter.
- **Q12** — Tests: per-step verification derived from obligations; test suites belong to Step 6.
- **Q13** — Scope: the `impl-proposal` skill directory, delivered as files; Step 4, fixes to existing skills, input format changes and a tree file are out of scope.
- **Q14** — Template: drafted in this task's own Step 3 and approved by the user; recorded here only as a criterion.
- **Q15** — Avoided-condition coverage: valid when there is a traceable reason the condition doesn't arise, either an enforced design decision or a concrete evidence-backed explanation.
- **Q16** — Accepted/Deferred impacts: listed as acknowledged; worsening one is an `analysis` overturn.
- **Q17** — Overturn report: `03-impl-proposal.overturn.md` with gap, evidence, target section, skill(s) to re-run and question; `03` untouched while pending; report passed manually to re-runs.
- **Q18** — Re-run: settled log, compare recorded question IDs, re-examine affected steps only, stable IDs, append decisions.
- **Q19** — Dependencies: no blockers; Step 4 will later be built to consume the `03` format (dependency note, not a criterion of this task).
- **Q20** — Finish message: names Step 4 as optional and Step 5 as next for manual implementation.
- **Q21** — Skill location: no source repository; deliver as a zip archive, the user handles placement.
- **Q22** — Codebase references: `analysis/` as primary reference; both templates as input contracts; `grilling.md` copied verbatim; `impact-lenses.md` as the definition of an impact for AC 14 and AC 16.
- **Q23** — Conventions: follow the conventions derived from `prep` and `analysis`, recorded in `CONVENTIONS.md`, with the dedicated overturn-report file (Q17) as the standard.
- **Q24** — Related work: none.
- **Q25** — External references: Agent Skills spec and `skills-ref validate`; SCF diagrams as the framework reference.
- **Q26** — Target agents: none specific; agnosticism is best-effort; teams are expected to fork the skill.
- **Q27** — Deadline and other constraints: none.
- **Q28** — `CONVENTIONS.md` placement: handled by the user; not part of this task's deliverable.
- **Q29** — AC 23 amended: the skill directory is delivered as a single zip archive.
- **Q30** — Forkability: recorded as a constraint; AC 3 remains strict.
