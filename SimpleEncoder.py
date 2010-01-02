#/usr/bin/python

from pycparser import c_parser, c_ast
import re

class SimpleEncoder:

    def __init__(self, code_list):
        self._code_list = code_list
        self._new_code = []

    def _check_encodable(self, symbol1, symbol2):
        if ((symbol1[0] == 'S' and symbol2[0] == 'W') or \
           (symbol1[0] == 'W' and symbol2[0] == 'S')) and \
           (type(symbol1[1][1]) != c_ast.Decl and \
           type(symbol2[1][1]) != c_ast.Decl):
            return True
        else:
            return False

    def _assignment_type_test(self, lvalue, rvalue):
        lvalue_re = re.compile('\b'+lvalue+'\b')
        ans = lvalue_re.match(rvalue)
        if ans != None:
            return 0
        else:
            return 1

    def _get_value(self, node):
        if type(node) == c_ast.ID:
            return node.name
        elif type(node) == c_ast.Constant:
            return node.value
        elif type(node) == c_ast.BinaryOp:
            str = self._get_value(node.left)
            str += node.op
            str += self._get_value(node.right)
            return str
        else:
            print "Unhandled type " + str(type(node))
            return None

    def _execute_encode(self, code1, code2):
        tmp_code = []

        y1 = self._get_value(code1[1].lvalue)
        y2 = self._get_value(code2[1].lvalue)

        r1 = '(' + self._get_value(code1[1].rvalue) + ')'
        r2 = '(' + self._get_value(code2[1].rvalue) + ')'

        if cmp(code1[1].op, "=") != 0:
            r1 = '(' + y1 + code1[1].op[0] + r1 + ')'

        if cmp(code2[1].op, "=") != 0:
            r2 = '(' + y2 + code2[1].op[0] + r2 + ')'

        tmp_code.append(y1 + ' = ' + r1 + ' + ' + r2 + ';\n')
        if self._assignment_type_test(y1, r1) == 1:
            tmp_code.append(y2 + ' = ' + y1 + ' - 2 * ' + r2 + ';\n')
        else:
            tmp_code.append(y2 + ' = ' + y1 + ' - ' + r2 + ';\n')
        tmp_code.append(y1 + ' = (' + y1 + ' + ' + y2 + ')/2;\n')
        tmp_code.append(y2 + ' = ' + y1 + ' - ' + y2 + ';\n')

        return tmp_code


    def encode(self):
        self._new_code = []

        i = 0
        limit = len(self._code_list)

        while i  < (limit - 1):
            if self._check_encodable(self._code_list[i], \
                                     self._code_list[i + 1]):
                tmp_code = self._execute_encode(self._code_list[i][1], \
                                                self._code_list[i + 1][1])
                for line in tmp_code:
                    self._new_code.append(line)

                i += 2
            else:
                self._new_code.append(self._code_list[i][1][0])
                i += 1

        self._new_code.append(self._code_list[i][1][0])

        return self._new_code

#if __name__ == "__main__":
#    code_list = [['S', 'i = 1;'],\
#                 ['W', 'j = 1;'],\
#                 ['S', 'i = 2;'],\
#                 ['W', 'j = 2;'],\
#                 ['S', 'i = 3;'],\
#                 ['W', 'j = 3;'],\
#                 ['S', 'i = 4;'],\
#                 ['W', 'j = 4;'],\
#                 ['S', 'i = 5;'],\
#                 ['S', 'i = 6;']]
#    se = SimpleEncoder(code_list)
#    ans = se.encode()
#
#    for i in ans:
#        print i
