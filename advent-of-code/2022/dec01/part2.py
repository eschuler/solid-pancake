
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

top_three = [0, 0, 0]

for x in calorie_counts:
    if x > top_three[0]:
        top_three[2] = top_three[1]
        top_three[1] = top_three[0]
        top_three[0] = x
    elif x > top_three[1]:
        top_three[2] = top_three[1]
        top_three[1] = x
    elif x > top_three[2]:
        top_three[2] = x

print("Max calories:\n{}\n{}\n{}".format(top_three[0], top_three[1], top_three[2]))
print("Total: {}".format(top_three[0] + top_three[1] + top_three[2]))

