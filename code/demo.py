from pprint import pprint

from db import DB
from parser_ast import search
from pathlib import Path

DB = DB("Test")
arr = search("/Users/kajetanserwecinski/Documents/Programming/CodeSearchQuenszu/code")

n = len(arr)

ids = [str(i) for i in range(1, n+1)]

DB.update(arr, ids)

while True:
    print("Heare I am")
    s = input()

    if s == 'q':
        break

    pprint(DB.query(s, 3))