
infile = "sample.txt"
#infile = "input.txt"

class Rock:
    def __init__(self, width, height, points):
        self.width = width
        self.height = height
        self.orig_points = points
        self.points = points
        
        self.left_edge = []
        for y in range(self.height):
            for x in range(self.width):
                if (x,y) in self.points:
                    self.left_edge.append((x,y))
                    break
                    
        #print("left edge: {}".format(self.left_edge))
        
        self.right_edge = []
        for y in range(self.height):
            for x in range(self.width - 1, -1, -1):
                if (x,y) in self.points:
                    self.right_edge.append((x,y))
                    break
                    
        #print("right edge: {}".format(self.right_edge))
        
        self.bottom_edge = []
        for x in range(self.width):
            for y in range(self.height):
                if (x,y) in self.points:
                    self.bottom_edge.append((x,y))
                    break
                    
        #print("bottom edge: {}".format(self.bottom_edge))
                
        
    def to_string(self, falling):
        if falling:
            char = '@'
        else:
            char = '#'
        
        grid = []
        for i in range(self.height):
            grid.append(['.' for j in range(self.width)])
        
        for p in self.points:
            grid[p[1]][p[0]] = char
            
        rock_str = ""
        i = self.height - 1
        while i >= 0:
            rock_str = rock_str + "".join(grid[i]) + "\n"
            i = i - 1
            
        return rock_str

class Shaft:

    def __init__(self):
        self.values = []
        self.num_cols = 7
        self.rock_idx = 0
        self.rocks_placed = 0
        self.rock_height = 0
        
        self.rocks = [
            Rock(4, 1, [(0,0),(1,0),(2,0),(3,0)]),
            Rock(3, 3, [(0,1),(1,0),(1,1),(1,2),(2,1)]),
            Rock(3, 3, [(0,0),(1,0),(2,0),(2,1),(2,2)]),
            Rock(1, 4, [(0,0),(0,1),(0,2),(0,3)]),
            Rock(2, 2, [(0,0),(0,1),(1,0),(1,1)])
        ]

    def get_col_height(self, col_idx):
        y = len(self.values) - 1
        
        while y >= 0:
            if self.values[y][col_idx] == '#':
                return y
                
        return 0

    def get_height():
        y = len(self.values) - 1
        
        max_height = 0
        
        for x in range(self.num_cols):
            col_height = get_col_height(x)
            if col_height > max_height:
                max_height = col_height
                
        return max_height
        
    def add_new_row(self):
        self.values.append(['.' for x in range(self.num_cols)])

    def place_new_rock(self):
    
        # new rock is 3 rows above highest placed rock
        for i in range(3):
            self.add_new_row()
            
        self.curr_rock = self.rocks[self.rock_idx]
        
        origin = (2, len(self.values))
        #print("origin = {}".format(origin))
            
        # add space for new rock
        for i in range(self.curr_rock.height):
            self.add_new_row()
            
        # populate shaft with new rock
        for pt in self.curr_rock.points:
            #print("pt = ({},{})".format(pt[1] + origin[1], pt[0] + origin[0]))
            self.values[pt[1] + origin[1]][pt[0] + origin[0]] = "@"
            
        self.current_origin = origin
        
        #self.rock_idx = self.rock_idx + 1
        #if self.rock_idx >= 4:
        #    self.rock_idx = 0
        #self.new_rock
        
    #def can_move_current_left(self):
    #    y = len(self.values) - 1
        
    #    while y >= 0:
    #        row_contains_falling_rock = False
    #        for x in range(len(self.num_cols)):
    
    def can_move_current_left(self):
    
        #print("current_origin: {}".format(self.current_origin))
            
        for pt in self.curr_rock.left_edge:
            ref_pt = (self.current_origin[0] + pt[0], self.current_origin[1] + pt[1])
            
            if ref_pt[0] == 0:
                return False
            
            # check if point to the left is blocked
            if self.values[ref_pt[1]][ref_pt[0] - 1] != ".":
                return False
            
        return True
    
    def can_move_current_right(self):
    
        #print("current_origin: {}".format(self.current_origin))
            
        for pt in self.curr_rock.right_edge:
            ref_pt = (self.current_origin[0] + pt[0], self.current_origin[1] + pt[1])
            #print("ref_pt: {}".format(ref_pt))
            
            if ref_pt[0] >= self.num_cols - 1:
                return False
            
            # check if point to the right is blocked
            if self.values[ref_pt[1]][ref_pt[0] + 1] != ".":
                return False
            
        return True
        
    def can_move_down(self):
    
        #print("current_origin: {}".format(self.current_origin))
            
        for pt in self.curr_rock.bottom_edge:
            ref_pt = (self.current_origin[0] + pt[0], self.current_origin[1] + pt[1])
            #print("ref_pt = {}".format(ref_pt))
            
            if ref_pt[1] == 0:
                return False
            
            # check if point below is blocked
            if self.values[ref_pt[1] - 1][ref_pt[0]] != ".":
                return False
                
        return True
                
        
    def move_current_left(self):
    
        #print("current_origin: {}".format(self.current_origin))
        
        for y in range(self.curr_rock.height):
            for x in range(self.curr_rock.width):
                ref_pt = (x + self.current_origin[0], y + self.current_origin[1])
                #print("ref_pt = {}".format(ref_pt))
                
                this_val = self.values[ref_pt[1]][ref_pt[0]]
                if this_val == "@":
                    next_val = self.values[ref_pt[1]][ref_pt[0] - 1]
                    
                    self.values[ref_pt[1]][ref_pt[0]] = next_val
                    self.values[ref_pt[1]][ref_pt[0] - 1] = "@"
                    
        self.current_origin = (self.current_origin[0] - 1, self.current_origin[1])
        
    def move_current_right(self):
    
        #print("current_origin: {}".format(self.current_origin))
        
        for y in range(self.curr_rock.height - 1, -1, -1):
            for x in range(self.curr_rock.width - 1, -1, -1):
                ref_pt = (x + self.current_origin[0], y + self.current_origin[1])
                #print("ref_pt = {}".format(ref_pt))
                
                this_val = self.values[ref_pt[1]][ref_pt[0]]
                if this_val == "@":
                    next_val = self.values[ref_pt[1]][ref_pt[0] + 1]
                    
                    self.values[ref_pt[1]][ref_pt[0]] = next_val
                    self.values[ref_pt[1]][ref_pt[0] + 1] = "@"
                    
        self.current_origin = (self.current_origin[0] + 1, self.current_origin[1])
                    
    def settle_rock(self):
        
        for y in range(self.curr_rock.height):
            for x in range(self.curr_rock.width):
                ref_pt = (x + self.current_origin[0], y + self.current_origin[1])
                
                if self.values[ref_pt[1]][ref_pt[0]] == "@":
                    self.values[ref_pt[1]][ref_pt[0]] = "#"
                    
        num_to_pop = 0
                    
        # remove blank rows at top
        for y in range(len(self.values) - 1, -1, -1):
            is_blank_row = True
            for x in range(self.num_cols):
                if self.values[y][x] != ".":
                    is_blank_row = False
                    break
            
            if is_blank_row:
                num_to_pop = num_to_pop + 1
            
        for x in range(num_to_pop):
            self.values.pop()
                    
        shaft.rocks_placed = shaft.rocks_placed + 1
            
        self.rock_idx = (self.rock_idx + 1) % len(self.rocks)
        
            
    def move_down(self):
    
        if not self.can_move_down():
            self.settle_rock()
            return True
    
        #print("current_origin: {}".format(self.current_origin))
        
        for y in range(self.curr_rock.height):
            for x in range(self.curr_rock.width):
                ref_pt = (x + self.current_origin[0], y + self.current_origin[1])
                #print("ref_pt = {}".format(ref_pt))
                
                if self.values[ref_pt[1]][ref_pt[0]] == "@":
                    self.values[ref_pt[1] - 1][ref_pt[0]] = "@"
                    self.values[ref_pt[1]][ref_pt[0]] = "."
            
        
        #self.values.pop()
                    
        self.current_origin = (self.current_origin[0], self.current_origin[1] - 1)
        
        return False
        
    def print_shaft(self):
        y = len(self.values) - 1
        
        shaft_str = "|" + (" " * self.num_cols) + "|\n"
        
        while y >= 0:
            row = "|"
            for x in range(self.num_cols):
                row = row + self.values[y][x]
            row = row + "|"
            shaft_str = shaft_str + row + "\n"
            y = y - 1
            
        shaft_str = shaft_str + "+" * (self.num_cols + 2)
            
        print(shaft_str + "\n")

