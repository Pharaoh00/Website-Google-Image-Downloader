#!/usr/bin/env python
#-*- coding:utf-8 -*-
#main.py

from parseImage import parse_Image
from test_path import join_paths
import pathlib
import time

def main():
    start = time.time()
    #Criando a pasta para os logs
    log_folder_name = "log"
    log_folder = join_paths(log_folder_name)
    pathlib.Path(log_folder).mkdir(parents=True,exist_ok=True)

    img_folder_name = "imgs"
    img_folder = join_paths(img_folder_name)
    pathlib.Path(img_folder).mkdir(parents=True,exist_ok=True)

    url = "https://stardewvalleywiki.com/Crops"
    home = "https://stardewvalleywiki.com"
    print("from main")
    parse_Image(url, img_folder, "NORMAL", home)
    end = time.time()
    print("Tempo total: {}".format(end-start))

main()
