# variable-support

Source: free text
Processed questions through Q14

## 1. Change Summary
Fulfilling the task introduces persistent single-letter variable storage (`a`-`z`, `A`-`Z`), assignment statement parsing (`<var> = <expr>`), and floating-point numeric literal tokenization (`double`). It modifies the AST evaluation interface to resolve variable values during tree traversal, updates division behavior to abort on zero divisors, and adapts factor parsing to handle floating-point values. It modifies the REPL lifecycle by replacing the `'q'`/`'Q'` termination shortcut with a case-insensitive `quit` command, provides explicit process stage logging (tokenization, parsing, evaluation/assignment) per input line, formats assignment confirmations and scalar values, and prevents memory leaks and bounds crashes across sessions.

## 2. Impact Map
- `headers/Nodes.hpp` — Relationship: origin — Adds variable evaluation and runtime error signaling across AST node hierarchy — Impacts: I1, I2, I3
- `headers/lexer.hpp` & `src/lexer.cpp` — Relationship: origin — Introduces identifier tokens, assignment operator, and floating-point literal tokenization — Impacts: I5
- `headers/parser.hpp` & `src/parser.cpp` — Relationship: origin — Introduces assignment statement parsing and floating-point decimal literal parsing — Impacts: I4, I6
- `src/main.cpp` — Relationship: downstream — Manages persistent variable state, handles `quit` termination command, explicitly logs process stages, reclaims AST memory, and updates banner — Impacts: I7, I8, I9, I10, I11

## 3. Impacts

### I1 — AST Evaluation Contract & Variable Context
- **Lens**: Contracts and interfaces
- **Severity**: High
- **Breaking**: Yes
- **Condition**: Unconditional
- **Evidence**: `headers/Nodes.hpp:6` defines `virtual double evaluate() const = 0` with zero arguments.
- **Consequence**: Evaluating variable nodes in the AST requires resolving identifiers against the session's variable table. If `evaluate()` signature is updated (e.g. taking a variable environment parameter), all existing AST node classes (`NumberNode`, `AddNode`, `SubtractNode`, `MultiplyNode`, `DivideNode`, `NegateNode`, `BinaryOperationNode`) and their callers must be updated to comply with the new contract.
- **Disposition**: Mitigate via: O1 (Settled in: Q1)

### I2 — Division by Zero Runtime Behavior
- **Lens**: Behavior and regressions
- **Severity**: High
- **Breaking**: Yes
- **Condition**: Unconditional
- **Evidence**: `headers/Nodes.hpp:79-81` in `DivideNode::evaluate()` performs native C++ `/` on `double`, yielding IEEE `inf`/`-inf`/`nan` without raising an error.
- **Consequence**: Without explicit zero-check mitigation, dividing by zero (e.g. `5 / 0` or `a / 0`) produces `inf` instead of reporting a runtime error, violating Acceptance Criteria 5 and Decision Q8.
- **Disposition**: Mitigate via: O2 (Settled in: Q2)

### I3 — Evaluation Error Propagation & Abort Mechanism
- **Lens**: Reliability and failure modes
- **Severity**: High
- **Breaking**: Yes
- **Condition**: Unconditional
- **Evidence**: `headers/Nodes.hpp:6`, `src/main.cpp:35`; `evaluate()` returns a scalar `double` with no error signaling mechanism.
- **Consequence**: When an evaluation error occurs (such as an unassigned variable or division by zero) deep within an expression tree, `evaluate()` has no way to signal failure unless an error mechanism (such as exceptions, error return, or result type) is used. If unhandled or improperly signaled, the REPL prints an invalid number or crashes, violating Acceptance Criteria 5.
- **Disposition**: Mitigate via: O3 (Settled in: Q3)

### I4 — Parser Factor Parsing Floating-Point Decimals
- **Lens**: Behavior and regressions
- **Severity**: High
- **Breaking**: No
- **Condition**: Unconditional
- **Evidence**: `src/parser.cpp:61` and `src/parser.cpp:78` use `std::stoi(temp.value)`.
- **Consequence**: When the lexer provides floating-point number tokens (e.g., `"3.14"`), `std::stoi` either truncates the decimal portion or fails, preventing floating-point calculations and violating Acceptance Criteria 4 and Decision Q4.
- **Disposition**: Mitigate via: O4 (Settled in: Q4)

