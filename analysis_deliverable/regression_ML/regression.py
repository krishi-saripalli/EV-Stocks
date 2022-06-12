import math
import sqlite3
import numpy as np
import statsmodels.api as sm
import pandas as pd
from sklearn.model_selection import train_test_split as splt
import matplotlib.pyplot as plt


# converts date from dash format to slash format to compare
def convert_date(date):
    year = date[2:4]
    month = date[5:7]
    if month[0] == "0":
        month = month[1]
    day = date[8:10]
    if day[0] == "0":
        day = day[1]
    return month + "/" + day + "/" + year


# convert lithium date format into the one we use in preprocessing
def convert_lithium(date):
    year = date[10:12]
    if date[0:3] == "Mar":
        month = "3"
    if date[0:3] == "Feb":
        month = "2"
    if date[0:3] == "Jan":
        month = "1"
    if date[0:3] == "Dec":
        month = "12"
    if date[0:3] == "Nov":
        month = "11"
    if date[0:3] == "Oct":
        month = "10"
    if date[0:3] == "Sep":
        month = "9"
    if date[0:3] == "Aug":
        month = "8"
    if date[0:3] == "Jul":
        month = "7"
    if date[0:3] == "Jun":
        month = "6"
    if date[0:3] == "May":
        month = "5"
    if date[0:3] == "Apr":
        month = "4"
    day = date[4:6]
    if day[0] == "0":
        day = day[1]
    return month + "/" + day + "/" + year


# all tickers present in our database
def get_tickers():
    conn = sqlite3.connect('project_data.db')
    # contains GOOGL, AAPL, QCOM, NVDA, RIVN, TSLA, NIO, GM, F, BIDU, NXPI, XPEV, HOG, BE, LCID, VNE, PLUG, AMBA, YNDX
    stocks = pd.read_sql_query('''SELECT DISTINCT symbol FROM ev_stocks''', con=conn)
    return stocks


# returns preprocessed dataframe of prices by date (if ticker is left blank, it averages all stocks for each day)
def preprocess_sequential_data(ticker=None):
    conn = sqlite3.connect('project_data.db')

    stock_dates = pd.read_sql_query('''SELECT DISTINCT date FROM ev_stocks ORDER BY date ASC''', con=conn,
                                    dtype="string").applymap(convert_date).applymap(lambda x: x.strip())
    oil_dates = pd.read_sql_query('''SELECT DISTINCT Date FROM oil_prices''', con=conn, dtype="string").applymap(
        lambda x: x[:-9]).applymap(convert_date).applymap(lambda x: x.strip())
    gold_dates = pd.read_sql_query('''SELECT DISTINCT Date FROM gold''', con=conn, dtype="string").applymap(
        lambda x: x.strip())
    lithium_dates = pd.read_sql_query('''SELECT DISTINCT date FROM lithium''', con=conn, dtype="string").applymap(
        lambda x: x.strip()).applymap(convert_lithium)

    stockoilmerge = stock_dates.merge(oil_dates, left_on='date', right_on='Date')  # gets dates in both stock/oil
    goldlithmerge = gold_dates.merge(lithium_dates, left_on='Date', right_on='date')  # gets dates in both gold/lithium
    all_common_dates = stockoilmerge.merge(goldlithmerge, left_on='Date', right_on='Date')['Date']
    all_common_dates = all_common_dates.values.reshape(-1, ).tolist()  # converts to a list

    # getting the full data from stocks, oil, and gold, applying map to normalize dates
    stockdata = pd.read_sql_query('''SELECT * FROM ev_stocks''', con=conn, dtype='string')
    stockdata['date'] = stockdata['date'].apply(convert_date).apply(lambda x: x.strip())
    oildata = pd.read_sql_query('''SELECT * FROM oil_prices''', con=conn, dtype='string')
    oildata['Date'] = oildata['Date'].apply(lambda x: x[:-9]).apply(convert_date).apply(lambda x: x.strip())
    golddata = pd.read_sql_query('''SELECT * FROM gold''', con=conn, dtype='string')
    golddata['Date'] = golddata['Date'].apply(lambda x: x.strip())
    lithiumdata = pd.read_sql_query('''SELECT * FROM lithium''', con=conn, dtype='string')
    lithiumdata['date'] = lithiumdata['date'].apply(lambda x: x.strip()).apply(convert_lithium)

    # finding all rows with our common dates in them
    stockdata = stockdata[stockdata['date'].isin(all_common_dates)]  # descending order by date
    stockdata = stockdata.iloc[::-1].reset_index()  # reverses to be ascending order by date
    oildata = oildata[oildata['Date'].isin(all_common_dates)].reset_index()  # ascending order by date
    golddata = golddata[golddata['Date'].isin(all_common_dates)].reset_index()  # ascending order by date
    lithiumdata = lithiumdata[lithiumdata['date'].isin(all_common_dates)]
    average_stock_prices = list()
    lithium_prices = list()
    for date in all_common_dates:
        all_companies = stockdata[stockdata['date'] == date]
        if ticker is not None:
            all_companies = all_companies[all_companies['symbol'] == ticker]  # selects only one ticker if specified
        avg = np.average(all_companies['close'].astype(np.float32))
        average_stock_prices.append(avg)
        lithium_row = lithiumdata[lithiumdata['date'] == date]
        lithium_prices.append(float(lithium_row['price']))

    final_data = {'Date': oildata['Date'], 'Oil': oildata['WTI_Spot'].astype(np.float32),
                  'Gold': golddata['Price'].astype(np.float32), 'Lithium': lithium_prices,
                  'Stocks': average_stock_prices}
    prices_by_date = pd.DataFrame(data=final_data)
    return prices_by_date


