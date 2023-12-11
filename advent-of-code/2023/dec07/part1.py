
import re
import time

start_time = time.time()

#infile = "sample.txt"
infile = "input.txt"

#ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

card_to_hex = {
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "T": "a",
    "J": "b",
    "Q": "c",
    "K": "d",
    "A": "e"
}

#     2 3 4 5 6 7 8 9 T J Q K A
# 0 1 2 3 4 5 6 7 8 9 A B C D E F

# 32T3K 765 32A3D 207421 one pair
# KTJJT 220 DABBA 895930 two pair
# KK677 28  DD677 906871 two pair
# T55J5 684 A55B5 677301 3oak
# QQQJA 483 CCCBE 838846 3oak

class Hand:

    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = int(bid)
        self.hand_to_hex()
        
        self.card_count = {}
        for c in self.cards:
            if c in self.card_count.keys():
                self.card_count[c] += 1
            else:
                self.card_count[c] = 1
                
        self.card_types = self.card_count.keys()
        self.card_counts = sorted([x[1] for x in self.card_count.items()])
        
        self.hand_type = ""
        
        if self.is_five_of_a_kind():
            self.hand_type = "5 of a kind"
        elif self.is_four_of_a_kind():
            self.hand_type = "4 of a kind"
        elif self.is_full_house():
            self.hand_type = "full house"
        elif self.is_three_of_a_kind():
            self.hand_type = "three of a kind"
        elif self.is_two_pair():
            self.hand_type = "two pair"
        elif self.is_one_pair():
            self.hand_type = "one pair"
        else:
            self.hand_type = "high card"
        
    def hand_to_hex(self):
        self.hex_str = "0x"
        for c in self.cards:
            self.hex_str += card_to_hex[c]
        self.hex_num = int(self.hex_str, 16)
        
    def is_five_of_a_kind(self):
        return len(self.card_types) == 1
        
    def is_four_of_a_kind(self):
        return len(self.card_types) == 2 and self.card_counts == [1, 4]
        
    def is_full_house(self):
        return len(self.card_types) == 2 and self.card_counts == [2, 3]
        
    def is_three_of_a_kind(self):
        return len(self.card_types) == 3 and self.card_counts == [1, 1, 3]
        
    def is_two_pair(self):
        return len(self.card_types) == 3 and self.card_counts == [1, 2, 2]
        
    def is_one_pair(self):
        return len(self.card_types) == 4 and self.card_counts == [1, 1, 1, 2]
        
    def is_high_card(self):
        return len(self.card_types) == 5
        
    def to_string(self):
        return "{} {:<3} {} {} {}".format( \
            "".join(self.cards), \
            self.bid, \
            self.hex_str, \
            self.hex_num, \
            self.hand_type)
            
hands = []

for line in open(infile):
    line = line.strip()
    
    line_split = line.split()
    
    hands.append(Hand(line_split[0], line_split[1]))
    
five = []
four = []
full_house = []
three = []
two = []
one = []
high = []
    
for h in hands:
    #print(h.to_string())
    
    if h.is_five_of_a_kind():
        five.append(h)
    elif h.is_four_of_a_kind():
        four.append(h)
    elif h.is_full_house():
        full_house.append(h)
    elif h.is_three_of_a_kind():
        three.append(h)
    elif h.is_two_pair():
        two.append(h)
    elif h.is_one_pair():
        one.append(h)
    else:
        high.append(h)
        
final_list = sorted(high, key=lambda hand: hand.hex_num) + \
    sorted(one, key=lambda hand: hand.hex_num) + \
    sorted(two, key=lambda hand: hand.hex_num) + \
    sorted(three, key=lambda hand: hand.hex_num) + \
    sorted(full_house, key=lambda hand: hand.hex_num) + \
    sorted(four, key=lambda hand: hand.hex_num) + \
    sorted(five, key=lambda hand: hand.hex_num)
    
final_sum = 0

for i in range(len(final_list)):
    h = final_list[i]
    final_sum += (i + 1) * h.bid
    print(h.to_string())
        
print("final_sum: {}".format(final_sum))
end_time = time.time()

print("Elapsed time: {} seconds".format(end_time - start_time))
    

