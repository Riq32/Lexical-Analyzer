from cst_node import CSTNode


class ParserCST:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # ----------------------------
    # Utility functions
    # ----------------------------
    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def match(self, expected_type):
        token = self.peek()

        if token.type == expected_type:
            self.advance()
            return token

        if expected_type == "SEMICOLON":
            self.error("Missing ';' at end of statement")
        elif expected_type == "RPAREN":
            self.error("Missing ')'")
        elif expected_type == "RBRACE":
            self.error("Missing '}'")
        elif expected_type == "LPAREN":
            self.error("Missing '(' after keyword")
        else:
            self.error(f"Expected {expected_type}")

    def error(self, message):
        token = self.peek()

        full_msg = (
            f"\n[SYNTAX ERROR]\n"
            f"Line {token.line}, Column {token.column}\n"
            f"Found: {token.type} ({token.value})\n"
            f"Problem: {message}\n"
        )

        raise Exception(full_msg)

    def node(self, name, children=None, value=None):
        return CSTNode(name, children, value)

    # ----------------------------
    # Grammar Implementation
    # ----------------------------

    def parse_program(self):
        children = []

        if self.peek().type == "LBRACE":
            self.match("LBRACE")
            children.append(self.node("LBRACE", value="{"))

            stmt_list = self.parse_statement_list()
            children.append(stmt_list)

            self.match("RBRACE")
            children.append(self.node("RBRACE", value="}"))

            return self.node("program", children)

        return self.node("program", [self.parse_statement_list()])

    def parse_statement_list(self):
        statements = []

        while self.peek().type != "EOF" and self.peek().type != "RBRACE":
            statements.append(self.parse_statement())

        return self.node("statement_list", statements)

    def parse_statement(self):
        token = self.peek()

        if token.type == "KEYWORD":
            if token.value == "if":
                return self.parse_if()
            elif token.value == "while":
                return self.parse_while()
            elif token.value == "print":
                return self.parse_print()
            else:
                self.error(f"Unknown keyword '{token.value}'")

        elif token.type == "IDENTIFIER":
            return self.parse_assignment()

        elif token.type == "UNKNOWN":
            self.error(f"Invalid symbol '{token.value}'")

        else:
            self.error("Invalid start of statement")

    # ----------------------------
    # Assignment
    # ----------------------------
    def parse_assignment(self):
        id_tok = self.match("IDENTIFIER")
        assign_tok = self.match("ASSIGN")

        expr = self.parse_expression()

        semi_tok = self.match("SEMICOLON")

        return self.node("assignment", [
            self.node("identifier", value=id_tok.value),
            self.node("ASSIGN", value=assign_tok.value),
            expr,
            self.node("SEMICOLON", value=semi_tok.value)
        ])

    # ----------------------------
    # IF
    # ----------------------------
    def parse_if(self):
        token = self.peek()
        if token.value != "if":
            self.error("Expected 'if'")
        self.advance()

        self.match("LPAREN")
        cond = self.parse_condition()
        self.match("RPAREN")

        self.match("LBRACE")
        stmts = self.parse_statement_list()
        self.match("RBRACE")

        return self.node("if_statement", [
            self.node("KEYWORD", value="if"),
            cond,
            stmts
        ])

    # ----------------------------
    # WHILE
    # ----------------------------
    def parse_while(self):
        token = self.peek()
        if token.value != "while":
            self.error("Expected 'while'")
        self.advance()

        self.match("LPAREN")
        cond = self.parse_condition()
        self.match("RPAREN")

        self.match("LBRACE")
        stmts = self.parse_statement_list()
        self.match("RBRACE")

        return self.node("while_statement", [
            self.node("KEYWORD", value="while"),
            cond,
            stmts
        ])

    # ----------------------------
    # PRINT
    # ----------------------------
    def parse_print(self):
        token = self.peek()
        if token.value != "print":
            self.error("Expected 'print'")
        self.advance()

        self.match("LPAREN")
        expr = self.parse_expression()
        self.match("RPAREN")
        self.match("SEMICOLON")

        return self.node("print_statement", [
            self.node("KEYWORD", value="print"),
            expr
        ])

    # ----------------------------
    # Expressions (FIXED STRUCTURE)
    # ----------------------------
    def parse_expression(self):
        term_node = self.parse_term()
        node = self.node("expression", [term_node])

        while self.peek().type == "ARITH_OP" and self.peek().value in ("+", "-"):
            op = self.peek()
            self.advance()
            right = self.parse_term()

            node = self.node("expression", [
                node,
                self.node("ARITH_OP", value=op.value),
                right
            ])

        return node

    def parse_term(self):
        factor_node = self.parse_factor()
        node = self.node("term", [factor_node])

        while self.peek().type == "ARITH_OP" and self.peek().value in ("*", "/"):
            op = self.peek()
            self.advance()
            right = self.parse_factor()

            node = self.node("term", [
                node,
                self.node("ARITH_OP", value=op.value),
                right
            ])

        return node

    def parse_factor(self):
        token = self.peek()

        if token.type == "NUMBER":
            self.advance()
            return self.node("factor", [
                self.node("number", value=token.value)
            ])

        elif token.type == "IDENTIFIER":
            self.advance()
            return self.node("factor", [
                self.node("identifier", value=token.value)
            ])

        elif token.type == "STRING":
            self.advance()
            return self.node("factor", [
                self.node("string", value=token.value)
            ])

        elif token.type == "LPAREN":
            self.advance()
            expr = self.parse_expression()
            self.match("RPAREN")

            return self.node("factor", [
                self.node("LPAREN", value="("),
                expr,
                self.node("RPAREN", value=")")
            ])

        elif token.type == "ARITH_OP":
            self.error("Operator cannot appear without operand")

        elif token.type == "UNKNOWN":
            self.error(f"Invalid symbol '{token.value}'")

        else:
            self.error("Invalid factor (expected number, identifier, or expression)")

    # ----------------------------
    # Condition
    # ----------------------------
    def parse_condition(self):
        left = self.parse_expression()

        if self.peek().type != "REL_OP":
            self.error("Expected relational operator")

        op = self.match("REL_OP")

        right = self.parse_expression()

        return self.node("condition", [
            left,
            self.node("REL_OP", value=op.value),
            right
        ])