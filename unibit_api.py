import requests
import os
import json
from datetime import datetime


ACCESS_KEY = open('api_key.config').read().strip()
API_ENDPOINT = 'https://api.unibit.ai/v2'
FINANCIAL_API = f'{API_ENDPOINT}/company/financials?'
COMPANIES_API = f'{API_ENDPOINT}/ref/companyList?'
PROFILE_API = f'{API_ENDPOINT}/company/profile?'
CACHE_FOLDER = 'cache'
COMPANIES_CSV = CACHE_FOLDER + '/exchange_{exchange}.csv'
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
    else:
        r = requests.get(FINANCIAL_API, params={
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

    return json.loads(_json)


def list_companies(exchange):
    r = requests.get(COMPANIES_API, params={
        'exchange': exchange,
        'accessKey': ACCESS_KEY
    })
    if r.status_code == 200:
        return r.json()


def download_company_profiles(exchange):
    companies = list_companies(exchange)
    tickers = [item['ticker'] for item in companies['result_data']]

    def divide_chunks(_list, chunk_size):
        for i in range(0, len(_list), chunk_size):
            yield _list[i:i + chunk_size]

    for sub_tickers in divide_chunks(tickers, chunk_size=50):
        r = requests.get(PROFILE_API, params={
            'tickers': ','.join(sub_tickers),
            'dataType': 'csv',
            'accessKey': ACCESS_KEY
        })
        if r.status_code == 200:
            with open(COMPANIES_CSV.format(exchange=exchange), 'a+') as out:
                out.write(r.text)
