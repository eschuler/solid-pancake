
infile = "input.txt"

total_score = 0

for line in open(infile):
    line = line.strip()
    #print(line)
    
    line_split = line.split()
    opponent = line_split[0]
    mine = line_split[1]
    
    if mine == "X":
        my_score = 1
    elif mine == "Y":
        my_score = 2
    elif mine == "Z":
        my_score = 3
        
    # 3 points for draw
    if opponent == "A" and mine == "X" or opponent == "B" and mine == "Y" or opponent == "C" and mine == "Z":
        my_score = my_score + 3
        
    # 6 points for win
    if opponent == "A" and mine == "Y" or opponent == "B" and mine == "Z" or opponent == "C" and mine == "X":
        my_score = my_score + 6
    
    #print(my_score)
    
    total_score = total_score + my_score
    
print(total_score)

