
# guesses:
# 53900 (too high)

import re

infile = "input.txt"

num_sum = 0

for line in open(infile):
    line = line.strip()
    #print(line)

    digits = []
    
    current_string = ""
    for char in line:
        if re.match("[0-9]", char) is not None:
            digits.append(int(char))
            current_string = ""
        else:
            current_string += char
            if re.match(".*one", current_string) is not None:
                digits.append(1)
                current_string = ""
            elif re.match(".*two", current_string) is not None:
                digits.append(2)
                current_string = ""
            elif re.match(".*three", current_string) is not None:
                digits.append(3)
                current_string = ""
            elif re.match(".*four", current_string) is not None:
                digits.append(4)
                current_string = ""
            elif re.match(".*five", current_string) is not None:
                digits.append(5)
                current_string = ""
            elif re.match(".*six", current_string) is not None:
                digits.append(6)
                current_string = ""
            elif re.match(".*seven", current_string) is not None:
                digits.append(7)
                current_string = ""
            elif re.match(".*eight", current_string) is not None:
                digits.append(8)
                current_string = ""
            elif re.match(".*nine", current_string) is not None:
                digits.append(9)
                current_string = ""
        #print("digits: {}, current_string: {}".format(digits, current_string))
    
    first_last = "{}{}".format(digits[0], digits[-1])
    #print("{}: {}".format(digits, first_last))
    #print(digits)
    num = int(first_last)
    num_sum += num
    
    #break
    
print("Sum = {}".format(num_sum))

