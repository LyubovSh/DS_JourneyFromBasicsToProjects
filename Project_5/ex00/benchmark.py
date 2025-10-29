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

if __name__=='__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com','anna@live.com', 'philipp@gmail.com']
    first_res = timeit.timeit(lambda: with_loop(emails), number=900)
    second_res = timeit.timeit(lambda: with_list_comprehension(emails), number=900)
    if first_res < second_res:
        print('Лучше использовать циклы', f'{first_res} vs {second_res}', sep = '\n')
    else:
        print('Лучше использовать списочные выражения', f'{second_res} vs {first_res}', sep = '\n')

