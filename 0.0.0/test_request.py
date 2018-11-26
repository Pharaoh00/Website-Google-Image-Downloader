#-*- coding:utf-8 -*-
#test_request.py

"""
Codigo baseado: 
https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py/16696317#16696317
"""

from bs4 import BeautifulSoup
import requests
import os

# url do site para download
url = "https://stardewvalleywiki.com/Crops"
# se necessario o site "home" page para download
# caso as imagens não estive no link informado
# usar a url da home
img_url = "https://stardewvalleywiki.com"

def download_file(url):
    local_filename = url.split("/")[-1]
    print("Download {} -> {}".format(url, local_filename))

    r = requests.get(url, stream=True)
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
                
    return local_filename

web_source = requests.get(url)
web_to_text = web_source.text
soup = BeautifulSoup(web_to_text, "html.parser")
for link in soup.findAll("img"):
    image_links = link.get("src")
    if not image_links.startswith('http'):
        # se tiver algum problema, usar a url ao inves da img_url
        # provavelmente o link das imagens serão direcionados
        # em cima da url da home page, não da url da pagina desejada
        image_links = img_url + "/" + image_links
    download_file(image_links)
