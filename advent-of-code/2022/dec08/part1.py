
#infile = "sample.txt"
infile = "input.txt"

tree_map = []

def is_visible(tree_map, row_idx, col_idx):

    row_count = len(tree_map)
    col_count = len(tree_map[0])

    # top and bottom rows
    if row_idx == 0 or row_idx == (row_count - 1):
        return True
        
    # left and right most columns
    if col_idx == 0 or col_idx == (col_count - 1):
        return True
        
    current_height = tree_map[row_idx][col_idx]
    
    left_visible = True
    for j in range(0, col_idx):
        if tree_map[row_idx][j] >= current_height:
            left_visible = False
    
    right_visible = True
    for j in range(col_idx + 1, col_count):
        if tree_map[row_idx][j] >= current_height:
            right_visible = False
    
    up_visible = True
    for i in range(0, row_idx):
        if tree_map[i][col_idx] >= current_height:
            up_visible = False
    
    down_visible = True
    for i in range(row_idx + 1, row_count):
        if tree_map[i][col_idx] >= current_height:
            down_visible = False
            
    #print("left_visible: {}".format(left_visible))
    #print("right_visible: {}".format(right_visible))
    #print("up_visible: {}".format(up_visible))
    #print("down_visible: {}".format(down_visible))
        
    return left_visible or right_visible or up_visible or down_visible

for line in open(infile):
    line = line.strip()
    #print(line)
    
    row = []
    
    for value in line:
        row.append(int(value))
    
    tree_map.append(row)
    
#print(tree_map)

visibility = []
num_visible = 0

for i in range(len(tree_map[0])):
    viz_row = []
    for j in range(len(tree_map)):
        visibile = is_visible(tree_map, i, j)
        
        if visibile:
            viz_row.append("V")
            num_visible = num_visible + 1
        else:
            viz_row.append("x")
            
    visibility.append(viz_row)
           
for i in range(len(visibility)):
    print("".join(visibility[i]))
    
print(num_visible)

# tried:
# 1328 (too low)