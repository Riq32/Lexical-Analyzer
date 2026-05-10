"""
=============================================================
  MiniLang Intermediate Code Generator (ICG)
  Representation: Three-Address Code using Quadruples
  Format: (operator, arg1, arg2, result)
=============================================================

Quadruple format:
  Each instruction is a tuple: (op, arg1, arg2, result)

  Examples:
    (=, 10, _, x)          — assignment
    (+, x, 1, t1)          — arithmetic
    (>, x, y, t2)          — relational comparison
    (if_false, t2, _, L1)  — conditional jump
    (goto, _, _, L2)       — unconditional jump
    (label, _, _, L1)      — label marker
    (print, x, _, _)       — print statement
"""

from cst_node import CSTNode


class ICGenerator:
    """Walks the Concrete Syntax Tree and emits Three-Address Code (quadruples)."""

    def __init__(self):
        self.quads = []          # list of (op, arg1, arg2, result)
        self.temp_count = 0      # counter for temporary variables  t1, t2, ...
        self.label_count = 0     # counter for labels  L0, L1, ...

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def emit(self, op, arg1="_", arg2="_", result="_"):
        """Append one quadruple to the list."""
        self.quads.append((op, str(arg1), str(arg2), str(result)))

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------
    def generate(self, tree):
        """Generate intermediate code from a CST root node."""
        self.visit(tree)
        return self.quads

    # ------------------------------------------------------------------
    # Dispatcher
    # ------------------------------------------------------------------
    def visit(self, node):
        if node is None:
            return None

        method_name = f"visit_{node.name}"
        visitor = getattr(self, method_name, None)

        if visitor:
            return visitor(node)

        # For nodes that simply wrap children, visit children
        for child in node.children:
            self.visit(child)

        return node.value

    # ------------------------------------------------------------------
    # Program & Statement List
    # ------------------------------------------------------------------
    def visit_program(self, node):
        for child in node.children:
            self.visit(child)

    def visit_statement_list(self, node):
        for child in node.children:
            self.visit(child)

    # ------------------------------------------------------------------
    # Assignment:  identifier = expression ;
    # ------------------------------------------------------------------
    def visit_assignment(self, node):
        # children: [identifier, ASSIGN, expression, SEMICOLON]
        target = node.children[0].value        # variable name
        expr_result = self.visit(node.children[2])  # evaluate RHS expression
        self.emit("=", expr_result, "_", target)

    # ------------------------------------------------------------------
    # If Statement:  if (condition) { statement_list }
    # ------------------------------------------------------------------
    def visit_if_statement(self, node):
        # children: [KEYWORD("if"), condition, statement_list]
        cond_result = self.visit(node.children[1])

        label_end = self.new_label()

        self.emit("if_false", cond_result, "_", label_end)

        # body
        self.visit(node.children[2])

        self.emit("label", "_", "_", label_end)

    # ------------------------------------------------------------------
    # While Statement:  while (condition) { statement_list }
    # ------------------------------------------------------------------
    def visit_while_statement(self, node):
        # children: [KEYWORD("while"), condition, statement_list]
        label_start = self.new_label()
        label_end = self.new_label()

        self.emit("label", "_", "_", label_start)

        cond_result = self.visit(node.children[1])
        self.emit("if_false", cond_result, "_", label_end)

        # body
        self.visit(node.children[2])

        self.emit("goto", "_", "_", label_start)
        self.emit("label", "_", "_", label_end)

    # ------------------------------------------------------------------
    # Print Statement:  print(expression)
    # ------------------------------------------------------------------
    def visit_print_statement(self, node):
        # children: [KEYWORD("print"), expression]
        expr_result = self.visit(node.children[1])
        self.emit("print", expr_result, "_", "_")

    # ------------------------------------------------------------------
    # Condition:  expression REL_OP expression
    # ------------------------------------------------------------------
    def visit_condition(self, node):
        # children: [expression, REL_OP, expression]
        left = self.visit(node.children[0])
        op = node.children[1].value
        right = self.visit(node.children[2])

        temp = self.new_temp()
        self.emit(op, left, right, temp)
        return temp

    # ------------------------------------------------------------------
    # Expression:  term ((+|-) term)*
    # ------------------------------------------------------------------
    def visit_expression(self, node):
        if len(node.children) == 1:
            return self.visit(node.children[0])

        # Binary: [left_expr, ARITH_OP, right_term]
        if len(node.children) == 3 and node.children[1].name == "ARITH_OP":
            left = self.visit(node.children[0])
            op = node.children[1].value
            right = self.visit(node.children[2])
            temp = self.new_temp()
            self.emit(op, left, right, temp)
            return temp

        # Fallback: visit all children
        result = None
        for child in node.children:
            result = self.visit(child)
        return result

    # ------------------------------------------------------------------
    # Term:  factor ((*|/) factor)*
    # ------------------------------------------------------------------
    def visit_term(self, node):
        if len(node.children) == 1:
            return self.visit(node.children[0])

        # Binary: [left_term, ARITH_OP, right_factor]
        if len(node.children) == 3 and node.children[1].name == "ARITH_OP":
            left = self.visit(node.children[0])
            op = node.children[1].value
            right = self.visit(node.children[2])
            temp = self.new_temp()
            self.emit(op, left, right, temp)
            return temp

        result = None
        for child in node.children:
            result = self.visit(child)
        return result

    # ------------------------------------------------------------------
    # Factor:  number | identifier | string | (expression)
    # ------------------------------------------------------------------
    def visit_factor(self, node):
        if len(node.children) == 1:
            child = node.children[0]
            if child.name in ("number", "identifier", "string"):
                return child.value
        # Parenthesized expression: (LPAREN, expression, RPAREN)
        if len(node.children) == 3 and node.children[0].name == "LPAREN":
            return self.visit(node.children[1])

        return self.visit(node.children[0])

    # ------------------------------------------------------------------
    # Leaf nodes
    # ------------------------------------------------------------------
    def visit_number(self, node):
        return node.value

    def visit_identifier(self, node):
        return node.value

    def visit_string(self, node):
        return node.value

    # ------------------------------------------------------------------
    # Output formatting
    # ------------------------------------------------------------------
    def print_quads(self):
        """Print quadruples in a formatted table."""
        W = 66
        print("=" * W)
        print("  INTERMEDIATE CODE — THREE-ADDRESS CODE (QUADRUPLES)")
        print("=" * W)
        print(f"  {'#':>4}  {'Operator':<12} {'Arg1':<12} {'Arg2':<12} {'Result':<12}")
        print("-" * W)

        for i, (op, a1, a2, res) in enumerate(self.quads):
            print(f"  {i:>4}  {op:<12} {a1:<12} {a2:<12} {res:<12}")

        print("=" * W)
        print(f"  Total quadruples: {len(self.quads)}")
        print("=" * W)