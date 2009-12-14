#/usr/bin/python

class SimpleMixer:

    def __init__(self):
        self._mix_code_list = []

    def set_source_code(self, source):
        self._source = source

    def set_watermark_code(self, watermark):
        self._watermark = watermark

    def work(self):
        self._mix_code_list = []
    
        src_len = len(self._source)
        wm_len = len(self._watermark)

        i = 0
        j = 0
        k = 0
        while i < src_len and j < wm_len:
            if (k % 2) == 0:
                self._mix_code_list.append(['S', self._source[i]])
                i += 1
            else:
                self._mix_code_list.append(['W', self._watermark[j]])
                j += 1
            k += 1

        while i < src_len:
            self._mix_code_list.append(['S', self._source[i]])
            i += 1

        while j < wm_len:
            self._mix_code_list.append(['W', self._watermark[j]])
            j += 1

        return self._mix_code_list

if __name__ == "__main__":
    src = [["i = 1", "123"], ["i = 2", "234"], ["i = 3", "345"], ["i = 4", "456"], ["i = 5", "567"], ["i = 6", "678"]]
    wm = [["j = 1", "321"], ["j = 2","432"], ["j = 3", "543"], ["j = 4", "654"]]
    mixer = SimpleMixer()
    mixer.set_source_code(src)
    mixer.set_watermark_code(wm)
    ans = mixer.work()
    for i in ans:
        print i
