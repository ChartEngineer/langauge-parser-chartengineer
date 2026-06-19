# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A tree-walking interpreter for a small custom C-like scripting language, written in Python. Source files use the `.lang` extension (see `examples/hello_world.lang`). The pipeline is the classic three stages: **source → lexer (tokens) → parser (AST) → interpreter (execution)**.

## ⚠️ Current state: incomplete

The repository is a partial implementation. `src/main.py` imports two modules that **do not exist yet**:

- `parser` → expected to provide a `Parser` class taking a token list, with a `parse()` method returning a `Program` AST node.
- `interpreter` → expected to provide an `Interpreter` class with an `interpret(ast)` method.

As a result, running `python3 src/main.py ...` currently fails with `ModuleNotFoundError: No module named 'parser'`. Only the lexer (`src/lexer.py`) and AST definitions (`src/ast_nodes.py`) are implemented. Completing the interpreter means writing `src/parser.py` and `src/interpreter.py` against the contracts the existing code already pins down (see below).

## Running

```bash
python3 src/main.py <file.lang>      # run a source file (e.g. examples/hello_world.lang)
python3 src/main.py --repl           # interactive REPL (default when no file given)
python3 src/main.py <file> --debug   # print tokens, AST, and execution trace
python3 src/lexer.py                 # run lexer standalone on its built-in sample
```

No build step. There is no test suite in the repo yet despite `pytest` being listed as a dependency.

## Dependencies

`requirements.txt` lists only optional/dev tools (`ply`, `pytest`, `black`) — the core code uses the standard library only. Install with `pip install -r requirements.txt`. Format with `black` (line conventions match its defaults).

## Architecture and contracts

Three components communicate through well-defined data structures. When adding the missing pieces, conform to these.

**`src/lexer.py`** — Hand-written character-by-character scanner (no regex-driven tokenizing). `Lexer(source).tokenize()` returns a `List[Token]` ending in an `EOF` token. Key types:
- `TokenType` (Enum): all literals, keywords, operators, and delimiters. Keywords are mapped in `Lexer.KEYWORDS`; single-char operators in `Lexer.SINGLE_CHAR_TOKENS`. Two-char operators (`==`, `!=`, `<=`, `>=`) and `//` line comments are handled inline in `tokenize()`.
- `Token` (dataclass): `type`, `value`, `line`, `column`.
- `LexerError`: raised with position info on unexpected/unterminated input.
- Note: `NEWLINE` and `COMMENT` tokens are emitted, not discarded — a parser must skip them.

**`src/ast_nodes.py`** — Node classes plus the Visitor pattern. The parser must build trees from these exact dataclasses; the interpreter consumes them via a visitor.
- Base classes: `ASTNode` (abstract, requires `accept(visitor)`), `Expression`, `Statement`, and `Program` (root, holds `statements`).
- Expressions: `LiteralExpression`, `IdentifierExpression`, `BinaryExpression`, `UnaryExpression`, `CallExpression`, `AssignmentExpression`.
- Statements: `ExpressionStatement`, `VarStatement`, `BlockStatement`, `IfStatement`, `WhileStatement`, `FunctionStatement`, `ReturnStatement`, `PrintStatement`.
- Every node has `accept(visitor)` dispatching to a `visit_*` method. The `Visitor` ABC declares all required `visit_*` methods — **any new interpreter or analysis pass should subclass `Visitor` and implement all of them** (Python won't instantiate it otherwise). `ASTPrinter` is the reference implementation and is used by `--debug` mode.

**`src/main.py`** — `LanguageInterpreter` orchestrates the pipeline (`run`, `run_file`, `repl`) and owns the CLI (argparse). The REPL auto-appends a `;` to single-line input lacking one. Errors are caught and printed; `--debug` adds a full traceback.

## Language reference (from the REPL `help` and examples)

- Variables: `var x = 10;`
- Functions: `function add(a, b) { return a + b; }` (recursion supported per examples)
- Conditionals: `if (cond) { ... } else { ... }`
- Loops: `while (cond) { ... }` (`for` and `null` keywords are tokenized but `for` has no statement node yet)
- Built-in: `print(...)` — note `PrintStatement` is a dedicated AST node, so `print` is language syntax, not an ordinary call.
- Operators: `+ - * / %`, comparisons `== != < <= > >=`, logical `and or not`, assignment `=`.
- Literals: numbers (int/float), strings (single or double quoted, with `\n \t \r \\` escapes), `true`/`false`, `null`.
- Comments: `// to end of line`.

## Conventions

- Keep the lexer/parser/interpreter strictly separated; they communicate only through `Token` lists and AST nodes — don't reach across layers.
- New AST nodes require: the dataclass + `accept`, a new abstract `visit_*` on `Visitor`, and implementations in every concrete visitor (`ASTPrinter`, and any future interpreter).
- AST nodes are `@dataclass`es; follow that style for additions.
- `src/` is added to `sys.path` at runtime by `main.py`, so intra-package imports are flat (`from lexer import ...`), not package-relative.
