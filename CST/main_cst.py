from scanner import Scanner
from parser_cst import ParserCST


def main():
    with open("sample.po") as f:
        source = f.read()

    scanner = Scanner(source)
    tokens = scanner.scan()

    scanner.report()

    if scanner.errors:
        print("\n Parsing stopped due to lexical errors.")
        return

    parser = ParserCST(tokens)

    try:
        tree = parser.parse_program()

        print("\n===== Concrete Parse Tree =====")
        print(tree)

    except Exception as e:
        print("\n PARSER ERROR:")
        print(e)


if __name__ == "__main__":
    main()