import sqlite3
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt

conn = sqlite3.connect('project_data.db') 
c = conn.cursor()

#gold table to dataframe
query = conn.execute("SELECT * From 'gold'")
cols = [column[0] for column in query.description]
gold = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
gold['Date'] = pd.to_datetime(gold.Date)



#oil table to dataframe
query2 = conn.execute("SELECT * From 'oil_prices'")
cols2 = [column[0] for column in query2.description]
oil = pd.DataFrame.from_records(data = query2.fetchall(), columns = cols2)
oil = oil[['Date','WTI_Spot']]
oil["Date"] = oil["Date"].str.replace("\s00:00:00", "")
oil['Date'] = pd.to_datetime(oil.Date)

#join tables on shared dates to removed any non shared values
merge_table = pd.merge(gold,oil,on ='Date')

#SPEARMAN CORRELATION COEEFICIENT
#H_0: There is NOT a relationship between gold and oil prices
#H_A: There IS a relationship between gold and oil prices

# merge_table.rename(columns={'Price': 'Gold_Price'}, inplace=True)
merge_table["Date"] = merge_table["Date"].astype("datetime64")
merge_table = merge_table.set_index('Date')
merge_table['Price'].plot(x='Date',y='Price')

# plt.xlabel("Date")
# plt.ylabel("Gold Price (USD/Ounce)")
# plt.title("Pandas Time Series Plot")
# plt.savefig("Gold_Prices")

# plt.xlabel("Date")
# plt.ylabel("Gold Price (USD/Ounce)")
# plt.title("Gold Prices From March 2020 to March 2022")
# plt.savefig("Gold_Prices")

spearman = stats.spearmanr(merge_table['Price'],merge_table['WTI_Spot'])
print(spearman)