from pprint import pprint

from db import DB
from parser_ast import search
from pathlib import Path
from voiceRecognision import voice

DB = DB("Test")
arr = search("C:/Users/user/Documents/github/CodeSearch/code")

n = len(arr)

ids = [str(i) for i in range(1, n+1)]

DB.update(arr, ids)
voice(DB)

