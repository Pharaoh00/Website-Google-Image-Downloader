#!/usr/bin/env python
#-*- coding:utf-8 -*-
#downloaderV4.py

from test_path import join_paths #Custom path join
import requests
from bs4 import BeautifulSoup
import random
import string
import re
import logging
import pathlib
import os
import datetime
import json

# Logging disable
# Muitos problemas gerados com a introdução
# do multiprocessing com Logging.
# Verei o que posso fazer.
# Se caso eu não consiga, tenho algumas ideias.
# Talvez exporta um json customizado,
# um dict contendo a url e o erro.

now = datetime.datetime.now()
format_log_file = now.strftime("%d-%m-%y-%H-%M")

log_folder_name = "log"
log_folder = join_paths(log_folder_name)
pathlib.Path(log_folder).mkdir(parents=True, exist_ok=True)

img_folder_name = "imgs"
img_folder = join_paths(img_folder_name)
pathlib.Path(img_folder).mkdir(parents=True,exist_ok=True)

#--Downloader--#
def download_File(url):
    """
    Requer uma url de uma imagem.
    Checa se a url é valida ou não.
    Caso sim, a imagem será processada de
    maneira "correta" e será baixada.
    Caso não, a imagem será ignorada.

    Requer o caminho de uma pasta para fazer download.
    (PS: Importante que o caminho passado seja abspath (absolute path),
    para não haver, por parte do python, confusão do caminho da pasta
    especificada. 
    Qualquer duvida olhar )

    Se necessário, aceita o camiho da pasta para o log file.
    Caso não especificado por padrão é "log"
    """
    repeat_urls = []
    print("--File: {}--".format(str(__file__)))
    print("--Começo Novo requests--")
    file_name = url.split("/")[-1]
    flag = True
    try:
        r = requests.get(url, stream=True)
        files_on_folder = os.listdir(join_paths(img_folder))
        if file_name in [i for i in files_on_folder]:
            flag = False
        else:
            flag = True
        if r.status_code == requests.codes.ok and flag == True:
            print("Tentando Baixar -> {}".format(url))
            #Check se o nome está em branco
            if not file_name:
                file_name = "".join(random.sample(string.ascii_letters,
                                                  10)) + ".jpg"

            #Check se algum character é invalido para o windows
            file_name = "".join(re.split(r'[<>:"/\|?*]', file_name))
            extension = (".jpg", ".jpeg", ".png")
            if not file_name.endswith(tuple(e for e in extension)):
                file_name = file_name = ".jpg"

            file_name = join_paths(img_folder, file_name)
            try:
                with open(file_name, "wb") as f:
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

            #Catching alguns comportamentos estranhos
            #Ainda não sei o motivo
            #Acredito que seja algo relacionado com o
            #nome do arquivo ser muito grande.
            #De qualquer forma, se o erro ocorre um novo nome
            #será gerado para fazer o download.
            #"Problema resolvido"
            except FileNotFoundError as err:
                file_name = "".join(random.sample(string.ascii_letters,
                                                  10)) + ".jpg"
                file_name = join_paths(img_folder, file_name)

        if not flag:
            repeat_urls.append(url)
        elif not r.status_code == requests.codes.ok:
            print("A url {} não pode ser carregada. Erro{}".format(url,
                                                                r.status_code))

    #Problema com a verificação de segurança em alguns links
    #Há certos ricos em deixar a verificação como False
    #Por esse motivo é melhor ignorar e passar para a próxima url
    #Caso necessário a url estará no log file. Pode ser baixada manualmente
    #Segurançã em risco (use por contra própria):
    #Tire o comentario da primeira linha "#r = requests.get(...."
    #Comente a terceira linha "pass"
    except requests.exceptions.SSLError as err:
        #r = requests.get(url, stream=True, verify=False)
        pass

    with open("repetidas-{}.json".format(format_log_file), "w") as f:
        json.dump(repeat_urls, f, indent=4)


#download_file("https://nanogamingnews.com/wp-content/uploads/2018/10/Stardew_Valley_Feature_SDV_iPad_8_1539085121.jpg", "imgs")

