# <task_name> — Analysis

Source: <ClickUp link, or "free text"> · Input: `01-brief-and-context.md` through Q<n>

## 1. Change Summary
<In 2–5 sentences: what fulfilling the task introduces, modifies, or removes in the system (behaviors, contracts, data, responsibilities), and the most severe impacts it carries.>

## 2. Impact Map
- `<path, module, service, endpoint, screen, or data>` — <origin | upstream | downstream> — <how it is affected> — I<n>[, I<m>]

## 3. Impacts

### I1 — <title>
- **Lens**: <lens from the impact lenses>
- **Severity**: <Critical | High | Medium | Low> · **Breaking**: <Yes | No>
- **Condition**: <Step 3 choice that triggers it, or "Unconditional">
- **Evidence**: <file paths, references, docs, or history>
- **Consequence**: <what goes wrong, and for whom, if unaddressed>
- **Disposition**: <Mitigate → O<n>[, O<m>] | Accept: <rationale> | Defer → <destination>: <rationale>> (Q<n>)

## 4. Obligations

### O1 — <title>
- **Requirement**: <what must hold, verifiable from outside the component>
- **Applies**: <"Always", or "If <Step 3 choice>">
- **Verification**: <how an outside observer confirms it holds>
- **Source**: I<n>[, I<m>]

## 5. Decision Log

- **Q<n>** — <question title>: <decision>
