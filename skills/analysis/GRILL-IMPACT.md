# Analysis: Grill the Impacts

Settle with the user **which candidate impacts are real, and what must be done about each one**, then write the output dossier.

## Input

The candidate impacts from the candidates file, and the Decision Logs of the input dossier and, on a re-run, of the existing output dossier. Treat every entry in either log as a settled branch.

## Dispositions

Every real impact gets exactly one disposition:

- **Mitigate**: the task must address it. Produces one or more obligations.
- **Accept**: the impact is real and knowingly left as is. Requires a rationale. A Critical or High impact may only be accepted with the user's explicit rationale, never on your recommendation alone.
- **Defer**: the impact is real and will be handled outside this task. Requires a destination (an existing ticket, or a decision that a new follow-up ticket will be created). If deferring it would leave an acceptance criterion unmet, it is an overturn instead (see Overturning).

An impact the user judges as not real, or not relevant to this task, is **dismissed**: it leaves no trace in the dossier except its Decision Log entry.

## Obligations

An obligation is a statement of **what must hold** once the task is done, derived from one or more impacts. Every obligation must pass all four checks:

1. **External**: it can be verified from outside the component.
2. **What, not how**: it names no internal structure, algorithm, or library choice.
3. **Traceable**: it cites the impact or impacts it comes from.
4. **Decidable**: an observer can tell unambiguously whether it holds.

A conditional impact produces a conditional obligation: "<under X condition>, <what must hold>." In the dossier, the condition goes in the obligation's **Applies** field and what must hold goes in its **Requirements**.

## Grilling session

Run **one** grilling session (it may span several rounds), following the Grilling Protocol. Seed the tree with one branch per candidate impact, in order by most severe, then breaking changes first within each severity.

For each candidate, ask a single question that presents the evidence and consequence and recommends a validity verdict, a disposition, and, for Mitigate, the draft obligation wording. The user accepts or amends it. Split a candidate into separate follow-up questions only if the user contests part of it.

Keep the tree tight:

- When one decision settles several candidates (e.g. "the endpoint stays backward compatible" resolves every consumer impact on it), ask it once, as the parent of those branches.
- If the user raises a new impact, red-team it first (evidence, severity, condition) and then add it as a branch.
- If an answer can only be given by changing the Task Brief, or rests on a fact that belongs in the Context, stop and follow the overturn procedure.
- If a question drifts toward *how* to implement the task, note that it belongs to Step 3 and move on.

## Completion rule

The session is done only when every candidate has been confirmed or dismissed, every confirmed impact has a disposition, every Mitigate has at least one obligation that passes all four checks, and no overturn is pending.

Before writing, check that nothing in the draft is unresolved: no "unknown", "unclear", "to be confirmed", "might affect", or open questions. A conditional statement that depends on a future choice is resolved; one whose condition is an unchecked fact is not. Keep grilling until it is.

Finally, show the user the complete dossier as it will be written and ask them to confirm it. Do not write anything until they confirm.

## Writing the file

Once the user confirms, write the output dossier from the Dossier Template:

- Fill in every section. Record only what the task affects.
- Number the final impacts `I1…I<n>` in severity order, and obligations `O1…On`. Cross-reference them in both directions.
- Do not continue the Decision Log numbering from the input dossier.
- Record the input dossier’s last Decision Log ID in the `Processed 01-brief-and-context questions` line
- On a re-run, update the dossier in place, keep existing IDs stable, and append new decisions instead of rewriting the log.
- Keep the template's section headings and field labels unchanged so later steps can locate them. Write all other content in the user's language. File paths are encouraged.
- Never modify the input dossier.
- Do delete the candidates file and overturn report, if any.
