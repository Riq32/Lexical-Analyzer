from node import Node


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # Utility functions
    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def match(self, expected_type):
        token = self.peek()
        if token.type == expected_type:
            self.advance()
            return token
        else:
            self.error(f"Expected {expected_type}, found {token.type}")

    def error(self, message):
        token = self.peek()
        raise Exception(f"[Syntax Error] Line {token.line}, Col {token.column}: {message}")

    # Grammar Implementation
    # ----------------------------

    # <program> ::= <statement_list>  OR { <statement_list> }
    def parse_program(self):
        # Handle program wrapped in { }
        if self.peek().type == "LBRACE":
            self.match("LBRACE")
            stmt_list = self.parse_statement_list()
            self.match("RBRACE")
            return Node("Program", [stmt_list])

        # Fallback (no braces)
        return Node("Program", [self.parse_statement_list()])

    # <statement_list>
    def parse_statement_list(self):
        statements = []

        while self.peek().type != "EOF" and self.peek().type != "RBRACE":
            statements.append(self.parse_statement())

        return Node("StatementList", statements)

    # <statement>
    def parse_statement(self):
        token = self.peek()

        if token.type == "KEYWORD":
            if token.value == "if":
                return self.parse_if()
            elif token.value == "while":
                return self.parse_while()
            elif token.value == "print":
                return self.parse_print()

        elif token.type == "IDENTIFIER":
            return self.parse_assignment()

        else:
            self.error("Invalid statement")

    # <assignment> ::= identifier = expression ;
    def parse_assignment(self):
        id_tok = self.match("IDENTIFIER")
        self.match("ASSIGN")
        expr = self.parse_expression()
        self.match("SEMICOLON")

        return Node("Assignment", [
            Node("Identifier", value=id_tok.value),
            expr
        ])

    # <if_statement>
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

        return Node("If", [cond, stmts])

    # <while_statement>
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

        return Node("While", [cond, stmts])

    # <print_statement>
    def parse_print(self):
        token = self.peek()
        if token.value != "print":
            self.error("Expected 'print'")
        self.advance()

        self.match("LPAREN")
        expr = self.parse_expression()
        self.match("RPAREN")
        self.match("SEMICOLON")

        return Node("Print", [expr])

    # ----------------------------
    # Expressions (NO left recursion)
    # ----------------------------

    def parse_expression(self):
        node = self.parse_term()

        while self.peek().type == "ARITH_OP" and self.peek().value in ("+", "-"):
            op = self.peek()
            self.advance()
            right = self.parse_term()
            node = Node("BinOp", [node, right], op.value)

        return node

    def parse_term(self):
        node = self.parse_factor()

        while self.peek().type == "ARITH_OP" and self.peek().value in ("*", "/"):
            op = self.peek()
            self.advance()
            right = self.parse_factor()
            node = Node("BinOp", [node, right], op.value)

        return node

    def parse_factor(self):
        token = self.peek()

        if token.type == "NUMBER":
            self.advance()
            return Node("Number", value=token.value)

        elif token.type == "IDENTIFIER":
            self.advance()
            return Node("Identifier", value=token.value)

        # ✅ FIX ADDED: STRING support
        elif token.type == "STRING":
            self.advance()
            return Node("String", value=token.value)

        elif token.type == "LPAREN":
            self.advance()
            node = self.parse_expression()
            self.match("RPAREN")
            return node

        else:
            self.error("Invalid factor")

    # <condition>
    def parse_condition(self):
        left = self.parse_expression()

        if self.peek().type == "REL_OP":
            op = self.peek()
            self.advance()
        else:
            self.error("Expected relational operator")

        right = self.parse_expression()

        return Node("Condition", [left, right], op.value)