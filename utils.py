
from pycparser import c_ast, c_lexer, c_parser, parse_file
from pycparser.plyparser import Coord

def split_codeblocks(blocks):
    ast = parse_blocks(blocks)
    return _recursive_show_code_blocks_2(ast)

def split_statements(statements):
    pass

def _is_a_branch(node):
    return isinstance(node, (
        c_ast.Break, c_ast.Case, c_ast.Continue, c_ast.Default,
        c_ast.DoWhile, c_ast.For, c_ast.FuncCall, c_ast.Goto,
        c_ast.If, c_ast.Switch, c_ast.TernaryOp, c_ast.While))

def _recursive_show_code_blocks_2(ast):
    all_nodes = []
    CompoundCloseMarker = object()

    def _recursive_collect_nodes(node):
        all_nodes.append(node)
        if isinstance(node, (c_ast.Decl,
                          c_ast.Assignment,
                          c_ast.FuncCall)):
            all_nodes.append(node)
            return
        if isinstance(node, (c_ast.Compound,)):
            for child in node.children():
                _recursive_collect_nodes(child)
            all_nodes.append(CompoundCloseMarker) # an end compound marker
        else:
            for child in node.children():
                _recursive_collect_nodes(child)

    _recursive_collect_nodes(ast)
    # print all_nodes

    begin, end = 0, 0
    for i in range(len(all_nodes)):
        if isinstance(all_nodes[i], c_ast.Compound):
            begin = i+1
        if _is_a_branch(all_nodes[i]) or all_nodes[i] is CompoundCloseMarker:
            end = i-1
            if begin != end and not isinstance(all_nodes[begin], c_ast.FuncCall):
                print map(lambda node: str(getattr(node, 'coord', None)),
                          (all_nodes[begin], all_nodes[end]))
            begin = end = i+1

