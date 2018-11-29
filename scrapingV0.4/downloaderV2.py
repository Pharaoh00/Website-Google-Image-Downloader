#!/usr/bin/env python
#-*- coding:utf-8 -*-
#downloaderV2.py 

from test_path import join_paths #Custom path join
#from log_handler import log_handler #Custom log handler
import requests
from bs4 import BeautifulSoup
import random
import string
import re
import os.path
import inspect

import logging
import pathlib
import os
import datetime
current_folder = inspect.getfile(inspect.currentframe())
current_path = os.path.dirname(os.path.abspath(current_folder))
#--Logging--#
now = datetime.datetime.now()
format_log_file = now.strftime("%d-%m-%y-%H-%M")

#--Folder deve ser criada em main.py
log_folder = "log"
pathlib.Path(log_folder).mkdir(parents=True, exist_ok=True)

#new_log_folder = os.path.join(os.path.sep, current_path, log_folder)
new_log_folder = pathlib.PurePath(current_path).joinpath(log_folder)
log_path = os.path.join(os.path.sep, new_log_folder, "download{}.log"
                        .format(format_log_file))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s(%(levelname)s): %(message)s")

log_file = logging.FileHandler(log_path, mode="w")
log_file.setLevel(logging.DEBUG)
log_file.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(log_file)
logger.addHandler(stream_handler)

#--Downloader--#
def download_File(url, folder, log_path=False):
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
    # if not log_path:
    #     #log_file = os.path.join(os.path.sep, current_path, "log")
    #     logger = log_handler(join_paths("log"))
    # else:
    #     logger = log_handler(log_path)
        
    #--Fazer com que a função também aceite listas de url's
    logger.info("--File: {}--".format(str(__file__)))
    logger.info("--Começo Novo requests--")
    file_name = url.split("/")[-1]
    try:
        r = requests.get(url, stream=True)
        if r.status_code == requests.codes.ok:
            logger.info("Tentando Baixar -> {}".format(url))
            #Check se o nome está em branco
            if not file_name:
                file_name = "".join(random.sample(string.ascii_letters,
                                                  10)) + ".jpg"
                logger.warn("Url vazia. Novo nome: {}".format(file_name))

            #Check se algum character é invalido para o windows
            file_name = "".join(re.split(r'[<>:"/\|?*]', file_name))
            extension = (".jpg", ".jpeg", ".png")
            if not file_name.endswith(tuple(e for e in extension)):
                logger.warn("O arquivo falta extensão {}".format(file_name))
                file_name = file_name = ".jpg"

            files_on_folder = os.listdir(join_paths(folder))
            if file_name in [i for i in files_on_folder]:
                logger.warn("Arquivo {} já existe.".format(file_name))
                file_name = "".join(random.sample(string.ascii_letters,
                                                  10)) + ".jpg"

            logger.info("Nome final do arquivo {}".format(file_name))
            file_name = join_paths(folder, file_name)
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

                    if file_name:
                        logger.info("A url {} foi baixada com sucesso! O arquivo foi baixado em: {}".format(url, file_name))
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
                file_name = join_paths(folder, file_name)
                logger.error("A url {} não pode ser baixada. Erro ocorrido {}. Um novo nome foi gerado {}".format(url, err, file_name))

        else:
            logger.error("A url {} não pode ser carregada. Erro{}".format(url, r.status_code))
            pass

    #Problema com a verificação de segurança em alguns links
    #Há certos ricos em deixar a verificação como False
    #Por esse motivo é melhor ignorar e passar para a próxima url
    #Caso necessário a url estará no log file. Pode ser baixada manualmente
    #Segurançã em risco (use por contra própria):
    #Tire o comentario da primeira linha "#r = requests.get(...."
    #Comente a terceira linha "pass"
    except requests.exceptions.SSLError as err:
        #r = requests.get(url, stream=True, verify=False)
        logger.erro("A url {} não pode ser baixada. Error: {}.".format(url, err))
        pass


#download_file("https://nanogamingnews.com/wp-content/uploads/2018/10/Stardew_Valley_Feature_SDV_iPad_8_1539085121.jpg", "imgs")