def oil_regression():
    prices = preprocess_sequential_data()
    Y = prices['Stocks']
    X = prices['Oil']
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    results = model.fit()
    print(results.summary())


def gold_regression():
    prices = preprocess_sequential_data()
    Y = prices['Stocks']
    X = prices['Gold']
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    results = model.fit()
    print(results.summary())


def lithium_regression():
    prices = preprocess_sequential_data()
    Y = prices['Stocks']
    X = prices['Lithium']
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    results = model.fit()
    print(results.summary())


def all_vars_regression(test_size, ticker=None, to_print=False):
    prices = preprocess_sequential_data(ticker)
    Y = prices['Stocks']
    X = prices[['Oil', 'Gold', 'Lithium']]
    X_train, X_test, Y_train, Y_test = splt(X, Y, test_size=test_size)
    X_train = sm.add_constant(X_train)
    model = sm.OLS(Y_train, X_train)
    results = model.fit()
    X_test = sm.add_constant(X_test)
    predictions = results.predict(X_test)
    mse = MSE(predictions, Y_test)
    me = MAE(predictions, Y_test)
    if to_print:
        print(results.summary())
        print("MSE on Test: " + str(mse) + ", Dummy: " + str(baseline_MSE(Y.reset_index())))
        print("MAE on Test: " + str(me) + ", Dummy: " + str(baseline_MAE(Y.reset_index())))
    return mse, results.rsquared


def all_sequential_regression(movement_test_size=86):
    prices = preprocess_sequential_data()
    Y = prices['Stocks']
    X = prices[['Oil', 'Gold', 'Lithium']]
    tr = len(X) - movement_test_size  # size of training sequence
    te = movement_test_size  # size of testing sequence
    seq_Xtrain = X[0:tr]
    seq_Xtest = X[-te:]
    seq_Ytrain = Y[0:tr]
    seq_Ytest = Y[-te:]
    seq_Xtrain = sm.add_constant(seq_Xtrain)
    model = sm.OLS(seq_Ytrain, seq_Xtrain)
    seq_results = model.fit()
    seq_Xtest = sm.add_constant(seq_Xtest)
    seq_preds = seq_results.predict(seq_Xtest)
    mm = movement_metric(seq_preds.reset_index(), seq_Ytest.reset_index(), te)
    print("Movement Metric: " + str(mm))
    mse = MSE(seq_preds, seq_Ytest)
    print("MSE on Test: " + str(mse) + ", Dummy: " + str(baseline_MSE(Y.reset_index())))
    return mm


# calculates MSE between predictions and labels from our linear model
def MSE(predictions, labels):
    se_list = list()
    for pred, lab in zip(predictions, labels):
        se_list.append(math.pow(lab - pred, 2))
    return np.average(se_list)


# mean absolute error
def MAE(predictions, labels):
    e_list = list()
    for pred, lab in zip(predictions, labels):
        e_list.append(abs(lab - pred))
    return np.average(e_list)


# if price is X this week, it assumes it will be X next week
# this is 17.5 for the entire dataset
def baseline_MSE(labels):
    se_list = list()
    for i in range(1, len(labels)):
        se_list.append(math.pow(labels['Stocks'][i - 1] - labels['Stocks'][i], 2))
    return np.average(se_list)


# if price is X this week, it assumes it will be X next week
def baseline_MAE(labels):
    se_list = list()
    for i in range(1, len(labels)):
        se_list.append(abs(labels['Stocks'][i - 1] - labels['Stocks'][i]))
    return np.average(se_list)


# tracks if model can predict sequential increases or decreases
# if output is negative, it fails the majority of the time, and if positive it succeeds
# movement metric = ((correct movement predictions - incorrect movement predictions) / test size) + 0.5
def movement_metric(predictions, seq_labels, movement_test_size):
    real_increase_decrease = list()
    for i in range(1, len(seq_labels)):
        if seq_labels['Stocks'][i] - seq_labels['Stocks'][i - 1] >= 0:
            real_increase_decrease.append(1)
        else:
            real_increase_decrease.append(-1)
    movement_list = list()  # 1 = correct movement prediction, -1 = incorrect prediction
    for i in range(1, len(predictions)):
        temp = 0  # represents increase or decrease
        if predictions[0][i] - predictions[0][i - 1] >= 0:
            temp = 1
        else:
            temp = -1
        if temp == real_increase_decrease[i-1]:
            movement_list.append(1)
        else:
            movement_list.append(-1)
    return (np.sum(movement_list) / movement_test_size) + 0.5


