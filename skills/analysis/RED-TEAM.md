# Analysis: Red-Team the Task

Find **every way fulfilling the task can affect the system beyond itself**, back each one with evidence, and prepare it for the user to settle.

## Input

The input dossier and anything else the user supplies, read as-is.

## Stance

You are the Red Team. Your job is to find everything that breaks, not to reassure.

- Assume the task gets done in the most plausible way consistent with the brief and the codebase's conventions. Then also consider the other reasonable ways it could be done: an impact that only appears under some of them is a **conditional impact**.
- An impact needs evidence. The absence of an impact is never recorded.

## Procedure

1. **Model the change.** From the Task Brief, state in system terms what fulfilling it introduces, modifies, or removes: behaviors, contracts, data, and responsibilities. This is the origin of the impact map.
2. **Trace outward.** Starting from the Context's Codebase entries, follow dependencies in both directions:
   - **Downstream**: everything that relies on what changes: callers, consumers, subscribers, UI screens, other services, scheduled jobs, reports, integrations, external clients.
   - **Upstream**: everything the change relies on, and every new demand it places on it: services, libraries, third-party APIs, quotas, infrastructure.
   The Context is a starting point, not a boundary: follow references wherever they lead. Use git history on the areas involved; past fixes there often encode invariants the task can violate. If you can dispatch sub-agents, explore lenses or directions in parallel.
3. **Sweep every impact lens** across every element on the map.
4. **Attack.** For each affected element, ask what happens when input is malicious, when a dependency is down, when existing data doesn't satisfy the new assumptions, who relied on the old behavior, and so on.
5. **Qualify each candidate** using the format below. Resolve every factual uncertainty by investigating. An uncertainty that depends on a choice Step 3 will make is not a gap: record the impact as conditional on that choice. An uncertainty you cannot resolve by investigating, or one that contradicts the Input Dossier is a gap (see Overturning).

## Severity scale

- **Critical**: data loss or corruption, a security or privacy breach, or a breaking change to a production consumer with no coordination.
- **High**: a regression in existing user-facing behavior, or an acceptance criterion that wouldn't be met unless mitigated.
- **Medium**: degraded but working behavior: performance, reliability, operability, or experience visibly worse.
- **Low**: a minor or cosmetic effect with no functional consequence.

## Completion rule

When the procedure is done, hand the candidates to GRILL-IMPACT.md, unless the user accepted an overturn.

## Writing the file

Write candidates to the Candidates File, one per impact. Use the Impact fields from the Dossier Template plus "**Recommendation**: your recommended disposition and, for Mitigate, the draft obligation (see Impact Grilling)."
