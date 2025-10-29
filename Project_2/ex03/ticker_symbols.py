import sys

def companies_and_stocks():
    COMPANIES = {'Apple': 'AAPL', 'Microsoft': 'MSFT', 'Netflix': 'NFLX', 'Tesla': 'TSLA', 'Nokia': 'NOK'}
    STOCKS = {'AAPL': 287.73, 'MSFT': 173.79, 'NFLX': 416.90, 'TSLA': 724.88, 'NOK': 3.37}
    return COMPANIES, STOCKS

def improved_dict():
    companies, stocks = companies_and_stocks()[0], companies_and_stocks()[1]
    key_is_ticker = dict()
    key_is_company = dict()
    key_is_price = dict()
    for key_1, value_1 in companies.items():
        for key_2, value_2 in stocks.items():
            if value_1 == key_2:
                key_is_ticker[key_2.lower()] = [key_1, value_2]
                key_is_company[key_1.lower()] = [value_1, value_2]
                key_is_price[str(value_2).lower()] = [key_1, key_2]
    return key_is_ticker, key_is_company, key_is_price

                
if __name__ == '__main__':
    if len(sys.argv)==2:
        search = (sys.argv[1]).lower()
        ticker, company, price = improved_dict()[0], improved_dict()[1], improved_dict()[2]
        if search in ticker:
            print(f'Тикер принадлежит компании: {ticker[search][0]}, цена акций компании {ticker[search][1]}')
        elif search in company:
            print(f'Тикер компании: {company[search][0]}, цена акций компании {company[search][1]}')
        elif search in price:
            print(f'Цена соответствует компании: {price[search][0]} с тикером {price[search][1]}')
        else:
            print('Неизвестная компания')
    else:
        exit()
