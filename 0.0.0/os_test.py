#-*- coding:utf-8 -*-
#os_test.py

import os
import inspect

current_folder = inspect.getfile(inspect.currentframe())
current_path = os.path.dirname(os.path.abspath(current_folder))

print(os.path.join(os.path.sep, current_path, "test4"))
