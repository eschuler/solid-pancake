
import os

class Directory:

    def __init__(self, name):
        self.name = name
        self.sub_dirs = []
        self.files = []
        
    def to_string(self):
        return "- {} (dir)".format(self.name)
        
    def get_size(self):
        size = 0
        for sub_dir in self.sub_dirs:
            size = size + sub_dir.get_size()
        for file in self.files:
            size = size + file.size
            
        return size
        
class File:

    def __init__(self, name, size):
        self.name = name
        self.size = size
        
    def to_string(self):
        return "- {} (file, size={})".format(self.name, self.size)
        
def print_dir(dir_obj, indent=0):
    
    print("{}{}".format("  " * indent, dir_obj.to_string()))
    
    for sub_dir in dir_obj.sub_dirs:
        print_dir(sub_dir, indent + 1)
    
    for file in dir_obj.files:
        print("{}{}".format("  " * (indent + 1), file.to_string()))
        
def add_dir(top_level_obj, path):

    #print("add_dir({}, {})".format(top_level_obj.name, path))

    if path.startswith("/"):
        path = path[1:]

    path_split = path.split("/")
    #print("path_split: {}".format(path_split))
    
    if len(path_split) == 1:
        new_dirname = path_split[0]
        
        for existing_subdir in top_level_obj.sub_dirs:
            if existing_subdir.name == new_dirname:
                print("Error! {} already contains directory {}".format(top_level_obj.name, new_dir))
                exit(1)

        top_level_obj.sub_dirs.append(Directory(new_dirname))
        
    else:
        subdir_name = path_split[0]
        
        found_subdir = False
        for existing_subdir in top_level_obj.sub_dirs:
            if existing_subdir.name == subdir_name:
                add_dir(existing_subdir, "/".join(path_split[1:]))
                found_subdir = True
                
        if not found_subdir:
            new_subdir = Directory(subdir_name)
            top_level_obj.sub_dirs.append(new_subdir)
            add_dir(new_subdir, "/".join(path_split[1:]))
        
def add_file(top_level_obj, path, size):

    #print("add_dir({}, {})".format(top_level_obj.name, path))

    if path.startswith("/"):
        path = path[1:]

    path_split = path.split("/")
    #print("path_split: {}".format(path_split))
    
    if len(path_split) == 1:
        file_name = path_split[0]
        
        for existing_file in top_level_obj.files:
            if existing_file == file_name:
                print("Error! {} already contains file {}".format(top_level_obj.name, file_name))
                exit(1)

        top_level_obj.files.append(File(file_name, size))
        
    else:
        subdir_name = path_split[0]
        
        found_subdir = False
        for existing_subdir in top_level_obj.sub_dirs:
            if existing_subdir.name == subdir_name:
                add_file(existing_subdir, "/".join(path_split[1:]), size)
                found_subdir = True
                
        if not found_subdir:
            new_subdir = Directory(subdir_name)
            top_level_obj.files.append(new_subdir)
            add_file(new_subdir, "/".join(path_split[1:]), size)
            
def traverse(top_level_obj, sizes):

    sizes[top_level_obj.name] = top_level_obj.get_size()
    
    for sub_dir in top_level_obj.sub_dirs:
        traverse(sub_dir, sizes)
            
if __name__ == "__main__":
    #infile = "sample.txt"
    infile = "input.txt"
    
    top_level_obj = Directory("/")
    
    #print_dir(top_level_obj)
    #print()
    
    processing_ls = False

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
                
                #print("    current_path = " + current_path)
                
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
                add_dir(top_level_obj, os.path.join(current_path, line_split[1]))
    
                #print_dir(top_level_obj)
                #print()

            # sub file
            else:
                add_file(top_level_obj, os.path.join(current_path, line_split[1]), int(line_split[0]))
    
                #print_dir(top_level_obj)
                #print()
    
    print_dir(top_level_obj)
    print()
    
    #print(top_level_obj.get_size())
    
    sizes = {}
    traverse(top_level_obj, sizes)
    
    total_size = 0
    
    for dir_name, size in sizes.items():
        #print("{} - {}".format(dir_name, size))
        
        if size <= 100000:
            print("{} - {}".format(dir_name, size))
            total_size = total_size + size
        
    print("\n{}".format(total_size))
