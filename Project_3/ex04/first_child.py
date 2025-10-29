import sys
from random import randint

class Research:
    def __init__(self, path, has_header=True):
        self.has_header = has_header
        self.path = path

    def file_reader(self):
        flag = True
        result_list = list()
        with open(self.path, 'r', encoding = 'utf-8') as file:
            file = file.readlines()
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

    class Calculations():
        def __init__(self, data):   
            self.data = data

        def counts(self):
            heads, tails = 0, 0
            for elem in self.data:
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

class Analytics(Research.Calculations):
    def predict_random(self, num_predictions):
        predictions = []
        for i in range(num_predictions):
            first = randint(0, 1)
            second = 1 - first
            predictions.append([first, second])
        return predictions
        
    def predict_last(self):
        return self.data[-1]


if __name__ == '__main__':
    path = sys.argv[1]
    if len(sys.argv) == 3:
        has_header = True if sys.argv[2] in 'True' else False
    else:
        has_header = True
    if path[-3:] == 'csv':
        class_instance = Research(path, has_header)
        data = class_instance.file_reader()
        print(data)
        calculations = Research.Calculations(data)
        heads, tails = calculations.counts()
        heads_percent, tails_percent = Research.Calculations.fractions(heads, tails)
        print(f"{heads} {tails}")
        print(f"{heads_percent} {tails_percent}")
        analytics = Analytics(data)
        print(analytics.predict_random(5))
        print(analytics.predict_last())
    else:
        raise ValueError("Некорректный файл")

