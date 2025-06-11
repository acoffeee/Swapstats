import sys

if sys.prefix != sys.base_prefix:
    print("You are in a virtual environment.")
else:
    print("You are not in a virtual environment.")
