# Implementation Proposal: Draft the Design

Find **every viable way to fulfill task**. Test each against targets and Input. List **real decisions** User must settle between them.

## Input

Input, read as-is. All of it: settled branches.

## Stance

You are designer, not decider. Choices between viable designs belong to User.

- Design only what targets require.
- Follow codebase conventions and prior art, including any you discover.
- Every claim about system needs evidence: file paths, symbols, references, or history.

## Procedure

1. **List targets and constraints.** Write every target Input states (acceptance criteria, obligations, etc.). Give each its applying condition and required verification, if any. Number them `T<n>`. Note where Input states each one, plus its id there if it has one. Then list every impact Input accepts or defers as constraint: design SHOULD NOT worsen it.
2. **Ground design in system.** Follow references wherever they lead: callers, consumers, conventions, prior art, git history if any. Input is starting point, not boundary. Can dispatch sub-agents? Explore areas in parallel. Reconcile conflicting information with User.
3. **Enumerate candidate designs.** Start from most plausible design consistent with conventions. Then add every other reasonable design that differs in a way that matters: contracts, data, files touched, dependencies, etc.
4. **Test every candidate.** Can it meet every target? Does it worsen any constraint? Does it introduce new problems per Impact Lenses? Answers set candidate quality.
5. **Sort.** Highest quality first. Drop unviable candidates outright. Every remaining candidate worsens same constraint? Tell User, with evidence.
6. **List real decisions.** Real decision: more than one viable option, and choice changes something observable or something a reviewer cares about. Examples: approach, contract shape, name others depend on, file placement, dependency. For each: record options, evidence, consequence of each option, and your recommendation.

Resolve every factual uncertainty by investigating. Investigation cannot resolve it? It is a non-discoverable fact missing from Input: suggest Overturn.

## Completion rule

Drafting done only when all hold:
- every target has at least one path to met or certified, in some remaining candidate
- every real decision listed, with recommendation
- no factual uncertainty remains

Then hand over to `GRILL-DESIGN.md`.

## Writing the file

Write working notes to Draft File. Keep it current as you go. Overwrite any file already at that path. Free-form working file, not validated. Parts:
- Facts: each with evidence.
- Targets: each `T<n>` with source and how it can be met or certified.
- Constraints.
- Candidates: delete dropped ones.
- Decisions: each with options and recommendation.

Write it in User's language.
