#!/usr/bin/env python3

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
 
if __name__=='__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com','anna@live.com', 'philipp@gmail.com']

    time_loop = timeit.timeit(lambda: with_loop(emails), number=900)
    time_list_comprehension = timeit.timeit(lambda: with_list_comprehension(emails), number=900)
    time_map = timeit.timeit(lambda: with_map(emails), number=900)

    if time_loop < time_list_comprehension and time_loop < time_map:
        print(f'Лучшие показалели времени исполнения у циклов {time_loop} против {time_list_comprehension} у списочных выражений и {time_map} у встроенной функции map')
    elif time_list_comprehension < time_loop and time_list_comprehension < time_map:
        print(f'Лучшие показалели времени исполнения у списочных выражений {time_list_comprehension} против {time_loop} у циклов и {time_map} у встроенной функции map')
    else:
        print(f'Лучшие показалели времени встроенной функции map {time_map} против {time_loop} у циклов и {time_list_comprehension} у списочных выражений')