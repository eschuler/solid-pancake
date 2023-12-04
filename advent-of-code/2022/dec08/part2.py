
#infile = "sample.txt"
infile = "input.txt"

tree_map = []

def get_scenic_score(tree_map, row_idx, col_idx):

    row_count = len(tree_map)
    col_count = len(tree_map[0])
    
    this_height = tree_map[row_idx][col_idx]
    scenic_score = 1
    
    # scan west
    curr_col_idx = col_idx - 1
    west_viewing_distance = 0
    while curr_col_idx >= 0:
        west_viewing_distance = west_viewing_distance + 1
        curr_height = tree_map[row_idx][curr_col_idx]
        
        if curr_height >= this_height:
            break
        
        curr_col_idx = curr_col_idx - 1
        
    #print(west_viewing_distance)
        
    scenic_score = scenic_score * west_viewing_distance
    if scenic_score == 0:
        return 0
    
    # scan east
    curr_col_idx = col_idx + 1
    east_viewing_distance = 0
    while curr_col_idx < col_count:
        east_viewing_distance = east_viewing_distance + 1
        curr_height = tree_map[row_idx][curr_col_idx]
        
        if curr_height >= this_height:
            break
        
        curr_col_idx = curr_col_idx + 1
        
    #print(east_viewing_distance)
        
    scenic_score = scenic_score * east_viewing_distance
    if scenic_score == 0:
        return 0
    
    # scan north
    curr_row_idx = row_idx - 1
    north_viewing_distance = 0
    while curr_row_idx >= 0:
        north_viewing_distance = north_viewing_distance + 1
        curr_height = tree_map[curr_row_idx][col_idx]
        
        if curr_height >= this_height:
            break
        
        curr_row_idx = curr_row_idx - 1
        
    #print(north_viewing_distance)
        
    scenic_score = scenic_score * north_viewing_distance
    if scenic_score == 0:
        return 0
    
    # scan south
    curr_row_idx = row_idx + 1
    south_viewing_distance = 0
    while curr_row_idx < row_count:
        south_viewing_distance = south_viewing_distance + 1
        curr_height = tree_map[curr_row_idx][col_idx]
        
        if curr_height >= this_height:
            break
        
        curr_row_idx = curr_row_idx + 1
        
    #print(south_viewing_distance)
        
    scenic_score = scenic_score * south_viewing_distance
        
    return scenic_score

for line in open(infile):
    line = line.strip()
    #print(line)
    
    row = []
    
    for value in line:
        row.append(int(value))
    
    tree_map.append(row)
    
#print(tree_map)

#get_scenic_score(tree_map, 1, 2)
#exit()

scenic_scores = []
max_score = 0

for i in range(len(tree_map[0])):
    score_row = []
    for j in range(len(tree_map)):
        score = get_scenic_score(tree_map, i, j)
        score_row.append(score)
        
        if score > max_score:
            max_score = score
            
    scenic_scores.append(score_row)
           
format_str = "{:3}" * len(scenic_scores[0])
for i in range(len(scenic_scores)):
    line_str = ""
    for j in range(len(scenic_scores[i])):
        line_str = line_str + "{:3}".format(scenic_scores[i][j])
    print(line_str)
    
print(max_score)