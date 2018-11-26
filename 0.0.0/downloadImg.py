#-*- coding:utf-8 -*-
#downloadImg.py

import random
import requests
from bs4 import BeautifulSoup

img_site = "https://stardewvalleywiki.com"

def download_file(url):
    local_filename = url.split('/')[-1]
    print("Downloading {} ---> {}".format(url, local_filename))
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

def Download_Image_from_Web(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    for link in soup.findAll('img'):
        image_links = link.get('src')
        if not image_links.startswith('http'):
            image_links = img_site + '/' + image_links
        download_file(image_links)

Download_Image_from_Web("https://stardewvalleywiki.com/Crops")
