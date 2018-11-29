#!/usr/bin/env python
#-*- coding:utf-8 -*-
#test_path.py

import pathlib
import inspect
import os.path

#current_file = inspect.getfile(inspect.currentframe())
#current_path = os.path.dirname(os.path.abspath(current_file))
#new_folder = "imgs"
#img_folder = pathlib.PurePath(current_path).joinpath(new_folder)
#img_file = pathlib.PurePath(img_folder).joinpath("aiksduwnjbvcxp.jpg")
#print(img_file)

def join_paths(new_Folder, file_Name=False):
    """
    Requer uma string. Nome da pasta a ser criada.
    Por padrão file_Name é False. 
    Quando file_Name é falso retorna o abspath da 
    pasta passada em folder.
    Quando file_Name é verdadeiro junta o abspath da pasta
    passada mais o nome do arquivo passado e retorna.
    """
    current_file = inspect.getfile(inspect.currentframe())
    current_path = os.path.dirname(os.path.abspath(current_file))
    path_folder = pathlib.PurePath(current_path).joinpath(new_Folder)
    if file_Name:
        path_to_file = pathlib.PurePath(path_folder).joinpath(file_Name)
        return path_to_file
    if not file_Name:
        return path_folder

#print(join_paths("img", "aiksduwnjbvcxp.jpg"))
#print(join_paths("img"))
















