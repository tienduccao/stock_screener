import requests
import os
import json
from datetime import datetime


ACCESS_KEY = open('api_key.config').read().strip()
API_ENDPOINT = 'https://api.unibit.ai/v2/company/financials?'
CACHE_FOLDER = 'cache'
if not os.path.exists(CACHE_FOLDER):
    os.mkdir(CACHE_FOLDER)


def financial_report(ticker, statement, interval='annual'):
    statement_cache_folder = f'{CACHE_FOLDER}/{statement}'
    if not os.path.exists(statement_cache_folder):
        os.mkdir(statement_cache_folder)

    ticker_cache_file = f'{statement_cache_folder}/{ticker}_{interval}'
    if os.path.exists(ticker_cache_file):
        with open(ticker_cache_file) as f:
            _json = f.read()
        return _json
    else:
        r = requests.get(API_ENDPOINT, params={
            'tickers': ticker,
            'statement': statement,
            'startDate': '2010-01-01',
            'endDate': datetime.now().strftime("%Y-%m-%d"),
            'interval': interval,
            'accessKey': ACCESS_KEY
        })
        if r.status_code == 200:
           _json = json.dumps(r.json())
           with open(ticker_cache_file, 'w+') as out: 
               out.write(_json)
           return _json
    
