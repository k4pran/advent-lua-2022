import sys
from typing import List

COMMAND_SYMB = '$'
COMMAND_CD = "cd"
COMMAND_LS = "ls"

ROOT_DIR =  "/"
PARENT_DIR = ".."

DIR = "dir"


class ElfFile:

    def __init__(self, name, file_size):
        self.name = name
        self.file_size = int(file_size)


class ElfDirectory:

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.sub_directories: List[ElfDirectory] = []
        self.files: List[ElfFile] = []

    def get_files_size(self):
        return sum([f.file_size for f in self.files])

    def get_dir_size(self):
        return sum([d.get_files_size() for d in self.get_directories_recursively()])

    def get_dir_size_with_max(self, max=sys.maxsize):
        return [d.get_dir_size() for d in root.get_directories_recursively() if d.get_dir_size() <= max]

    def get_directories_recursively(self):
        all_dirs = [self]
        for dir in self.sub_directories:
            if dir.sub_directories:
                all_dirs += dir.get_directories_recursively()
            else:
                all_dirs += [dir]
        return all_dirs

    def add_sub_dir(self, sub_dir):
        for current_sub in self.sub_directories:
            if current_sub.name == sub_dir.name:
                print("dir already exists, ignoring")
                return
        self.sub_directories.append(sub_dir)

    def add_file(self, file: ElfFile):
        for current_file in self.files:
            if current_file.name == file.name:
                print("file already exists, ignoring")
                return
        self.files.append(file)


root = ElfDirectory("/", parent="/")
pwd: ElfDirectory = None

def is_cd(line):
    return line[0] == COMMAND_SYMB and COMMAND_CD in line


def is_ls(line):
    return line[0] == COMMAND_SYMB and COMMAND_LS in line


def cd_to_root():
    global pwd
    pwd = root

def cd_to_parent():
    global pwd
    pwd = pwd.parent


def is_dir(line: str):
    return line[0] != COMMAND_SYMB and line.startswith(DIR)

def is_file(line: str):
    return line[0] != COMMAND_SYMB and line.split(" ")[0].isdigit()

def handle_cd(line: str):
    global pwd
    if line.endswith(ROOT_DIR):
        cd_to_root()
    elif line.endswith(PARENT_DIR):
        cd_to_parent()
    else:
        target_dir = line.split(" ")[-1]
        for sub_dir in pwd.sub_directories:
            if sub_dir.name == target_dir:
                pwd = sub_dir
                break


def get_dir_name(line: str):
    return line.split(" ")[-1]


def get_file_name(line: str):
    return line.split(" ")[-1]


def get_file_size(line: str):
    return line.split(" ")[0]


def handle_ls_dir(line: str):
    pwd.add_sub_dir(ElfDirectory(get_dir_name(line), pwd))


def handle_ls_file(line: str):
    pwd.add_file(ElfFile(get_file_name(line), get_file_size(line)))


with open("resources/day7.txt", 'r') as f:
    for line in f.read().splitlines():
        if is_cd(line):
            handle_cd(line)
        elif is_ls(line):
            continue
        elif is_dir(line):
            handle_ls_dir(line)
        elif is_file(line):
            handle_ls_file(line)
        else:
            raise AttributeError("Unknown command " + line)


# root.get_directories_recursively()
print("answer part a: " + str(sum(root.get_dir_size_with_max(100000))))

total_space = 70000000
total_used = root.get_dir_size()
space_left = total_space - total_used

unused_space_required = 30000000

dir_to_delete = root
for d in root.get_directories_recursively():
    if  (space_left + d.get_dir_size()) > unused_space_required and d.get_dir_size() < dir_to_delete.get_dir_size():
        dir_to_delete = d

print("answer part b: " + str(dir_to_delete.get_dir_size()))