#!/usr/bin/env python3

import string
import re
import os
from bs4 import BeautifulSoup as BS
import sys



def recurse_create(e, current_key):
    if current_key == sys.argv[3]:
        for key in e[current_key]:
            if key in e:
                os.system(f"mkdir -p {current_key}/{key}")
                recurse_create(e, f"{current_key}/{key}")
            else:
                os.system(f"touch {current_key}/{key}")
    else:
        for key in e[current_key.split("/")[-1]]:
            if key in e:
                os.system(f"mkdir -p {current_key}/{key}")
                recurse_create(e, f"{current_key}/{key}")
            else:
                os.system(f"touch {current_key}/{key}")


def recurse_path(e, current_key):
    if (current_key == "."):
        return "."
    else:
        for key in e:
            if current_key in e[key]:
                return f"{recurse_path(e, key)}/{current_key}"


if len(sys.argv) != 4:
    print("Usage: ./main.py url login destination_folder")
    exit(1)

try:
    os.system(f"curl {sys.argv[1]} 2>/dev/null > r.tmp")
except Exception as err:
    print(f'Error occurred: {err}')

f = open("r.tmp", "r")

soup = BS(f, "html.parser")

codes = soup.find_all("code", attrs={"class":"language-none"})

all_pres = soup.find_all("code", attrs={"class":"language-bash"})

for elem in all_pres:
    if "git" in elem.string:
        git_url = elem.string.split("clone ")[1]


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
previouskey = f"{sys.argv[3]}"
parentkeys = [f"{sys.argv[3]}"]

e = {".":[sys.argv[3]], sys.argv[3]:[]}

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

recurse_create(e, f"{sys.argv[3]}")

login = sys.argv[2];

path_authors = recurse_path(e, "AUTHORS")
content = f"{re.sub('[0-9]','',login).split('.')[0].capitalize()}\n{login.split('.')[1].capitalize()}\n{login}\n{login}@epita.fr\n"
g = open(path_authors, "w")
g.write(content)
g.close()


all_pres = soup.find_all("code", attrs={"class":"language-c"})

for iterator in range(len(all_pres)):
    all_pres[iterator] = (all_pres[iterator].parent.previous_sibling.previous_sibling.string,all_pres[iterator])

to_remove = []

for iterator in range(len(all_pres)):
    if (all_pres[iterator] is None):
        to_remove.append(all_pres[iterator])

for delete in to_remove:
    all_pres.remove(delete)

while len(all_pres) > 0:
    for key in e:
        if all_pres[0][0] in e[key]:
            path = recurse_path(e, all_pres[0][0])
            content = str(all_pres[0][1].string)
            file_content = "\n".join([line[padding::] for line in content.split("\n")[1:]])
            g = open(path, "w")
            g.write(file_content)
            g.close()

    del all_pres[0]

all_pres = soup.find_all("code", attrs={"class":"language-makefile"})

for iterator in range(len(all_pres)):
    all_pres[iterator] = (all_pres[iterator].parent.previous_sibling.previous_sibling.string,all_pres[iterator])

to_remove = []

for iterator in range(len(all_pres)):
    if (all_pres[iterator] is None):
        to_remove.append(all_pres[iterator])

for delete in to_remove:
    all_pres.remove(delete)

all_files = []

for key in e:
    for elem in e[key]:
        if re.match("(\w*(?<!main|test)\.(c|h))$", elem) and elem[-2] not in all_files:
            all_files.append(elem[:-2])

while len(all_pres) > 0:
    content = str(all_pres[0][1].string)
    file_content = "\n".join([line[padding::] for line in content.split("\n")[1:]])
    for elem in re.findall("(\w*\.(o|c|h))", file_content):
        if elem[0][:-2] in all_files:
            path_file = recurse_path(e, f"{elem[0][:-2]}.c").split("/")
            path_makefile = path_file
            path_makefile[-1] = "Makefile"
            path_makefile = "/".join(path_makefile)
            g = open(path_makefile, "w")
            g.write(file_content)
            g.close()

    del all_pres[0]


git_url = git_url.replace("john.smith", login)

os.system(f"cd {sys.argv[3]} && git init")
os.system(f"cd {sys.argv[3]} && git remote add origin {git_url}")


f.close()

os.system("rm r.tmp")
