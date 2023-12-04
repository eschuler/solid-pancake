
import re

#infile = "sample.txt"
infile = "input.txt"

min_x = 999
max_x = -999
min_y = 0
max_y = -999

rock_lines = []

def get_manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

class Sensor:

    def __init__(self, position, closest_beacon):
        self.position = position
        self.closest_beacon = closest_beacon
        
    def get_dist_to_closest_beacon(self):
        return get_manhattan_distance(self.position, self.closest_beacon)
        
    def can_sense_row(self, row):
        return abs(self.position[1] - row) <= self.get_dist_to_closest_beacon()
        
    def can_sense_pos(self, pos):
        return get_manhattan_distance(self.position, pos) <= self.get_dist_to_closest_beacon()
        
    def get_x_range_for_row(self, row):
        if not self.can_sense_row(row):
            return None
        dist_to_row = abs(self.position[1] - row)
        remainder = self.get_dist_to_closest_beacon() - dist_to_row
        return (self.position[0] - remainder, self.position[0] + remainder)
        
    def to_string(self):
        return "Sensor: {}, closest beacon: {}".format(self.position, self.closest_beacon)
        
pattern = "Sensor at x=(\d+), y=(\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
sensors = []

min_x = 999
max_x = -999
min_y = 999
max_y = -999

for line in open(infile):
    line = line.strip()
    #print(line)
    
    match_obj = re.match(pattern, line)
    
    if match_obj is None:
        print("Failure!")
        exit(1)
        
    sensor_pos = (int(match_obj.group(1)), int(match_obj.group(2)))
    closest_beacon = (int(match_obj.group(3)), int(match_obj.group(4)))
    s = Sensor(sensor_pos, closest_beacon)
    
    if sensor_pos[0] < min_x: min_x = sensor_pos[0]
    if sensor_pos[0] > max_x: max_x = sensor_pos[0]
    if sensor_pos[1] < min_y: min_y = sensor_pos[1]
    if sensor_pos[1] > max_y: max_y = sensor_pos[1]
    if closest_beacon[0] < min_x: min_x = closest_beacon[0]
    if closest_beacon[0] > max_x: max_x = closest_beacon[0]
    if closest_beacon[1] < min_y: min_y = closest_beacon[1]
    if closest_beacon[1] > max_y: max_y = closest_beacon[1]
    
    sensors.append(s)

    #print("{} ({})".format(s.to_string(), s.get_dist_to_closest_beacon()))
    
print("Bounds: {}, {}\n".format((min_x, max_x), (min_y, max_y)))
    
#s = sensors[0]
#print("{} ({})".format(s.to_string(), s.get_dist_to_closest_beacon()))
#for i in range(-10, 30):
#    print("Can sensor reach row {}? {}".format(i, s.can_sense_row(i)))
#for x in range(min_x, max_x + 1):
#    for y in range(min_y, max_y + 1):
#        pos = (x,y)
#        can_sense = s.can_sense_pos(pos)
#        if can_sense:
#            print(pos)

#detections = {}
#for x in range(min_x, max_x + 1):
#    detections[x] = False

#row_n = 10
row_n = 2000000
x_ranges = []
for s in sensors:
    if not s.can_sense_row(row_n):
        continue
        
    print("{} ({})".format(s.to_string(), s.get_dist_to_closest_beacon()))
    
    x_range_for_row = s.get_x_range_for_row(row_n)
    #print("    x range: {}".format(x_range_for_row))
    
    x_ranges.append(x_range_for_row)
    #print()
    
print()
    
x_ranges = sorted(x_ranges, key=lambda x: x[0])
    
for r in x_ranges:
    print(r)
print()
    
i = 0
curr_range = x_ranges[i]
print("curr_range = {}".format(curr_range))

consolidated_ranges = []
while i < len(x_ranges) - 1:
    next_range = x_ranges[i+1]
    print("next_range = {}".format(next_range))
    
    if next_range[0] >= curr_range[0] and next_range[1] <= curr_range[1]:
        i = i + 1
    
    elif curr_range[1] >= next_range[0]:
        curr_range = (curr_range[0], next_range[1])
        print("curr_range = {}".format(curr_range))
        
    else:
        consolidated_ranges.append(curr_range)
        curr_range = next_range
        print("curr_range = {}".format(curr_range))
        
    
    i = i + 1
    
    #break
    
consolidated_ranges.append(curr_range)
print()

detections = 0
for r in consolidated_ranges:
    print(r)
    detections = detections + (r[1] - r[0] + 1)
print()
    
print("Removing beacon locations from count")
sensor_locs = []
for s in sensors:
    if s.closest_beacon[1] == row_n and s.closest_beacon not in sensor_locs:
        print(s.closest_beacon)
        sensor_locs.append(s.closest_beacon)
detections = detections - len(sensor_locs)
print()
        
print("Number of detections in row {}: {}".format(row_n, detections))

# Attempts:

# 4005518 (too low)

# Bounds: (-802154, 3980003), (-546524, 4282497)
#
# Sensor: (1333433, 35725), closest beacon: (1929144, 529341) (1089327)
# Sensor: (2219206, 337159), closest beacon: (1929144, 529341) (482244)
# Sensor: (2574308, 111701), closest beacon: (1929144, 529341) (1062804)
# Sensor: (3909938, 1033557), closest beacon: (3493189, -546524) (1996830)
# Sensor: (474503, 1200604), closest beacon: (-802154, 776650) (1700611)
# Number of detections in row 10: 4005518
