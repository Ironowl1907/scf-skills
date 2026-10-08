# variable-support

Source: free text · Status: Completed

## 1. Task Brief

### Problem Statement
The current mathematical expression evaluator evaluates expressions immediately and statelessly. Users cannot define variables, store intermediate calculation results, or reuse previously calculated values across lines in the REPL. Additionally, numerical inputs are restricted to integers, preventing floating-point calculations, and typing `q` or `Q` terminates the session prematurely.

### Expected Outcome
The REPL allows users to define and reassign single-letter variables using floating-point arithmetic (`double`), evaluate expressions combining variables and literals across REPL inputs, and see clear confirmation messages for assignments (`<var> = <value>`) and computed scalar values for expressions. The REPL handles errors (undefined variables, division by zero, syntax errors) gracefully without crashing, and exits cleanly only when `quit` is entered.

### Acceptance Criteria
1. **Variable Storage and Scope**:
   - Variables are identified by a single alphabetic character (`a`-`z`, `A`-`Z`).
   - Variable names are case-sensitive (`a` and `A` are distinct variables).
   - Variables retain their assigned values throughout the active REPL session until reassigned or until the program exits.
2. **Assignment Operation**:
   - Accepts statements of the form `<var> = <expr>` with arbitrary whitespace around tokens (e.g., `a=5`, `a = 2 * (3 + 1.5)`).
   - Upon assignment, evaluates the RHS expression, updates/stores the variable's value, and outputs confirmation in the format `<var> = <value>` (e.g., `a = 7`).
   - Supports reassignment of existing variables to new values.
3. **Expression Evaluation**:
   - Variables can be referenced within any arithmetic expression (e.g., `a + 3`, `a * b`).
   - Evaluating a non-assignment expression outputs the evaluated scalar value directly (e.g., `7`).
4. **Data Type and Literals**:
   - All numbers and calculations use `double` precision.
   - Literals in input can be integers or floating-point decimals (e.g., `42`, `3.14`, `0.5`).
5. **Error Handling**:
   - Attempting to evaluate an unassigned variable prints an explicit error message (e.g., `[Evaluation ERROR] Undefined variable '<var>'`) and aborts evaluation of that line without modifying session state or crashing.
   - Division by zero prints an explicit runtime error message (e.g., `[Evaluation ERROR] Division by zero`) and aborts evaluation of that line without modifying session state or crashing.
   - Lexing and parsing syntax errors print descriptive messages and abort evaluation for that line without crashing.
6. **REPL Control**:
   - The REPL exits only when the user inputs `quit` (case-insensitive: `quit`, `Quit`, `QUIT`).
   - Typing `q` or `Q` alone evaluates variable `q` or `Q` (or reports undefined variable if unassigned), rather than quitting the REPL.

### Out of Scope
- Multi-character variable names or identifiers (e.g., `foo`, `x1`).
- Chained assignments (e.g., `a = b = 5`).
- Multiple statements or expressions on a single line (e.g., separated by `;`).
- Variable deletion or unsetting commands.
- Persisting variable state to disk, files, or across REPL restarts.
- Data types other than `double` (e.g., strings, booleans, arrays).
- Custom functions or control-flow constructs.

## 2. Context

### Codebase
- [headers/lexer.hpp](file:///home/ironowl/dev/MathExpressionEvaluator/headers/lexer.hpp) & [src/lexer.cpp](file:///home/ironowl/dev/MathExpressionEvaluator/src/lexer.cpp) — Token types and tokenizer; needs to support single-letter identifier tokens, assignment operator `=`, and floating-point numeric literals (`double`).
- [headers/Nodes.hpp](file:///home/ironowl/dev/MathExpressionEvaluator/headers/Nodes.hpp) — AST class hierarchy; polymorphic base `Node` with `virtual double evaluate() const = 0` and concrete nodes. Needs variable evaluation support and runtime error handling (e.g. division by zero, undefined variable).
- [headers/parser.hpp](file:///home/ironowl/dev/MathExpressionEvaluator/headers/parser.hpp) & [src/parser.cpp](file:///home/ironowl/dev/MathExpressionEvaluator/src/parser.cpp) — Recursive descent parser; handles operator precedence and statement/expression syntax (assignment statements `<var> = <expr>` vs expressions).
- [src/main.cpp](file:///home/ironowl/dev/MathExpressionEvaluator/src/main.cpp) — Interactive REPL driver; manages session input loop, persists variable state across lines, checks `quit` keyword, and displays formatted output/errors.
- [Makefile](file:///home/ironowl/dev/MathExpressionEvaluator/Makefile) — Build configuration compiling with `g++` into executable `final.out`.

### Conventions & Prior Art
- **Polymorphic AST**: Class hierarchy rooted at `Node` using virtual methods (`evaluate()`) and virtual destructors (`~Node()`).
- **Memory Management**: Manual dynamic memory allocation with raw pointers (`new` / `delete`).
- **Project Structure**: Header/source separation under `headers/` and `src/`.
- **Parsing Style**: Classic recursive descent parsing (`ParseExpr`, `ParseTerm`, `ParseFactor`).

### Related Work
- None (standalone project, single active branch `main`, no external PRs or issues).

### External References
- C++11 (and above) Standard Library documentation (`<iostream>`, `<string>`, `<vector>`, `<map>` / `<unordered_map>`).

### Constraints
- **Language Standard**: Standard C++11 or later (`cxx11`), using only standard library features.
- **Dependencies**: Zero external / third-party dependencies.
- **Pedagogical / Architecture**: Implementation must be clean, easily readable, and maintain the educational focus on OOP polymorphism and basic compiler AST architecture.
- **Compiler**: Must compile with `g++` via the existing `Makefile`.

### People to Consult
- Repository owner (`@Ironowl1907`).

## 3. Decision Log

- **Q1** — Assignment Syntax and REPL Output: Support `<var> = <expr>` with arbitrary RHS expressions, allow reassignment, and output `<var> = <value>` confirmation on assignment while outputting plain evaluated value for expressions.
- **Q2** — Variable Case Sensitivity: Variable names are case-sensitive (`a` and `A` are distinct).
- **Q3** — REPL Exit Command vs Variable 'q': Require `quit` keyword to exit REPL so single letters `q` and `Q` can be valid variables.
- **Q4** — Floating-Point Number Literals: Support full `double` literals (e.g. decimals like `3.14`) in the lexer and parser.
- **Q5** — Undefined Variables: Abort line evaluation and print a clear error message without crashing.
- **Q6** — Chained Assignment & Multi-Statement Scope: Single assignment or single expression per line only; chained assignment and multi-statements are out of scope.
- **Q7** — Confirmation Message Format for Assignments: Format is `<var> = <value>` (e.g., `a = 5`).
- **Q8** — Division by Zero Behavior: Abort line evaluation and report runtime error without crashing.
- **Q9** — Whitespace and Assignment Syntax Flexibility: Fully whitespace-insensitive syntax.
- **Q10** — Codebase Areas: Confirmed all five project areas (`lexer`, `Nodes`, `parser`, `main`, `Makefile`) comprise the full scope of the project.
- **Q11** — Standard & Dependencies: Standard C++11+, standard library only, zero third-party dependencies.
- **Q12** — Architectural Priority: Clean and easily readable code focusing on fundamental OOP polymorphism and AST concepts.
- **Q13** — Related Work & Collaborators: Solo project on `main` branch with no external branches, PRs, or tickets.
- **Q14** — Logging: Explicit logging of each of the processes given on the REPL
