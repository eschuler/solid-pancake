
#infile = "sample.txt"
infile = "input.txt"

sand_source = [500, 0]

min_x = 999
max_x = -999
min_y = 0
max_y = -999

rock_lines = []

def print_cave(cave_map):
    print()
    
    # print header
    xrange = range(min_x, max_x + 1)
    xrange_str = ["{}".format(x) for x in xrange]
    
    row1 = ""
    row2 = ""
    row3 = ""
    for val in xrange_str: 
        row1 = row1 + val[0]
        row2 = row2 + val[1]
        row3 = row3 + val[2]
    
    print("{:3}{}".format("", row1))
    print("{:3}{}".format("", row2))
    print("{:3}{}".format("", row3))
    
    # print map
    for y in range(len(cave_map)):
        print("{:<3}{}".format(y, "".join(cave_map[y])))
        
    print()
    
def get_col_idx(col_label):
    return col_label# - min_x
    
def get_line_points(line):

    points = []

    #for coord in line:
    #    print(coord)

    i = 0
    curr_point = line[i]
    next_point = line[i+1]
    
    while i < len(line) - 1:
            
        points.append([curr_point[0], curr_point[1]])
    
        #print("curr_point = {}, next_point = {}".format(curr_point, next_point))
            
        if curr_point[0] == next_point[0] and curr_point[1] == next_point[1]:
            i = i + 1
            if i == len(line) - 1:
                break
            next_point = line[i+1]
    
            #print("curr_point = {}, next_point = {}".format(curr_point, next_point))
        
        # next_point is above or below
        if curr_point[0] == next_point[0]:
        
            # above
            if next_point[1] < curr_point[1]:
                curr_point[1] = curr_point[1] - 1
                
            # below
            else:
                curr_point[1] = curr_point[1] + 1
        
        # next_point is left or right
        elif curr_point[1] == next_point[1]:
        
            # left
            if next_point[0] < curr_point[0]:
                curr_point[0] = curr_point[0] - 1
                
            # below
            else:
                curr_point[0] = curr_point[0] + 1
            
        else:
            print("Diagonal point!")
            exit(1)
            
    #for p in points:
    #    print(p)
            
    return points
    
def is_at_rest(cave_map, loc):
    
    below = cave_map[loc[1] + 1][get_col_idx(loc[0])]
    below_left = cave_map[loc[1] + 1][get_col_idx(loc[0] - 1)]
    below_right = cave_map[loc[1] + 1][get_col_idx(loc[0] + 1)]
    
    #print("at rest {}? {}".format(loc, (below != "." and below_left != "." and below_right != ".")))
    
    return below != "." and below_left != "." and below_right != "."
        
    
def get_next_sand_loc(cave_map):

    curr_loc = sand_source
    
    if cave_map[curr_loc[1]][get_col_idx(curr_loc[0])] == "o":
        return None
    
    while not is_at_rest(cave_map, curr_loc):
    
        #print("curr_loc = {}".format(curr_loc))
        
        next_loc = [curr_loc[0], curr_loc[1] + 1]
        next_loc_value = cave_map[next_loc[1]][get_col_idx(next_loc[0])]
        
        if next_loc_value == ".":
            curr_loc = next_loc
            #print("curr_loc = {}".format(curr_loc))
        
            #if curr_loc[1] > max_y or curr_loc[0] < min_x or curr_loc[0] >= max_x:
            #    return None
            
            #break
            continue
            
        next_loc = [curr_loc[0] - 1, curr_loc[1] + 1]
        next_loc_value = cave_map[next_loc[1]][get_col_idx(next_loc[0])]
        
        if next_loc_value == ".":
            curr_loc = next_loc
            #print("curr_loc = {}".format(curr_loc))
        
            #if curr_loc[1] > max_y or curr_loc[0] < min_x or curr_loc[0] >= max_x:
            #    return None
                
            #break
            continue
            
        curr_loc = [curr_loc[0] + 1, curr_loc[1] + 1]
        
        #if curr_loc[1] > max_y or curr_loc[0] < min_x or curr_loc[0] >= max_x:
        #    return None
    
        #print("curr_loc = {}".format(curr_loc))
        
        #break
        
    return curr_loc
        

for line in open(infile):
    line = line.strip()
    print(line)
    
    coordinates = line.split(" -> ")
    parsed_coord = []
    
    for c in coordinates:
        c_split = c.split(',')
        c_split_int = [int(x) for x in c_split]
        
        if c_split_int[0] < min_x:
            min_x = c_split_int[0]
        
        if c_split_int[0] > max_x:
            max_x = c_split_int[0]
        
        #if c_split_int[1] < min_y:
        #    min_y = c_split_int[1]
        
        if c_split_int[1] > max_y:
            max_y = c_split_int[1]
            
        parsed_coord.append(c_split_int)
        
    print(parsed_coord)
    rock_lines.append(parsed_coord)
    
print("min_x  = {}".format(min_x))
print("max_x  = {}".format(max_x))
print("max_y  = {}".format(max_y))
    
cave_map = []
for y in range(max_y + 1):
    row = ['.' for i in range(0, 1000)]
    cave_map.append(row)
cave_map.append(['.' for i in range(0, 1000)])
cave_map.append(['#' for i in range(0, 1000)])
    
# mark the sand source
cave_map[0][get_col_idx(500)] = '+'

# mark the rocks
print()
for line in rock_lines:
    points = get_line_points(line)
    
    for p in points:
        cave_map[p[1]][get_col_idx(p[0])] = '#'
    
#print_cave(cave_map)
    
#print("x bounds: {}".format((min_x, max_x)))
#print("y bounds: {}".format((min_y, max_y)))

i = 0
while True:

    next_sand_loc = get_next_sand_loc(cave_map)
    
    if next_sand_loc is None:
        break
    
    #print("next_sand_loc = {}".format(next_sand_loc))
    cave_map[next_sand_loc[1]][get_col_idx(next_sand_loc[0])] = "o"
    
    #print_cave(cave_map)
    
    i = i + 1
    print("{} iterations complete".format(i))
    
    #if i >= 100:
    #    break
    
#print_cave(cave_map)
print("Full after {} iterations".format(i))


