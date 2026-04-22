import tree_sitter_python
from tree_sitter import Parser

code = b"""
class Test:
    \"\"\"
    A holistic, AI-driven paradigm.
    \"\"\"
    pass
"""

parser = Parser(tree_sitter_python.language())
tree = parser.parse(code)

def walk(n):
    print(f"Node: {n.type}, Text: {n.text[:20]}...")
    for c in n.children: walk(c)

walk(tree.root_node)
