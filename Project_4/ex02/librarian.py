#!/usr/bin/env python3
import os
import subprocess

virtual_env = os.getenv('VIRTUAL_ENV', default=None)

if virtual_env != None:
    with open('lib.txt', 'w', encoding = 'utf-8') as file_1:
        file_1.write('beautifulsoup4\npytest\n')
        lib_install = subprocess.run(['pip', 'install', '-r', 'lib.txt'], check=True)
        os.remove("lib.txt")
    result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
    with open('requirements.txt', 'w', encoding = 'utf-8') as file_2:
        file_2.write(result.stdout)
    print(result.stdout)
else:
    raise Exception('Скрипт должен быть запущен из виртуального окружения')