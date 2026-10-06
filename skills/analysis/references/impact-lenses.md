# Impact Lenses

Apply every lens to every element on the impact map. The questions are prompts, not a checklist to answer in the dossier: record only the impacts they surface.

## 1. Contracts and interfaces
Anything another party calls, reads, or parses: HTTP/GraphQL/RPC endpoints, events and messages, exported functions and types, CLI commands, configuration keys, file formats, webhooks.
- Does the shape, meaning, status code, error format, or default of anything change?
- Is a field added, removed, renamed, made required, or given new semantics?
- Can old clients keep working unchanged? Can new clients talk to old servers?

## 2. Downstream consumers
Everything that relies on what changes, including implicit behavior nobody documented.
- Who calls, subscribes to, renders, reports on, or exports this? Inside the repo, other services, external clients, scheduled jobs?
- Do consumers rely on ordering, timing, error messages, nullability, or side effects that will change?
- Which existing features share the code paths or data being changed?

## 3. Upstream dependencies
Everything the change relies on, and every new demand it places.
- Does the task need behavior, data, or capacity its dependencies don't currently provide?
- Does it increase calls to rate-limited, paid, or slow services?
- Does it rely on a library, service, or API version the system doesn't currently use?

## 4. Data and state
- Does a schema, stored format, or cache change? Does existing data satisfy the new assumptions?
- Is a migration or backfill needed, and can old and new code read the data during the transition?
- Are integrity, uniqueness, idempotency, or consistency guarantees at risk, including under concurrent writes?

## 5. Behavior and regressions
- Which existing behaviors could change as a side effect?
- Which past fixes in this area (per git history) encode invariants the task could violate?
- What happens at the edges: empty, maximum, duplicated, out-of-order, partially failed?

## 6. Security and privacy
- Does the task add or widen an entry point, a permission check, or a trust boundary?
- Is input validated where it enters? Can a user reach data or actions beyond their role?
- Does it handle secrets, credentials, tokens, or personal data? Where could they leak (logs, errors, responses, analytics)?
- Does it add abuse vectors: enumeration, injection, replay, resource exhaustion?

## 7. Performance and capacity
- Does the task add work to a hot path, add queries per request, or grow payload sizes?
- How does it behave as data volume or traffic grows?
- Does it introduce new latency, memory, storage, or cost budgets that must hold?

## 8. Reliability and failure modes
- What happens when each dependency is slow, down, or wrong?
- Can partial failure leave the system inconsistent? Is retrying safe?
- Can the change be rolled back without leaving data or consumers broken?

## 9. Responsibilities and boundaries
- Does a part of the system take on a new responsibility (validation, orchestration, state, presentation)?
- Is a new component, service, endpoint, or screen needed for the outcome to exist?
- Does the task cross an ownership boundary (another team, module, or service)?

## 10. User experience
- Which flows, screens, and states (loading, empty, error) change?
- Do existing users see different behavior without having asked for it?
- Are accessibility, localization, or copy affected?

## 11. Rollout and operations
- Must changes across services, apps, or databases be deployed in a specific order?
- Are configuration, environment variables, feature flags, permissions, or infrastructure changes needed?
- Will logs, metrics, alerts, or dashboards still describe the system correctly after the change?

## 12. Compliance and policy
- Does the task touch regulated data, audit trails, retention rules, licensing, or contractual obligations with clients?
