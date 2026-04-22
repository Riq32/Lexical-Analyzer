class CSTNode:
    def __init__(self, name, children=None, value=None):
        self.name = name
        self.children = children if children else []
        self.value = value

    def __repr__(self, level=0):
        indent = "  " * level

        if self.value is not None:
            result = f"{indent}<{self.name}> → {self.value}\n"
        else:
            result = f"{indent}<{self.name}>\n"

        for child in self.children:
            result += child.__repr__(level + 1)

        return result