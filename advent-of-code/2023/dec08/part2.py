
import re
import time

start_time = time.time()

#infile = "sample2.txt"
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
starting_nodes = []

for line in lines[2:]:
    match_obj = re.match("([A-Z0-9][A-Z0-9][A-Z0-9]) = \(([A-Z0-9][A-Z0-9][A-Z0-9]), ([A-Z0-9][A-Z0-9][A-Z0-9])\)", line)
    if match_obj is None:
        print("Could not parse line! " + line)
        exit()
        
    #print(match_obj)
        
    #print(match_obj.groups())
    new_node = Node(match_obj.group(1), match_obj.group(2), match_obj.group(3))
    nodes[match_obj.group(1)] = new_node
    if match_obj.group(1)[-1] == "A":
        starting_nodes.append(new_node)
    
print("Starting nodes:")
for node_obj in starting_nodes:
    print("    " + node_obj.to_string())

all_nodes_end_with_z = False

steps_until_end = []
orig_directions = directions

for starting_node in starting_nodes:
    directions = orig_directions
    starting_id = starting_node.node_id
    
    num_steps = 0
    
    while starting_node.node_id[-1] != "Z":
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
    
    steps_until_end.append(num_steps)
        
    #print("# steps for {} to get to {}: {}".format(starting_id, starting_node.node_id, steps_until_end))
    
print("Steps: {}".format(steps_until_end))
end_time = time.time()

print("Elapsed time: {} seconds".format(end_time - start_time))
    

