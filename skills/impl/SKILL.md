---
name: impl
description: Step 4 (Agentic Implementation) of team's 8-step AI collaboration framework. Takes curated Input, executes code changes and checks strictly as specified with no invented decisions or contracts, and produces implementation Dossier. Must only be invoked manually by the User.
---

# Implementation

Execute Input **to the letter**. Apply only unambiguous code changes and commands present at prompt-time. Run checks. Record results. Never ask design questions. Never invent behavior. Never assume unstated contracts.

## References

- [Execution Procedure](EXECUTE.md)
- [Caveman Protocol](references/caveman.md)
- [Dossier Renderer](scripts/dossier-renderer)
- [Dossier Validator](scripts/dossier-validator)
- [Dossier Structure](assets/impl.json)
- Output File: `.ai/tasks/<task_name>/04-impl.md`
- Overturn Report: `.ai/tasks/<task_name>/04-impl.overturn.md`
- Preview File: `.ai/tasks/<task_name>/04-impl.preview.md`

## Input

Curated info User provides: `03-impl-proposal.md` (Recipe `S<n>`, Checks `V<n>`), partial earlier Dossiers, Overturn Reports, or free-text prompt.

- Read Input as-is, whatever its state. Never reject it.
- User's own words beat everything else.
- Every Decision Log entry in Input is settled branch: never re-ask it.
- Execute only unambiguous instructions present at prompt-time. No design grilling, no invented fallbacks, no assumed contracts. Missing, ambiguous, or contradictory info is a gap (see Overturning).

## Process

Follow Caveman Protocol in every User interaction and every file written.

1. **Read Input** per Input section.
2. **Read and run `EXECUTE.md`.** Runs steps in order, runs checks, handles gaps per Overturning, validates Dossier with Dossier Validator, writes Output File after User confirms.
3. **Finish**: give User Output File path. Say Implementation complete. Next step: Audit.

Do not declare Implementation complete while Overturn is pending.
Each step blocked until previous step completes.

## Overturning

Skill never edits Input. Never invents design decisions. Stop affected work and raise gap when any holds:

1. **Missing contract or open choice**: signature, schema, config key, target file/symbol, or behavior missing or left open ("TBD", "as appropriate", etc.).
2. **Ambiguous instruction**: two readings yield different code, data, or side effects.
3. **System contradicts Input**: codebase, types, or existing contracts conflict with Input instructions or literal blocks.
4. **Check fails despite exact adherence**: step applied to the letter, but `V<n>` check fails.

Gap found:

1. Stop before guessing on blocked step. Independent steps with zero dependency on gap may finish first if safe; otherwise stop immediately.
2. Show gap with evidence. Offer User three options:
   - **(Recommended) Overturn**: stop run, write Overturn Report to `.ai/tasks/<task_name>/04-impl.overturn.md`.
   - **Settle on the spot**: User gives exact contract, disambiguation, or fix now. Log in Decision Log (`Q<n>`). Continue.
   - **Ignore gap and continue**: state explicit risk first. User chooses this? Skip blocked step/target or leave existing code untouched. Record in `4. Ignored Gaps` and `5. Decision Log` (`Q<n>`). Continue remaining steps.
3. User accepts Overturn:
   - Do not create or update Output File.
   - Workspace files modified in this run? Ask User whether to keep or revert edits.
   - Show complete Overturn Report content. Write only after User confirms. Per gap, state: what is missing, contradicted, or failing; evidence; target Dossier and section; skill(s) to re-run in order; question each skill must settle.
   - Delete Preview File, if present.
   - Give User Overturn Report path. Tell User to re-run listed skill(s), then invoke `impl` again. End run.

## Output

Output Dossier at Output File path, plus workspace changes. Structure: Dossier Structure. Written once at end of `EXECUTE.md`, after passing Dossier Validator and User confirmation. Format: caveman style, within schema constraints.
