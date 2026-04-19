from scanner import Scanner
from parser import Parser

def main():
    with open("sample.po", "r") as f:
        source = f.read()

    # Step 1: Scan
    scanner = Scanner(source)
    tokens = scanner.scan()
    scanner.report()

    # Step 2: Parse
    parser = Parser(tokens)
    tree = parser.parse_program()

    print("\n===== PARSE TREE =====")
    print(tree)


if __name__ == "__main__":
    main()