# Data Deliverable
This is the data deliverable's master directory! Please use the following shortcut links to access the different components of this deliverable.

### Reports
- [Tech Report](data/tech_report/README.md)

### Link to Data
You can download our initial data from the links provided in our tech report! You can also download our database from
project_data.db in this repository or from ***INSERT LINK HERE***

### Easily Viewable Data

### Data Spec for Oil Prices
* ***Oil Price Attributes***:
  * *Date*
    * Type of data: SQL TIMESTAMP data type
    * Default value: No default value
    * Range of value: March 23, 2020, to February 28, 2022
    * Distribution: Sequential? It's just a bunch of dates
    * Is this an identifier?: Yes! The date will be used to match oil prices with corresponding prices in EVs and precious metals
    * Are the values unique?: Yes, each date is unique
    * Are we using this to detect duplicates?: Yes, we are (just by comparing if a date already exists). However, we've found in the oil dataset, there aren't duplicates.
    * Is this required?: Yes, it is
    * Are we using this in analysis?: Not directly, but the date will be used to match up an oil prices and EV and metal prices on each day
    * Contains sensitive information?: Nope!
  * *WTI Spot Price*
    * Type of data: SQL REAL data type
    * Default value: No default value
    * Range of value: 72.8 (Max = 96.13, Min = 23.33)
    * Distribution: Typically, stock/commodity prices are log-normal distributed (that is, it's much harder for a stock to increase from 0 than from larger values). Here, from viewing the distribution of oil prices x in each bucket (x<20<x<30<x<40... etc), it seems to be somewhere between normal and log-normally distributed. The values are skewed to favor lower prices, yet there are still some significant amounts at higher prices too.
    * Is this an identifier?: No, it isn't
    * Are the values unique?: The values aren't unique; the spot price of oil on a certain day may be anything, including duplicates of previous prices
    * Are we using this to detect duplicates?: Nope!
    * Is this required?: Yes, it is
    * Are we using this in analysis?: Yes! We'll be comparing the trends in oil prices and EV stock prices to see if there's any correlation between a rise/fall in oil prices and rise/fall in EV stock prices
    * Contains sensitive information?: Nope!
  * *Brent Spot Price*
    * Type of data: SQL REAL data type
    * Default value: No default value
    * Range of value: 79.33 (Max = 103.08, Min = 23.75)
    * Distribution: Typically, stock/commodity prices are log-normal distributed (that is, it's much harder for a stock to increase from 0 than from larger values). Here, from viewing the distribution of oil prices x in each bucket (x<20<x<30<x<40... etc), it seems to be somewhere between and log-normally distributed. The values are skewed to favor lower prices, yet there are still some significant amounts at higher prices too.
    * Is this an identifier?: No, it isn't
    * Are the values unique?: The values aren't unique; the spot price of oil on a certain day may be anything, including duplicates of previous prices
    * Are we using this to detect duplicates?: Nope!
    * Is this required?: Yes, it is
    * Are we using this in analysis?: Yes! We'll be comparing the trends in oil prices and EV stock prices to see if there's any correlation between a rise/fall in oil prices and rise/fall in EV stock prices
      * This is the second spot price index we're using here. It may be beneficial to compare oil prices to two indexes, since they differ slightly in how they compare
      * If we find that there is a correlation between both indexes, it's likely to be true!
      * However, if we find a correlation between stock prices and only one oil spot index, it's less likely to be true!
    * Contains sensitive information?: Nope!
  
  
### Data Spec For Lithium
[Data spec](data/)
Collected the historical pricing data for Lithium Carbonate 99% in the currency CNY converted into USD. This data measures the price of lithium and how it changes from 3/22/2020 to 3/2/2022.

* ***Lithium Price Attributes***:
    * *Date*
        * Type of data: SQL DATE data type
        * Default value: No default value
        * Range of value: March 23, 2020, to March 2, 2022
        * Distribution: Sequential? It's just a bunch of dates in order from earliest to most recent
        * Is this an identifier?: Yes! The date will be used to match lithium prices with corresponding prices in EVs and precious metals like gold.
        * Are the values unique?: Yes, each date is unique
        * Are we using this to detect duplicates?: Yes, we are (just by comparing if a date already exists). However, we've found in the lithium dataset, there aren't duplicates.
        * Is this required?: Yes, it is, as you need a date for the data to be useful.
        * Are we using this in analysis?: Not directly, but the date will be used to match up lithium prices and EV and metal prices on each day
        * Contains sensitive information?: Nope!
    * *Price*
        * Type of data: float
        * Default value: No default value
        * Range of values: 63450 (Max = 69375, Min = 5925)
        * Distribution: The distribution here seems to indicate a strong increase in the price in the past several weeks, so this is similar to an exponentially increasing distribution.
        * Is this an identifier?: No, it isn't
        * Are the values unique?: The values aren't unique; the spot price of lithium on a certain day may be anything, including duplicates of previous prices
        * Are we using this to detect duplicates?: Nope!
        * Is this required?: Yes, it is
        * Are we using this in analysis?: Yes! We'll be comparing the trends in lithium prices and EV stock prices to see if there's any correlation between a rise/fall in lithium prices and rise/fall in EV stock prices
        * Contains sensitive information?: Nope!
    * *Open*
        * Type of data: float
        * Default value: No default value
        * Range of values: 63375 (Max = 69375, Min = 6000)
        * Distribution: The distribution here seems to indicate a strong increase in the opening price in the past several weeks, so this is similar to an exponentially increasing distribution.
        * Is this an identifier?: No, it isn't
        * Are the values unique?: The values aren't unique; the open price of lithium on a certain day may be anything, including duplicates of previous prices
        * Are we using this to detect duplicates?: Nope!
        * Is this required?: Yes, it is
        * Are we using this in analysis?: Not directly, since the actual price column will be more relevant. We'll be comparing the trends in lithium prices and EV stock prices to see if there's any correlation between a rise/fall in lithium prices and rise/fall in EV stock prices
        * Contains sensitive information?: Nope!
    * *Low*
      * Type of data: float
      * Default value: No default value
      * Range of values: 63600 (Max = 69000, Min = 5775)
      * Distribution: The distribution here seems to indicate a strong increase in the low price in the past several weeks, so this is similar to an exponentially increasing distribution. It follows very closely with the price attribute.
      * Is this an identifier?: No, it isn't
      * Are the values unique?: The values aren't unique; the low price of lithium on a certain day may be anything, including duplicates of previous prices
      * Are we using this to detect duplicates?: Nope!
      * Is this required?: Yes, it is
      * Are we using this in analysis?: Not directly, since the actual price column will be more relevant. We'll be comparing the trends in lithium prices and EV stock prices to see if there's any correlation between a rise/fall in lithium prices and rise/fall in EV stock prices
      * Contains sensitive information?: Nope!
    * *change_pct*
      * Type of data: float
      * Default value: No default value
      * Range of values: 6.07 (Max = 4.05, Min = -2.02)
      * Distribution: The distribution here is quite varied and certainly not as consistent as the price. Higher change percentages have aligned with the recent big increase in prices.
      * Is this an identifier?: No, it isn't
      * Are the values unique?: The values aren't unique; the change percentage price of lithium on a certain day may be anything, including duplicates of previous change percentages
      * Are we using this to detect duplicates?: Nope!
      * Is this required?: Yes, it is
      * Are we using this in analysis?: Not directly, since the actual price column will be more relevant. We'll be comparing the trends in lithium prices and EV stock prices to see if there's any correlation between a rise/fall in lithium prices and rise/fall in EV stock prices. This data could be useful for any rate or change analysis.
      * Contains sensitive information?: Nope!

### Data Spec for Stocks
[Stocks Data Spec](data/tech_report/historicalSPEC.md) 

### Data Spec For Lithium
[Gold Data Spec](/data/goldPrices/goldDataSpec)

