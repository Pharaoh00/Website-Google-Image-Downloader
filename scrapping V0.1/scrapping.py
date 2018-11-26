#-*- coding:utf-8 -*-
#screapping.py

import requests
from bs4 import BeautifulSoup
import os
import random
import json
import datetime
import logging

now = datetime.datetime.now()
name_file = now.strftime("%d-%m-%y-%H-%M")

logging.basicConfig(filename="logs/download{}.log".format(name_file),
                    filemode = "w",
                    level=logging.DEBUG,
                    format="%(asctime)s: %(message)s")

def download_file(url) :
    local_filename = url.split("/")[-1]
    print("-> Tentando Baixar {}".format(url))

    r = requests.get(url, stream=True)
    with open(local_filename, "wb") as f:
        # chunck_size é a quantidade de codigo processador por vez
        # que vai ir para a memoria.
        # Não é o tamanho do arquivo que sera baixado.
        # Numeros muitos grandes podem causar problemas de memoria,
        # Cuidado é crucial
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                # força a limpeza da memoria
                f.flush()
                os.fsync(f.fileno())

        if local_filename:
            print("Download {} -> {}".format(url, local_filename))
            logging.info("{} Baixado com sucesso! Arquivo {}.".format(url,local_filename))
    return local_filename

url = "https://www.google.com/search?hl=en&site=imghp&tbm=isch&tbs\=isz:l&q=stardew valley crops"
au = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"]

headers = {"User-Agent": random.choice(au)}
web_source = requests.get(url, headers=headers)
html = web_source.content

soup = BeautifulSoup(html, "lxml")

images = soup.find_all("div", {"class":"rg_meta notranslate"})
images = [i.text for i in images]
images = [json.loads(i) for i in images]

for link in images:
    img = link["ou"]
    try:
        download_file(img)
    except Exception as e:
        print("O link {} não pode ser baixado por causa {}.".format(url, e))
        logging.exception("O link {} não pode ser baixado por causa {}.".format(url,e))
        pass
