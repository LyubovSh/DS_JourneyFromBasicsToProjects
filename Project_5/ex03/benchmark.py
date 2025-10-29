#!/usr/bin/env python3
import sys
import timeit
from functools import reduce

def sum_using_loops(num):
    res  = 0
    for i in range(1, num+1):
        res += i**2
    return res

def sum_using_reduce(num):
    return reduce(lambda x, y: x+y**2, range(1, num+1), 0)

if __name__ == '__main__':
    if len(sys.argv) == 4:
        try:
            type_processing = sys.argv[1].lower()
            iter = int(sys.argv[2])
            num_sqrt = int(sys.argv[3])
        except ValueError:
            print('Некорректные параметры')
            sys.exit() 
        if type_processing == 'loop':
            print(timeit.timeit(lambda: sum_using_loops(num_sqrt), number = iter))
        elif type_processing == 'reduce':
            print(timeit.timeit(lambda: sum_using_reduce(num_sqrt), number = iter))
        else:
            raise Exception('Введите 3 аргумента: тип обработки, число повторений и число для суммирования')
    else:
        raise Exception('Введите 3 аргумента: тип обработки, число повторений и число для суммирования')