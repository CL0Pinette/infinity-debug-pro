#!/usr/bin/env python3

import string
import os
import requests
from bs4 import BeautifulSoup as BS
import sys



def recurse_create(e, current_key):
    for key in e[current_key.split("/")[-1]]:
        if key in e:
            os.system(f"mkdir {current_key}/{key}")
            recurse_create(e, f"{current_key}/{key}")
        else:
            os.system(f"touch {current_key}/{key}")


if len(sys.argv) != 2:
    print("Usage: ./main.py url")
    exit(1)

try:
    os.system(f"curl {sys.argv[1]} > r.tmp")
except Exception as err:
    print(f'Error occurred: {err}')

f = open("r.tmp", "r")

soup = BS(f, "html.parser")

codes = soup.find_all("code", attrs={"class":"language-none"})

for code in codes:
    if "$ tree" in str(code.string):
        tree = str(code.string)
        break

d = {}

padding = 0

line_number = 0

lines = tree.split("\n")
for line in lines:
    if "$ tree" in line:
        line_number += 1
        for c in line:
            if c != "$":
                padding += 1
            else:
                break
        break

    else:
        line_number += 1


while line_number > 0:
    del lines[0]
    line_number -= 1

lines_bis = []

for line in lines:
    lines_bis.append(line[padding::])

lines = lines_bis

lines_number = len(lines) - 1
iterator = 0
j_iterator = 0

while iterator < lines_number:
    if (lines[j_iterator] == ""):
        del lines[j_iterator]
    else:
        j_iterator += 1
    iterator += 1

valid_chars = string.printable
valid_chars = "".join(valid_chars.split(" "))

for j_iterator in range(len(lines)):
    pad = 0
    for iterator in range(len(lines[j_iterator])):
        if lines[j_iterator][iterator] in valid_chars:
            start = iterator
            break
        else:
            pad += 1
    key = f"{j_iterator}-{lines[j_iterator][start::]}"
    d[key] = int(pad/4)

to_remove = []

for (key,val) in d.items():
    if (val == 0):
        to_remove.append(key)

for key in to_remove:
    d.pop(key)

lastvals = [0]
previouskey = "."
parentkeys = ["."]

e = {".":[]}


for (key, val) in d.items():
    if (val == lastvals[-1]):
        e[parentkeys[-1]].append(key.split("-")[1])
        previouskey = key.split("-")[1]
    elif (val > lastvals[-1]):
        lastvals.append(val)
        parentkeys.append(previouskey)
        e[parentkeys[-1]] = [key.split("-")[1]]
        previouskey = key.split("-")[1]
    else:
        parentkeys.pop()
        lastvals.pop()
        e[parentkeys[-1]].append(key.split("-")[1])
        previouskey = key.split("-")[1]


recurse_create(e, ".")

os.system("rm r.tmp")
