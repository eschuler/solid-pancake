
import re

infile = "input.txt"

numbers = []

regex1 = re.compile("[a-z]*([0-9])")
regex2 = re.compile(".*([0-9])[a-z]*")

num_sum = 0

for line in open(infile):
    line = line.strip()
    
    match1 = regex1.match(line)
    
    if match1 is None:
        print("Invalid match1! " + line)
        continue
    
    match2 = regex2.match(line)
    
    if match2 is None:
        print("Invalid match2! " + line)
        continue
    
    digits = "{}{}".format(match1.group(1), match2.group(1))
    num = int(digits)
    num_sum += num
    
print("Sum = {}".format(num_sum))

