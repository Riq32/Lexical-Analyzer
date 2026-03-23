"""
=============================================================
  MiniLang Lexical Scanner — Built from Scratch (no lexer tools)
  Language: Python 3
=============================================================
 
TOKEN SPECIFICATION
--------------------
Keywords     : if, while, print
Numbers      : [0-9]+  (integers)
Identifiers  : [A-Za-z_][A-Za-z0-9_]*
Strings      : "..." (double-quoted)
Arithmetic   : + - * /
Relational   : < > ==
Assignment   : =
Separators   : ( ) { } ;
Comments     : // single-line   /* multi-line */  (skipped)
Whitespace   : ignored
"""
 
import re
import sys
from dataclasses import dataclass
from typing import List
 
# ─────────────────────────────────────────────
#  Keywords
# ─────────────────────────────────────────────
KEYWORDS = {'if', 'while', 'print'}
 
# ─────────────────────────────────────────────
#  Token patterns  (ORDER IS CRITICAL)
# ─────────────────────────────────────────────
TOKEN_SPEC = [
    # Comments — must come before operators so // is not split into two /
    ('BLOCK_COMMENT',  r'/\*[\s\S]*?\*/'),
    ('LINE_COMMENT',   r'//[^\n]*'),
 
    # Literals
    ('NUMBER',         r'[0-9]+'),
    ('STRING',         r'"[^"\n]*"'),
 
    # Identifiers / Keywords (checked against KEYWORDS set after match)
    ('IDENTIFIER',     r'[A-Za-z_][A-Za-z0-9_]*'),
 
    # Relational operators — == must come before = (longest match first)
    ('REL_OP',         r'==|<|>'),
 
    # Assignment operator
    ('ASSIGN',         r'='),
 
    # Arithmetic operators
    ('ARITH_OP',       r'[+\-*/]'),
 
    # Separators
    ('LPAREN',         r'\('),
    ('RPAREN',         r'\)'),
    ('LBRACE',         r'\{'),
    ('RBRACE',         r'\}'),
    ('SEMICOLON',      r';'),
 
    # Whitespace — skip silently
    ('WHITESPACE',     r'[ \t\r\n]+'),
 
    # Catch-all for unknown characters — triggers an error
    ('UNKNOWN',        r'.'),
]
 
# Compile all patterns into one master regex with named groups
MASTER_PATTERN = re.compile(
    '|'.join('(?P<%s>%s)' % (name, pattern) for name, pattern in TOKEN_SPEC)
)
 
 
# ─────────────────────────────────────────────
#  Token data class
# ─────────────────────────────────────────────
@dataclass
class Token:
    type:   str
    value:  str
    line:   int
    column: int
 
 
# ─────────────────────────────────────────────
#  Scanner class
# ─────────────────────────────────────────────
class Scanner:
    """Hand-built lexical scanner for MiniLang."""
 
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.errors: List[str]  = []
 
    # ------------------------------------------------------------------
    def scan(self) -> List[Token]:
        line       = 1
        line_start = 0
 
        for mo in MASTER_PATTERN.finditer(self.source):
            kind  = mo.lastgroup          # token type name
            value = mo.group()            # matched text
            col   = mo.start() - line_start + 1
 
            # ── Track line numbers inside multi-line spans ──
            if kind in ('WHITESPACE', 'BLOCK_COMMENT', 'LINE_COMMENT', 'STRING'):
                newlines = value.count('\n')
                if newlines:
                    line      += newlines
                    line_start = mo.end() - (len(value) - value.rfind('\n') - 1)
 
            # ── Skip whitespace and comments ──
            if kind in ('WHITESPACE', 'LINE_COMMENT', 'BLOCK_COMMENT'):
                continue
 
            # ── Promote matching identifiers to KEYWORD ──
            if kind == 'IDENTIFIER' and value in KEYWORDS:
                kind = 'KEYWORD'
 
            # ── Record unknown characters as errors ──
            if kind == 'UNKNOWN':
                msg = f'[Line {line}, Col {col}] Unrecognized character: {repr(value)}'
                self.errors.append(msg)
 
            self.tokens.append(Token(kind, value, line, col))
 
        # Append end-of-file sentinel
        self.tokens.append(Token('EOF', 'EOF', line, 0))
        return self.tokens
 
    # ------------------------------------------------------------------
    def report(self):
        """Print a formatted token table to stdout."""
        W = 62
        print('=' * W)
        print('  MINILANG LEXICAL SCANNER — TOKEN OUTPUT')
        print('=' * W)
        print(f"  {'Line':>5}  {'Col':>4}   {'Token Type':<16}  Value")
        print('-' * W)
 
        for tok in self.tokens:
            # Truncate long comment / string values for display
            display = tok.value.replace('\n', '\\n')
            if len(display) > 35:
                display = display[:35] + '...'
            print(f'  {tok.line:>5}  {tok.column:>4}   {tok.type:<16}  {display}')
 
        print('=' * W)
        print(f'  Total tokens : {len(self.tokens)}')
 
        if self.errors:
            print(f'  Errors found : {len(self.errors)}')
            for e in self.errors:
                print(f'    ✗ {e}')
        else:
            print('  Errors found : 0  ✓')
        print('=' * W)
 
 
# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print('Usage: python scanner.py <source_file>')
        sys.exit(1)
 
    path = sys.argv[1]
    try:
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f'Error: File not found — {path}')
        sys.exit(1)
 
    scanner = Scanner(source)
    scanner.scan()
    scanner.report()
 
 
if __name__ == '__main__':
    main()
 