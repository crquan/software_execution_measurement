
import re, random

class SimplePointerAliasing:

    # this regular can now only match a simple assignment statement;
    #
    _regular_line = re.compile(r'[A-Za-z_][A-Za-z0-9_]+(.*)=(.*);$')

    def __init__(self):
        self._mix_code_list = []

    def set_source_code(self, source):
        self._source_code = source

    def set_pbwm_code(self, pbwm_code):
        self._pbwm_code = pbwm_code

    # keep new added watermark code between 30% of the original
    # to 130%, a moderate ratio of original code
    def work(self, ):
        self._mix_code_list = []

        srclen = len(self._source_code)
        pbwmlen = len(self._pbwm_code)

        internal_stacks = []
        internal_names = []

        for line in self._source_code:
            print line.strip()
            result = re.match(r"([A-Za-z_][A-Za-z0-9_]*) +([A-Za-z_][A-Za-z0-9_]*) = (.*);",
                        line.strip())
            if result:
                print result.groups()
                internal_names.append(result.group(2))
                self._mix_code_list.append(line)

            # empty lines
            if re.match(r"^$",
                        line.strip()):
                print "empty lines split data definition and statements"
                _wm_lines = []
                for i in range(len(internal_names)):
                    _wm_lines.append(("wm_pointer[%d] = &(%s);" % (i, internal_names[i])))
                self._mix_code_list.append("\n".join(_wm_lines))
                self._mix_code_list.append("\n")

            # Reference lines:
            # changed the right value into (pointer alias + original value) / 2 style
            if re.match(r"([A-Za-z_][A-Za-z0-9_]+) ([A-Za-z_][A-Za-z0-9_]) = (.*);",
                        line.strip()):
                self._mix_code_list.append(line)

        prepend_line = "int *wm_pointer[%d];" % (len(internal_names),)
        self._mix_code_list.insert(0, prepend_line)
        return self._mix_code_list


if __name__ == "__main__":
    source = ["uint32_t A = ctx->A;",
              "uint32_t B = ctx->B;",
              "uint32_t C = ctx->C;",
              "uint32_t D = ctx->D;",
              "",
              "uint32_t A_save = A;",
              "uint32_t B_save = B;",
              "uint32_t C_save = C;",
              "uint32_t D_save = D;",
             ]

    pbwm = ["int *wm_pointer[];",
            "wm_pointer[0]=&SOURCE;",
            "DEST=(*wm_pointer[0]+SOURCE)/2)"]

    sppawmm = SimplePointerAliasing()
    sppawmm.set_source_code(source)
    sppawmm.set_pbwm_code(pbwm)

    mix_code = sppawmm.work()
    print "\nThe output Program:\n\n", "\n".join(mix_code)

