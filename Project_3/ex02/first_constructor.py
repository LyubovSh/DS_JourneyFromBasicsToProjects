import sys
import os

class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self):
        with open(self.path, 'r', encoding = 'utf-8') as file:
            return file.read()

if __name__ == '__main__':
    path = ' '.join(sys.argv[1:])
    if os.path.exists(path) and os.path.isfile(path) and os.access(path, os.R_OK) and path[-3:] == 'csv':
        with open(path, 'r', encoding = 'utf-8') as file:
            flag = True
            title = (file.readline()).split(',')
            title = [elem.strip() for elem in title]
            if title[0].isdigit() is True or title[1].isdigit() is True:
                raise ValueError("Некоректный заголовок")
            file_list = file.readlines()
            for i in range(len(file_list)):
                line = file_list[i].split(',')
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
            if flag:
                class_instance = Research(path)
                print(class_instance.file_reader()) 
    else:
        raise ValueError("Некорректный файл")

