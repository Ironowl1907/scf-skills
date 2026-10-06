# Analysis: Red-Team the Task

Find **every way fulfilling the task can affect the system beyond itself**, back each one with evidence, and prepare it for the developer to settle. Nothing is written to disk in this step.

## Input

The validated input dossier. On a re-run, also the existing output dossier: its settled impacts stay settled unless the input changed in a way that touches them.

## Stance

You are the Red Team. Your job is to find what breaks, not to reassure.

- Assume the task gets done in the most plausible way consistent with the brief and the codebase's conventions. Then also consider the other reasonable ways it could be done: an impact that only appears under some of them is a **conditional impact**.
- An impact needs evidence. The absence of an impact needs nothing: it is never recorded.
- Facts are your job. Do not ask the developer for anything you can find in the repository, its docs, its git history, or the related work listed in the Context.

## Procedure

1. **Model the change.** From the Task Brief, state in system terms what fulfilling it introduces, modifies, or removes: behaviors, contracts, data, and responsibilities. This is the origin of the impact map.
2. **Trace outward.** Starting from the Context's Codebase entries, follow dependencies in both directions:
   - **Downstream**: everything that relies on what changes: callers, consumers, subscribers, UI screens, other services, scheduled jobs, reports, integrations, external clients.
   - **Upstream**: everything the change relies on, and every new demand it places on it: services, libraries, third-party APIs, quotas, infrastructure.
   The Context is a starting point, not a boundary: follow references wherever they lead. Use git history on the areas involved; past fixes there often encode invariants the task can violate. If you can dispatch sub-agents, explore lenses or directions in parallel.
3. **Sweep every lens** in [Impact Lenses](references/impact-lenses.md) across every element on the map. A lens that yields nothing produces nothing.
4. **Attack.** For each affected element, ask what happens when input is malicious, empty, huge, duplicated, or out of order; when a dependency is slow, down, or returns something unexpected; when old and new versions run side by side during rollout; when existing data doesn't satisfy the new assumptions; and who relied on the old behavior even though nobody promised it.
5. **Qualify each candidate** using the format below. Resolve every factual uncertainty by investigating. An uncertainty that depends on a choice Step 3 will make is not a gap: record the impact as conditional on that choice. An uncertainty you cannot resolve by investigating is an overturn (see `SKILL.md`).
6. **Check against the input dossier.** Before handing off, check every candidate against the overturn triggers in `SKILL.md`: does it contradict the Context or a settled decision, or could it only be addressed by changing the Task Brief?

## Candidate impact format

Hold candidates in the conversation, one per impact:

- **ID**: `C<n>`
- **Title**: a short name for the impact.
- **Lens**: the lens that surfaced it.
- **Elements**: the affected paths, modules, services, endpoints, screens, or data, and their direction (origin, upstream, or downstream).
- **Evidence**: file paths, references, docs, or history that show the impact is real.
- **Consequence**: what goes wrong, and for whom, if it is left unaddressed.
- **Severity**: per the scale below.
- **Breaking**: `Yes` if it breaks an existing contract or behavior someone relies on; otherwise `No`.
- **Condition**: the Step 3 choice that triggers it, or `Unconditional`.
- **Recommendation**: your recommended disposition and, for Mitigate, the draft obligation (see `GRILL-IMPACT.md`).

## Severity scale

- **Critical**: data loss or corruption, a security or privacy breach, or a breaking change to a production consumer with no coordination.
- **High**: a regression in existing user-facing behavior, or an acceptance criterion that can't be met as things stand.
- **Medium**: degraded but working behavior: performance, reliability, operability, or experience visibly worse.
- **Low**: a minor or cosmetic effect with no functional consequence.

## Completion

This step is done when every lens has been applied to every element on the impact map, every candidate has evidence, and every candidate has been checked against the overturn triggers. If any overturn was found, follow the overturn procedure in `SKILL.md` instead of continuing. Otherwise, hand the candidates to `GRILL-IMPACT.md`.
