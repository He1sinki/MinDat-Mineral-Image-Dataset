# function that keep the essential information of the name of the mineral
def clean(string):
    string = string.lower()
    string = string.replace(' ', '')
    start = -1
    if 'var' in string:
        for character in range(len(string)):
            if string[character] == '(':
                start = character
        string = string[:start]
    return string


# open the file
with open('img_url_list.csv', 'r') as f:
    lines = f.readlines()

# clean the file and write the result to a new file
with open('img_url_list_cleaned.csv', 'w') as f:
    for line in lines:
        new_line = line.split(',')
        mineral_name = clean(new_line[1])
        f.write(new_line[0] + ',' + mineral_name + '\n')