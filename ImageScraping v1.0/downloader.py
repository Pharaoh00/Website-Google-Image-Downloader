#!/usr/bin/env python
#-*- coding:utf-8 -*-
#downloader.py

import tools # Custom little tools
from bs4 import BeautifulSoup
import requests
import pathlib
import os
import re
import random
import json

class DownloaderImg:

    # Não esquecer de fazer um custom log
    # A ideia é ter uma lista geral com tudo que esta acontecendo
    # E depois formatar e colocar em um json
    # Porque não usar logging?
    # Multiprocessing...
    def __init__(self, url):
        self.url = url
        self.folder = "img"
        self.path = tools.join_paths(self.folder) # Caminho para a pasta das img
        self.mode = "NORMAL"
        self.home = False
        self.parsed_links = []

    def setFolder(self, name):
        # Set nome do arquivo
        self.folder = name

    def setMode(self, mode):
        # Set o modo para parse
        self.mode = mode

    def setHome(self, url):
        # Set homepage do website
        self.home = url

    def getParsedLinks(self):
        return tools.CustomIter(self.parsed_links)

    def createImgFolder(self, folder=None):
        # Cria a pasta para as imagens
        # Se necessário folder pode ser um caminho.
        # Exemplo:
        # C:\User\MyUser\Desketop\Imgs
        if folder:
            folder_name = folder
        if not folder:
            folder_name = self.folder
        img_folder = tools.join_paths(folder_name) # Custom path/join converter
        pathlib.Path(img_folder).mkdir(parents=True,exist_ok=True)
        self.path = img_folder

    def parse_Image(self):
        """
        Retorna uma lista com todas as url's encontradas

        Requer uma url.

        mode = NORMAL ou GOOGLE
        NORMAL significa que o site desejado não é o google, qualquer outro site.
        (PS: As imagens podem ser procurada por simples "img" / "src")
        Google significa que o site desajado é o google imagens.
        (PS: As imagens são procurada por "div" "class: rg_meta notranslate",
        essa classe contem todas as informações do site da imagem, 
        inclusive a url,
        a classe é na verdade um json, dentro do json gerado.
        Url da imagem esta em ["ou"].

        Para o google:
        De preferencia a url deve começar com "http://www.google.com/search?"

        Para outros sites:
        Muitas vezes a imagem não esta na src da imagem encontrada, 
        na maioria das vezes o link real da imagem esta na homepage do website.
        Por exemplo:
        A src da imagem do Blue Jazz na wikia do Stardew Valley é:
        /mediawiki/images/2/2f/Blue_Jazz.png

        Mas a página a onde a imagem está é:
        https://stardewvalleywiki.com/Crops

        O link final ficaria: (certo?)
        https://stardewvalleywiki.com/mediawiki/images/2/2f/Blue_Jazz.png

        Errado.
        O link final ficaria:
        https://stardewvalleywiki.com/Crops/mediawiki/images/2/2f/Blue_Jazz.png
        img = url + "/" + img

        O link certo seria:
        https://stardewvalleywiki.com/mediawiki/images/2/2f/Blue_Jazz.png
        img = home + "/" + img

        Passar home se caso o path da imagem desejada seja a homepage do website
        e não a url de onde a imagem está.
        Você pode checar se o path da imagem vem da homepage/ou de qualquer outro
        lugar, olhando o link da imagem na própria página onde deseja fazer 
        o download.
        """

        # LEMBRAR:
        # Olhar na pagina:
        # https://docs.python.org/3/library/concurrent.futures.html
        # sobre cuncurrent.futures
        # Em ThreadPoolExecutor Example
        # a lista é de URL, ao invez de retonar requests da urls
        # retorna o search das coisas pedidas.
        # Por exemplo:
        # No search da wiki do stardew ao invez dele processar
        # linha por linha, ter workes que passem por toda a "lista"
        # do html = source_code.content e append na lista.
        
        au = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"]
        headers= {"User-Agent": random.choice(au)}
        source_code = requests.get(self.url, headers=headers)
        html = source_code.content
        soup = BeautifulSoup(html, "lxml")

        if self.mode is "GOOGLE":
            for link in soup.find_all("div", {"class": "rg_meta notranslate"}):
                img = json.loads(link.text)
                print(img)
                self.parsed_links.append(img["ou"])

        elif self.mode is "NORMAL":
            for link in soup.find_all("img"):
                img = link.get("src")
                if self.home:
                    if not img.startswith("http"):
                        if not img.startswith("/"):
                            img = self.home + "/" + img
                            print(img)
                        elif img.startswith("//"):
                            img = self.home + "".join(img.split("/", 1))
                        else:
                            img = self.home + img
                        
                    self.parsed_links.append(img)

                elif not self.home:
                    if not img.startswith("http"):
                        if not img.startswith("/"):
                            img = self.url + "/" + img
                        elif img.startswith("//"):
                            img = self.url + "".join(img.split("/", 1))
                        else:
                            img = self.url + img
                            
                self.parsed_links.append(img)
        print(self.parsed_links)

    def download_File(self, url):
        """
        Requer uma url de uma imagem.
        Checa se a url é valida ou não.
        Caso sim, a imagem será processada de
        maneira "correta" e será baixada.
        Caso não, a imagem será ignorada.

        Requer o caminho de uma pasta para fazer download.
        (Ver a função createImgFolder.)
        """
        file_name = url.split("/")[-1]
        flag = True
        try:
            r = requests.get(url, stream=True) 

            # Check se o arquivo já existe na pasta
            # Necessário? Talvez não...
            # Mas as vezes, por algum razão, imagens pode ter o mesmo
            # nome que outras.
            files_on_folder = os.listdir(tools.join_paths(self.folder))
            if file_name in [i for i in files_on_folder]:
                flag = False
                
            if not flag:
                # Append urls que já existem para o "Custom log"
                print("Arquivo já existe {}".format(file_name))

            if r.status_code == requests.codes.ok and flag == True:
                print("Tentando baixar > {}".format(url))

                # LEMBRAR:
                # Não seria melhor checar todas essas coisas
                # em uma função a parte?
                # E retornar a url certa antes mesmo de fazer o requests.
                
                # Check se o nome está em branco
                if not file_name:
                    file_name = "".join(random.sample(string.ascii_letters,
                                                      10)) + ".jpg"

                # Check se algum character é invalido para o windows
                file_name = "".join(re.split(r'[<>:"/\|?*]', file_name))

                # Check se a url termina com as extensões
                extensions = [".jpg", ".jpeg", ".png"]
                if not file_name.endswith(tuple(e for e in extensions)):
                    file_name = file_name + ".jpg"

                # Jutando o nome do arquivo mais a pasta destinada
                file_name = tools.join_paths(self.path, file_name) 

                # Hora de criar o arquivo
                try:
                    with open(file_name, "wb") as f:
                        # chunck_size é a quantidade de codigo
                        # processador por vez
                        # que vai ir para a memoria.
                        # Não é o tamanho do arquivo que sera baixado.
                        # Numeros muitos grandes podem causar
                        # problemas de memoria,
                        # Cuidado é crucial
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                # Força a limpeza da memória
                                f.flush()
                                os.fsync(f.fileno())

                    if file_name:
                        # Print o arquivo baixado
                        # Futuramente irá para o "custom log"
                        print("Arquivo {} baixado com sucesso".format(file_name))

                # Catching alguns comportamentos estranhos
                # Ainda não sei o motivo
                # Acredito que seja algo relacionado com o
                # nome do arquivo ser muito grande.
                # De qualquer forma, se o erro ocorre, um novo nome
                # será gerado para fazer o download.
                # "Problema resolvido"
                except FileNotFoundError as err:
                    print("A url {} não pode ser carregada. Erro {}".format(url,
                                                                  r.status_code))
            elif not r.status_code == requests.codes.ok:
                # Append urls + erro para o "Custom log"
                print("A url {} não pode ser carregada. Erro: {}".format(url,
                                                                  r.status_code))
                
        # Problema com a verificação de segurança em alguns links
        # Há certos ricos em deixar a verificação como False
        # Por esse motivo é melhor ignorar e passar para a próxima url
        # Caso necessário a url estará no log file. Pode ser baixada manualmente
        # Segurança em risco (use por contra própria):
        # Tire o comentario da primeira linha "#r = requests.get(...."
        # Comente a terceira linha "pass"
        except requests.exceptions.SSLError as err:
            # r = requests.get(url, stream=True, verify=False)
            pass
