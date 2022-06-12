import sqlite3
import pandas as pd
import numpy as np

# imports price data from excel (dollars/barrel for past 10 years by week)
oil_frame = pd.read_excel('Oil_Daily.xls', sheet_name='Data 1')
oil_frame = oil_frame.iloc[2:, :]  # cuts off metadata in the sheet
oil_frame.index = np.arange(1, len(oil_frame) + 1)  # sets indices to start a week count from 1
oil_frame = oil_frame.rename(columns={'Back to Contents': 'Date', 'Data 1: Crude Oil': 'WTI_Spot', 'Brent': 'Brent_Spot'})

# removes all rows where WTI_spot has missing  or negative value
oil_frame = oil_frame.drop(oil_frame[oil_frame.WTI_Spot < 0].index)
oil_frame = oil_frame.drop(oil_frame[oil_frame.Brent_Spot < 0].index)
oil_frame = oil_frame.dropna()  # drops all NaN values

# converts to correct data types; currently: TIMESTAMP, STRING, STRING
oil_frame['WTI_Spot'] = oil_frame['WTI_Spot'].astype(float)
oil_frame['Brent_Spot'] = oil_frame['Brent_Spot'].astype(float)

# Create connection to database
conn = sqlite3.connect('../project_data.db')
c = conn.cursor()
# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "oil_prices";')
oil_frame.to_sql('oil_prices', conn, index=False)  # adds oil_prices to database; field types: TIMESTAMP, REAL, REAL
conn.commit()

# DEPRECATED CODE BELOW

# Checking data types of all SQL tables
# c.execute('PRAGMA table_info(oil_prices);')
# print(c.fetchall())

# Viewing distribution of WTI_Spot prices (how many entries in each category there are)
# oil_viewer = oil_frame.copy()
# print(len(oil_viewer[oil_viewer.WTI_Spot < 20]))
# oil_viewer = oil_viewer.drop(oil_viewer[oil_viewer.WTI_Spot < 20].index)
# print(len(oil_viewer[oil_viewer.WTI_Spot < 30]))
# oil_viewer = oil_viewer.drop(oil_viewer[oil_viewer.WTI_Spot < 30].index)
# print(len(oil_viewer[oil_viewer.WTI_Spot < 40]))
# oil_viewer = oil_viewer.drop(oil_viewer[oil_viewer.WTI_Spot < 40].index)
# print(len(oil_viewer[oil_viewer.WTI_Spot < 50]))
# oil_viewer = oil_viewer.drop(oil_viewer[oil_viewer.WTI_Spot < 50].index)
# print(len(oil_viewer[oil_viewer.WTI_Spot < 60]))
# oil_viewer = oil_viewer.drop(oil_viewer[oil_viewer.WTI_Spot < 60].index)
# print(len(oil_viewer[oil_viewer.WTI_Spot < 70]))
# oil_viewer = oil_viewer.drop(oil_viewer[oil_viewer.WTI_Spot < 70].index)
# print(len(oil_viewer[oil_viewer.WTI_Spot < 80]))
# oil_viewer = oil_viewer.drop(oil_viewer[oil_viewer.WTI_Spot < 80].index)
# print(len(oil_viewer[oil_viewer.WTI_Spot < 90]))
# oil_viewer = oil_viewer.drop(oil_viewer[oil_viewer.WTI_Spot < 90].index)
# print(len(oil_viewer[oil_viewer.WTI_Spot < 100]))
# oil_viewer = oil_viewer.drop(oil_viewer[oil_viewer.WTI_Spot < 100].index)
