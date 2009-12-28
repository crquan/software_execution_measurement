typedef long int __off_t;
typedef __off_t off_t;
typedef unsigned IPos;

off_t deflate()
{
    IPos hash_head;
    IPos prev_match;
    int flush;
    int match_available = 0;
    register unsigned match_length = 3 -1;

    if (compr_level <= 3) return deflate_fast();


    while (lookahead != 0) {



        ((ins_h = (((ins_h)<<((15 +3 -1)/3)) ^ (window[(strstart) + 3 -1])) & ((unsigned)(1<<15)-1)), prev[(strstart) & (0x8000 -1)] = hash_head = (prev+0x8000)[ins_h], (prev+0x8000)[ins_h] = (strstart));



        prev_length = match_length, prev_match = match_start;
        match_length = 3 -1;

        if (hash_head != 0 && prev_length < max_lazy_match &&
            strstart - hash_head <= (0x8000 -(258 +3 +1)) &&
            strstart <= window_size - (258 +3 +1)) {




            match_length = longest_match (hash_head);

            if (match_length > lookahead) match_length = lookahead;


            if (match_length == 3 && strstart-match_start > 4096){



                match_length--;
            }
        }



        if (prev_length >= 3 && match_length <= prev_length) {

            ;

            flush = ct_tally(strstart-1-prev_match, prev_length - 3);




            lookahead -= prev_length-1;
            prev_length -= 2;
            do {
                strstart++;
                ((ins_h = (((ins_h)<<((15 +3 -1)/3)) ^ (window[(strstart) + 3 -1])) & ((unsigned)(1<<15)-1)), prev[(strstart) & (0x8000 -1)] = hash_head = (prev+0x8000)[ins_h], (prev+0x8000)[ins_h] = (strstart));





            } while (--prev_length != 0);
            match_available = 0;
            match_length = 3 -1;
            strstart++;
            if (flush) flush_block(block_start >= 0L ? (char*)&window[(unsigned)block_start] : (char*)((void *)0), (long)strstart - block_start, (0)), block_start = strstart;

        } else if (match_available) {




            ;
            if (ct_tally (0, window[strstart-1])) {
                flush_block(block_start >= 0L ? (char*)&window[(unsigned)block_start] : (char*)((void *)0), (long)strstart - block_start, (0)), block_start = strstart;
            }
            strstart++;
            lookahead--;
        } else {



            match_available = 1;
            strstart++;
            lookahead--;
        }
        ;






        while (lookahead < (258 +3 +1) && !eofile) fill_window();
    }
    if (match_available) ct_tally (0, window[strstart-1]);

    return flush_block(block_start >= 0L ? (char*)&window[(unsigned)block_start] : (char*)((void *)0), (long)strstart - block_start, (1));
}