# plots MSE and R-squared values corresponding the size of the test set we use to validate our model!
def plot_model_data(mse=False, r2=False, mm_kf=False, mse_kf=False, kf_dist=False):
    if mse or r2:
        test_sizes = [i / 100 for i in range(50, 0, -2)]
        mse_list = list()
        rsquared_list = list()
        for size in test_sizes:
            mse, rsquared = all_vars_regression(size)
            mse_list.append(mse)
            rsquared_list.append(rsquared)

    if mse:
        fig, ax = plt.subplots()
        ax.plot(test_sizes, mse_list, color='black', linewidth=3.5)
        plt.title('Mean Square Error by Test Size', fontsize=14)
        plt.xlabel('Test Set Proportion of Total Data')
        plt.ylabel('Mean Square Error')
        ax.hlines(y=17.5, xmin=0, xmax=0.5, color='r')
        plt.gcf().set_size_inches(10, 5)
        plt.legend(['MSE', 'Baseline MSE'], loc='upper right')
        plt.show()

    if r2:
        plt.plot(test_sizes, rsquared_list, color='black', linewidth=3.5)
        plt.title('Model Fit R-squared by Test Size', fontsize=14)
        plt.xlabel('Test Set Proportion of Total Data')
        plt.ylabel('R-squared Metric')
        plt.gcf().set_size_inches(10, 5)
        plt.show()

    if mm_kf:
        k_list = [i for i in range(2, 21)]
        mms = list()
        for k in k_list:
            _, _, mm = k_fold_val(k)
            mms.append(mm)
        plt.plot(k_list, mms, color='black', linewidth=3.5)
        plt.title('% Correct Movement Direction by K', fontsize=14)
        plt.xlabel('Number of Folds (K)')
        plt.ylabel('% Correct Stock Movement Direction Classification')
        plt.gcf().set_size_inches(10, 5)
        plt.xticks([i for i in range(2, 21)])
        plt.show()

    if mse_kf:
        mse_list = list()
        k_list = [i for i in range(2, 21)]
        for k in k_list:
            mse, _, _ = k_fold_val(k)
            mse_list.append(mse)
            print(mse)
            print(k)
        fig, ax = plt.subplots()
        ax.plot(k_list, mse_list, color='black', linewidth=3.5)
        plt.title('Cross-Validated MSE Per K-Value', fontsize=14)
        plt.xlabel('K-Folds')
        plt.ylabel('Mean Square Error')
        plt.gcf().set_size_inches(10, 5)
        plt.xticks([i for i in range(2, 21)])
        ax.hlines(y=17.5, xmin=2, xmax=20, color='r')
        plt.legend(['MSE', 'Baseline MSE'], loc='upper right')
        plt.show()

    if kf_dist:
        _, mse_dist = k_fold_val(20)
        plt.hist(mse_dist, bins=25, color='orange', edgecolor='black')
        plt.title('Distribution of MSE K=20', fontsize=14)
        plt.xlabel('Mean Square Error')
        plt.ylabel('Quantity in MSE Bucket')
        plt.gcf().set_size_inches(10, 5)
        plt.xticks([i for i in range(0, 2750, 250)])
        plt.show()


# k-fold cross validation of model! Returns the average MSE and distribution of MSE as well.
# CUSTOM MADE K_FOLD_CROSS_VAL METHOD LETS GOOOOOOOOO
# splits data into K folds, uses K-1 to train, then 1 to test
# default k=5, or an 80/20 split
def k_fold_val(k=5):
    prices = preprocess_sequential_data()
    Y = prices['Stocks']
    X = prices[['Oil', 'Gold', 'Lithium']]

    gs = round(len(Y) / k) - 1  # group size

    mse_list = list()
    mm_list = list()
    for i in range(k):
        X_train = X.iloc[(i+1) * gs:].append(X.iloc[0:i * gs])
        X_test = X.iloc[i * gs:(i+1) * gs]
        Y_train = Y.iloc[(i+1) * gs:].append(Y.iloc[0:i * gs])
        Y_test = Y.iloc[i * gs:(i+1) * gs]
        X_train = sm.add_constant(X_train)
        model = sm.OLS(Y_train, X_train)
        results = model.fit()
        X_test = sm.add_constant(X_test)
        predictions = results.predict(X_test)
        mse = MSE(predictions, Y_test)
        mse_list.append(mse)
        mm = movement_metric(predictions.reset_index(), Y_test.reset_index(), len(Y_test))
        mm_list.append(mm)
    avg_mse = np.average(mse_list)
    avg_mm = np.average(mm_list)
    return avg_mse, mse_list, avg_mm


if __name__ == "__main__":
    # all_vars_regression(0.33, to_print=True)
    # all_sequential_regression()
    plot_model_data(mm_kf=True)
    # k_fold_val()
