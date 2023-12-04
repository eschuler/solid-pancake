
import re

# 560570 (too low)

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
                symbol_locs[(curr_row, curr_col)] = True
                
    if curr_num != "":
        part_numbers.append(PartNumber(int(curr_num), (curr_row, curr_col - len(curr_num))))
                
    curr_row += 1
    
#print("\nSymbol locations:")
#for sym_loc in sorted(symbol_locs.keys()):
#    print("    {}".format(sym_loc))
    
part_number_sum = 0

print("\nPart numbers:")
for pn in part_numbers:
    adj_string = ""
    if pn.is_adjacent_to_symbol():
        adj_string = " - adjacent to symbol!"
        part_number_sum += pn.number
    else:
        adj_string = " - not adjacent to symbol!"
    print("    " + pn.to_string() + adj_string)
    #break
    
print("Part number sum: {}".format(part_number_sum))
    

