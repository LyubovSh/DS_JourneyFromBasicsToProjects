'''Создайте ещё один скрипт, 
который принимает адрес электронной почты, 
ищет соответствующее имя в файле, 
созданном первым скриптом, и возвращает первый абзац письма: 
Уважаемый Иван, добро пожаловать в нашу команду! Мы уверены, что вам будет приятно работать с вами.
 Это обязательное условие для специалистов, которых нанимает наша компания.
Использование конструкции 'la-la {0}'.format(text) запрещено. 
Вместо этого используйте f-строки. Они быстрее и удобнее для чтения.'''
import sys

if __name__ == '__main__':
    if len(sys.argv) == 2:
        find_email = sys.argv[1]
        with open('employees.tsv', 'r', encoding = 'utf-8') as file:
            for line in file:
                line = line.split('\t')
                if find_email in line:
                    print(f'Dear {line[0]}, welcome to our team! We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires.')
                    break

