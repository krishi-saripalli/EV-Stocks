import numpy as np
import pandas as pd
from sqlite3 import connect

import scipy.stats as stats
import statsmodels.graphics.gofplots
import matplotlib.pyplot as plt


def f(row):
    tech = ["GOOGL", "APPL", "QCOM", "NVDA", "BIDU", "NXPI", 'YNDX']
    auto = ["XPEV", "BE", "RIVN", "TSLA", "NIO", "GM", 'F', "HOG", "AMBA", "LCID", "VNE", "PLUG"]
    if row["symbol"] in tech:
        val = "TECH"
    elif row["symbol"] in auto:
        val = "AUTO"
    else:
        val = "ELSE"
    return val

conn = connect('data.db')

df = pd.read_sql_query("SELECT * FROM HISTORICAL", conn)

#classify the companies
df['Type'] = df.apply(f, axis=1)

result = df["Type"].unique()

print("hey")



# dfTECH = pd.read_sql_query("SELECT * from historical WHERE symbol is \"AAPL\" OR symbol is \"GOOGL\" OR symbol is \"QCOM\" OR symbol is \"NVDA\" OR symbol is \"BIDU\" OR symbol is \"NXPI\" OR symbol is \"YNDX\"", conn)
# dfAUTO = pd.read_sql_query("SELECT * from historical WHERE symbol is \"XPEV\" OR symbol is \"BE\" OR symbol is \"RIVN\" OR symbol is \"TSLA\" OR symbol is \"NIO\" OR symbol is \"GM\" OR symbol is \"F\" OR symbol is \"HOG\" OR symbol is \"AMBA\" OR symbol is \"LCID\" OR symbol is \"VNE\" OR symbol is \"PLUG\"", conn)

#check assumptions- normality and homogeneity of variance
stats.probplot(df[df['Type'] == "TECH"]['close'], dist="norm", plot = plt)
plt.title("Probability Plot - TECH")
plt.show()

stats.probplot(df[df['Type'] == "AUTO"]['close'], dist="norm", plot = plt)
plt.title("Probability Plot - AUTO")
plt.show()

#failed normality test, must do a log transformation
autoTransformed = np.log(df[df['Type'] == "AUTO"]['close'])
techTransformed = np.log(df[df['Type'] == "TECH"]['close'])

stats.probplot(autoTransformed, dist="norm", plot = plt)
plt.title("Probability Plot Transformed- AUTO")
plt.show()

stats.probplot(techTransformed, dist="norm", plot = plt)
plt.title("Probability Plot Transformed - TECH")
plt.show()

# #homogenous variances are required; Barlett's test?
stat, p = stats.bartlett(autoTransformed, techTransformed)
print(p)

# #don't interpret above, perform homogeneity of variance assumption check
# ratio = df.groupby('Type').std().max() /df.groupby('Type').std().min()
# print(ratio)
# #ratio for close is 13,4, too big (threshold is 2)

F, p = stats.f_oneway(autoTransformed, techTransformed)
print("wait")