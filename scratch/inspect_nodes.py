import tree_sitter_language_pack
from tree_sitter import Parser

def count_nodes(path: str):
    lang_pkg = tree_sitter_language_pack.get_language("python")
    parser = Parser(lang_pkg)
    with open(path, 'r') as f: code = f.read()
    tree = parser.parse(code.encode('utf8'))
    
    logic_types = (
        "assignment", "augmented_assignment", "binary_expression", "boolean_expression", 
        "comparison_operator", "call", "subscript", "if_statement", "for_statement", 
        "while_statement", "return_statement", "yield", "raise_statement", "unary_operator"
    )
    boilerplate_types = (
        "class_definition", "function_definition", "parameters", "block", "module",
        "comment", "string", "try_statement", "except_clause", "finally_clause", "pass_statement",
        "decorator", "expression_statement"
    )
    
    counts = {"logic": 0, "boilerplate": 0, "other": {}}
    
    def walk(n):
        if n.type in logic_types: counts["logic"] += 1
        elif n.type in boilerplate_types: counts["boilerplate"] += 1
        else:
            counts["other"][n.type] = counts["other"].get(n.type, 0) + 1
        for c in n.children:
            walk(c)
            
    walk(tree.root_node)
    print(f"Logic: {counts['logic']}")
    print(f"Boilerplate: {counts['boilerplate']}")
    print("Other types found:")
    for k, v in sorted(counts["other"].items()):
        if v > 2: print(f" - {k}: {v}")

count_nodes("temp_test_slop.py")
