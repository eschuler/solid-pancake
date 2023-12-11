
import re
import time

start_time = time.time()

infile = "sample.txt"
#infile = "input.txt"

class Pipe:

    def __init__(self, shape):
        self.shape = shape
        self.dist_from_start = -1
        
    def get_next_directions(self):
        if self.shape == "|":
            return [(-1,0), (1,0)]
        elif self.shape == "-":
            return [(0,-1), (0,1)]
        elif self.shape == "L":
            return [(-1,0), (0,1)]
        elif self.shape == "J":
            return [(0,-1), (-1,0)]
        elif self.shape == "7":
            return [(0,-1), (1,0)]
        elif self.shape == "F":
            return [(0,1), (1,0)]
        else:
            print("Unknown pipe shape! " + self.shape)
            exit(1)
        
    def to_string(self):
        return self.shape

row = 0
pipe_map = {}

chars = []

for line in open(infile):
    line = line.strip()
    
    chars.append([c for c in line])
    
#for row in chars:
#    print(row)
    
starting_loc = (-1, -1)

num_rows = len(chars)
num_cols = len(chars[0])

def is_valid_loc(loc):
    return loc[0] >= 0 and loc[0] < num_rows and loc[1] >= 0 and loc[1] < num_cols
    
def print_map(print_dist=False):
    for row_idx in range(num_rows):
        row_str = ""
        
        for col_idx in range(num_cols):
            if (row_idx, col_idx) in pipe_map:
                if print_dist:
                    dist = pipe_map[(row_idx, col_idx)].dist_from_start
                    if dist == -1:
                        row_str += pipe_map[(row_idx, col_idx)].shape
                    else:
                        row_str += "{}".format(dist)
                else:
                    row_str += pipe_map[(row_idx, col_idx)].shape
            else:
                row_str += "."
                
        print(row_str)

for row_idx in range(num_rows):
    row = chars[row_idx]
    
    for col_idx in range(num_cols):
        curr_char = chars[row_idx][col_idx]
    
        if curr_char == ".":
            pass
        elif curr_char == "S":
            starting_loc = (row_idx, col_idx)
            
            if infile == "sample.txt":
                pipe_map[(row_idx, col_idx)] = Pipe("F")
            elif infile == "input.txt":
                pipe_map[(row_idx, col_idx)] = Pipe("|")
            else:
                print("No starting pipe!")
                exit(1)
            
        else:
            pipe_map[(row_idx, col_idx)] = Pipe(curr_char)
            
print_map()

dist_from_start = {}
dist_from_start[starting_loc] = 0
pipe_map[starting_loc].dist_from_start = 0
stack = [(starting_loc, pipe_map[starting_loc])]

print()
print_map(True)

#for loc, pipe in pipe_map.items():
#    print("{}: {}".format(loc, pipe.to_string()))
#while len(stack) > 0:
#    next_loc = stack.pop(0)
        
#print(": {}".format(my_sum))
end_time = time.time()

print("Elapsed time: {} seconds".format(end_time - start_time))
    

