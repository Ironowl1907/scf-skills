# Analysis: Grill the Impacts

Settle with User **which candidate impacts are real, and what must be done about each one**. Then write Output File.

## Input

Candidate impacts from Candidates File, plus Decision Log of Input File. Treat every entry in it as settled branch.

## Dispositions

Every real impact gets exactly one disposition:

- **Mitigate**: task must address it. Produces one or more obligations.
- **Accept**: impact is real, knowingly left as is. Requires rationale. Critical or High impact: accept only with User's explicit rationale, never on your recommendation alone.
- **Defer**: impact is real, handled outside this task. Requires destination: existing ticket, or decision to create new follow-up ticket. Deferring leaves acceptance criterion unmet? That is gap (see Overturning).

Impact User judges not real, or not relevant to this task, is **dismissed**. It leaves no trace in Dossier except its Decision Log entry.

## Obligations

Obligation states **what must hold** once task is done. It derives from one or more impacts. Every obligation must pass all four checks:

1. **External**: verifiable from outside the component.
2. **What, not how**: names no internal structure, algorithm, or library choice.
3. **Traceable**: cites the impact or impacts it comes from.
4. **Decidable**: observer can tell unambiguously whether it holds.

Conditional impact produces conditional obligation: "<under X condition>, <what must hold>." In Dossier, condition goes in obligation's **Applies** field. What must hold goes in its **Requirements**.

## Grilling session

Run **one** grilling session, per Grilling Protocol. It may span several rounds. Seed tree with one branch per candidate impact. Order: most severe first; within each severity, breaking changes first.

Per candidate, ask single question. Present evidence and consequence. Recommend validity verdict and disposition. For Mitigate, also recommend draft obligation wording. User accepts or amends. Split candidate into separate follow-up questions only if User contests part of it.

Keep tree tight:

- One decision settles several candidates? Ask it once, as parent of those branches. Example: "the endpoint stays backward compatible" resolves every consumer impact on it.
- User raises new impact? Red-team it first (evidence, severity, condition). Then add it as branch.
- Answer possible only by changing Task Brief, or rests on fact belonging in Context? Follow overturn procedure.
- Question drifts toward *how* to implement task? Note it belongs to Step 3. Move on.

## Completion rule

Session done only when all hold:

- every candidate confirmed or dismissed;
- every confirmed impact has disposition;
- every Mitigate has at least one obligation passing all four checks;
- no overturn pending.

Before writing, check nothing in Draft File is unresolved. Forbidden: "unknown", "unclear", "to be confirmed", "might affect", open questions. Conditional statement depending on future choice is resolved. One whose condition is unchecked fact is not. Keep grilling until it is.

## Writing the file

Fill in Draft File, generated from Dossier Template:

- Fill in every section. Record only what task affects.
- Number final impacts `I1…I<n>` in severity order, obligations `O1…On`. Cross-reference them in both directions.
- Start Decision Log at Q1. Do not continue Decision Log numbering from Input File.
- Keep template section headings and field labels unchanged, so later steps can locate them. Write all other content in User's language. File paths encouraged.
- Never modify Input File.

Run Validation Script on Draft File. Warnings or errors raised? Do not proceed. Iterate on Dossier structure until all validation requirements pass. Then show User complete Dossier as it will be written. Ask User to confirm it. Do not write anything until User confirms.

User confirms: write to Output File path. Then delete Draft File and Candidates File.
