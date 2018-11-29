#!/usr/bin/env python
#-*- coding:utf-8 -*-
#parseImage.py

from downloaderV2 import download_File
import requests
from bs4 import BeautifulSoup
import random

def parse_Image(url, folder, mode="NORMAL", home=False, log_path=False):
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

    Muitas vezes a imagem não esta na src da imagem encontrada, na maioria das
    vezes o link real da imagem esta na homepage do website.
    Por exemplo:
    A imagem do Blue Jazz na wiki do Stardew Valley é:
    https://stardewvalleywiki.com/mediawiki/images/2/2f/Blue_Jazz.png
    
    Mas a página a onde a imagem está aparecendo é:
    https://stardewvalleywiki.com/Crops

    A src da imagem é:
    /mediawiki/images/2/2f/Blue_Jazz.png

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
    if mode == "GOOGLE":
        for link in soup.find_all("div", {"class": "rg_meta notranslate"}):
            img = json.loads(link.text)
            download_file(img["ou"])
    elif mode == "NORMAL":
        for link in soup.find_all("img"):
            img = link.get("src")
            if home:
                if not img.startswith("http"):
                    img = home + img
            if not home:
                if not img.startswith("http"):
                    img = url + img
            if log_path:
                download_File(img, folder, log_path)
            else:
                download_File(img, folder)
