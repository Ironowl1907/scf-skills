## Grilling protocol

Interview the User relentlessly. Map the conversation as an **uncertainty tree**: every decision branches into the decisions that depend on it.

Work in **rounds**. The **frontier** is every decision whose prerequisites are already settled. Ask the whole frontier in one round: number each question, and give your recommended answer to each. Then wait for the User's answers.

```
**Q<n>** - **<question title>**: <question body; may include multiple choices and/or paragraphs>

Recommendation: <your recommended answer>

---

**Q<n+1>** - **<question title>**: ...
```

Each set of answers reshapes the tree. Recompute the frontier and ask the next round. A question that depends on another question still open in the current round belongs to a *later* round.

**Facts are your job; decisions are the User's.** Never ask the User something you could look up yourself. If you can dispatch sub-agents, send them to explore in parallel. Otherwise, ask the questions that don't depend on exploration first, and explore while the User answers.

The session is done only when **every branch of the tree has been resolved, and no open questions remain**.
