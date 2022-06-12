import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

connection = sqlite3.connect('../data_deliverable/data/project_data.db')

ev_stock_df = pd.read_sql_query("SELECT * FROM ev_stocks", connection)
lithium_df = pd.read_sql_query("SELECT * FROM lithium", connection)
oil_df = pd.read_sql_query("SELECT * FROM oil_prices", connection)
for index, row in oil_df.iterrows():
    new_date = str(row[0]).replace(' 00:00:00', '')
    oil_df.loc[index,"Date"] = new_date


ev_date = []
ev_price = []
for i in range(0, 492):
    is_date = ev_stock_df['date'] == ev_stock_df.loc[i, "date"]
    ev_stock_df_copy = ev_stock_df[is_date]
    ev_date.append(ev_stock_df.loc[i, "date"])
    ev_price.append(ev_stock_df_copy["close"].mean())

new_ev_stock_df = pd.DataFrame(list(zip(ev_date, ev_price)),
                  columns =['Date', 'EV_Price'])


lithium_df.rename(columns = {'date':'Date'}, inplace = True)
lithium_df.rename(columns = {'price':'Price'}, inplace = True)
new_ev_stock_df.rename(columns = {'EV_Price':'Price'}, inplace = True)
oil_df.rename(columns = {'WTI_Spot':'Price'}, inplace = True)
oil_df = oil_df.loc[::-1].set_index(oil_df.index)

lith_bool = lithium_df.Date.isin(new_ev_stock_df.Date) & lithium_df.Date.isin(oil_df.Date)
ev_bool = new_ev_stock_df.Date.isin(oil_df.Date) & new_ev_stock_df.Date.isin(lithium_df.Date)
oil_bool = oil_df.Date.isin(new_ev_stock_df.Date) & oil_df.Date.isin(lithium_df.Date)
lithium_df = lithium_df[lith_bool][["Date", "Price"]]
new_ev_stock_df = new_ev_stock_df[ev_bool]
oil_df = oil_df[oil_bool][["Date", "Price"]]
lithium_df = lithium_df.reset_index(drop=True)
new_ev_stock_df = new_ev_stock_df.reset_index(drop=True)
oil_df = oil_df.reset_index(drop=True)

final_date = []
final_lithium = []
final_oil = []
final_ev = []
for index, row in lithium_df.iterrows():
    final_date.append(row["Date"])
    final_lithium.append(lithium_df.loc[index, "Price"])
    final_oil.append(oil_df.loc[index, "Price"])
    final_ev.append(new_ev_stock_df.loc[index, "Price"])

final_df = pd.DataFrame(list(zip(final_lithium, final_oil, final_ev)),
             columns =['Lithium', 'Oil', 'EV'])
final_df_graph = pd.DataFrame(list(zip(final_date, final_lithium, final_oil, final_ev)),
                        columns =['Date', 'Lithium', 'Oil', 'EV'])

connection.commit()
connection.close()

x = final_df.drop('EV',axis=1)
y = final_df['EV']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)
LR = LinearRegression()
LR.fit(x_train,y_train)
y_prediction =  LR.predict(x_test)
score=r2_score(y_test,y_prediction)
print("r2 score for oil and lithium to EV is ",score)
print("mean_squared_error is",mean_squared_error(y_test,y_prediction))
print("root_mean_squared error is",np.sqrt(mean_squared_error(y_test,y_prediction)))


x2 = final_df.drop(['EV', 'Oil'], axis=1)
y2 = final_df['EV']

x_train2, x_test2, y_train2, y_test2 = train_test_split(x2, y2, test_size = 0.2, random_state = 42)
LR2 = LinearRegression()
LR2.fit(x_train2,y_train2)
y_prediction2 =  LR2.predict(x_test2)
score2=r2_score(y_test2,y_prediction2)
print("r2 score for oil to ev is ",score2)
print("mean_squared_error is",mean_squared_error(y_test2,y_prediction2))
print("root_mean_squared error is",np.sqrt(mean_squared_error(y_test2,y_prediction2)))


x3 = final_df.drop(['EV', 'Lithium'], axis=1)
y3 = final_df['EV']

x_train3, x_test3, y_train3, y_test3 = train_test_split(x3, y3, test_size = 0.2, random_state = 42)
LR3 = LinearRegression()
LR3.fit(x_train3,y_train3)
y_prediction3 =  LR3.predict(x_test3)
score3=r2_score(y_test3,y_prediction3)
print("r2 score for lithium to ev is ",score3)
print("mean_squared_error is",mean_squared_error(y_test3,y_prediction3))
print("root_mean_squared error is",np.sqrt(mean_squared_error(y_test3,y_prediction3)))

final_df_graph.plot(x='Date', y='Lithium', style='.', color='purple', figsize=(11,9), title='Lithium Price (USD/Metric Ton) Over Time')
plt.savefig('lithium_over_time')

final_df_graph.plot(x='Date', y='Oil', style='.', color='purple', figsize=(11,9), title='WTI Spot Oil Price (USD/Barrel) Over Time')
plt.savefig('oil_over_time')

final_df_graph.plot(x='Date', y='EV', style='.', color='purple', figsize=(11,9), title='Avg EV Stock Prices (USD) Over Time')
plt.savefig('ev_stocks_over_time')


# I referenced this site to run linear regression tests:
# https://www.analyticsvidhya.com/blog/2021/05/multiple-linear-regression-using-python-and-scikit-learn/






















