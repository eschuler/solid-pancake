
#infile = "sample.txt"
infile = "sample2.txt"
#infile = "input.txt"

def sort_by_x(locs):
    return sorted(locs, cmp=lambda p: p[0])

def sort_by_y(locs):
    return sorted(locs, cmp=lambda p: p[1])
    
def is_open_space(land_map, loc):
    return loc not in land_map.keys() or land_map[loc] == "."
    
def get_nw(loc):
    return (loc[0] - 1, loc[1] - 1)
    
def get_n(loc):
    return (loc[0], loc[1] - 1)
    
def get_ne(loc):
    return (loc[0] + 1, loc[1] - 1)
    
def get_sw(loc):
    return (loc[0] - 1, loc[1] + 1)
    
def get_s(loc):
    return (loc[0], loc[1] + 1)
    
def get_se(loc):
    return (loc[0] + 1, loc[1] + 1)
    
def get_w(loc):
    return (loc[0] - 1, loc[1])
    
def get_e(loc):
    return (loc[0] + 1, loc[1])
    
def get_adjacent(loc, starting_dir):
    adjacent = [
        get_nw(loc),
        get_n(loc),
        get_ne(loc),
        get_se(loc),
        get_s(loc),
        get_sw(loc),
        get_w(loc),
        get_e(loc)
    ]
    
    if starting_dir == "east":
        adjacent = adjacent[2:] + adjacent[:2]
    elif starting_dir == "south":
        adjacent = adjacent[4:] + adjacent[:4]
    elif starting_dir == "west":
        adjacent = adjacent[6:] + adjacent[:6]
        
    return adjacent

lines = []

directions = ['north', 'south', 'west', 'east']

for line in open(infile):
    line = line.strip()
    lines.append(line)
    print(line)
    
print()
    
num_cols = len(lines[0])

land_map = {}
    
for y in range(len(lines)):
    row = lines[y]
    for x in range(num_cols):
        if row[x] == "#":
            #print((x,y))
            land_map[(x,y)] = "#"
            
#print()
            
while True:
    votes = {}
    
    for loc, item in land_map.items():
    
        vote = None
        
        print("elf: {}".format(loc))
        
        adjacent = get_adjacent(loc, directions[0])
        
        print("adjacent: {}".format(adjacent))
        
        # check direction 1
        if "#" not in adjacent[:3]:
            vote = adjacent[1]
            
        # check direction 2
        elif "#" not in adjacent[3:5]:
            vote = adjacent[3]
            
        # check direction 3
        elif "#" not in adjacent[5:7]:
            vote = adjacent[5]
            
        # check direction 4
        elif "#" not in adjacent[6:]:
            vote = adjacent[7]
            
        print("vote: {}".format(vote))
        
        print()
        #break

    break

