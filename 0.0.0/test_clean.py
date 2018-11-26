#-*- coding:utf-8 -*-

import json
new_list = []

with open("images.json", "r") as infile:
    reader = json.load(infile)
    for row in reader:
        #if row.endswith("g"):
        #    row = row
        #    new_list.append(row)
        #elif not row.endswith("g"):
        #    row = row + ".jpg"
        #    new_list.append(row)

        if row[len(row)-4:len(row)] == ".jpg":
            row = row
            new_list.append(row)
        elif row[len(row)-4:len(row)] == ".png":
            row = row
            new_list.append(row)
        elif row[len(row)-5:len(row)] == ".jpeg":
            row = row
            new_list.append(row)
        elif not row[len(row)-4:len(row)] == ".jpg":
            row = row + ".jpg"
            new_list.append(row)
        elif not row[len(row)-4:len(row)] == ".png":
            row = row + ".jpg"
            new_list.append(row)
        elif not row[len(row)-5:len(row)] == ".jpeg":
            row = row + ".jpg"
            new_list.append(row)

with open("images_cleanV3.json", "w") as outfile:
    json.dump(new_list, outfile, indent=4)
