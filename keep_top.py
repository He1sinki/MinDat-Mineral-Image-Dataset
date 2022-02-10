# open the url file and the name of the top mineral name
with open('img_url_list_converted.csv', 'r') as f:
    lines = f.readlines()
with open('top-15.txt', 'r') as f:
    top_15_lines = f.readlines()

url_list = []

# read the mineral name and keep the url if the name is in the top 15
for line in lines:
    mineral_name = line.rpartition(',')[2]
    if mineral_name in top_15_lines:
        url_list.append(line)

# write the url list to a new file
with open('top_15_url_list.csv', 'w') as f:
    for url in url_list:
        f.write(url)
