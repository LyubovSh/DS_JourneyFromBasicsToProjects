#!/usr/bin/env python3

import urllib3
from bs4 import BeautifulSoup
import sys
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def data_parser(ticker_name, field_name):
    url = f"https://finance.yahoo.com/quote/{ticker_name}/financials/?p={ticker_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
    response = http.request('GET', url, headers=headers, timeout=15)

    if response.status == 200:

        soup = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        if soup.find('div', id='consent-page'):
            raise Exception("Обнаружена страница согласия. Необходимо ручное вмешательство или использование API")
            
        field_div = soup.find('div', attrs={'title': field_name})
        if field_div is not None:
            parent_row = field_div.find_parent('div', class_='row')
            result = [field_name]
            value_cells = parent_row.find_all('div', class_='column')
            
            for cell in value_cells:
                text = cell.text.strip()
                if text and any(char.isdigit() for char in text):
                    result.append(text)
            return tuple(result)
        else:
            raise Exception(f"Field '{field_name}' not found")
    else:
        raise Exception(f"URL does not exist (status code: {response.status})")
    
if __name__ == "__main__":
    if len(sys.argv) == 3:
        ticker = sys.argv[1].upper()
        field = sys.argv[2]
        print(data_parser(ticker, field))
    else:
        raise Exception(f"Incorrect arguments")