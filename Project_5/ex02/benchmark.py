#!/usr/bin/env python3
import sys
import timeit

def with_loop(mail_list):
    result_list = list()
    for mail in mail_list * 5:
        if '@gmail.com' in mail:
            result_list.append(mail)
    return result_list

def with_list_comprehension(mail_list):
    return [mail for mail in mail_list * 5 if '@gmail.com' in mail]

def with_map(mail_list):
    return map(lambda x: x if '@gmail.com' in x else None, mail_list*5)

def with_filter(mail_list):
    return filter(lambda x: '@gmail.com' in x,mail_list*5)

if __name__ == '__main__':
    param = sys.argv
    if len(param) == 3:
        emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com','anna@live.com', 'philipp@gmail.com']
        try:
            iter = int(sys.argv[2])
            type_processing = sys.argv[1].lower()
        except ValueError:
            print('Некорректные параметры')
            sys.exit() 
        if type_processing == 'loop':
            print(timeit.timeit(lambda: with_loop(emails), number=iter))
        elif type_processing == 'list comprehension':
            print(timeit.timeit(lambda: with_list_comprehension(emails), number=iter))
        elif type_processing == 'map':
            print(timeit.timeit(lambda: with_map(emails), number=iter))
        elif type_processing == 'filter':
            print(timeit.timeit(lambda: with_filter(emails), number=iter))
        else:
            raise Exception('Введите 2 параметра: тип обработки и число повторений')
    else:
        raise Exception('Введите 2 параметра: тип обработки и число повторений')

