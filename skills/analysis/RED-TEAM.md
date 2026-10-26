# Analysis: Red-Team the Task

Find **every way fulfilling the task can affect system beyond itself**. Back each one with evidence. Prepare each one for User to settle.

## Input

Input, read as-is.

## Stance

You are Red Team. Your job: find everything that breaks. Do not reassure.

- Assume task gets done in most plausible way consistent with brief and codebase conventions. Then also consider other reasonable ways. Impact that appears only under some of them is **conditional impact**.
- Impact needs evidence. Never record absence of impact.

## Procedure

1. **Model the change.** From Task Brief, state in system terms what fulfilling it introduces, modifies, or removes: behaviors, contracts, data, responsibilities. This is origin of impact map.
2. **Trace outward.** Start from Context's Codebase entries. Follow dependencies in both directions:
   - **Downstream**: everything relying on what changes: callers, consumers, subscribers, UI screens, other services, scheduled jobs, reports, integrations, external clients.
   - **Upstream**: everything the change relies on, plus every new demand it places on them: services, libraries, third-party APIs, quotas, infrastructure.
   Context is starting point, not boundary: follow references wherever they lead. Use git history on areas involved. Past fixes there often encode invariants task can violate. If you can dispatch sub-agents, explore lenses or directions in parallel.
3. **Sweep every impact lens** across every element on map.
4. **Attack.** Per affected element, ask what happens when: input is malicious, dependency is down, existing data does not satisfy new assumptions. Ask who relied on old behavior. And so on.
5. **Qualify each candidate** with format below. Resolve every factual uncertainty by investigating. Uncertainty depending on choice Step 3 will make is not gap: record impact as conditional on that choice. Uncertainty you cannot resolve by investigating is gap (see Overturning). Same for uncertainty contradicting Input.

## Severity scale

- **Critical**: data loss or corruption, security or privacy breach, or breaking change to production consumer with no coordination.
- **High**: regression in existing user-facing behavior, or acceptance criterion not met unless mitigated.
- **Medium**: degraded but working behavior: performance, reliability, operability, or experience visibly worse.
- **Low**: minor or cosmetic effect, no functional consequence.

## Completion rule

Procedure done: hand candidates to GRILL-IMPACT.md. Exception: User accepted overturn.

## Writing the file

Write candidates to Candidates File, one per impact. Use Impact fields from Dossier Template, plus "**Recommendation**: your recommended disposition and, for Mitigate, the draft obligation (see Impact Grilling)."
