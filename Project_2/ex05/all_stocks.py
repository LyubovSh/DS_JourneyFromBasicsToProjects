import sys

def companies_and_stocks():
    COMPANIES = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Netflix': 'NFLX',
    'Tesla': 'TSLA',
    'Nokia': 'NOK'
    }

    STOCKS = {
    'AAPL': 287.73,
    'MSFT': 173.79,
    'NFLX': 416.90,
    'TSLA': 724.88,
    'NOK': 3.37
    }
    return COMPANIES, STOCKS

def parse_dict():
    dict_1, dict_2 = companies_and_stocks()
    result_dict = {}

    for key, value in dict_1.items():
        result_dict[key.lower()] = f'Тикер компании {key} - {value}, цена акций {key} — {dict_2[value]}'

    for key_2, value_2 in dict_2.items():
        tmp_company = ''
        price = 0

        for key_1, value_1 in dict_1.items():
            if key_2 == value_1:
                tmp_company = key_1
                price = value_2
        result_dict[key_2.lower()] = f'Тикер принадлежит компании {tmp_company}, цена акций {tmp_company} — {price}'
        result_dict[value_1.lower()] = f'Цена акций соответствует компании {tmp_company} и тикеру {value_1}' 
    
    return result_dict

if __name__ == '__main__':
    if len(sys.argv) != 1:
        input_str = sys.argv[1].split(',')
        for i in range(len(input_str)):
            if input_str[i] in ",' ":
                exit()
            else:
                input_str[i] = (input_str[i].lower()).strip()
        for elem in input_str:
            print(parse_dict().get(elem, 'Неизвестная компания'))
