#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ----------------------------------------------------------- #
# Filename: main.py
# Creation Date: segunda-feira, 10 dezembro 2018 07:50
# Author: Hamon-Rá Taveira Guimarães
# Contact:
#         GitHub: https://github.com/
#         E-mail: hamoncsl@hotmail.com
#         Facebook: https://www.facebook.com/hamonra.taveira
# ----------------------------------------------------------- #

from downloader import DownloaderImg
from multiprocessing import Pool
from multiprocessing import Process
import time
import math

def main():
    
    d = DownloaderImg(url, mode="GOOGLE")
    d.parse_Image()

    with Pool(processes=10) as pool:
        pool.map(d.download_File, d.getParsedLinks())
    # for x in d.getParsedLinks():
    #     d.download_File(x)

if __name__ == "__main__":
    
    start = time.time()
    url = "https://www.google.com.br/search?q=terraria&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjX3fyq75ffAhUDI5AKHUkVDeYQ_AUIECgD&biw=1360&bih=628"
    home = ""
    main()
    end = time.time()
    print("Tempo Total {}".format((end-start)/60))
