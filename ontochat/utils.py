"""
General-purpose utility functions.
"""

def read_key(file_path: str = "key.txt"):
    with open(file_path, "r") as fo:
        key = fo.read()
    return key

def read_list(file_path: str):
    with open(file_path, "r") as fo:
        str_list = fo.readlines()
    return [s.strip() for s in str_list]

