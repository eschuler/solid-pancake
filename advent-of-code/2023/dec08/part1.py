
import re
import time

start_time = time.time()

#infile = "sample.txt"
infile = "input.txt"

class Node:

    def __init__(self, node_id, left, right):
        self.node_id = node_id
        self.left = left
        self.right = right
        
    def to_string(self):
        return "{} = ({}, {})".format(self.node_id, self.left, self.right)
        
directions = ""

lines = []
for line in open(infile):
    lines.append(line.strip())
    
directions = lines[0]
nodes = {}

for line in lines[2:]:
    match_obj = re.match("([A-Z][A-Z][A-Z]) = \(([A-Z][A-Z][A-Z]), ([A-Z][A-Z][A-Z])\)", line)
    if match_obj is None:
        print("Could not parse line! " + line)
        continue
        
    #print(match_obj.groups())
    new_node = Node(match_obj.group(1), match_obj.group(2), match_obj.group(3))
    nodes[match_obj.group(1)] = new_node
    
starting_node = nodes["AAA"]
    
#for node_id, node_obj in nodes.items():
#    print(node_obj.to_string())
    
num_steps = 0
    
while starting_node.node_id != "ZZZ":
    next_direction = directions[0]
    if next_direction == "L":
        next_node = nodes[starting_node.left]
    else:
        next_node = nodes[starting_node.right]
        
    if starting_node.node_id == next_node.node_id:
        print("Infinite loop detected! Tried to go {} on {}".format(next_direction, starting_node.node_id))
        break
        
    starting_node = next_node
    
    directions = directions[1:] + next_direction
        
    num_steps += 1
        
print("# steps: {}".format(num_steps))
end_time = time.time()

print("Elapsed time: {} seconds".format(end_time - start_time))
    

