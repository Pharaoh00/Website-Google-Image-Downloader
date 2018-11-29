#!/usr/bin/env python
#-*- coding:utf-8 -*-
#parseImageV2.py

import requests
from bs4 import BeautifulSoup
import random
import json


def parse_Image(url, mode="NORMAL", home=False):
    """
    (In progress)
    Retorna uma lista com todas as url's encontradas
    
    Requer uma url.
    Para o google:
    De preferencia a url deve começar com "http://www.google.com/search?"

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
    
    #Não esquecer de olhar multithreads
    #Fazer com que o download seja mais rapido.
    #append os links encontrados em uma lista, dividir a lista
    #na quantidade de threads desejados, e passar a cada lista
    #para seu respectivo download_file(url)
    links_list = []
    au = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"]
    headers= {"User-Agent": random.choice(au)}
    source_code = requests.get(url, headers=headers)
    html = source_code.content
    soup = BeautifulSoup(html, "lxml")
    
    if mode == "GOOGLE":
        for link in soup.find_all("div", {"class": "rg_meta notranslate"}):
            img = json.loads(link.text)
            links_list.append(img["ou"])
    elif mode == "NORMAL":
        for link in soup.find_all("img"):
            img = link.get("src")
            if home:
                if not img.startswith("http"):
                    #Não esquecer de checar se a url termina com "/"
                    #Caso não, adicionar a "/"
                    #if not img.endswith("/"):
                    #img = home + "/" + img
                    #etc...
                    img = home + img
                    links_list.append(img)
            elif not home:
                if not img.startswith("http"):
                    img = url + img
                    links_list.append(img)
            else:
                links_list.append(img)

    return links_list

# url = "https://stardewvalleywiki.com/Crops"
# home = "https://stardewvalleywiki.com"
# print(len(parse_Image(url, "NORMAL", home)))
