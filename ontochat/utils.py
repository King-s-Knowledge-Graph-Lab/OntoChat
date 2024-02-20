"""
General-purpose utility functions.
"""

def read_key(file_path: str = "key.txt"):
    with open(file_path, "r") as fo:
        key = fo.read()
    return key

