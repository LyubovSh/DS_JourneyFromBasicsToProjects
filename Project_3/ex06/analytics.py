import os
from random import randint
import logging
import requests 
import json 

logging.basicConfig(
    filename='analytics.log',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
   
class Research:
    def __init__(self, path, has_header=True):
        self.path = path
        self.has_header = has_header
        logging.info('Экземпляр класса создан с путем: %s', path)

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

    def send_telegram_message(self, flag):
        bot_token = '8344568047:AAEXzy4TlJk067lJPYLyzWdYTWo_spbprT8'
        chat_id = '8384118597'
        webhook_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}"
  
        if flag:
            message = "Отчёт успешно создан"
        else:
            message = "Отчёт не создан из-за ошибки"

        info = {'text': message, 'chat_id': chat_id}   
        response = requests.post(webhook_url, data=json.dumps(info), headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            logging.info('Сообщение успешно отправлено в Telegram')
            return True
        else:
            logging.error('Ошибка отправки в Telegram: %s', response.text)
            return False


    class Calculations:
        def __init__(self, data):   
            self.data = data

        def counts(self):
            logging.info('Подсчет числа орлов и решек')
            heads, tails = 0, 0
            for elem in self.data:
                if elem[0] == 1:
                    heads += 1
                else:
                    tails += 1
            logging.info(f'Орлов {heads} и {tails} решек')
            return heads, tails

        @staticmethod
        def fractions(heads, tails):
            if heads + tails != 0:
                logging.info(f'Подсчитываем проценты')
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
        logging.info('Делаем предсказания')
        return predictions
        
    def predict_last(self):
        logging.info('Возвращаем последний элемент')
        return self.data[-1]

    def save_data(self, data, file_name = 'tmp', extension = 'txt'):
        file_name = f'{file_name}.{extension}'
        with open(file_name, 'w', encoding = 'utf-8') as file:
            if isinstance(data, list):
                for item in data:
                    file.write(f"{item}\n")
            else:
                file.write(str(data))
        logging.info('Сохраняем результат в файл')
        return file_name
            
   