from scanner import Scanner
from parser_cst import ParserCST

def main():
    with open("sample.po") as f:
        source = f.read()

    scanner = Scanner(source)
    tokens = scanner.scan()

    parser = ParserCST(tokens)
    tree = parser.parse_program()

    print("\n===== CONCRETE SYNTAX TREE =====")
    print(tree)

if __name__ == "__main__":
    main()