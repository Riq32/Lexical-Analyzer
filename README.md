# Lexical Analyzer — MiniLang Scanner

A hand-built lexical scanner for **MiniLang**, a simple imperative mini-language.
Built from scratch in **Python 3** using regular expressions — no lexer tools (PLY, ANTLR, Flex) used.

---

## 📌 Table of Contents
- [Overview](#overview)
- [Token Specification](#token-specification)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Sample Output](#sample-output)
- [Test Cases](#test-cases)
- [How the Scanner Works](#how-the-scanner-works)
- [Group Members](#group-members)

---

## Overview

A **lexical scanner** (also called a lexer or tokenizer) is the first phase of a compiler. It reads raw source code character by character and groups the characters into meaningful units called **tokens**, which are then passed to the parser.

This scanner was built from scratch as part of a **Compiler Construction** group assignment. The approach taken was a **hand-built regex master pattern** — all token types are defined as named regular expression groups and compiled into one master pattern using Python's `re` module.

---

## Token Specification

| Token Type | Description | Examples |
|---|---|---|
| `KEYWORD` | Reserved words of MiniLang | `if`, `while`, `print` |
| `NUMBER` | Integer numeric literals | `0`, `5`, `42`, `100` |
| `IDENTIFIER` | Variable and function names | `x`, `counter`, `result`, `_val` |
| `STRING` | Double-quoted string literals | `"Hello"`, `"done"` |
| `ARITH_OP` | Arithmetic operators | `+`, `-`, `*`, `/` |
| `REL_OP` | Relational operators | `<`, `>`, `==` |
| `ASSIGN` | Assignment operator | `=` |
| `LPAREN` | Left parenthesis | `(` |
| `RPAREN` | Right parenthesis | `)` |
| `LBRACE` | Left curly brace | `{` |
| `RBRACE` | Right curly brace | `}` |
| `SEMICOLON` | Statement terminator | `;` |
| `UNKNOWN` | Illegal / unrecognized character | `@`, `#`, `$`, `^`, `~` |
| `EOF` | End of file sentinel | `EOF` |

> **Note:** Comments (`//` single-line and `/* */` block) and whitespace are recognized but silently skipped — they do not appear in the token output.

---

## Project Structure

```
Lexical-Analyzer/
│
├── scanner.py                    # Main scanner — run this
├── sample.ml                     # Sample MiniLang program (0 errors)
├── test1_illegal_chars.ml        # Error test: illegal characters @ # $ ^
├── test2_unterminated_string.ml  # Error test: unclosed string literal
├── test3_mixed_errors.ml         # Error test: mixed valid and invalid tokens
└── README.md                     # This file
```

---

## How to Run

### Requirements
- Python 3.x (no external libraries needed)

### Run the scanner on any `.ml` file
```bash
python scanner.py <source_file>
```

### Examples
```bash
# Scan the main sample program
python scanner.py sample.ml

# Run error test cases
python scanner.py test1_illegal_chars.ml
python scanner.py test2_unterminated_string.ml
python scanner.py test3_mixed_errors.ml
```

---

## Sample Output

Running `python scanner.py sample.ml` produces:

```
==============================================================
  MINILANG LEXICAL SCANNER — TOKEN OUTPUT
==============================================================
   Line   Col   Token Type        Value
--------------------------------------------------------------
      5     1   LBRACE            {
      7     5   IDENTIFIER        x
      7     7   ASSIGN            =
      7     9   NUMBER            10
      7    11   SEMICOLON         ;
      8     5   IDENTIFIER        y
      8     7   ASSIGN            =
      8     9   NUMBER            3
      8    10   SEMICOLON         ;
     19     5   KEYWORD           if
     19     8   LPAREN            (
     19     9   IDENTIFIER        x
     19    11   REL_OP            >
     19    13   IDENTIFIER        y
     19    14   RPAREN            )
     19    16   LBRACE            {
     20     9   KEYWORD           print
     20    14   LPAREN            (
     20    15   STRING            "x is greater"
     ...
     46     0   EOF               EOF
==============================================================
  Total tokens : 133
  Errors found : 0  ✓
==============================================================
```

---

## Test Cases

### Test 1 — Illegal Characters (`test1_illegal_chars.ml`)
Tests characters that are not part of the MiniLang language: `@`, `#`, `$`, `^`.

**Expected result:** 4 errors, one per illegal character. All surrounding valid tokens are still correctly produced — the scanner recovers and continues after each error.

```
Errors found : 4
  ✗ [Line 6, Col 11] Unrecognized character: '@'
  ✗ [Line 7, Col 11] Unrecognized character: '#'
  ✗ [Line 8, Col 12] Unrecognized character: '$'
  ✗ [Line 9, Col 14] Unrecognized character: '^'
```

---

### Test 2 — Unterminated String (`test2_unterminated_string.ml`)
Tests a string literal that is opened with `"` but never closed on the same line.

**Expected result:** 1 error. Because the `STRING` pattern (`"[^"\n]*"`) does not allow newlines, the opening `"` fails to match and is flagged as `UNKNOWN`. The rest of the line is rescanned fresh, so `Hello` and `World` become `IDENTIFIER` tokens. The next valid string `"Alice"` on the following line is correctly recognized.

```
Errors found : 1
  ✗ [Line 5, Col 11] Unrecognized character: '"'
```

---

### Test 3 — Mixed Valid and Invalid (`test3_mixed_errors.ml`)
Tests recovery when illegal characters (`~`, `&`) appear in the middle of otherwise valid statements.

**Expected result:** 2 errors. The scanner flags both illegal characters, then continues tokenizing the rest of the program correctly — including `float`, `string`, and `print()` calls that appear after the errors.

```
Errors found : 2
  ✗ [Line 6, Col 25] Unrecognized character: '~'
  ✗ [Line 7, Col 15] Unrecognized character: '&'
```

---

## How the Scanner Works

### 1. Token Patterns (`TOKEN_SPEC`)
All token types are defined as an ordered list of `(type, regex)` pairs. **Order is critical** — for example, `REL_OP` includes `==` before `ASSIGN` matches `=`, preventing `==` from being split into two assignment tokens.

### 2. Master Pattern
All patterns are joined into one compiled regex using Python's named capture groups:
```python
MASTER_PATTERN = re.compile(
    '|'.join('(?P<%s>%s)' % (name, pattern) for name, pattern in TOKEN_SPEC)
)
```
The regex engine tries each alternative left-to-right — the first match wins, which is why ordering controls priority.

### 3. Scanning with `re.finditer()`
The scanner walks the entire source string in one pass. For each match it extracts the token type, value, line number, and column number.

### 4. Keyword Promotion
After an `IDENTIFIER` is matched, its value is checked against the `KEYWORDS` set `{'if', 'while', 'print'}`. If it matches, the token type is reclassified as `KEYWORD`.

### 5. Error Recovery
When an `UNKNOWN` token is encountered the scanner does **not crash**. It logs the error with the exact location, appends the token to the list, and continues scanning — reporting all errors in a single pass.

### 6. EOF Sentinel
After all input is consumed, a final `EOF` token is appended to signal the end of the token stream to any downstream parser.

---

## Group Members

| Member | Role |
|---|---|
| Member 1 | Grammar Designer — token spec, sample program, test inputs |
| Member 2 | Scanner Core Developer — regex patterns, master pattern, line tracking |
| Member 3 | Token Classification & Error Handling — keywords, UNKNOWN, report output |
| Member 4 | Report Writer & Demo Lead — documentation, screenshots, live demo |
