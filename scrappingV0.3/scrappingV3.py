#-*- coding:utf-8 -*-
#scrappingV3.py

from bs4 import BeautifulSoup
import requests
import inspect
import os
import re
import string
import pathlib
import random
import json
import logging
import datetime

current_folder = inspect.getfile(inspect.currentframe())
current_path = os.path.dirname(os.path.abspath(current_folder))

#--Debug--#
#Não esquecer de passar toda a parte de debug
#para outro arquivo, main.py (de preferencia)
#e do main.py chamar as funções para download.
#Organizar toda a parte de criação de pastas
#no main.py 
now = datetime.datetime.now()
format_log_file = now.strftime("%d-%m-%y-%H-%M")

log_folder = "log2"
pathlib.Path(log_folder).mkdir(parents=True, exist_ok=True)

new_log_folder = os.path.join(os.path.sep, current_path, log_folder)
log_path = os.path.join(os.path.sep, new_log_folder, "download{}.log"
                        .format(format_log_file))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s(%(levelname)s) %(message)s")

log_file = logging.FileHandler(log_path, mode="w")
log_file.setLevel(logging.DEBUG)
log_file.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(log_file)
logger.addHandler(stream_handler)

def download_file(url):
    """
    Requer uma url de uma imagem.
    Checa se a url é valida ou não.
    Caso sim, a imagem será processada de
    maneira "correta" e será baixada.
    Caso não, a imagem será ignorada.
    """
    #--Fazer com que a função também aceite lista de url"s
    logger.info("--Começo Novo request--")
    new_folder = "test6"
    #Para o nome do arquivo
    file_name = url.split("/")[-1]
    try:
        r = requests.get(url, stream=True)
        if r.status_code == requests.codes.ok:
            logger.info("Tentando Baixar -> {}".format(url))
            # Check se o nome esta em branco
            if not file_name:
                file_name = "".join(random.sample(string.ascii_letters,
                                                  10)) + ".jpg"
                #Loggar o nome do arquivo escolhido
                logger.error("O arquivo {} esta sem nome".format(file_name))
                logger.info("Novo nome escolhido {}".format(file_name))

            #Check se algum character é invalido para o windows
            file_name = "".join(re.split(r'[<>:"/\|?*]', file_name))

            extension = (".jpg", ".jpeg", ".png")
            if not file_name.endswith(tuple(e for e in extension)):
                logger.warn("O arquivo falta extensão {}".format(file_name))
                file_name = file_name + ".jpg"
                
            #Cria a pasta para download (Depois, talvez ser um argumento?)
            new_folder = os.path.join(os.path.sep, current_path, new_folder)
            #--pathlib está sendo chamado todas as vezes
            #--que o parse_Image e chamado
            #Isso não esta certo.
            #Colocar a crianção de de pastas fora do loop em main.py
            pathlib.Path(new_folder).mkdir(parents=True, exist_ok=True)
            files_on_folder = os.listdir(new_folder)
            if file_name in [i for i in files_on_folder]:
                logger.warn("Arquivo {} já existe.".format(file_name))
                file_name = "".join(random.sample(string.ascii_letters,
                                                  10)) + ".jpg"
            #Loggar o nome do arquivo final
            logger.info("Nome final do arquivo: {}".format(file_name))
            print("-> Tentando baixar {}!".format(url))
            #file_name = current_path + new_folder + file_name
            file_name = os.path.join(os.path.sep, new_folder, file_name)
            print(file_name)
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
                        print("Download {} -> {}".format(url, file_name))
                        # Loggar o arquivo baixando com sucesso + nome do arquivo
                        logger.info("A url {} foi baixada com sucesso com o nome de: {}".format(url, file_name))

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
                file_name = os.path.join(os.path.sep, new_folder, file_name)
                #Loggar o ocorrido + o nome do arquivo escolhido
                logger.error("A url {} não pode ser baixada. Erro ocorrido {}. Um novo nome foi gerado {}".format(url, err, file_name))

        else:
            print("A ulr não pode ser carregada. Erro {}.".format(r.status_code))
            # Loggar a url + o erro
            logger.error("A url não pode ser carregada. Erro: {}."
                         .format(r.status_code))

    except requests.exceptions.SSLError as err:
        print("Imagem {} não pode ser baixada. Erro {}.".format(file_name, err))
        logger.erro("A url {} não pode ser baixada. Erro: {}.".format(url, err))
        # Loggar a url + o erro
        pass
    
def parse_Image(url, mode="NORMAL", home=None):
    """
    Requer uma url.
    De preferencia a url deve começar com "http://www.google.com/search?"
    Processa o google imagens.

    mode = NORMAL ou GOOGLE
    NORMAL significa que o site desejado não é o google, qualquer outro site.
    (PS: As imagens podem ser procurada por simples "img" / "src")
    Google significa que o site desajado é o google imagens.
    (PS: As imagens são procurada por "div" "class: rg_meta notranslate",
    essa classe contem todas as informações do site da imagem, inclusive a url,
    a classe é na verdade um json, dentro do json gerado a url da imagem esta 
    em ["ou"].
    """
    
    #Não esquecer de olhar multithreads
    #Fazer com que o download seja mais rapido.
    #append os links encontrados em uma lista, dividir a lista
    #na quantidade de threads desejados, e passar a cada lista
    #para seu respectivo download_file(url)
    au = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"]
    headers= {"User-Agent": random.choice(au)}
    source_code = requests.get(url, headers=headers)
    html = source_code.content
    soup = BeautifulSoup(html, "lxml")
    if mode == "NORMAL":
        for link in soup.find_all("div", {"class": "rg_meta notranslate"}):
            img = json.loads(link.text)
            download_file(img["ou"])
    elif mode == "GOOGLE":
        for link in soup.findl_all("img"):
            img = link.get("src")
            if home == None:
                if not image_links.startswith("http"):
                    img = url + "/" + img
            if not home == None:
                if not image_links.startwith("http"):
                    img = home + "/" + img
    download_file(img)
        

url = "https://www.google.com/search?hl=en&site=imghp&tbm=isch&tbs\=isz:l&q=stardew valley"

parse_Image(url)

# new_folder = "\\test4"
# files_on_folder = os.listdir(current_path + new_folder)
# print(files_on_folder)
# with open("files_on_folder.json", "w") as outfile:
#     json.dump(files_on_folder, outfile, indent=4)
