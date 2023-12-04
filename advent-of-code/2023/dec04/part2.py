
import re

#infile = "sample.txt"
infile = "input.txt"

class Card:

    def __init__(self, card_num, winning_numbers, my_numbers):
        self.card_num = card_num
        self.winning_numbers = sorted([int(x) for x in match_obj.group(2).split()])
        self.my_numbers = sorted([int(x) for x in match_obj.group(3).split()])
    
        self.num_winning_numbers = 0

        for n in self.winning_numbers:
            if n in self.my_numbers:
                self.num_winning_numbers += 1
                
        self.num_copies = 1
        
    def to_string(self):
        #return "Card # {}, winning numbers {}, my numbers {}, # matching {}, # copies: {}".format(
        return "Card # {}, # matching {}, # copies: {}".format(
            self.card_num, 
            #self.winning_numbers, 
            #self.my_numbers,
            self.num_winning_numbers,
            self.num_copies)
            
def print_cards():
    print()
    for c in cards:
        print(c.to_string())
            
cards = []

for line in open(infile):
    line = line.strip()
    
    match_obj = re.match("Card +(\d+): ([\d ]+) \| ([\d ]+)", line)
    
    if match_obj is None:
        print("No regex match!" + line)
        continue
        
    this_card = Card(match_obj.group(1), match_obj.group(2), match_obj.group(3))
    
    #print(this_card.to_string())
    
    cards.append(this_card)
    
#print_cards()
num_scratch_cards = 0
    
while len(cards) > 0:

    for i in range(cards[0].num_winning_numbers):
        cards[i + 1].num_copies += 1

    num_scratch_cards += 1
    cards[0].num_copies -= 1

    if cards[0].num_copies == 0:
        cards.pop(0)

    #print_cards()

    #break
        
print("# scratch cards: {}".format(num_scratch_cards))
    

