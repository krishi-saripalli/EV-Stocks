from distutils import errors
from bs4 import BeautifulSoup
import numpy
import requests
import os
import urllib
import json
import sqlite3
import pandas as pd
from pandas import json_normalize 
import datetime

import pandas as pd
import sqlite3

conn = sqlite3.connect('/Users/saripallikrishi/Desktop/goldprices.db')
cursor = conn.cursor()
df = pd.read_csv('/Users/saripallikrishi/Desktop/Gold Prices - Sheet1.csv')
df["Price (USD/Ounce)"] = df["Price (USD/Ounce)"].replace(",", "", regex=True)
df["Price (USD/Ounce)"] = df["Price (USD/Ounce)"].apply(pd.to_numeric, downcast='float', errors='coerce')
df = df.rename(columns={'Price (USD/Ounce)': 'Price'})
pd.to_datetime(df['Date'])
df.to_sql('gold',conn,if_exists='replace', index=False)
cursor.execute("""ALTER TABLE gold ALTER COLUMN Price FLOAT ALTER COLUMN Date DATE""")
conn.commit()


# conn = sqlite3.connect('gold.db')
# c = conn.cursor()

# c.execute('CREATE TABLE IF NOT EXISTS products (product_name text, price number)')
# conn.commit()

# data = {'product_name': ['Computer','Tablet','Monitor','Printer'],
#         'price': [900,300,450,150]
#         }

# df = pd.DataFrame(data, columns= ['product_name','price'])
# df.to_sql('products', conn, if_exists='replace', index = False)
 
# c.execute('''  
# SELECT * FROM products
#           ''')

# for row in c.fetchall():
#     print (row)
