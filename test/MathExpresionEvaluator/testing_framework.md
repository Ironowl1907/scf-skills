# Prep

## Prompt

```
/prep

For the following basic math expression evaluator project, I want to add single letter variables.
```

---

## 1st Grilling Round

### Questions

  Proposed task name: single-letter-variables

  Q1 - Task name: Is single-letter-variables the preferred task name for this work?

  • A) Yes, use single-letter-variables.
  • B) Custom name (provide alternative slug).

  Recommendation: A
  ──────
  Q2 - Assignment syntax and lifecycle: How should variable values be defined and persist in the evaluator?

  • A) REPL assignment statements using = (e.g., x = 5), persisting in memory for the duration of the REPL session across subsequent expressions.
  • B) Prompts asking for variable values when an expression containing variables is evaluated.
  • C) Command-line arguments passed at program startup.

  Recommendation: A
  ──────
  Q3 - Supported characters and case sensitivity: Which characters are valid single-letter variables, and how should case be handled?

  • A) Both uppercase and lowercase ASCII letters (a-z, A-Z), case-sensitive (a and A are distinct variables).
  • B) Both uppercase and lowercase ASCII letters (a-z, A-Z), case-insensitive (a and A refer to the same variable).
  • C) Lowercase ASCII letters only (a-z).

  Recommendation: A
  ──────
  Q4 - Collision with REPL quit command: Currently, typing q or Q quits the application. If q and Q are valid variables, how should the quit command be
  differentiated?

  • A) Reserve exit and quit (or :q) for quitting, allowing q and Q to be used as variables.
  • B) Keep q and Q as exit commands, making q and Q invalid variable names.
  • C) Only quit when quit or Quit is entered, freeing q and Q as valid single-letter variables.

  Recommendation: C
  ──────
  Q5 - Undefined variable handling: What should happen when an expression references a variable that has not been assigned a value?

  • A) Print an error message (e.g. [Evaluation ERROR] Undefined variable 'x') and abort evaluation of that expression without crashing.
  • B) Default unassigned variables to 0.
  • C) Prompt the user in real time to provide a value.

  Recommendation: A
  ──────
  Q6 - Assignment expression return value: When a variable assignment is executed (e.g., x = 5 or x = 2 + 3), what should the REPL output?

  • A) Print the assigned value (e.g., 5), matching standard REPL behavior.
  • B) Print an acknowledgment message (e.g., x = 5).
  • C) Silent success (print nothing, prompt for next input).

  Recommendation: A

### Answers

  Q1: Use `single-character-variables`.
  Q2: Follow recommendation, use `x = 5` as value definition.
  Q3: Case sensitive, use recommendation
  Q4: Only quit when `quit` is typed.
  Q5: Follow recommendation
  Q6: Follow recommendation


## 2nd Grilling Round

### Questions

  **Q7** - **Assignment statement scope and nesting**: Can assignments only occur as standalone top-level statements, or can they be embedded inside expressions?
  - A) Top-level statements only (format `<variable> = <expression>`, such as `x = 5` or `x = 2 + 3 * y`). Embedded assignment like `1 + (x = 2)` or chained
  assignment like `a = b = 3` is not allowed.
  - B) Assignment is an expression that yields a value and can be embedded anywhere a factor or expression is valid (e.g., `a = b = 3`, `10 + (x = 2)`).

  Recommendation: A

  ---

  **Q8** - **Variable reassignment**: Is reassigning a variable that already has a value allowed during the session?
  - A) Yes, variables can be reassigned any number of times (e.g., `x = 1`, then `x = 2`).
  - B) No, variables are immutable once defined.

  Recommendation: A

  ---

  **Q9** - **Variable expression support**: Can variables be used anywhere numbers are allowed in expressions (e.g., in binary operations `x + 2`,
  inside parentheses `(x * y)`, and with unary negation `-x`)?
  - A) Yes, variables evaluate as double values anywhere a numeric operand or factor is valid.
  - B) No, restrict variable usage (specify restrictions).

  Recommendation: A

### Answers

Q7: Follow recommendation
Q8: Yes, let variables be reassigned any number of times
Q9: Recommendation


