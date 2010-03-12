#!/usr/bin/python

"""
This file is in charge of generating the path based watermark template
"""

import random

class SimplePBWMTemplate:
    
    _predicate_list = \
                    [
                        ["1", 0],\
                        ["0", 1]
                    ]

    def __init__(self):
        self._code_list = []
        random.seed()
        self._namesource = "0123456789"
        
        self._wmid_name = "PBWM_" + "".join(random.sample(self._namesource, 10)) 
        
        self._wmval_name = "PBWM_" + "".join(random.sample(self._namesource, 10))
        while(self._wmval_name == self._wmid_name):
            self._wmval_name = "PBWM_" + "".join(random.sample(self._namesource, 10))

        self._wmbuf_name = "PBWM_" + "".join(random.sample(self._namesource, 10))
        while(self._wmbuf_name == self._wmid_name or \
              self._wmbuf_name == self._wmval_name):
            self._wmbuf_name = "PBWM_" + "".join(random.sample(self._namesource, 10))

    def _negate_bit(self, bit):
        if bit == '0':
            return '1'
        elif bit == '1':
            return '0'
        else:
            return 'X'

    def get_template(self, bitstr):
        """
            bitstr: bit string to be embedded
        """
        length = len(bitstr)
        if length <= 0:
            return [[],""] 

        full_code_header = []
        full_code_header.append("void pbwm_stub()\n")
        full_code_header.append("{\n")
        
        full_code_footer = []
        full_code_footer.append("}\n")

        self._code_list.extend(full_code_header)
        
        self._code_list.append("int " + self._wmid_name + ";\n");
        self._code_list.append("int " + self._wmval_name + ";\n");
        self._code_list.append("char " + self._wmbuf_name + ";\n");

        self._code_list.append(self._wmid_name + " = request_initialise_wm();\n\n");

        i = 0
        while i < length:
            predicate_str = "/* embed bit " + bitstr[i] + " */\n"
            predicate_choice = random.randrange(len(self._predicate_list))
            predicate_str += "if(" + self._predicate_list[predicate_choice][0] \
                            + ")\n" + "{\n"
            if self._predicate_list[predicate_choice][1] == 0:
                predicate_str += self._wmbuf_name + " = \'" + bitstr[i] + "\';\n"
            elif self._predicate_list[predicate_choice][1] == 1:
                predicate_str += self._wmbuf_name + " = \'" + \
                                 self._negate_bit(bitstr[i]) + "\';\n"
            else:
                pass
            predicate_str += "request_update_wm(" + self._wmid_name + ", &" + \
                             self._wmbuf_name + ", 1);\n"
            predicate_str += "}\nelse\n{\n"
            if self._predicate_list[predicate_choice][1] == 0:
                predicate_str += self._wmbuf_name + " = \'" + \
                                 self._negate_bit(bitstr[i]) + "\';\n"
            elif self._predicate_list[predicate_choice][1] == 1:
                predicate_str += self._wmbuf_name + " = \'" + bitstr[i] + "\';\n"
            else:
                pass
            predicate_str += "request_update_wm(" + self._wmid_name + ", &" + \
                             self._wmbuf_name + ", 1);\n"
            predicate_str += "}\n\n"

            self._code_list.append(predicate_str)

            i += 1

        self._code_list.append("request_retrieval_wm(" + self._wmid_name + 
                               ", &" + self._wmval_name + ");\n")
        self._code_list.append("printf(\"Next block's ID is %d\\n\", " + 
                               self._wmval_name + ");\n")
        self._code_list.append("request_release_wm(" + self._wmid_name + ");\n")

        self._code_list.extend(full_code_footer)
    
        fullcode = "".join(self._code_list)

        return [self._code_list, fullcode]

if __name__ == "__main__":
    spbwmt = SimplePBWMTemplate()
    [codelist, fullcode] = spbwmt.get_template("001011101001")
    for line in codelist:
        print line

    print
    print fullcode
