
import re
import time

start_time = time.time()

#infile = "sample.txt"
infile = "input.txt"

class Sequence:

    def __init__(self, numbers):
        #self.offset = numbers[0]
        #self.numbers = [x - self.offset for x in numbers]
        self.numbers = numbers
        self.next_number = self.numbers[-1]
        
        self.diffs = []
        
        #print(self.to_string())
        
        current_nums = self.numbers
        all_zeros = False
        while not all_zeros:
            all_zeros = True
            
            current_diffs = []
            for i in range(len(current_nums) - 1):
                next_diff = current_nums[i+1] - current_nums[i]
                if next_diff != 0:
                    all_zeros = False
                current_diffs.append(next_diff)
            self.diffs.append(current_diffs)
            
            if self.numbers[0] == 7:
                print("    {}".format(current_diffs))
            
            self.next_number += current_diffs[-1]
            current_nums = current_diffs
        
    def to_string(self):
        return "{}, next number {}".format(self.numbers, self.next_number)

final_sum = 0

for line in open(infile):
    line = line.strip()
    
    s = Sequence([int(n) for n in line.split()])
    print(s.to_string())
    final_sum += s.next_number
    
    #break
        
print("final_sum: {}".format(final_sum))
end_time = time.time()

print("Elapsed time: {} seconds".format(end_time - start_time))

# guesses:
# 1901328346 (Too high)
    