orig_wind = []
wind = []
with open(infile) as input_file:
    for char in input_file.readline().strip():
        orig_wind.append(char)
        wind.append(char)
    
#print(wind)

shaft = Shaft()

#shaft.print_shaft()

shaft.place_new_rock()
#for row in shaft.values:
#    print(row)

#shaft.print_shaft()

rocks_to_place = 2022

while shaft.rocks_placed < rocks_to_place:

    if len(wind) == 0:
        wind = [x for x in orig_wind]

    direction = wind.pop(0)
    
    #print(direction)
    
    if direction == ">":
        
        if shaft.can_move_current_right():
            shaft.move_current_right()
            #shaft.print_shaft()
        else:
            #print("cannot move right")
            pass
        
    else:
        
        if shaft.can_move_current_left():
            shaft.move_current_left()
            #shaft.print_shaft()
        else:
            #print("cannot move left")
            pass
        
    is_rock_settled = shaft.move_down()
    #shaft.print_shaft()
    
    if is_rock_settled:
        
        if shaft.rocks_placed >= rocks_to_place:
            #shaft.print_shaft()
            break
            
        if shaft.rocks_placed % 1000 == 0:
            print("Placed {} rocks".format(shaft.rocks_placed))
            
        shaft.place_new_rock()
        #shaft.print_shaft()

    #curr_rock = rocks[rock_idx]
    
    #print(curr_rock)

    #rock_idx = rock_idx + 1
    #if rock_idx > 4:
    #    rock_idx = 0

    #break
    
print("Final height: {}".format(len(shaft.values)))