### I5 — Lexer Floating-Point Literal and Dot Tokenization
- **Lens**: Behavior and regressions
- **Severity**: High
- **Breaking**: No
- **Condition**: Unconditional
- **Evidence**: `src/lexer.cpp:47-59` only accepts `isdigit()` for numeric tokens and classifies `.` as an illegal character, returning `token(Error)`.
- **Consequence**: Expressions containing decimal literals (e.g., `3.14`, `0.5`) fail at tokenization time with syntax error messages, preventing floating-point literal support required by Acceptance Criteria 4. Additionally, malformed decimal literals (e.g. `1.2.3` or lone `.`) must produce a lexing error without infinite loops or crashes.
- **Disposition**: Mitigate via: O5 (Settled in: Q5)

### I6 — Parser Statement vs Expression Handling
- **Lens**: Contracts and interfaces
- **Severity**: High
- **Breaking**: No
- **Condition**: Unconditional
- **Evidence**: `headers/parser.hpp:20` defines `Node *Parse(std::vector<Token> raw)`.
- **Consequence**: Currently, `Parser::Parse` assumes every input is an expression producing a `Node*`. Fulfilling variable support introduces assignment statements (`<var> = <expr>`) alongside expressions. If the parser does not distinguish statements from expressions, it cannot validate assignment syntax (e.g. invalid LHS, missing RHS) or communicate assignment semantics to the REPL driver.
- **Disposition**: Mitigate via: O6 (Settled in: Q6)

### I7 — REPL Out-of-Bounds Crash on Empty or Whitespace Input
- **Lens**: Reliability and failure modes
- **Severity**: High
- **Breaking**: No
- **Condition**: Unconditional
- **Evidence**: `src/main.cpp:24-25` executes `if (TokenList[0].type == Error)` directly on the returned token vector without checking if `TokenList.empty()`.
- **Consequence**: Pressing Enter on an empty line or line with only whitespace causes undefined behavior / segmentation fault (out-of-bounds vector access), terminating the REPL and losing all stored variable state.
- **Disposition**: Mitigate via: O7 (Settled in: Q7)

### I8 — REPL Exit Command Workflow and 'q' / 'Q' Evaluation
- **Lens**: Downstream consumers
- **Severity**: Medium
- **Breaking**: Yes
- **Condition**: Unconditional
- **Evidence**: `src/main.cpp:21` currently terminates if `input == "q" || input == "Q" || input == "Quit" || input == "quit"`.
- **Consequence**: Existing users accustomed to typing single-letter `q` or `Q` to quit will no longer quit; instead, typing `q` or `Q` evaluates the variable `q` or `Q` (or reports undefined variable). The session only exits on `quit` (case-insensitive: `quit`, `Quit`, `QUIT`).
- **Disposition**: Mitigate via: O8 (Settled in: Q8)

### I9 — REPL Session State Preservation and Mutation Atomicity
- **Lens**: Data and state
- **Severity**: Medium
- **Breaking**: No
- **Condition**: Unconditional
- **Evidence**: `src/main.cpp:16-36` contains no variable storage across iterations.
- **Consequence**: Variables must persist in memory throughout the REPL session across lines. If an assignment statement encounters an error during RHS evaluation (e.g. division by zero or referencing an undefined variable), partial assignment must not mutate or corrupt existing variable state.
- **Disposition**: Mitigate via: O9 (Settled in: Q9)

### I10 — REPL AST Memory Leaks Across Lines
- **Lens**: Performance and capacity
- **Severity**: Medium
- **Breaking**: No
- **Condition**: Unconditional
- **Evidence**: `src/main.cpp:32-38` allocates `Tree = parser.Parse(...)` inside the loop, but `delete Tree;` is placed outside the loop.
- **Consequence**: In an interactive session with persistent state where users enter multiple expressions and assignments, every line executed leaks heap-allocated AST nodes. Over extended sessions, leaked AST nodes accumulate.
- **Disposition**: Mitigate via: O10 (Settled in: Q10)

