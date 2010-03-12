#/usr/bin/python

import sys, os
from CodeBlocksVisitor import CodeBlocksVisitor
from SimpleWatermarkTemplate import SimpleWatermarkTemplate
from SimpleMixer import SimpleMixer
from SimpleEncoder import SimpleEncoder

class Main:
    """
        main
    """
    _WM2_HEADER = \
    ["""
        extern int request_initialise_wm();
        extern int request_update_wm(int, char *, int);
        extern int request_retrieval_wm(int, int *);
        extern int request_release_wm(int);
    """]

    def __init__(self, code_lines):
        self._origin_code_lists = code_lines

    def _block_list_extend(self, info, code_list):
        new_list = []

        for info_i in info:
            start = info_i[0][0] - 1
            end = info_i[0][1] - 1

            tmp_list = []

            i = start
            j = 0
            while i <= end:
                if cmp(code_list[i].replace("\n", ""), "") != 0:
                    tmp_list.append([code_list[i], info_i[1][j]])
                    j += 1
                i += 1

            new_list.append(tmp_list)

        return new_list

    def _merge_blocks(self, org_code_list, org_block_info, encode_block_list):
        merged_blocks = []

        i = 0
        j = 0
        for block_info in org_block_info:
            while i < block_info[0][0] - 1:
                merged_blocks.append(org_code_list[i])
                i += 1
            for line in encode_block_list[j]:
                merged_blocks.append(line)
            i = block_info[0][1]
            j += 1

        while i < len(org_code_list):
            merged_blocks.append(org_code_list[i])
            i += 1

        return merged_blocks

    def run(self):
        origin_text = "".join(self._origin_code_lists)
        origin_cbv = CodeBlocksVisitor(origin_text)
        origin_block_list_info = origin_cbv.get_code_blocks()
        origin_block_list = self._block_list_extend(origin_block_list_info, \
                                                    self._origin_code_lists)

        print "Origin code blocks"
        for block in origin_block_list:
            print block
        print

        i = 0
        encode_block_list = []
        for block in origin_block_list:
            print "Dealing with block " + str(i)
            i += 1

            wm_generator = SimpleWatermarkTemplate()
            [wm_code_lists, wm_text, wm_info] = wm_generator.get_template(len(block))

            print "The watermark code is:"
            print wm_text

            wm_cbv = CodeBlocksVisitor(wm_text)
            wm_block_list_info = wm_cbv.get_code_blocks()
            wm_block_list = self._block_list_extend(wm_block_list_info, \
                                                    wm_code_lists)

            print "Watermark code blocks"
            for wmblock in wm_block_list:
                print wmblock
            print

            mixer = SimpleMixer()
            mixer.set_source_code(block)
            mixer.set_watermark_code(wm_block_list[0])
            mixcode = mixer.work()
            output_str = "printf(\"\\n %s = %s \\n\", %s);\n" % \
                         (wm_info[1], wm_info[0], wm_info[1])
            mixcode.append(['', [output_str, '']])

            tmp_code = []
            for code in mixcode:
                tmp_code.append(code[1][0])
            print "Mixed code is"
            print "".join(tmp_code)
            print

            encoder = SimpleEncoder(mixcode)
            encoded_code_list = encoder.encode()
            
            print "Encoded code is"
            print "".join(encoded_code_list)
            print

            encode_block_list.append(encoded_code_list)
        
        new_code = self._WM2_HEADER + self._merge_blocks(self._origin_code_lists, \
                                      origin_block_list_info, \
                                      encode_block_list)

        return new_code
     



if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit(0)
    
    filename = sys.argv[1]

    lines = file(filename).readlines()

    main = Main(lines)
    nc = main.run()
    print "".join(nc)

    dst = file("wm_" + filename, "w")
    dst.write("".join(nc))
    dst.close()

    os.popen("indent " + "wm_" + filename)

