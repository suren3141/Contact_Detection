from __future__ import print_function

import json
import os
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def init_json(name):
    if os.path.exists(name):
        print("File already exists : %s"%name)
    else:
        print("Init file : %s"%name)
        write_json({}, name)
    return read_json(name)


def write_json(data, name):
    with open(name, 'w+') as outfile:
        json.dump(data, outfile, indent=4)


def update_json(data, name):
    temp = read_json(name)
    temp.update(data)
    write_json(temp, name)


def read_json(name):
    with open(name, 'r') as file:
        if len(file.readlines()) != 0: file.seek(0)
        data = json.load(file)
    return data
