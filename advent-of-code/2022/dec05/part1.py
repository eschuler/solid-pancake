
import re

infile_start = "inputs-start.txt"
infile_moves = "inputs-moves.txt"
num_stacks = 9
stacks = []
stacks.append(["G", "T", "R", "W"])
stacks.append(["G", "C", "H", "P", "M", "S", "V", "W"])
stacks.append(["C", "L", "T", "S", "G", "M"])
stacks.append(["J", "H", "D", "M", "W", "R", "F"])
stacks.append(["P", "Q", "L", "H", "S", "W", "F", "J"])
stacks.append(["P", "J", "D", "N", "F", "M", "S"])
stacks.append(["Z", "B", "D", "F", "G", "C", "S", "J"])
stacks.append(["R", "T", "B"])
stacks.append(["H", "N", "W", "L", "C"])

pattern = "move (\d+) from (\d) to (\d)"

for line in open(infile_moves):
    line = line.strip()
    #print(line)
    
    match_obj = re.match(pattern, line)
    num_to_move = int(match_obj.group(1))
    from_stack = int(match_obj.group(2)) - 1
    to_stack = int(match_obj.group(3)) - 1
    
    for i in range(num_to_move):
        stacks[to_stack].append(stacks[from_stack].pop())
    
    #print(num_to_move)
    #print(from_stack)
    #print(to_stack)
    #print(match_obj)
    
for stack in stacks:
    print(stack.pop())

