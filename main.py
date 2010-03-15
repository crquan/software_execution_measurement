#/usr/bin/python

import sys, os, random, math
from CodeBlocksVisitor import CodeBlocksVisitor
from SimpleWatermarkTemplate import SimpleWatermarkTemplate
from SimpleMixer import SimpleMixer
from SimpleEncoder import SimpleEncoder
from SimplePBWMMixer import SimplePBWMMixer
from SimplePBWMTemplate import SimplePBWMTemplate

class Main:
    """
        main
    """
    _PBWM_HEADER = \
    ["""
        /* Path-based watermark library functions declaration begin */
        extern int request_initialise_wm();
        extern int request_update_wm(int, char *, int);
        extern int request_retrieval_wm(int, int *);
        extern int request_release_wm(int);
        /* Path-based watermark library functions declaration end */
    """]

    def __init__(self, code_lines):
        self._origin_code_lists = code_lines
        random.seed()

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

    def _encoding_block_id(self, id_list):
        '''
        Encode the block id into binary strings with specific length. Unused bits are 
        padded with '0's
        '''
        max_id = max(id_list)
        min_bitstring_length = int(math.ceil(math.log(max_id) / math.log(2)))
        print "Minimal Bit String Length is %d, please give your preferred value:" % (min_bitstring_length,)
        bitstring_length = int(raw_input()) 
        while bitstring_length < min_bitstring_length:
            bitstring_length = int(raw_input()) 

        encoded_list = []
        for id in id_list:
            id_string = ["0" for i in range(bitstring_length)]
            i = bitstring_length - 1
            while id != 0:
                if id % 2 == 1:
                    id_string[i] = '1'
                i -= 1
                id /= 2
            encoded_list.append("".join(id_string))

        return encoded_list

    def run(self):
        origin_text = "".join(self._origin_code_lists)
        origin_cbv = CodeBlocksVisitor(origin_text)
        origin_block_list_info = origin_cbv.get_code_blocks()
        origin_block_list = self._block_list_extend(origin_block_list_info, \
                                                    self._origin_code_lists)

        '''
        Assign each block a unique ID number
        '''
        block_id_list = range(0, len(origin_block_list) * 2)
        random.shuffle(block_id_list)
        block_id_list = block_id_list[:len(origin_block_list)]
        i = 0
        print "Origin code blocks"
        for block in origin_block_list:
            print "Block %d: ID --- %d, content %s\n" % \
                    (i, block_id_list[i], block)
            i += 1
        print

        '''
        Encoding the block IDs into binary strings
        '''
        print "Encoding Block ID..."
        block_id_string_list = self._encoding_block_id(block_id_list)

        '''
        transform on each block
        '''
        i = 0
        encode_block_list = []
        for block in origin_block_list:
            print "Dealing with block " + str(i)

            '''
            Generate the watermark template
            '''
            wm_generator = SimpleWatermarkTemplate()
            [wm_code_lists, wm_text, wm_info] = wm_generator.get_template(len(block))

            print "The watermark code is:"
            print wm_text

            wm_cbv = CodeBlocksVisitor(wm_text)
            wm_block_list_info = wm_cbv.get_code_blocks()
            wm_block_list = self._block_list_extend(wm_block_list_info, \
                                                    wm_code_lists)

            '''
            Mix the watermark code with original code
            '''
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

            '''
            Encode the mixed code
            '''
            encoder = SimpleEncoder(mixcode)
            encoded_code_list = encoder.encode()
            
            print "Encoded code is"
            print "".join(encoded_code_list)
            print


            print "Generate path based watermark template"
            spbwmt = SimplePBWMTemplate()
            [spbwmt_code_list, spbwmt_full_code] = spbwmt.get_template(block_id_string_list[i])
            print "Path based watermark template is:"
            print spbwmt_full_code
            print

            print "Mix the encoded code with path based watermark template"
            spbwmm = SimplePBWMMixer()
            spbwmm.set_source_code(encoded_code_list)
            spbwmm.set_pbwm_code(spbwmt_code_list)
            encoded_code_list = spbwmm.work()
            print "Final mixed code is"
            print "".join(encoded_code_list)
            print
        
            encoded_code_list.insert(0, "/* Block ID: %d, %s */" % 
                                     (block_id_list[i], block_id_string_list[i]))
            encode_block_list.append(encoded_code_list)
            i += 1

        
        '''
        Add the external watermark declaration to the processed program
        '''
        new_code = self._PBWM_HEADER + self._merge_blocks(self._origin_code_lists, \
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

