#!/usr/bin/python

import sys, os
from pycparser import split_blocks, split_statements
from utils import interleave_code

if len() < 2:
    print >>sys.stderr, "Usage: %s input-file" % sys.argv[0]
    sys.exit(1)

input_name  = sys.argv[1]

# the input and output opening file
input_file  = open(input_name, "r")
output_file = open(append_trans_ext(input_name), "w")

blocks   = split_blocks(input_file)
pointers = []

for block in blocks:
    eval_seg = choose_random_from_templates(templates)
    block = interleave_code(eval_seg, block)
    constant_pool = collect_constants(block)
    CT = build_constant_tree(constant_pool, pointers)
    CT_val = decode_CT(CT)

    for statement in split_statements(block):
        if have_constant(statment):
            pointer = CT.rootnode
            substitude(statement, constant, "decode(pointer)")

        # the left val is always variables to be assigned
        analyze_left_var(statement)

        # choose a the root node in the graph to be changed
        selected = random(pointers)
        # translated code
        sm1 = construct_proper_update_for_output("updateCT(CT, val, root_of_subgraph_to_update)")
        append_translated_statements(sm1)

    # generate initialization code for output
    insert_at_begin(block, mixed_program_constant_tree)
    generate_output_file_blocks()
