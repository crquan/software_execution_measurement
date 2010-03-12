#/usr/bin/python

import sys
from pycparser import c_parser, c_ast, parse_file

class IDVisitor(c_ast.NodeVisitor):
    def __init__(self, text):
        c_ast.NodeVisitor.__init__(self)
        self._ID_list = []
        self._parser = c_parser.CParser()
        self._ast = self._parser.parse(text, filename='<none>')
        self.visit(self._ast)

    def visit_ID(self, node):
        if node.name not in self._ID_list:
            self._ID_list.append(node.name)

    def get_ID_list(self):
        return self._ID_list


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        exit(0)

    content = "".join(file(filename).readlines())
    idv = IDVisitor(content)
    ans = idv.get_ID_list()

    for i in ans:
        print i
