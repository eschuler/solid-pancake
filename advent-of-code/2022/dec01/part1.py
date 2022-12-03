
infile = "input.txt"

calorie_counts = []
current_calories = 0

for line in open(infile):
    line = line.strip()
    #print(line)
    
    if len(line) == 0:
        calorie_counts.append(current_calories)
        current_calories = 0
        
    else:
        current_calories += int(line)
        
calorie_counts.append(current_calories)

#print(calorie_counts)

max_calories = 0

for x in calorie_counts:
    if x > max_calories:
        max_calories = x
        
print("Max calories: {}".format(max_calories))

