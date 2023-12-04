
#infile = "sample.txt"
#infile = "sample2.txt"
infile = "input.txt"

curr_register = 1
register_history = [curr_register]

def signal_strength(cycle_num):
    
    print("value = {}".format(register_history[cycle_num + 1]))

for line in open(infile):
    line = line.strip()
    #print(line)
    
    if line == "noop":
        register_history.append(curr_register)
        
    elif line.startswith("addx"):
        add_val = int(line.split()[1])
        register_history.append(curr_register)
        curr_register = curr_register + add_val
        register_history.append(curr_register)
        
    else:
        print("Error! {}".format(line))
        exit(1)
        
for i in range(len(register_history)):
    print("{} - {}".format(i+1, register_history[i]))
    
final_sum = 0
cycles = [20, 60, 100, 140, 180, 220]
for cycle in cycles:
    signal_strength = register_history[cycle-1] * cycle
    final_sum = final_sum + signal_strength
    print(signal_strength)
    print("Signal strength: {} - {}".format(cycle, signal_strength))
    print()
    
print("Final sum: {}".format(final_sum))
    

