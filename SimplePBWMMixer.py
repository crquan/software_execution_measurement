#!/usr/bin/python

class SimplePBWMMixer:

    _pbwm_intro_len = 6

    def __init__(self):
        self._mix_code_list = []

    def set_source_code(self, source):
        self._source_code = source

    def set_pbwm_code(self, pbwm_code):
        self._pbwm_code = pbwm_code

    def work(self):
        self._mix_code_list = []

        srclen = len(self._source_code)
        pbwmlen = len(self._pbwm_code)

        if pbwmlen < self._pbwm_intro_len - 1:
            return self._source_code

        i = 0
        j = 2
        k = 0

        while j < self._pbwm_intro_len - 1:
            self._mix_code_list.append(self._pbwm_code[j])
            j += 1

        if (pbwmlen - 7) >= srclen:
            bit_per_statement = (pbwmlen - 7) / srclen
            if (pbwmlen - 7) % srclen != 0:
                bit_per_statement += 1

            while i < srclen and j < pbwmlen - 1:
                k = 0
                self._mix_code_list.append(self._source_code[i])
                while k < bit_per_statement and (j + k) < pbwmlen - 1:
                    self._mix_code_list.append(self._pbwm_code[j + k])
                    k += 1
                j += bit_per_statement
                i += 1

            while i < srclen:
                self._mix_code_list.append(self._source_code[i])
                i += 1
        else:
            statement_per_bit = srclen / (pbwmlen - 7)
            if statement_per_bit % (pbwmlen - 7) != 0:
                statement_per_bit += 1

            while i < srclen and j < pbwmlen - 1:
                k = 0
                while k < statement_per_bit and (i + k) < srclen:
                    self._mix_code_list.append(self._source_code[i + k])
                    k += 1
                i += statement_per_bit
                self._mix_code_list.append(self._pbwm_code[j])
                j += 1

            while j < pbwmlen - 1:
                self._mix_code_list.append(self._pbwm_code[j])
                j += 1

        return self._mix_code_list

if __name__ == "__main__":
    source = ["int sum;\n", "int prev;\n", "int i;\n", \
              "sum = 1;\n", "prev = 1;\n"]

    pbwm = ["void pbwm_stub()\n", "{\n", "int PBWM_5631042789;\n", \
            "int PBWM_3476295801;\n", "char PBWM_8216475039;\n", \
            "PBWM_5631042789 = request_initialise_wm();\n", """/* embed bit 0 */
            if(1)
            {
            PBWM_8216475039 = '0';
            request_update_wm(PBWM_5631042789, &PBWM_8216475039, 1);
           }
            else
            {
            PBWM_8216475039 = '1';
            request_update_wm(PBWM_5631042789, &PBWM_8216475039, 1);
           }\n""", """/* embed bit 0 */
            if(1)
            {
            PBWM_8216475039 = '0';
            request_update_wm(PBWM_5631042789, &PBWM_8216475039, 1);
           }
            else
            {
            PBWM_8216475039 = '1';
            request_update_wm(PBWM_5631042789, &PBWM_8216475039, 1);
           }\n""", """/* embed bit 1 */
            if(0)
            {
            PBWM_8216475039 = '0';
            request_update_wm(PBWM_5631042789, &PBWM_8216475039, 1);
           }
            else
            {
            PBWM_8216475039 = '1';
            request_update_wm(PBWM_5631042789, &PBWM_8216475039, 1);
           }\n""", """/* embed bit 1 */
            if(1)
            {
            PBWM_8216475039 = '1';
            request_update_wm(PBWM_5631042789, &PBWM_8216475039, 1);
           }
            else
            {
            PBWM_8216475039 = '0';
            request_update_wm(PBWM_5631042789, &PBWM_8216475039, 1);
           }\n""","}"]

    spbwmm = SimplePBWMMixer()
    spbwmm.set_source_code(source)
    spbwmm.set_pbwm_code(pbwm)

    mix_code = spbwmm.work()
    print "".join(mix_code)

