#!/usr/bin/python

# here source code block means blocks without branches

import sys

from pycparser import c_ast, c_lexer, c_parser, parse_file
from pycparser.plyparser import Coord

class CodeBlocksVisitor(c_ast.NodeVisitor):
    """ Code Blocks without branches visitor """

    def __init__(self, text):
        self._codeblocks = []
        self._last_coord = None
        self._last_node = None
        self._last_non_branch = []
        self._all_nodes = []
        self._parser = c_parser.CParser()
        self._ast = self._parser.parse(text, filename='<none>')
        self._recursive_show_code_blocks_2(self._ast)

    def _recursive_collect_nodes(self, node):
        if type(node) in (c_ast.Decl, c_ast.Assignment):
            self._all_nodes.append(node)
            return
        if self._judge_branch(node) or type(node) in (c_ast.Compound,):
            self._all_nodes.append(node)
            for child in node.children():
                self._recursive_collect_nodes(child)
            self._all_nodes.append(None) # an end compound marker
        else:
            for child in node.children():
                self._recursive_collect_nodes(child)

    def _recursive_show_code_blocks_2(self, ast):

        self._all_nodes.append(ast)
        self._recursive_collect_nodes(ast)

        begin, end = 0, 0
        for i in range(len(self._all_nodes)):
            if isinstance(self._all_nodes[i], c_ast.Compound):
                begin = i+1
            if self._judge_branch(self._all_nodes[i]) or self._all_nodes[i] is None:
                end = i-1
                if begin <= end:
                    loc_info = map(lambda node: str(node.coord), (self._all_nodes[begin], self._all_nodes[end]))
                    node_info = []
                    j = begin
                    while j <= end:
                        node_info.append(self._all_nodes[j])
                        j += 1

                    self._codeblocks.append([loc_info, node_info])
                begin = end = i+1

    def _judge_branch(self, node):
        return type(node) in (
            c_ast.Break, c_ast.Case, c_ast.Continue, c_ast.Default,
            c_ast.DoWhile, c_ast.For, c_ast.FuncCall, c_ast.Goto,
            c_ast.If, c_ast.Switch, c_ast.TernaryOp, c_ast.While,
            c_ast.Label, c_ast.Return)

    def show_code_blocks(self):
        for block in self._codeblocks:
            print block

    def get_code_blocks(self):
        blk_list = []
        for block in self._codeblocks:
            blk_list.append([[int((block[0][0].split(':'))[1]), \
                             int((block[0][1].split(':'))[1])], block[1]])
        return blk_list

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage: %s source-file-name.c\n" \
            % sys.argv[0]
        sys.exit(1)
    
    code = "".join(file(sys.argv[1]).readlines())

    cbv = CodeBlocksVisitor(code)
    
    cbv.show_code_blocks()
    print
    block_list = cbv.get_code_blocks()
    for block in block_list:
        print block
