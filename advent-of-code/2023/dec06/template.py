
import re
import time

start_time = time.time()

#infile = "sample.txt"
#infile = "input.txt"

class Item:

    def __init__(self):
        pass
        
    def to_string(self):
        return ""
            
def print_cards():
    print()
    for c in cards:
        print(c.to_string())

for line in open(infile):
    line = line.strip()
    
    # do something with line
        
#print(": {}".format(my_sum))
end_time = time.time()

print("Elapsed time: {} seconds".format(end_time - start_time))
    

