
import re

infile = "input.txt"

max_cubes = {
    "red":12,
    "green":13,
    "blue":14
}

def is_hand_possible(hand_dict):

    for color, num in hand_dict.items():
        if num > max_cubes[color]:
            return False
    
    return True
    
def calculate_power(min_red, min_green, min_blue):
    return min_red * min_green * min_blue
    
print("power = {}".format(calculate_power(4,2,6)))

total_sum = 0

for line in open(infile):
    line = line.strip()
    
    match_obj = re.match("Game (\d+): (.*)", line)
    game_id = int(match_obj.group(1))
    hands = match_obj.group(2)
    
    #print("id {}, hands \"{}\"".format(game_id, hands))
    
    hands = hands.split(";")
    is_valid = True
    
    min_cubes = {
        "red":0,
        "green":0,
        "blue":0
    }
    
    for hand in hands:
        hand = hand.strip()
        hand_dict = {
            "red":0,
            "green":0,
            "blue":0
        }
        
        for item in hand.split(","):
            item = item.strip()
            match_obj = re.match("(\d+) (red|blue|green)", item)
            num_cubes = int(match_obj.group(1))
            color = match_obj.group(2)
            hand_dict[color] = num_cubes
            
        if hand_dict["red"] > min_cubes["red"]:
            min_cubes["red"] = hand_dict["red"]
        if hand_dict["green"] > min_cubes["green"]:
            min_cubes["green"] = hand_dict["green"]
        if hand_dict["blue"] > min_cubes["blue"]:
            min_cubes["blue"] = hand_dict["blue"]
            
    power = calculate_power(min_cubes["red"], min_cubes["green"], min_cubes["blue"])
    print("{}: {}".format(power, min_cubes))
    total_sum += power
    
print("Sum: {}".format(total_sum))
    

