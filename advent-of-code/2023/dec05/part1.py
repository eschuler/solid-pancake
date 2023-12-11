
import re
import time

start_time = time.time()

#infile = "sample.txt"
infile = "input.txt"

class Mapping:

    def __init__(self, name):
        self.name = name
        self.mappings = []
    
    def add_range(self, new_dest_start, new_source_start, new_range_length):
        self.mappings.append((new_dest_start, new_source_start, new_range_length))
        
    def transform(self, source_num):
    
        dest_num = source_num
    
        for m in self.mappings:
            dest_range_start = m[0]
            source_range_start = m[1]
            range_length = m[2]
            source_range_end = source_range_start + range_length
            
            if source_num >= source_range_start and source_num < source_range_end:
                #print("    Transform match: {}".format((dest_range_start, source_range_start, range_length)))
                dest_num = \
                    source_range_start - \
                    (source_range_start - dest_range_start) + \
                    (source_num - source_range_start)
                break
                
        return dest_num
        
    def to_string(self):
        return_val = "{} map:".format(self.name)
        for m in self.mappings:
            return_val += " ({}, {}, {})".format(m[0], m[1], m[2])
        return return_val
        
m = Mapping("seed-to-soil")
m.add_range(50, 98, 2)
m.add_range(52, 50, 48)

#print("{:<6}{:<6}".format("Seed", "Soil"))
#for i in range(101):
#    print("{:<6}{:<6}".format(i, m.transform(i)))

seeds = []
mappings = []
current_map = None

for line in open(infile):
    line = line.strip()
    
    # skip empty lines
    if len(line) == 0:
        if current_map is not None:
            mappings.append(current_map)
            current_map = None
        continue
    
    match_obj = re.match("seeds: ([\d ]+)", line)
    if match_obj is not None:
        seeds = [int(x) for x in match_obj.group(1).split()]
        print("\nSeeds: {}".format(seeds))
        continue
        
    match_obj = re.match("([a-z-]+) map:", line)
    if match_obj is not None:
        current_map = Mapping(match_obj.group(1))
        continue
        
    match_obj = re.match("(\d+) (\d+) (\d+)", line)
    if match_obj is not None:
        #print(match_obj)
        nums = [int(x) for x in match_obj.groups()]
        #print("nums: {}".format(nums))
        if current_map is not None:
            current_map.add_range(nums[0], nums[1], nums[2])
            continue
    
if current_map is not None:
    mappings.append(current_map)
    current_map = None
    
#for m in mappings:
#    print("\n" + m.to_string())

locations = []

for seed_num in seeds:
    loc_num = seed_num
    #print("Seed {}".format(seed_num))
    for mapping in mappings:
        loc_num = mapping.transform(loc_num)
        #print("After {}, {}".format(mapping.name, loc_num))
    print("Seed {}: location {}".format(seed_num, loc_num))
    locations.append(loc_num)
    #break
        
print("Lowest location: {}".format(min(locations)))
end_time = time.time()

print("\nElapsed time: {} seconds".format(end_time - start_time))
    

