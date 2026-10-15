# Implementation Proposal: Draft the Design

Find **every viable way to fulfil the task**, test each one against the targets and the analysis, and list the **real decisions** the user must settle between them.

## Input

Both input dossiers, read as-is. On a re-run, also the existing output dossier and any decisions carried forward from a previous Draft File. Every entry in any of their Decision Logs is a settled branch.

## Stance

You are the designer, not the decider. Facts are yours to find; choices between viable designs are the user's.

- Design only what the targets require. No extra features, no refactors, no test suites, documentation, or PR text (those are Steps 6 and 7), unless an acceptance criterion or obligation demands them.
- Follow the codebase's conventions and prior art recorded in the Context, and any you discover yourself.
- Every claim about the system needs evidence: file paths, symbols, references, or history.

## Procedure

1. **List the targets.** Write down every AC<n> and every O<n>, with each obligation's Applies condition and Verification. Also list every deferred impact and every accepted impact, with the extent `02-analysis.md` records for it.
2. **Ground the design in the system.** Read every Codebase entry of the Context and follow references wherever they lead: callers, consumers, conventions, prior art, and git history if there is any. The Context is a starting point, not a boundary. If you can dispatch sub-agents, explore areas in parallel. Whenever the system contradicts an input dossier, that is an overturn (see `SKILL.md`).
3. **Enumerate candidate designs.** Start from the most plausible design consistent with the conventions. Then add every other reasonable design that differs in a way that matters: contracts, data, files touched, dependencies, or ordering.
4. **Test every candidate.**
   - **Targets**: for each AC and each applicable obligation, can the candidate meet it with recipe steps, or can you certify with evidence that it already holds? A conditional obligation applies when its condition holds under the candidate. When the condition is a fact, settle it by investigating.
   - **Impacts**: sweep every Impact Lens across what the candidate introduces, modifies, or removes. Map each impact you find to `02-analysis.md`: flag the candidate if it worsens or widens a deferred impact, or introduces an unanalyzed impact.
5. **Prune.**
   - A candidate that fails a target is not viable. If no candidate meets or certifies some target, overturn: route an acceptance criterion as a gap in `01-brief-and-context.md`, and an obligation as an unmeetable obligation.
   - Drop every viable candidate that introduces an unanalyzed impact some other viable candidate avoids. If every viable candidate introduces the same unanalyzed impact, overturn.
   - Drop every viable candidate that worsens or widens a deferred impact, if some other viable candidate doesn't. If every viable candidate does, overturn.
6. **List the real decisions.** A decision is real when more than one remaining option is viable and the choice changes something observable, or something a reviewer would care about: an approach, a contract's shape, a name others depend on, a file's placement, a dependency, or an ordering. For each one, record the options, the evidence, the consequence of each on targets and impacts, and your recommendation with its rationale.
   - A choice fully determined by the conventions, prior art, or inputs is not a decision: record it as a fact with its evidence.
   - A choice with no observable consequence and no governing convention (a local variable name, for example) is not grilled: you make it, and it appears in the complete dossier the user confirms.

Resolve every factual uncertainty by investigating. An uncertainty you cannot resolve by investigating is a non-discoverable fact missing from `01-brief-and-context.md`: overturn.

## Completion

Drafting is done when every target has at least one path to being met or certified in some remaining candidate, every impact found has been mapped to `02-analysis.md`, every real decision is listed with a recommendation, and no factual uncertainty remains. Then hand over to `GRILL-DESIGN.md`, unless an overturn was found.

## Writing the file

Write your working notes to the Draft File, and keep it current as you go. It is a free-form working file, not validated, with these parts: Facts (each with evidence), Targets (each with how it can be met or certified), Candidates (with their verdicts and the reasons for pruning), and Decisions (each with options and a recommendation). Write it in the user's language.
