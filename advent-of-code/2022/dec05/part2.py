
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

#stacks = []
#stacks.append(["Z", "N"])
#stacks.append(["M", "C", "D"])
#stacks.append(["P"])

pattern = "move (\d+) from (\d) to (\d)"
    
#for stack in stacks:
#    print(stack)
#print()

for line in open(infile_moves):
    line = line.strip()
    #print(line)
    
    match_obj = re.match(pattern, line)
    num_to_move = int(match_obj.group(1))
    from_stack = int(match_obj.group(2)) - 1
    to_stack = int(match_obj.group(3)) - 1
    
    substack = stacks[from_stack][len(stacks[from_stack]) - num_to_move:len(stacks[from_stack])]

    #print("substack: {}".format(substack))
    stacks[to_stack].extend(substack)
    stacks[from_stack] = stacks[from_stack][:len(stacks[from_stack]) - num_to_move]
    
    #for stack in stacks:
    #    print(stack)
    #print()
    
    #print(num_to_move)
    #print(from_stack)
    #print(to_stack)
    #print(match_obj)
    
for stack in stacks:
    print(stack.pop())

