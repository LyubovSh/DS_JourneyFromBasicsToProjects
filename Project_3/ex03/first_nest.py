import sys
import os


class Research:
    def __init__(self, path, has_header=True):
        self.path = path
        self.has_header = has_header

    def file_reader(self):
        flag = True
        with open(self.path, 'r', encoding = 'utf-8') as file:
            file = file.readlines()
            result_list = list()
            for line in file[int(self.has_header):]:
                line = line.split(',')
                try:
                    line = list(map(lambda x: int(x), line))
                except ValueError:
                    print('Файл содержит некорректные значения')
                    flag = False
                if flag:
                    if line[0] not in (0, 1) or line[1] not in (0, 1):
                        raise ValueError("Файл должен содержать 0 и 1")
                        flag = False
                    if line[0] == line[1]:
                        raise ValueError("Значения не должны быть =")
                result_list.append(line)
            if flag:
                return result_list
            else:
                exit()

    class Calculations:
        @staticmethod
        def counts(data):
            heads, tails = 0, 0
            for elem in data:
                if elem[0] == 1:
                    heads += 1
                else:
                    tails += 1
            return heads, tails

        @staticmethod
        def fractions(heads, tails):
            if heads + tails != 0:
                return ((heads / (heads + tails)) * 100),  ((tails / (heads + tails)) * 100)
            else:
                return 0, 0

if __name__ == '__main__':
    path = sys.argv[1]
    if len(sys.argv) == 3:
        has_header = True if sys.argv[2] in 'True' else False
    else:
        has_header = True
    if os.path.exists(path) and os.path.isfile(path) and os.access(path, os.R_OK) and path[-3:] == 'csv':
            class_instance = Research(path, has_header)
            data = class_instance.file_reader()
            print(data)
            heads, tails = Research.Calculations.counts(data)
            heads_percent, tails_percent = Research.Calculations.fractions(heads, tails)
            print(f"{heads} {tails}")
            print(f"{heads_percent} {tails_percent}")
    else:
        raise ValueError("Некорректный файл")

