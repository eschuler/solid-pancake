
#infile = "sample.txt"
infile = "input.txt"

class Path:
    def __init__(self, sequence, length):
        self.sequence = []
        for loc in sequence:
            self.sequence.append(loc)
        self.length = length
        
    def add_to_path(self, loc):
        self.sequence.append(loc)
        self.length = self.length + 1
        
    def to_string(self):
        return "{}: length {}".format(self.sequence, self.length)
    
elev_map_letters = []
elev_map = []
start_loc = None
end_loc   = None

ord_a = ord('a')

curr_row_idx = 0

for line in open(infile):
    curr_row_letters = []
    curr_row_values = []
    
    line = line.strip()
    print(line)
    
    curr_col_idx = 0
    for char in line:
    
        if char == "S":
            if start_loc is not None:
                print("Found two start locations!")
            else:
                start_loc = (curr_row_idx, curr_col_idx)
            char = "a"
    
        elif char == "E":
            if end_loc is not None:
                print("Found two end locations!")
            else:
                end_loc = (curr_row_idx, curr_col_idx)
            char = "z"
            
        curr_row_letters.append(char)
        curr_row_values.append(ord(char) - ord_a)
        curr_col_idx = curr_col_idx + 1
    
    elev_map_letters.append(line)
    elev_map.append(curr_row_values)
    curr_row_idx = curr_row_idx + 1
    
row_count = len(elev_map_letters)
col_count = len(elev_map_letters[0])
    
print()
print("Start: {}".format(start_loc))
print("End: {}".format(end_loc))
print("row_count: {}".format(row_count))
print("col_count: {}".format(col_count))

# print()
# for row in elev_map:
    # row_str = ""
    # for val in row:
        # row_str = row_str + "{:<2} ".format(val)
    # print(row_str)

valid_up = []
valid_down = []
valid_left = []
valid_right = []
shortest_path = []

# zero populate validity
for i in range(row_count):
    valid_up.append([False for x in range(col_count)])
    valid_down.append([False for x in range(col_count)])
    valid_left.append([False for x in range(col_count)])
    valid_right.append([False for x in range(col_count)])
    shortest_path.append([-1 for x in range(col_count)])
    
shortest_path[start_loc[0]][start_loc[1]] = 0

for i in range(row_count):
    for j in range(col_count):
    
        # check valid up
        if i > 0:
            valid_up[i][j] = elev_map[i-1][j] <= (elev_map[i][j] + 1)
    
        # check valid down
        if i < row_count - 1:
            valid_down[i][j] = elev_map[i+1][j] <= (elev_map[i][j] + 1)
    
        # check valid left
        if j > 0:
            valid_left[i][j] = elev_map[i][j-1] <= (elev_map[i][j] + 1)
    
        # check valid right
        if j < col_count - 1:
            valid_right[i][j] = elev_map[i][j+1] <= (elev_map[i][j] + 1)
            
# print valid_up
# print("\nvalid_up:")
# for i in range(row_count):
    # row_str = ""
    # for j in range(col_count):
        # if valid_up[i][j]:
            # row_str = row_str + "^  "
        # else:
            # row_str = row_str + ".  "
    # print(row_str)
            
# print valid_down
# print("\nvalid_down:")
# for i in range(row_count):
    # row_str = ""
    # for j in range(col_count):
        # if valid_down[i][j]:
            # row_str = row_str + "v  "
        # else:
            # row_str = row_str + ".  "
    # print(row_str)
            
# print valid_left
# print("\nvalid_left:")
# for i in range(row_count):
    # row_str = ""
    # for j in range(col_count):
        # if valid_left[i][j]:
            # row_str = row_str + "<  "
        # else:
            # row_str = row_str + ".  "
    # print(row_str)
            
# print valid_right
# print("\nvalid_right:")
# for i in range(row_count):
    # row_str = ""
    # for j in range(col_count):
        # if valid_right[i][j]:
            # row_str = row_str + ">  "
        # else:
            # row_str = row_str + ".  "
    # print(row_str)
    
paths = [Path([start_loc], 0)]

while len(paths) > 0:
    
    path = paths.pop(0)
    curr_loc = path.sequence[len(path.sequence) - 1]
    
    #print()
    #print("Current path: " + path.to_string())
    #print(loc)
    
    if valid_up[curr_loc[0]][curr_loc[1]]:
        new_loc = (curr_loc[0] - 1, curr_loc[1])
        new_path = Path(path.sequence, path.length)
        new_path.add_to_path((new_loc[0], new_loc[1]))
                
        if shortest_path[new_loc[0]][new_loc[1]] == -1:
            shortest_path[new_loc[0]][new_loc[1]] = new_path.length
            paths.append(new_path)
        else:
            if new_path.length < shortest_path[new_loc[0]][new_loc[1]]:
                shortest_path[new_loc[0]][new_loc[1]] = new_path.length
    
    if valid_down[curr_loc[0]][curr_loc[1]]:
        new_loc = (curr_loc[0] + 1, curr_loc[1])
        new_path = Path(path.sequence, path.length)
        new_path.add_to_path((new_loc[0], new_loc[1]))
                
        if shortest_path[new_loc[0]][new_loc[1]] == -1:
            shortest_path[new_loc[0]][new_loc[1]] = new_path.length
            paths.append(new_path)
        else:
            if new_path.length < shortest_path[new_loc[0]][new_loc[1]]:
                shortest_path[new_loc[0]][new_loc[1]] = new_path.length
    
    if valid_left[curr_loc[0]][curr_loc[1]]:
        new_loc = (curr_loc[0], curr_loc[1] - 1)
        new_path = Path(path.sequence, path.length)
        new_path.add_to_path((new_loc[0], new_loc[1]))
        
        if shortest_path[new_loc[0]][new_loc[1]] == -1:
            shortest_path[new_loc[0]][new_loc[1]] = new_path.length
            paths.append(new_path)
        else:
            if new_path.length < shortest_path[new_loc[0]][new_loc[1]]:
                shortest_path[new_loc[0]][new_loc[1]] = new_path.length
    
    if valid_right[curr_loc[0]][curr_loc[1]]:
        new_loc = (curr_loc[0], curr_loc[1] + 1)
        new_path = Path(path.sequence, path.length)
        new_path.add_to_path((new_loc[0], new_loc[1]))
        
        if shortest_path[new_loc[0]][new_loc[1]] == -1:
            shortest_path[new_loc[0]][new_loc[1]] = new_path.length
            paths.append(new_path)
        else:
            if new_path.length < shortest_path[new_loc[0]][new_loc[1]]:
                shortest_path[new_loc[0]][new_loc[1]] = new_path.length
            
    #print shortest_path
    # print("\nshortest_path:")
    # for i in range(row_count):
        # row_str = ""
        # for j in range(col_count):
            # row_str = row_str + "{:3}".format(shortest_path[i][j])
        # print(row_str)
        
    # print("\nPaths remaining:")
    # for path in paths:
        # print("\t" + path.to_string())
        
    #break
        
print("\nShortest path to peak: {}".format(shortest_path[end_loc[0]][end_loc[1]]))

# Answers guessed:
#   1. 381 (too high)
    
