#!/usr/bin/env python

import re, math

infile_path = "sample.txt"
#infile_path = "input.txt"

zero_count = 0
curr_dial = 50

regex = re.compile("(L|R)(\d+)")

print("Current value: {}; zero_count: {}".format(curr_dial, zero_count))

with open(infile_path, "r") as infile:

    for line in infile:
        line = line.strip()
        match_obj = regex.match(line)
        
        if match_obj is None:
            print("ERROR: " + line)
            exit(1)
            
        print(line)
            
        groups = match_obj.groups()
        direction = groups[0]
        amount = int(groups[1])
        
        if direction == "L":
            amount *= -1
            
        curr_dial += amount
        curr_dial %= 100
        
        # full rotations
        zero_count += math.floor(abs(amount) / 100)
        amount %= 100
        
        curr_dial += amount
        
        if curr_dial > 100:
            curr_dial %= 100
            zero_count += 1
        elif curr_dial < -100:
            curr_dial %= 100
            zero_count += 1
        
        #while curr_dial < -100:
        #    curr_dial += 100
        #    zero_count += 1
            
        #while curr_dial > 100:
        #    curr_dial -= 100
        #    zero_count += 1
        
        if curr_dial == 0:
            zero_count += 1
            
        print("Current value: {}; zero_count: {}".format(curr_dial, zero_count))
            
print("zero count: {}".format(zero_count))