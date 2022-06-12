import sqlite3

import pyEX as p
import csv
import json
import pandas as pd

import requests

class MyStock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.fiveDayAvg = None
        self.previousDayClosing = None
        self.canBeAdded = True
        self.historicalData = None
        self.analystRecs = None

    def setFiveDayAvg(self, average):
        self.fiveDayAvg = average
    def setPreviousDayClosing(self, prev):
        self.previousDayClosing = prev
    def dontAddToDatabase(self):
        self.canBeAdded = False

def csvParse(pathname, symbols):

    texts = open(pathname, 'r')
    read_file = csv.reader(texts)

    line_count = 0
    for row in read_file:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        elif row[2] != "":
            symbols.append(row[1])
            line_count += 1

IEX_TOKEN = 'pk_867243fb385545f2aeb650e9e79cd86f'

tickers = []

csvParse('driv_full-holdings_20220224.csv', tickers)
print(tickers)

data = []

client = p.Client(api_token = 'pk_58cac1674c65441cb2ac96d2cb886978', version='stable')

conn = sqlite3.connect('../project_data.db')
c = conn.cursor()

count = 0
for stock in tickers:
    c.execute('DROP TABLE IF EXISTS ' + stock + ';')

    count += 1
    print(stock)

    try:
        historicalPrices = client.chart(timeframe = '5y', closeOnly = True, symbol = stock, format = 'json')

        df = pd.json_normalize(historicalPrices)
        name = [[stock] * df.size]
        df['symbol'] = stock
        data.append(df)
    except:
        print("no data for " + stock)
final = data[0]
data.remove(data[0])
for each in data:
    final = final.append(each, ignore_index= True)

c.execute('DROP TABLE IF EXISTS ' + "ev_stocks" + ';')
final.to_sql("ev_stocks", conn)
print("test")