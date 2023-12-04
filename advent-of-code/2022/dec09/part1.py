
#infile = "sample.txt"
infile = "input.txt"

start = [0, 0]
head  = [0, 0]
tail  = [0, 0]

tail_locs = {}
tail_locs[0] = {}
tail_locs[0][0] = True

def adjacent():
    if head == tail:
        return True
        
    return abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1
    
def is_diagonal():
    if head == tail: return False
    
    if head[0] == tail[0] or head[1] == tail[1]: return False
    
    return True
    
def print_board():
    board = ""
    for i in range(5):
        row = ""
        for j in range(6):
            if head[0] == i and head[1] == j:
                row = row + "H"
            elif tail[0] == i and tail[1] == j:
                row = row + "T"
            elif i == 0 and j == 0:
                row = row + "s"
            else:
                row = row + "."
        board = row + "\n" + board
    print(board)

def step(direction):

    orig_head = []
    orig_head.append(head[0])
    orig_head.append(head[1])

    # right
    if direction == "R":
        head[1] = head[1] + 1

    # left
    if direction == "L":
        head[1] = head[1] - 1

    # up
    if direction == "U":
        head[0] = head[0] + 1

    # down
    if direction == "D":
        head[0] = head[0] - 1
        
    if not adjacent():
        #print("orig_head : {}".format(orig_head))
        tail[0] = orig_head[0]
        tail[1] = orig_head[1]
        
        if tail[0] not in tail_locs.keys():
            tail_locs[tail[0]] = {}
        tail_locs[tail[0]][tail[1]] = True
        
print_board()

idx = 0

for line in open(infile):
    line = line.strip()
    #print("== " + line + " ==\n")
    
    line_split = line.split()
    
    direction = line_split[0]
    amount = int(line_split[1])
    
    for i in range(amount):
        step(direction)
        #print("new head: {}".format(head))
        #print("new tail: {}".format(tail))
        #print_board()
    
    idx = idx + 1
    
#print(adjacent())
    
num_tail_locs = 0
for x in sorted(tail_locs.keys()):
    for y in sorted(tail_locs[x].keys()):
        print("({}, {})".format(x, y))
        num_tail_locs = num_tail_locs + 1
        
print("{} total".format(num_tail_locs))
    
    

