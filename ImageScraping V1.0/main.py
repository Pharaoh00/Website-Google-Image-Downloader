#!/usr/bin/env python
#-*- coding:utf-8 -*-
#main.py

from downloader import DownloaderImg
from multiprocessing import Pool
from multiprocessing import Process
import time
import math

def main():
    
    d = DownloaderImg(url)
    #d.setHome(home)
    #d.setMode("GOOGLE")
    d.parse_Image()
    d.createImgFolder()

    with Pool(processes=10) as pool:
        pool.map(d.download_File, d.getParsedLinks())
    
        

if __name__ == "__main__":
    
    start = time.time()
    url = "http://dofuswiki.wikia.com/wiki/Profession"
    home = "https://stardewvalleywiki.com"
    main()
    end = time.time()
    print("Tempo Total {}".format((end-start)/60))