### I11 — REPL Startup Banner and Process Execution Logging
- **Lens**: User experience
- **Severity**: Low
- **Breaking**: No
- **Condition**: Unconditional
- **Evidence**: `src/main.cpp:15` prints `"'Q' to quit"`, conflicting with Acceptance Criteria 6 and Decision Q3. Input dossier Decision Log Q14 specifies explicit logging of each process given on the REPL, while `src/main.cpp:28-30` and `src/lexer.cpp:15` currently contain incomplete ad-hoc logs (`Input`, `N Tokens: ...`, `------------------------`) without explicit logging for parsing and evaluation/assignment stages.
- **Consequence**: The startup banner misguides users to believe `'Q'` exits the REPL, and the REPL lacks explicit, consistent logging for each process stage (tokenization, parsing, evaluation/assignment execution) as required by Decision Q14.
- **Disposition**: Mitigate via: O11 (Settled in: Q12)

## 4. Obligations

### O1 — AST Variable Context Resolution
- **Requirements**: AST evaluation must accept a variable environment/context to resolve single-letter variable values during traversal without relying on unencapsulated global state.
- **Applies**: Always
- **Verification**: Expressions referencing defined variables evaluate to the correct numerical results using the provided variable values.
- **Source**: I1

### O2 — Division by Zero Runtime Detection
- **Requirements**: Division by zero during arithmetic evaluation must be detected, abort evaluation of the current line, and emit an explicit runtime error message (`[Evaluation ERROR] Division by zero`) without crashing or altering session state.
- **Applies**: Always
- **Verification**: Evaluating any expression that divides by zero (e.g. `1 / 0`, `a / 0`) produces the error message `[Evaluation ERROR] Division by zero` on standard output, does not crash, and leaves variable state untouched.
- **Source**: I2

### O3 — Evaluation Abort and State Protection
- **Requirements**: Any runtime evaluation error (such as an undefined variable or division by zero) must immediately abort evaluation of the line, output a descriptive error message, and prevent any modification of variable session state.
- **Applies**: Always
- **Verification**: In an assignment statement whose right-hand side produces an evaluation error (e.g., `a = 5 / 0` or `a = b` where `b` is undefined), the target variable `a` is not created or modified, and an error message is printed.
- **Source**: I3

### O4 — Floating-Point Literal Parsing
- **Requirements**: The parser must parse numeric literals containing decimals into floating-point numbers without precision loss or truncation to integers.
- **Applies**: Always
- **Verification**: Evaluating expressions with decimal literals (e.g., `3.14 + 2.5`) outputs the accurate floating-point sum (`5.64`).
- **Source**: I4

### O5 — Floating-Point Tokenization and Validation
- **Requirements**: The lexer must tokenize numeric literals containing decimal points into numeric tokens and must emit an error token for malformed numbers containing multiple decimal points or solitary dots.
- **Applies**: Always
- **Verification**: Inputs like `3.14` and `0.5` produce valid numeric tokens; inputs like `3.14.15` or `.` produce error tokens and an informative syntax error message without hanging or crashing.
- **Source**: I5

### O6 — Assignment Statement and Expression Distinction
- **Requirements**: The parser must distinguish assignment statements (`<var> = <expr>`) from expressions, enforce syntactic constraints for both, and supply the parsed target variable and expression tree to the caller.
- **Applies**: Always
- **Verification**: Valid assignments (`a = 5`) and expressions (`a + 2`) are both parsed correctly; invalid assignments (such as missing RHS `a =` or non-variable LHS `1 = 2`) report parsing errors.
- **Source**: I6

### O7 — Empty and Whitespace Input Handling
- **Requirements**: The REPL must accept empty lines and whitespace-only lines without crashing, printing errors, or modifying session state.
- **Applies**: Always
- **Verification**: Pressing Enter on an empty line or typing spaces in the REPL displays a new prompt without terminating or outputting error messages.
- **Source**: I7

