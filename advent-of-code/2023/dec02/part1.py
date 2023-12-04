
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

game_id_sum = 0

for line in open(infile):
    line = line.strip()
    
    match_obj = re.match("Game (\d+): (.*)", line)
    game_id = int(match_obj.group(1))
    hands = match_obj.group(2)
    
    #print("id {}, hands \"{}\"".format(game_id, hands))
    
    hands = hands.split(";")
    is_valid = True
    
    for hand in hands:
        hand = hand.strip()
        hand_dict = {}
        for item in hand.split(","):
            item = item.strip()
            match_obj = re.match("(\d+) (red|blue|green)", item)
            num_cubes = int(match_obj.group(1))
            color = match_obj.group(2)
            hand_dict[color] = num_cubes
            
        if not is_hand_possible(hand_dict):
            is_valid = False
            break
        
        #print(hand_dict)
        
    if not is_valid:
        continue
        
    game_id_sum += game_id
    print("Game {} is possible".format(game_id))
    
print("Sum: {}".format(game_id_sum))
    

