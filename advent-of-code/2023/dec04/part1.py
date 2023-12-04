
import re

#infile = "sample.txt"
infile = "input.txt"

total_sum = 0

point_totals = [1]
for i in range(100):
    point_totals.append(point_totals[i] * 2)
#print(point_totals[:10])

for line in open(infile):
    line = line.strip()
    
    match_obj = re.match("Card +(\d+): ([\d ]+) \| ([\d ]+)", line)
    
    if match_obj is None:
        print("No regex match!" + line)
        continue
        
    winning_numbers = sorted([int(x) for x in match_obj.group(2).split()])
    my_numbers = sorted([int(x) for x in match_obj.group(3).split()])
    
    num_winning_numbers = 0
    
    for n in winning_numbers:
        if n in my_numbers:
            num_winning_numbers += 1
            
    if num_winning_numbers > 0:
        total_sum += point_totals[num_winning_numbers - 1]
        
    #print("Card # {}, winning numbers {}, my numbers {}".format(
    #    match_obj.group(1), 
    #    winning_numbers, 
    #    my_numbers))
    #print("Winning numbers: {}".format(num_winning_numbers))
    
print("Total sum: {}".format(total_sum))
        
    
    