## 3rd Grilling Round

  **Q10** - **Compiler and external constraints**: Are there any compiler version constraints (e.g., C++11, C++17, C++20) or third-party
  dependencies required, or should we strictly follow the existing `g++` setup in `Makefile` with C++ Standard Library only?
  - A) Follow existing `g++` setup with C++ Standard Library only; no external dependencies.
  - B) Other constraint (please specify).

  Recommendation: A

  ---

  **Q11** - **Prior art reference**: Git commit `b499caf` previously contained an implementation proposal and task brief for single-character variables
  before being reverted in `400e621`. Should this prior work be recorded as prior art context?
  - A) Yes, record commit `b499caf` as prior art context for conventions, while following our confirmed Task Brief decisions.
  - B) No, treat this task as fresh with no prior art.

  Recommendation: A

### Answers

Q10: Recommendation, do not accommodate any new build system, just integrate with the existing one
Q11: Treat this task as a fresh start with no prior art

# Analysis

## Prompt

```
/analysis For task `single-character-variables`
```

## Answer
  Red-team found 7 candidate impacts. Starting grilling session round 1.

  ---

  **Q1** - **Undefined variable output suppression**: In [`src/main.cpp`](file:///home/ironowl/dev/MathExpressionEvaluator/src/main.cpp#L35),
  `std::cout << solve(Tree) << '\n';` runs unconditionally whenever parsing succeeds. 
  In [`headers/Nodes.hpp`](file:///home/ironowl/dev/MathExpressionEvaluator/headers/Nodes.hpp#L6), `Node::evaluate()` 
  returns `double` without error signaling. If an expression references an undefined variable, returning a dummy double prints
  an unwanted number after the error message, violating Acceptance Criterion 6.

  Recommendation: Confirm impact. Disposition: **Mitigate**. Draft obligation: The evaluation mechanism must abort without outputting
  a numeric result when an undefined variable error occurs.

  ---

  **Q2** - **REPL startup banner text**: In [`src/main.cpp`](file:///home/ironowl/dev/MathExpressionEvaluator/src/main.cpp#L15), the startup banner
  prints `'Q' to quit`. Acceptance Criterion 7 requires typing `quit` (or `Quit`) to exit, freeing `q` and `Q` for variable use. Users following
  the printed banner will not exit and will instead trigger variable evaluation.

  Recommendation: Confirm impact. Disposition: **Mitigate**. Draft obligation: The REPL startup banner must instruct the user to enter
  `quit` (or `Quit`) to exit instead of `'Q' to quit`.

  ---

  **Q3** - **REPL single-letter quit regression**: In [`src/main.cpp`](file:///home/ironowl/dev/MathExpressionEvaluator/src/main.cpp#L21),
  input matching `q` or `Q` immediately exits the program. Freeing `q` and `Q` breaks compatibility for external callers or workflows that exit with a single letter.

  Recommendation: Confirm impact. Disposition: **Accept**. Rationale: Intended breaking change mandated by Acceptance Criterion 7 and Decision Log Q4.

  ---

  **Q4** - **Unary negation factor parsing on variables**: In [`src/parser.cpp`](file:///home/ironowl/dev/MathExpressionEvaluator/src/parser.cpp#L74-L90),
  `Parser::ParseFactor` handles unary minus only when followed by `Integer` or `OpenPar`. Input such as `-x` triggers a parse error, violating Acceptance Criterion 5.

  Recommendation: Confirm impact. Disposition: **Mitigate**. Draft obligation: The parser must recognize and parse unary negation applied to variable factors.

  ---

  **Q5** - **State preservation on failed assignment**: Acceptance Criteria 3, 4, and 6 require assignments to store values on success and undefined
  variable errors to abort without mutating prior state. If the symbol table updates before the right-hand side finishes evaluating,
  expressions like `x = 1 + undefined_var` will overwrite or clear the previous value of `x`.

  Recommendation: Confirm impact. Disposition: **Mitigate**. Draft obligation: Session symbol table updates for assignment statements must occur
  only after the right-hand side expression evaluates successfully.

  ---

  **Q6** - **Assignment operator scope enforcement**: Acceptance Criteria 3 and the Out of Scope section restrict assignment to top-level statements
  and forbid chained (`a = b = 3`) or inline (`1 + (x = 2)`) assignments. If `=` is parsed as an expression operator, invalid nested assignments could be accepted or misparsed.

  Recommendation: Confirm impact. Disposition: **Mitigate**. Draft obligation: The assignment operator `=` must only be accepted in top-level statements of
  the form `<var> = <expr>`, and rejected with a syntax error in all other positions.

  ---

  **Q7** - **REPL loop AST node memory leak**: In [`src/main.cpp`](file:///home/ironowl/dev/MathExpressionEvaluator/src/main.cpp#L32-L38),
  `Tree` is overwritten every iteration and only deleted once after the loop terminates. Repeated evaluations and assignments leak allocated AST nodes on heap.

  Recommendation: Confirm impact. Disposition: **Mitigate**. Draft obligation: Dynamically allocated AST nodes must be deallocated within each REPL
  loop iteration after evaluation or error handling completes.

### Answer

```
Acknowledge all and follow recocommendations
```


# Impl-proposal

## Prompt
```
/impl-proposal For task `single-character-variables`
```

## Questions

  **Q1** - **Assignment statement representation**: How should assignment statements be represented by the parser and executed against the symbol table?

  - **Option 1**: Return a `Statement` struct (`bool isAssignment`, `char variable`, `Node *node`) from `Parser::Parse`.
  AST holds only expression nodes with `virtual double evaluate(const SymbolTable &symbols) const = 0`. If `stmt.isAssignment` is true and evaluation succeeds,
  `src/main.cpp` assigns `symbolTable[stmt.variable] = val`.
  - **Option 2**: Create `AssignmentNode : public Node` holding variable name and right-hand side node.
  Change `evaluate` signature to accept mutable `SymbolTable &symbols`, mutating the symbol table inside `AssignmentNode::evaluate`.

  Recommendation: Option 1. Preserves const-correctness and pure evaluation in AST nodes. Prevents partial mutations on
  evaluation failure and isolates statement logic to the REPL.

  ---

  **Q2** - **Evaluation error signaling mechanism**: How should `VariableNode` signal an undefined variable to
  `src/main.cpp` to abort evaluation and suppress numeric output per Acceptance Criterion 6 and Obligation O1?

  - **Option 1**: Define `class EvaluationError : public std::exception` in `headers/Nodes.hpp`. `VariableNode::evaluate` prints
  `[Evaluation ERROR] Undefined variable '<var>'` and throws `EvaluationError`. `src/main.cpp` catches `EvaluationError` and suppresses numeric output.
  - **Option 2**: Change `evaluate` signature across all nodes to return status, e.g. `bool evaluate(const SymbolTable &symbols, double &out) const` or `std::optional<double>`.

  Recommendation: Option 1. Standard C++ unwinding, zero boilerplate error-propagation branches in `AddNode`, `SubtractNode`, `MultiplyNode`, `DivideNode`, and `NegateNode`.

  ---

  **Q3** - **Symbol table container type**: What type should represent the session symbol table for single-character variables?

  - **Option 1**: `using SymbolTable = std::map<char, double>;`
  - **Option 2**: `using SymbolTable = std::unordered_map<char, double>;`

  Recommendation: Option 1. ASCII `char` keys enforce case-sensitivity (`'a' != 'A'`) with minimal overhead across 52 possible letters.

  ---

  **Q4** - **Trailing unconsumed token validation**: Should `Parser::Parse` verify that all tokens in `Input` are consumed?

  - **Option 1**: Assert `index == Input.size()`. If trailing tokens remain unparsed, emit `[Parsing ERROR] Unexpected token '<val>' at line: <index>`,
  delete any parsed AST, and return failure.
  - **Option 2**: Retain existing parser behavior where trailing tokens are ignored.

  Recommendation: Option 1. Strictly enforces grammar, rejecting chained assignments like `a = b = 3` and malformed expressions like `1 2` or `x y` per Obligation O5.

  ---

  **Q5** - **REPL startup banner text**: What exact banner text should replace `'Q' to quit` in `src/main.cpp:15` per Obligation O2?

  - **Option 1**: `'quit' to quit`
  - **Option 2**: `Enter 'quit' to quit`

  Recommendation: Option 1. Matches existing banner style while clarifying the required exit command.

## Answers

Q1: Follow recommendation
Q2: Recommendation
Q3: Recommendation
Q4: Recommendation
Q5: Option 1


# Impl

```
/impl for task single-character-variables
```
