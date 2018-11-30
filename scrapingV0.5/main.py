#!/usr/bin/env python
#-*- coding:utf-8 -*-
#main.py

from parseImageV2 import parse_Image
from downloaderV4 import download_File
from test_path import join_paths
#from split_seq import split_seq
import pathlib
import time
#import multiprocessing
from multiprocessing import Pool
import os
import json

def main():
    start = time.time()

    url = "https://stardewvalleywiki.com/Crops"
    # url = "https://www.google.com/search?hl=en&site=imghp&tbm=isch&tbs\=isz:l&q=stardew valley crops"
    home = "https://stardewvalleywiki.com"
    print("from main")

    number = 8
    urls_link = parse_Image(url, "NORMAL", home)
    #urls_link = parse_Image(url, "GOOGLE", home)
    #urls_link = split_seq(urls_link, number)

    p = Pool(10)
    record = p.map(download_File, iter(urls_link))
    p.terminate()
    p.join()

    # processes = []
    # for i in range(number):
    #     processes.append(multiprocessing.Process(target=download_File,
    #                                              args=(urls_link[i],
    #                                                    img_folder)))
    # for process in processes:
    #     process.start()
    # for process in processes:
    #     process.join()
    #download_File(parse_Image(url, "NORMAL", home), img_folder)
    
    end = time.time()
    print("Tempo total: {}".format(end-start))
    #CURRENT TIME = 435.0/60 = 7.5m
    #With pool(10) CURRENT TIME (for beat) = 212.7/60 = 3.55m
    #NEW RECORD CURRENT TIME 107.1/60 = 1.79m

if __name__ == "__main__":
    main()



