
import re

#infile = "sample.txt"
infile = "input.txt"

min_x = 0
max_x = 20
min_y = 0
max_y = 20

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
        
    def get_vertices(self):
        x = self.position[0]
        y = self.position[1]
        length = self.get_dist_to_closest_beacon()
        
        vertices = []
        vertices.append((x, y - length))
        vertices.append((x + length, y))
        vertices.append((x, y + length))
        vertices.append((x - length, y))
        
        return vertices
        
    def to_string(self):
        return "Sensor: {}, closest beacon: {}".format(self.position, self.closest_beacon)
        
pattern = "Sensor at x=(\d+), y=(\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
sensors = []

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
    
    sensors.append(s)

    #print("{} ({})".format(s.to_string(), s.get_dist_to_closest_beacon()))
    
for s in sensors:
    print("{} ({})".format(s.to_string(), s.get_dist_to_closest_beacon()))
    print("    {}".format(s.get_vertices()))