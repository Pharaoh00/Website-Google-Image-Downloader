#!/usr/bin/env python
#-*- coding:utf-8 -*-
#tools.py

import pathlib
import inspect
import os.path

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
        # Retorna o nome da pasta passada mais o nome do arquivo passado
        # PS: O nome do arquivo passado será o arquivo dentro da pasta desejada
        # Exemplo:
        # C:\User\MyUser\Desketop\CurrentProjet\Img\someImage.jpg
        return path_to_file
    if not file_Name:
        # Retorna somente o nome da pasta passada
        # Exemplo:
        # C:\User\MyUser\Desketop\CurrentProjet\Img\
        return path_folder

class CustomIter:
    def __init__(self, items):
        self.item = items
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.item):
            raise StopIteration

        index = self.index
        self.index += 1
        return self.item[index]
