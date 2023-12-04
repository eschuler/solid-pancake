
import re

#infile = "sample.txt"
infile = "input.txt"
    
monkeys = []

class Monkey:

    def __init__(self, id):
        self.id = id
        self.num_inspected_items = 0
        
    def take_turn(self):
        print("Monkey {}".format(self.id))
        
        for item in self.items:
            self.num_inspected_items = self.num_inspected_items + 1
            print("  Monkey inspects an item with a worry level of {}".format(item))
            
            if self.operand_is_num:
                operand = self.operand
            else:
                operand = item
                
            if self.operator == "+":
                new_worry = item + operand
                print("    Worry level increases by {} to {}".format(operand, new_worry))
            else:
                new_worry = item * operand
                print("    Worry level is multiplied by {} to {}".format(operand, new_worry))
                
            new_worry = int(new_worry / 3)
            print("    Monkey gets bored with item. Worry level is divided by 3 to {}".format(new_worry))
                
            if new_worry % self.test_val == 0:
                print("    Current worry level is divisible by {}".format(self.test_val))
                new_monkey = self.true_monkey
            else:
                print("    Current worry level is not divisible by {}".format(self.test_val))
                new_monkey = self.false_monkey
                
            print("    Item with worry level {} is thrown to monkey {}".format(new_worry, new_monkey))
            monkeys[new_monkey].items.append(new_worry)
            
        self.items = []
        
    def to_string(self):
        return "Monkey {}: {}".format(self.id, self.items)

for line in open(infile):
    line = line.strip()
    #print(line)
    
    monkey_regex    = re.compile("Monkey (\d+)")
    items_regex     = re.compile("Starting items: ([\d, ]*)")
    operation_regex = re.compile("Operation: new = old (\+|\*) (\d+|old)")
    test_regex      = re.compile("Test: divisible by (\d+)")
    true_regex      = re.compile("If true: throw to monkey (\d+)")
    false_regex     = re.compile("If false: throw to monkey (\d+)")
    
    match_obj = re.match("Monkey (\d+)", line)
    
    if monkey_regex.match(line):
        monkey_id = int(monkey_regex.match(line).group(1))
        #print("Id {}".format(monkey_id))
        curr_monkey = Monkey(monkey_id)
        
    elif items_regex.match(line):
        items = items_regex.match(line).group(1).split(", ")
        items_int = [int(x) for x in items]
        #print("Items: {}".format(items))
        curr_monkey.items = items_int
        
    elif operation_regex.match(line):
        match_obj = operation_regex.match(line)
        curr_monkey.operator = match_obj.group(1)
        
        if match_obj.group(2) == "old":
            curr_monkey.operand_is_num = False
        else:
            curr_monkey.operand_is_num = True
            curr_monkey.operand = int(match_obj.group(2))
            #print("Operator: {}, operand = {}".format(curr_monkey.operator, curr_monkey.operand))
        
    elif test_regex.match(line):
        test_val = int(test_regex.match(line).group(1))
        #print("Test value: {}".format(test_val))
        curr_monkey.test_val = test_val
        
    elif true_regex.match(line):
        true_monkey = int(true_regex.match(line).group(1))
        #print("True monkey: {}".format(true_monkey))
        curr_monkey.true_monkey = true_monkey
        
    elif false_regex.match(line):
        false_monkey = int(false_regex.match(line).group(1))
        #print("False monkey: {}".format(false_monkey))
        curr_monkey.false_monkey = false_monkey
        
    elif len(line) == 0:
        monkeys.append(curr_monkey)
        curr_monkey = None
        
    else:
        print("Could not parse line: " + line)
        exit(1)
        

monkeys.append(curr_monkey)
        
for monkey in monkeys:
    print(monkey.to_string())
        
print()
        
num_turns = 20
for i in range(num_turns):
    for monkey in monkeys:
        monkey.take_turn()
        
    print()
        
    print("After round {}, the monkeys are holding these items:".format(i+1))
    for monkey in monkeys:
        print(monkey.to_string())
        
print()
        
inspection_times = []
for monkey in monkeys:
    inspection_times.append(monkey.num_inspected_items)
    print("Monkey {} inspected items {} times".format(monkey.id, monkey.num_inspected_items))
    
sorted_times = sorted(inspection_times, reverse=True)
monkey_business = sorted_times[0] * sorted_times[1]

print("Monkey business: {}".format(monkey_business))
    
