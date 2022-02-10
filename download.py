import requests
import os
import imghdr
from tqdm import *
from queue import Queue
import threading

url_queue = Queue(50)
thLock = threading.Lock()
base_save_path = 'data/'
counter = 0
url_list = []

# take url and name, split it and store it
with open('top_15_url_list.csv', 'r') as f:
    lines = f.readlines()
for line in lines:
    url_list.append(line.split(','))


# download images
def worker():
    while True:
        url_and_label = url_queue.get()
        img_url = url_and_label[0]
        label = url_and_label[1]
        name = base_save_path + ''.join(label).replace('\n', '')
        # distinct name
        global counter
        with thLock:
            name = name + '/' + 'image_' + str(counter).zfill(7)
            counter += 1
        request = requests.get(img_url)
        if request.status_code == 200:
            img_data = request.content
            img_type = imghdr.what(None, img_data)
            if img_type is not None:
                with open(name + '.' + img_type, 'wb') as image:
                    image.write(img_data)
        url_queue.task_done()


# thread creation
for i in range(150):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

# adding url to the queue
for url in tqdm(url_list):
    url_queue.put(url)
url_queue.join()
