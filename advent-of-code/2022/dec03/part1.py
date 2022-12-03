
infile = "input.txt"

sum = 0

for line in open(infile):
    line = line.strip()
    #print(line)
    
    num_items = len(line)
    num_items_per_compartment = int(num_items / 2)
    comp1 = line[:num_items_per_compartment]
    comp2 = line[num_items_per_compartment:]
    
    #print(comp1)
    #print(comp2)
    #print()
    
    for letter in comp1:
        if letter in comp2:
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
    
print(sum)

