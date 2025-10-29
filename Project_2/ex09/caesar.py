import sys

def ceaar(param):
    result = ''
    if param[0] not in ('encode','decode'):
        raise ValueError('Некорректный режим кодировки')
    for letters in param[1]:
        flag = True
        if (ord(letters) < 65) or (ord(letters) > 122):
            shift = ord(letters)
            flag = False
            if letters.isalpha():
                raise ValueError('Скрипт пока не поддерживает ваш язык')
        base = ord('a') if letters.islower() else ord('A')
        if param[0] == 'encode' and flag:
            shift = ((ord(letters) - base + int(param[2])) % 26 + base)
        elif param[0] == 'decode' and flag:
            shift = ((ord(letters) - base - int(param[2])) % 26 + base)
        letters = chr(shift)
        result += letters
    return result

if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise ValueError('Недопустимое количество параметров')
    else:
        parametrs = sys.argv[1:]
        print(ceaar(parametrs))



