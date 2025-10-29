#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import sys
import time
import pytest

def data_parser(ticker_name, field_name):
    time.sleep(5)
    
    url = f"https://finance.yahoo.com/quote/{ticker_name}/financials/?p={ticker_name}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    request = requests.get(url, headers=headers, timeout=15)
    
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, 'html.parser')

        if soup.find('div', id='consent-page'):
            raise Exception("Обнаружена страница согласия. Необходимо ручное вмешательство или использование API")

        field_div = soup.find('div', attrs={'title': field_name})

        if field_div != None:
            parent_row = field_div.find_parent('div', class_='row')
            result = [field_name]  
            value_cells = parent_row.find_all('div', class_='column')
                
            for cell in value_cells:
                text = cell.text.strip()
                if text and any(char.isdigit() for char in text):
                    result.append(text)
            return ((result))
        else:
            raise Exception(f"Field '{field_name}' not found")
    else:
        raise Exception(f"URL does not exist")

def test_invalid_field_raises_exception():
    with pytest.raises(Exception) as exc_info:
        data_parser('INVALID', 'NonExistentField')
    assert "not found" in str(exc_info.value).lower()

def test_type(param):
    assert isinstance(result, tuple), f"Invalid return value type {type(param)}"

def test_return_value(param, arg):
    assert param[0] == arg, 'It was necessary to find other information'

if __name__ == "__main__":
    flag = True
    if len(sys.argv) != 3:
        flag = False
    if flag:
        ticker = sys.argv[1].upper()
        field = sys.argv[2]
        result = data_parser(ticker, field)
        print(result)
        test_type(result)
        test_return_value(result, field)
    else:
        raise Exception(f"Incorrect arguments")
    test_invalid_field_raises_exception()
