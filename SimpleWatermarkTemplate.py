#/usr/bin/python

import random

class SimpleWatermarkTemplate:

    def __init__(self):
        self._code_list = []
        random.seed()
        self._namesource = "0123456789"
        self._val_name = "WM_" + "".join(random.sample(self._namesource, 10))

    def get_template(self, length):
        if length <= 0:
            return [[],""] 

        full_code_header = []
        full_code_header.append("\n")
        full_code_header.append("int stub()\n")
        full_code_header.append("{\n")
        
        full_code_footer = []
        full_code_footer.append("printf(\"%d\\n\"," + self._val_name + ");\n")
        full_code_footer.append("return " + self._val_name + ";\n")
        full_code_footer.append("}\n")

        for code in full_code_header:
            self._code_list.append(code)

        self._code_list.append("int " + self._val_name + " = 0;\n")
        length -= 1
        
        i = 0
        while i < length:
            self._code_list.append(self._val_name + " += " + str(i + 1) + ";\n")
            i += 1

        for code in full_code_footer:
            self._code_list.append(code)

        full_code = "".join(self._code_list) 

        return [self._code_list, full_code, ["%d", self._val_name]]

if __name__ == "__main__":
    swt = SimpleWatermarkTemplate()
    [codelist, fullcode] = swt.get_template(5)
    
    for line in codelist:
        print line

    print
    print fullcode
