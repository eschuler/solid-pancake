
infile = "input.txt"

sum = 0

def contains(start, end, val):
    return val >= start and val <= end

def fully_contains(start1, end1, start2, end2):
    return contains(start1, end1, start2) and contains(start1, end1, end2)
    
count = 0

for line in open(infile):
    line = line.strip()
    
    line_split = line.split(",")
    range1 = line_split[0]
    range2 = line_split[1]
    
    range1_split = range1.split("-")
    range1_s = int(range1_split[0])
    range1_e = int(range1_split[1])
    
    range2_split = range2.split("-")
    range2_s = int(range2_split[0])
    range2_e = int(range2_split[1])
    
    if fully_contains(range1_s, range1_e, range2_s, range2_e) or fully_contains(range2_s, range2_e, range1_s, range1_e):
        count = count + 1
        
print(count)

