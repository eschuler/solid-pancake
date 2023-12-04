
import re

infile = "input.txt"

numbers = []

first_digit_regex = re.compile("[a-z]*([0-9])")
first_word_regex = re.compile("[a-z]*(one|two|three|four|five|six|seven|eight|nine)")
last_digit_regex = re.compile(".*([0-9])[a-z]*")
last_word_regex = re.compile(".*(one|two|three|four|five|six|seven|eight|nine)[a-z]*")

num_sum = 0

converter = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

for line in open(infile):
    line = line.strip()
    print(line)
    
    digits = ""
    
    first_digit_match = re.search("[0-9]", line)
    word_pattern = "one|two|three|four|five|six|seven|eight|nine"
    first_word_match = re.search("(" + word_pattern + ")", line)
    last_digit_match = re.search("[0-9]", line[::-1])
    last_word_match = re.search("(" + word_pattern[::-1] + ")", line[::-1])
    
    first_word = ""
    first_word_idx = -1
    if first_word_match is not None:
        first_word = first_word_match.group(0)
        first_word_idx = line.find(first_word)
    
    last_word = ""
    last_word_idx = -1
    if last_word_match is not None:
        last_word = last_word_match.group(0)[::-1]
        #print(line[::-1])
        #print(line[::-1].find(last_word_match.group(0)))
        #print(len(line) - line[::-1].find(last_word_match.group(0)))
        #print(len(line) - line[::-1].find(last_word_match.group(0)) - len(last_word))
        last_word_idx = len(line) - line[::-1].find(last_word_match.group(0)) - len(last_word)
        
    first_digit = ""
    first_digit_idx = -1
    if first_digit_match is not None:
        first_digit = first_digit_match.group(0)
        first_digit_idx = line.find(first_digit)
        
    last_digit = ""
    last_digit_idx = -1
    if last_digit_match is not None:
        last_digit = last_digit_match.group(0)
        last_digit_idx = len(line) - line[::-1].find(last_digit) - 1
        
    #print("    first: {}, idx {}; {}, idx {}".format(first_digit, first_digit_idx, first_word, first_word_idx))
    #print("    last: {}, idx {}; {}, idx {}".format(last_digit, last_digit_idx, last_word, last_word_idx))
    
    if first_word_idx >= 0 and first_digit_idx >= 0:
        if first_word_idx < first_digit_idx:
            first_number = converter[first_word]
        else:
            first_number = int(first_digit)
    elif first_word_idx >= 0:
        first_number = converter[first_word]
    else:
        first_number = int(first_digit)
    
    if last_word_idx >= 0 and last_digit_idx >= 0:
        if last_word_idx > last_digit_idx:
            last_number = converter[last_word]
        else:
            last_number = int(last_digit)
    elif last_word_idx >= 0:
        last_number = converter[last_word]
    else:
        last_number = int(last_digit)
    
    digits = "{}{}".format(first_number, last_number)
    #print(digits)
    num = int(digits)
    num_sum += num
    
print("Sum = {}".format(num_sum))

