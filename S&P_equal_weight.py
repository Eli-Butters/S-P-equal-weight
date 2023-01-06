import numpy as np
import pandas as pd
import requests
import math
import xlsxwriter

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

stocks = pd.read_csv('sp_500_stocks.csv')

IEX_CLOUD_API_TOKEN = 'sk_88ede6c864fb433a92ac08d2ab9e555a'

my_columns = ['Ticker', 'Stock Price', 'Market Cap', 'Shares']
final_df = pd.DataFrame(columns=my_columns)

symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []

#for idx, stock in enumerate(stocks['Ticker']):
    #api_url = f'https://api.iex.cloud/v1/data/core/quote/{stock}?token={IEX_CLOUD_API_TOKEN}'
    #data = requests.get(api_url).json()
    #final_df.loc[idx] = [stock, data[0]['latestPrice'], data[0]['marketCap'], 'N/A']

for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

count = 0

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://api.iex.cloud/v1/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_df.loc[count] = [symbol, data[symbol]['quote']['latestPrice'], data[symbol]['quote']['marketCap'], 'N/A']
        count += 1
    
portfolio_size = input('Enter the value of your portfolio:')

try:
    val = float(portfolio_size)
except ValueError: 
    print("That's not a number! /nPlease try again")
    portfolio_size = input('Enter the value of your portfolio:')
    val = float(portfolio_size)

position_size = val/len(final_df.index)

for i in range(len(final_df.index)):
    final_df.loc[i, 'Shares'] = math.floor(position_size/final_df.loc[i, 'Stock Price'])

print(final_df)