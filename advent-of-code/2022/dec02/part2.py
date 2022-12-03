
infile = "input.txt"

total_score = 0

for line in open(infile):
    line = line.strip()
    #print(line)
    
    line_split = line.split()
    opponent = line_split[0]
    result = line_split[1]
    
    # need to lose
    if result == "X":
        if opponent == "A":
            mine = "Z"
        elif opponent == "B":
            mine = "X"
        elif opponent == "C":
            mine = "Y"
            
    # need to draw
    elif result == "Y":
        if opponent == "A":
            mine = "X"
        elif opponent == "B":
            mine = "Y"
        elif opponent == "C":
            mine = "Z"
    
    # need to win 
    elif result == "Z":
        if opponent == "A":
            mine = "Y"
        elif opponent == "B":
            mine = "Z"
        elif opponent == "C":
            mine = "X"
    
    if mine == "X":
        my_score = 1
    elif mine == "Y":
        my_score = 2
    elif mine == "Z":
        my_score = 3
        
    # 3 points for draw
    if result == "Y":
        my_score = my_score + 3
        
    # 6 points for win
    if result == "Z":
        my_score = my_score + 6
    
    #print(my_score)
    
    total_score = total_score + my_score
    
print(total_score)

