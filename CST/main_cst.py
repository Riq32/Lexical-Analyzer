"""
=============================================================
  MiniLang Compiler Pipeline — Full Demo
  Phase 1: Lexical Analysis   (Scanner)
  Phase 2: Syntax Analysis    (Parser → CST)
  Phase 3: Intermediate Code  (ICG → Quadruples)
=============================================================
"""

from scanner import Scanner
from parser_cst import ParserCST
from icg import ICGenerator


def main():
<<<<<<< Updated upstream
    # ── Read source program ──
    with open("sample.po") as f:
=======
    with open("sample2.po") as f:
>>>>>>> Stashed changes
        source = f.read()

    print("\n" + "=" * 66)
    print("  MINILANG COMPILER PIPELINE")
    print("=" * 66)
    print("\n──── SOURCE PROGRAM (sample.po) ────")
    print(source)

    # ── Phase 1: Lexical Analysis ──
    print("═" * 66)
    print("  PHASE 1: LEXICAL ANALYSIS (Scanner)")
    print("═" * 66)

    scanner = Scanner(source)
    tokens = scanner.scan()
    scanner.report()

    if scanner.errors:
        print("\n ✗ Compilation stopped due to lexical errors.")
        return

    # ── Phase 2: Syntax Analysis ──
    print()
    print("═" * 66)
    print("  PHASE 2: SYNTAX ANALYSIS (Parser → Concrete Syntax Tree)")
    print("═" * 66)

    parser = ParserCST(tokens)

    try:
        tree = parser.parse_program()
        print("\n───── Concrete Parse Tree ─────")
        print(tree)

    except Exception as e:
        print("\n ✗ PARSER ERROR:")
        print(e)
        return

    # ── Phase 3: Intermediate Code Generation ──
    print("═" * 66)
    print("  PHASE 3: INTERMEDIATE CODE GENERATION (ICG → Quadruples)")
    print("═" * 66)

    icg = ICGenerator()
    quads = icg.generate(tree)
    icg.print_quads()

    # ── Summary ──
    print()
    print("═" * 66)
    print("  COMPILATION SUMMARY")
    print("═" * 66)
    print(f"  Tokens generated     : {len(tokens)}")
    print(f"  Lexical errors       : {len(scanner.errors)}")
    print(f"  Parse tree root      : <{tree.name}>")
    print(f"  Quadruples generated : {len(quads)}")
    print(f"  Temp variables used  : {icg.temp_count}")
    print(f"  Labels used          : {icg.label_count}")
    print("═" * 66)
    print("  ✓ Compilation completed successfully.")
    print("═" * 66)


if __name__ == "__main__":
    main()