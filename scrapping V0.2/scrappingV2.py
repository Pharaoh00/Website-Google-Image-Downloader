#-*- coding:utf-8 -*-
#scrappingV2.py

import requests
from bs4 import BeautifulSoup as bs
import os
import inspect
import pathlib
import datetime
import random
import re
import string
import json
import logging

all_imgs = []
current_folder = inspect.getfile(inspect.currentframe())
current_path = os.path.dirname(os.path.abspath(current_folder))

now = datetime.datetime.now()
name_file = now.strftime("%d-%m-%y-%H-%M")

logging.basicConfig(filename="logs/download{}.log".format(name_file),
                    filemode = "w",
                    level=logging.DEBUG,
                    format="%(asctime)s: %(message)s")

# def check_for_Extension(string):
#     if string[len(string)-4:len(string)] == ".jpg":
#         string = string
#     elif string[len(string)-4:len(string)] == ".png":
#         string = string
#     elif string[len(string)-5:len(string)] == ".jpeg":
#         string = string
#     elif not string[len(string)-4:len(string)] == ".jpg":
#         string = string + ".jpg"
#     elif not string[len(string)-4:len(string)] == ".png":
#         string = string + ".jpg"
#     elif not string[len(string)-5:len(string)] == ".jpeg":
#         string = string + ".jpg"

#     return string

def download_file(url):
    #Para o nome do arquivo
    local_filename = url.split("/")[-1]
    # Outra solução mais elegante
    # import re
    # local_file = ''.join(re.split(r['<>:"/\|?*'], local_filename))
    try:
        r = requests.get(url, stream=True)
        # O download só irá começar se status for 2**
        if r.status_code == requests.codes.ok:
            #Check se o nome esta em branco
            if not local_filename:
                local_filename = ''.join(random.sample(string.ascii_letters,
                                                       10)) + ".jpg"
                logging.info("Nome do arquivo escolhido foi: {}."
                             .format(local_filename))
                print(local_filename) #não esquecer de output isso no log
            # Outra solução mais elegante
            print(local_filename)
            #Check se tem algum character invalido para o windows
            local_filename = ''.join(re.split(r'[<>:"/\|?*]', local_filename))
            # --
            #Check se tem algum character q o windows não deixa criar
            #<>:"/\|?* todos esses characters não podem conter no nome do arquivo
            #local_filename = ''.join(c for c in local_filename if c not in '<>:"/\|?*')
            # Outra solução BEM mais simples
            # if not local_filename.endswith((".jpg", ".jpeg", ".png")):
            #     local_filename = local_filename + ".jpg"
            extension = (".jpg", ".jpeg", ".png")
            if not local_filename.endswith(tuple(e for e in extension)):
                local_filename = local_filename + ".jpg"
            #local_filename = check_for_Extension(local_filename)
            logging.info("File name: {}".format(local_filename))
            print("-> Tentando Baixar {}".format(url))
            
            pathlib.Path(current_path + "\\test4").mkdir(parents=True,
                                                         exist_ok=True)
            local_filename = current_path + "\\test4\\" + local_filename
            with open(local_filename, "wb") as f:
                # chunck_size é a quantidade de codigo processador por vez
                # que vai ir para a memoria.
                # Não é o tamanho do arquivo que sera baixado.
                # Numeros muitos grandes podem causar problemas de memoria,
                # Cuidado é crucial
                for chunk in r.iter_content(chunk_size=4096):
                    if chunk:
                        f.write(chunk)
                        # força a limpeza da memoria
                        f.flush()
                        os.fsync(f.fileno())

                if local_filename:
                    print("Download {} -> {}".format(url, local_filename))
                    logging.info("{} Baixado com sucesso! Nome do arquiv {}."
                                 .format(url, local_filename))
        else:
            print("A url não pode ser carregada, Erro {}.".format(r.status_code))
    except requests.exceptions.SSLError as err:
        print("Imagem {} não pode ser baixada Erro: {}.".format(local_filename,
                                                                err))
        logging.exception("O link {} não pode ser baixado por causa {}".format(url, err))
        pass

def parse_Image_from_Google(url):
    au = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"]
    headers = {"User-Agent": random.choice(au)}
    source_code = requests.get(url, headers=headers)
    html = source_code.text
    soup = bs(html, "lxml")
    for link in soup.find_all("div", {"class":"rg_meta notranslate"}):
        img = json.loads(link.text)
        all_imgs.append(img["ou"])
        download_file(img["ou"])
        #print(images["ou"])

url = "https://www.google.com/search?hl=en&site=imghp&tbm=isch&tbs\=isz:l&q=stardew valley"

parse_Image_from_Google(url)
#all_links = []
#for links in all_imgs:
    #local_filename = links.split("/")[-1]
    #local_filename = ''.join(c for c in local_filename if c not in '<>:"/\|?*')
#    all_links.append(local_filename)
#with open("images.json", "w") as outfile:
#    json.dump(all_imgs, outfile, indent=4)
#with open("links.json", "w") as outfile:
#    json.dump(all_links, outfile, indent=4)
