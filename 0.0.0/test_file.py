#-*- coding:utf-8 -*-
#test_file.py

import os
import inspect
import pathlib

current_folder = inspect.getfile(inspect.currentframe())
current_path = os.path.dirname(os.path.abspath(current_folder))
#check_folder = os.path.exists(current_path + "\test")

pathlib.Path(current_path + "\\test").mkdir(parents=True, exist_ok=True)
