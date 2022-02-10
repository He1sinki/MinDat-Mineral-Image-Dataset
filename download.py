from io import StringIO, BytesIO
import requests
from lxml import etree
import os
import sys
import imghdr
from tqdm import *
from queue import Queue
import threading

# base path to save images
base_save_path = 'data/mindat-images/'

# read list of img urls
with open('img_url_list_converted.csv', 'r') as f:
    lines = f.readlines()
url_list = []
for characters in lines:
    url_list.append(characters.replace(' ', '').split(','))

# make worker
url_queue = Queue(50)

thLock = threading.Lock()
global counter
counter = 0


def worker():
    while True:
        url_and_label = url_queue.get()
        if len(url_and_label) > 3:
            continue
        img_url = url_and_label[0]
        label = url_and_label[1]
        label.sort()
        name = base_save_path + ''.join(label).replace('/', '')

        if not os.path.exists(name):
            os.makedirs(name)
        with thLock:
            name = name + '/' + 'image_'.join(str(counter).zfill(7))
            counter += 1
        if not os.path.exists(name):
            img_data = requests.get(img_url).content
            with open(name, 'wb') as handler:
                handler.write(img_data)
        url_queue.task_done()


for i in range(150):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

# get all 900,000 urls
for url in tqdm(url_list):
    url_queue.put(url)
url_queue.join()
