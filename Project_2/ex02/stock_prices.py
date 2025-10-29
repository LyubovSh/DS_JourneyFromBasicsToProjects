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

    result_dict = COMPANIES | STOCKS
    return result_dict

if __name__ == '__main__':
    if len(sys.argv)==2:
        search_company = sys.argv[1]
        search_company = companies_and_stocks().get(search_company.title(), 'Unknown company')
        if search_company != 'Unknown company':
            print(companies_and_stocks()[search_company])
        else:
            print(search_company)
    else:
        exit()
