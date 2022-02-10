import os
import sys
from tqdm import *


# helper function
def _convert_string_to_mineral_list(string):
    string = string.lower()
    string = string.replace(' ', '')
    start = -1
    end = -1
    if 'var' in string:
        for i in range(len(string)):
            if string[i] == '(':
                start = i
        string = string[:start]
    return string


with open('img_url_list.csv', 'r') as f:
    lines = f.readlines()

# split url out
for i in range(len(lines)):
    new_line = lines[i].split(',')
    replace_line = [new_line[0]]
    mineral_name = _convert_string_to_mineral_list(new_line[1])
    replace_line.append(mineral_name)
    lines[i] = replace_line

img_url_list_converted_file = open("img_url_list_converted.csv", "w")
for line in lines:
    if len(line) == 1:
        continue
    img_url_list_converted_file.write(line[0] + ',' + line[1] + '\n')
