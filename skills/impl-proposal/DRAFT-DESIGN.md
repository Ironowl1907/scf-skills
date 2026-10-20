# Implementation Proposal: Draft the Design

Find **every viable way to fulfill the task**, test each one against the targets and the analysis, and list the **real decisions** the user must settle between them.

## Input

Any input dossiers, read as-is. Treat all of that data as settled branches.

## Stance

You are the designer, not the decider. Choices between viable designs are the user's.

- Design only what the targets require, unless an acceptance criterion or obligation demands them.
- Follow the codebase's conventions and prior art, and any you discover yourself.
- Every claim about the system needs evidence: file paths, symbols, references, or history.

## Procedure

1. **List the targets.** Write down every AC<n> and every O<n>, with each obligation's Applies condition and Verification. Ignore accepted or deferred impacts.
2. **Ground the design in the system.** Follow references wherever they lead: callers, consumers, conventions, prior art, and git history if there is any. The context is a starting point, not a boundary. If you can dispatch sub-agents, explore areas in parallel. Concile conflicting information with the user.
3. **Enumerate candidate designs.** Start from the most plausible design consistent with the conventions. Then add every other reasonable design that differs in a way that matters: contracts, data, files touched, dependencies, etc.
4. **Test every candidate.** Can the candidate meet all the specified requirements? Does it introduce new problems, according to the Impact Lenses? The answer to those questions determines the candidate's quality.
5. **Sort.** Highest quality candidates go first, and the worst candidates are dropped outright.
6. **List the real decisions.** Decisions with more than one viable option, where the choice changes something observable, or something a reviewer would care about: an approach, a contract's shape, a name others depend on, a file's placement, a dependency, etc. For each one, record the options, the evidence, the consequence of each, and your recommendation.

Resolve every factual uncertainty by investigating. An uncertainty you cannot resolve by investigating is a non-discoverable fact missing from `01-brief-and-context.md`: suggest an overturn.

## Completion

Drafting is done when every target has at least one path to being met or is certified in some remaining candidate, every real decision is listed with a recommendation, and no factual uncertainty remains. Hand over to `GRILL-DESIGN.md`.

## Writing the file

Write your working notes to the Draft File, and keep it current as you go. It is a free-form working file, not validated, with these parts: Facts (each with evidence), Targets (each with how it can be met or certified), Candidates (do delete dropped candidates, though), and Decisions (each with options and a recommendation). Write it in the user's language.
