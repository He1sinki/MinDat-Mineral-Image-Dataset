import requests
from lxml import etree
from tqdm import *
from queue import Queue
from threading import Thread

base_path = 'https://www.mindat.org/'
img_urls = []
url_queue = Queue(100)


# checks if string is valid ascii
def is_ascii(string):
    return all(ord(character) < 128 for character in string)


# take an url and store the url and the label of the mineral
def worker():
    while True:
        url = url_queue.get()
        try:
            page = requests.get(url, timeout=60)
        except requests.exceptions.RequestException as e:
            print(e)
            url_queue.task_done()
            continue
        html = etree.HTML(page.content)
        # find image url, if empty break
        url = html.xpath('.//img[@id="mainphoto"]')
        if not (len(url) == 0):
            url = img_url[0].attrib['src']
            url = base_path + url
            # find mineral names
            html_mineral = html.xpath('.//meta[@property="og:title"]')[0]
            html_mineral = html_mineral.attrib['content']
            # find dimensions
            html_dimension_body = html.xpath(".//table[contains(@class, 'picshowextradata')]")[0]
            html_dimension_tr0 = html_dimension_body[0]
            html_dimension_tr1 = html_dimension_tr0
            try:
                html_dimension_tr1 = html_dimension_body[1]
            except IndexError:
                pass
            # depending on the html, the xpath change
            if 'Dimensions' in html_dimension_tr0[0].text:
                html_dimension = html_dimension_tr0[1].text
            else:
                html_dimension = html_dimension_tr1[1].text
            html_dimension = html_dimension.split('(')[1][0]
            # keep only mineral that have one label without doubt and that the dimension is higher than 1
            if ',' in html_mineral or '?' in html_mineral or '0' in html_dimension:
                url_queue.task_done()
                continue
            # check if valid name and then add to list
            if is_ascii(html_mineral):
                img_urls.append(url + ',' + html_mineral + '\n')
        url_queue.task_done()


# launch threads
for i in range(100):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

# get all 1,200,000 urls
for i in tqdm(range(1200)):
    for j in tqdm(range(1000)):
        url_queue.put(base_path + 'photo-' + str(j + 1000 * i) + '.html')
    url_queue.join()
    print("saving URLs")
    # save all data every 1,000 urls
    img_url_file = open("img_urls/url_" + str(i).zfill(5) + ".csv", "w")
    for img_url in img_urls:
        img_url_file.write(img_url)
    img_url_file.close()
    img_urls = []
