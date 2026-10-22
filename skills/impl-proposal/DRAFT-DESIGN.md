# Implementation Proposal: Draft the Design

Find **every viable way to fulfill the task**, test each one against the targets and the Input, and list the **real decisions** the User must settle between them.

## Input

The Input, read as-is. Treat all of it as settled branches.

## Stance

You are the designer, not the decider. Choices between viable designs are the User's.

- Design only what the targets require.
- Follow the codebase's conventions and prior art, and any you discover yourself.
- Every claim about the system needs evidence: file paths, symbols, references, or history.

## Procedure

1. **List the targets and constraints.** Write down every target the Input states (acceptance criteria, obligations, etc.), each with any condition under which it applies and any verification it requires. Number them `T<n>`, and note where the Input states each one, with its id there if it has one. Then list every impact the Input accepts or defers as a constraint: the design SHOULD NOT worsen it.
2. **Ground the design in the system.** Follow references wherever they lead: callers, consumers, conventions, prior art, and git history if there is any. The Input is a starting point, not a boundary. If you can dispatch sub-agents, explore areas in parallel. Reconcile conflicting information with the User.
3. **Enumerate candidate designs.** Start from the most plausible design consistent with the conventions. Then add every other reasonable design that differs in a way that matters: contracts, data, files touched, dependencies, etc.
4. **Test every candidate.** Can the candidate meet every target? Does it worsen any constraint, or introduce new problems according to the Impact Lenses? The answers determine the candidate's quality.
5. **Sort.** Highest quality candidates go first, and the worst candidates are dropped outright. If every remaining candidate worsens the same constraint, tell the User, with the evidence.
6. **List the real decisions.** Decisions with more than one viable option, where the choice changes something observable, or something a reviewer would care about: an approach, a contract's shape, a name others depend on, a file's placement, a dependency, etc. For each one, record the options, the evidence, the consequence of each, and your recommendation.

Resolve every factual uncertainty by investigating. An uncertainty you cannot resolve by investigating is a non-discoverable fact missing from the Input: suggest an Overturn.

## Completion rule

Drafting is done when every target has at least one path to being met or certified in some remaining candidate, every real decision is listed with a recommendation, and no factual uncertainty remains. Hand over to `GRILL-DESIGN.md`.

## Writing the file

Write your working notes to the Draft File, and keep it current as you go. Overwrite any file already at that path. It is a free-form working file, not validated, with these parts: Facts (each with evidence), Targets (each `T<n>` with its source and how it can be met or certified), Constraints, Candidates (do delete dropped candidates, though), and Decisions (each with options and a recommendation). Write it in the User's language.
