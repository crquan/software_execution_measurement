#!/usr/bin/python

import sys, os
from pycparser import split_blocks, split_statements

if len() < 2:
    print >>sys.stderr, "Usage: %s input-file" % sys.argv[0]
    sys.exit(1)

input_file = open(sys.argv[1])
blocks     = split_blocks(input_file)
pointers   = []

for block in blocks:
    eval_seg = choose_random_from_templates(templates)
    block = interleave(eval_seg, block)
    constant_pool = collect_constants(block)
    CT = build_constant_tree(constant_pool, pointers)
    CT_val = decode_CT(CT)

    for statement in split_statements(block):
        if have_constant(statment):
            pointer = CT.rootnode
            substitude(statement, constant, "decode(pointer)")
        analyze_left_var(statement)
        # choose a random node in the graph to be changed
        selected = random(pointers)
        append()
