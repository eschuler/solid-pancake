
infile = "sample.txt"
#infile = "input.txt"

class Valve:

    def __init__(self, name, flow_rate):
        self.name = name
        self.flow_rate = flow_rate
        self.closed = True
        
    def open():
        self.closed = False

for line in open(infile):
    line = line.strip()
    print(line)


