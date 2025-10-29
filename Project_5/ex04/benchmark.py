#!/usr/bin/env python3
import timeit
import random
from collections import Counter

def using_counter(list_elem):
    return Counter(list_elem)

def using_my_func(list_elem):
    unique_elem = set(list_elem)
    result_dict = dict()
    for elem in unique_elem:
        result_dict[elem] = list_elem.count(elem)
    return result_dict

def top_using_counter(counter_dict):
    return counter_dict.most_common(10)

def top_using_my_func(my_func_dict):
    my_func_dict = sorted(my_func_dict.items(), key=lambda x: x[1], reverse=True)
    return my_func_dict[:10]
        
if __name__ == '__main__':
    list_num = [random.randrange(0, 100) for _ in range(20)]
    time_counter = timeit.timeit(lambda: using_counter(list_num))
    time_func = timeit.timeit(lambda: using_my_func(list_num))
    print(f'Время работы Counter: {time_counter}\nВремя работы моей функции: {time_func}')
    obj_1 = using_counter(list_num)
    obj_2 = using_my_func(list_num)
    time_top_counter = timeit.timeit(lambda: top_using_counter(obj_1))
    time_top_func = timeit.timeit(lambda: top_using_my_func(obj_2))
    print(f'Время работы поиска топ 10 у Counter: {time_top_counter}\nВремя работы поиска топ 10 у моей функции: {time_top_func}')


    


