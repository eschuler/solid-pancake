#!/usr/bin/env python

import re

infile_path = "sample.txt"

zero_count = 0
curr_dial = 50

regex = re.compile("(L|R)(\d+)")

with open(infile_path, "r") as infile:

    for line in infile:
        line = line.strip()
        match_obj = regex.match(line)
        
        if match_obj is None:
            print("ERROR: " + line)
            exit(1)
            
        groups = match_obj.groups()
        direction = groups[0]
        amount = int(groups[1])
        
        print("{} -> {}".format(direction, amount))