
import re

infile = "input.txt"

symbol_locs = {}

class PartNumber:
        
    def __init__(self, number, start_loc):
        self.number = number
        self.row = start_loc[0]
        self.start_col = start_loc[1]
        
        if number > 100:
            self.end_col = self.start_col + 2
        elif number > 10:
            self.end_col = self.start_col + 1
        else:
            self.end_col = self.start_col
            
    def is_adjacent_to_symbol(self):
        for curr_col in range(self.start_col - 1, self.end_col + 2):
            #print("Checking {}".format((self.row - 1, curr_col)))
            if (self.row - 1, curr_col) in symbol_locs:
                #print("Match!")
                return True
            #print("Checking {}".format((self.row + 1, curr_col)))
            if (self.row + 1, curr_col) in symbol_locs:
                #print("Match!")
                return True
        #print("Checking {}".format((self.row, self.start_col - 1)))
        if (self.row, self.start_col - 1) in symbol_locs:
            #print("Match!")
            return True
        #print("Checking {}".format((self.row, self.end_col + 1)))
        if (self.row, self.end_col + 1) in symbol_locs:
            #print("Match!")
            return True
        return False
        
    def is_adjacent_to(self, loc):
        for curr_col in range(self.start_col - 1, self.end_col + 2):
            #print("Checking {}".format((self.row - 1, curr_col)))
            if (self.row - 1, curr_col) == loc:
                #print("Match!")
                return True
            #print("Checking {}".format((self.row + 1, curr_col)))
            if (self.row + 1, curr_col) == loc:
                #print("Match!")
                return True
        #print("Checking {}".format((self.row, self.start_col - 1)))
        if (self.row, self.start_col - 1) == loc:
            #print("Match!")
            return True
        #print("Checking {}".format((self.row, self.end_col + 1)))
        if (self.row, self.end_col + 1) == loc:
            #print("Match!")
            return True
        return False
        
    def to_string(self):
        return "{}, start loc {}, end loc {}".format(self.number, (self.row, self.start_col), (self.row, self.end_col))

part_num_sum = 0
curr_row = 0

part_numbers = []

for line in open(infile):
    line = line.strip()
    
    curr_num = ""
    
    for curr_col in range(0, len(line)):
        char = line[curr_col]
            
        if re.match("[0-9]", char) is not None:
            curr_num += char
        
        else:
            if len(curr_num) > 0:
                part_numbers.append(PartNumber(int(curr_num), (curr_row, curr_col - len(curr_num))))
            curr_num = ""
            
            if char != ".":
                symbol_locs[(curr_row, curr_col)] = char
                
    if curr_num != "":
        part_numbers.append(PartNumber(int(curr_num), (curr_row, curr_col - len(curr_num))))
                
    curr_row += 1
    
gear_ratio_sum = 0
    
#print("\nSymbol locations:")
for sym_loc in sorted(symbol_locs.keys()):
    #print("    {}".format(sym_loc))
    if symbol_locs[sym_loc] != "*":
        continue
        
    adjacent_parts = []
    
    print("Potential gear: {}".format(sym_loc))
        
    for pn in part_numbers:
        #print(pn.row)
        if pn.row > sym_loc[0] + 1:
            #print("pn.row is {}; stopping iteration".format(pn.row))
            break
        if pn.is_adjacent_to(sym_loc):
            adjacent_parts.append(pn.number)
            
    print("    Num adjacent parts: {}".format(len(adjacent_parts)))
    
    if len(adjacent_parts) == 2:
        gear_ratio = adjacent_parts[0] * adjacent_parts[1]
        print("    Gear ratio = {}".format(gear_ratio))
        gear_ratio_sum += gear_ratio
            
    #break
    
print("Gear ratio sum: {}".format(gear_ratio_sum))
    

