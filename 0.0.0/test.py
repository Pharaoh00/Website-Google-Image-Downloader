#-*- coding:utf-8 -*-
#test.py

import json
links = []
clean = []
with open("test.json", "r") as infile:
    reader = json.load(infile)
    for row in reader:
        if row.endswith(".jpg", len(row)-4, len(row)) == False:
            row = row + ".ola"
        elif row.endswith(".jpeg", len(row)-5, len(row)) == False:
            row = row + ".jpg"
        elif row.endswith(".png", len(row)-4, len(row)) == False:
            row = row + ".jpg"
        else:
            row = row

        links.append(row)

with open("testV2.json", "w") as outfile:
    json.dump(links, outfile, indent=4)