### O8 — Case-Insensitive 'quit' Termination and 'q' / 'Q' Variable Support
- **Requirements**: The REPL session must only terminate when the user inputs `quit` (case-insensitive: `quit`, `Quit`, `QUIT`), and must evaluate single-letter inputs `q` and `Q` as variable references or assignment targets.
- **Applies**: Always
- **Verification**: Typing `q` or `Q` in the REPL evaluates the variable or reports an undefined variable error; typing `quit`, `Quit`, or `QUIT` cleanly terminates the REPL.
- **Source**: I8

### O9 — Persistent and Atomic Session Variable State
- **Requirements**: Variables assigned during a REPL session must persist across subsequent inputs until explicitly reassigned or until the REPL terminates; failed assignments must not alter existing variable values.
- **Applies**: Always
- **Verification**: Defining `a = 10` followed by evaluating `a + 5` outputs `15`; a subsequent failed assignment `a = 1 / 0` leaves `a` equal to `10`.
- **Source**: I9

### O10 — AST Memory Reclaim per Iteration
- **Requirements**: All dynamically allocated AST nodes created for a REPL input line must be freed at the conclusion of that line's processing, regardless of whether execution succeeded or failed.
- **Applies**: Always
- **Verification**: Running multiple expressions or failed statements in a single REPL session does not leak AST nodes on each iteration.
- **Source**: I10

### O11 — Updated REPL Startup Banner and Process Stage Logging
- **Requirements**: The REPL startup banner must instruct the user to type `quit` to exit, and the REPL must explicitly log each process stage (tokenization, parsing, evaluation/assignment execution) during input line processing, followed by the formatted assignment confirmation (`<var> = <value>`), scalar evaluation result, or error message.
- **Applies**: Always
- **Verification**: Launching the REPL displays `quit` exit instructions in the startup banner. Submitting an expression or assignment explicitly logs each process stage (tokenization, parsing, evaluation/assignment execution) before displaying the result or confirmation.
- **Source**: I11

## 5. Decision Log

- **Q1** — AST Evaluation Contract & Variable Context: Confirm impact I1; mitigate via obligation O1 by passing a variable context/environment during evaluation.
- **Q2** — Division by Zero Runtime Error Handling: Confirm impact I2; mitigate via obligation O2 by detecting zero divisors, aborting evaluation, and printing an explicit error.
- **Q3** — Evaluation Error Propagation & Abort Mechanism: Confirm impact I3; mitigate via obligation O3 by establishing an error abort channel that prevents variable mutation on failed evaluations.
- **Q4** — Parser Floating-Point Literal Parsing: Confirm impact I4; mitigate via obligation O4 by parsing numerical tokens as `double`.
- **Q5** — Lexer Decimal Floating-Point Tokenization: Confirm impact I5; mitigate via obligation O5 by tokenizing decimal numbers and rejecting malformed decimals with error tokens.
- **Q6** — Parser Statement vs Expression Discrimination: Confirm impact I6; mitigate via obligation O6 by distinguishing statements from expressions and enforcing assignment syntax.
- **Q7** — REPL Out-of-Bounds Crash on Empty or Whitespace Input: Confirm impact I7; mitigate via obligation O7 by handling empty token sequences safely.
- **Q8** — REPL Exit Command & Variable 'q' / 'Q' Evaluation: Confirm impact I8; mitigate via obligation O8 by reserving `quit` (case-insensitive) for exiting and allowing `q` and `Q` to evaluate as variables.
- **Q9** — REPL Variable Session State Preservation & Mutation Atomicity: Confirm impact I9; mitigate via obligation O9 by retaining variables in session memory and ensuring assignments update state atomically only upon successful evaluation.
- **Q10** — REPL AST Memory Leaks Across Lines: Confirm impact I10; mitigate via obligation O10 by freeing all allocated AST nodes on every REPL line iteration.
- **Q11** — REPL Startup Banner and Debug Log Output Noise: Confirm impact I11; mitigate via obligation O11 by updating the startup banner to mention `quit` and removing debug print statements from production output.
- **Q12** — REPL Startup Banner and Process Execution Logging (Revising I11 / O11): Confirm impact I11; mitigate via obligation O11 by updating the startup banner to mention `quit` and explicitly logging each process stage (tokenization, parsing, evaluation/assignment execution) in the REPL per Decision Q14.
