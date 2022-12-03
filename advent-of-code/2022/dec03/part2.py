
infile = "input.txt"

sum = 0

lines = []

for line in open(infile):
    line = line.strip()
    lines.append(line)
    #print(line)
    
i = 0

while i < len(lines) - 2:

    pack1 = lines[i]
    pack2 = lines[i+1]
    pack3 = lines[i+2]
    
    #print("Group {}:".format(i % 3))
    #print(pack1)
    #print(pack2)
    #print(pack3)
    #print()
    
    for letter in pack1:
        if letter in pack2 and letter in pack3:
            common_letter = letter
    
    priority = ord(common_letter)
    
    # lowercase
    if priority >= 97 and priority <= 122:
        priority = priority - 96
        
    # uppercase
    elif priority >= 65 and priority <= 90:
        priority = priority - 65 + 27
            
    #print("{} - {}".format(common_letter,  priority))
    
    sum = sum + priority
    
    i = i + 3
    
print(sum)

