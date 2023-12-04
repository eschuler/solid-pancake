
infile = "input.txt"

code = ""

def contains_repeat(substring):
    for i in range(len(substring)):
        for j in range(i+1, len(substring)):
            if substring[i] == substring[j]:
                return False
    return True
            

for line in open(infile):
    code = line.strip()

print(code)

curr_idx = 0

while curr_idx < len(code) - 3:
    window = ""
    window = code[curr_idx : curr_idx + 4]

    has_repeats = contains_repeat(window)
    print("{} - {}".format(window, has_repeats))
    
    if has_repeats:
        break
    
    curr_idx = curr_idx + 1
    
print(curr_idx + 4)

