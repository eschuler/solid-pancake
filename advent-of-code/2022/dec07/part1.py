
import os
class DataObject:

    def __init__(self, is_dir, name, size=0):
        self.is_dir = is_dir
        self.name = name
        self.sub_objects = []
        
        if not is_dir:
            self.size = size
        else:
            self.size = 0
        
    def add_object(self, path):
        if obj in self.sub_objects:
            print("Cannot add " + obj.name + " to " + self.name + "; object already exists!")
        else:
            self.sub_objects.append(obj)
            
    def print(self, level=0):
        for item in self.sub_objects:
            item.print(level + 1)
            
def find(top_level_obj, path):
    path_split = file_path.split("/")
    
    if (len(path_split)) == 1:
        for obj in top_level_obj.sub_objects:
            if obj == path_split[0]:
                return obj
            
def print_tree(top_level_obj, indent):
    for obj in top_level_obj.sub_objects:
        print(indent + obj.name)

def add_file(top_level_obj, file_path, size):
    path_split = file_path.split("/")
    if len(path_split) == 1:
        top_level_obj.sub_objects.append(DataObject(False, path_split[0], size))

def add_dir(top_level_obj, dir_path):
    path_split = file_path.split("/")
    
    if len(path_split) == 1:
        top_level_obj.sub_objects.append(DataObject(True, path_split[0], size))
        
    else:
        add_dir

def get_sub_obj(obj, path):
    path_split = path.split("/")
    
def get_total_size(dir_sizes, path):

    total_size = 0
    
    for dir_path, dir_size in dir_sizes.items():
        if dir_path.startswith(path):
            total_size = total_size + dir_size
            
    return total_size
            
if __name__ == "__main__":
    #infile = "sample.txt"
    infile = "input.txt"
    
    top_level_obj = DataObject(True, "/")
    
    processing_ls = False
    
    file_sizes = {}
    dir_sizes = {}

    for line in open(infile):
        line = line.strip()
        #print(line)
        
        # command
        if line.startswith("$"):
        
            processing_ls = False
        
            # cd command
            if line.startswith("$ cd"):
                cmd_split = line.split()
                new_dir = cmd_split[2]
                
                # absolute path
                if new_dir == "/":
                    current_path = new_dir
                    
                # cd up a directory
                elif new_dir == "..":
                    current_path = os.path.split(current_path)[0]
                    
                # relative path
                else:
                    current_path = os.path.join(current_path, new_dir)
                
                print("    current_path = " + current_path)
                
                #if current_path not in current_obj.keys():
                #    directory[current_path] = DataObject(True, current_path)
            
            elif line.startswith("$ ls"):
                processing_ls = True
            
            else:
                print("Unrecognized command!")
            
        # result of ls
        else:
            if not processing_ls:
                print("Error! Non command line when not processing ls!")
                continue
                
            line_split = line.split()
            
            # sub dir
            if line_split[0] == "dir":
                pass

            # sub file
            else:
                file_size = int(line_split[0])
                if current_path not in dir_sizes.keys():
                    dir_sizes[current_path] = file_size
                else:
                    dir_sizes[current_path] = dir_sizes[current_path] + file_size
                    
                file_sizes[os.path.join(current_path, line_split[1])] = file_size
                
    total_total_size = 0
    
    for dir_path in dir_sizes.keys():
        total_size = get_total_size(dir_sizes, dir_path)
        
        print("{}: {}".format(dir_path, total_size))
            
        if total_size <= 100000:
            total_total_size = total_total_size + total_size
            #print("{}: {}".format(dir_path, total_size))
            
    print(total_total_size)