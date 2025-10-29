#!/usr/bin/env python3

import sys
import resource

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding = 'utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print('Некорректное имя файла')
        sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        start_time = resource.getrusage(resource.RUSAGE_SELF)
        list_from_file = read_file(sys.argv[1])
        end_time = resource.getrusage(resource.RUSAGE_SELF)
        for line in list_from_file:
            pass
        peak_memory = end_time.ru_maxrss / 1024 / 1024 / 1024
        user_time = end_time.ru_utime - start_time.ru_utime
        system_time = end_time.ru_stime - start_time.ru_stime
        total_time = user_time + system_time
        print(f"Peak Memory Usage = {peak_memory:.3f} GB")
        print(f"User Mode Time + System Mode Time = {total_time:.2f}s")
    else:
        raise Exception('Скрипт должен принимать 1 аргумент - путь к файлу')
