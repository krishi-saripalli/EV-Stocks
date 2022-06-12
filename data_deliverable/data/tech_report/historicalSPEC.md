# Data Spec: Historical Stock Data
This is where you will be describing your data spec comprehensively. Please refer to the handout for a couple of examples of good data specs.

You will also need to provide a sample of your data in this directory. Please delete the example `sample.db` and replace it with your own data sample. ***Your sample does not necessarily have to be in the `.db` format; feel free to use `.json`, `.csv`, or any other data format that you are most comfortable with***.

Data Types:
    
The historical data encompasses the historical stock pricing for twenty publicly traded companies that are active and relevant to the electric 
vehicles' industry. 

This is a table of various data types, varying from dates, float numbers, and texts. None of the values here have default values, as this would create issues for 
calculations using this data. Any missing data entries resulted in the exclusion of the entirety of that date's information.
    
    For this portion of the data, there are only seven attributes (date, closing price, trading volume, total change, changePercent, changeOverTime, and trading symbol)

Date: All values here are unique dates (for each stock symbol) in the YYYY-MM-DD format. There is no default value, and the dates range from 
2018-03-02 until 2022-03-01. This is a uniform distribution of dates that alongside the stock symbol attribute can be used as an identifier.
The date will not be used in analysis aside from any expected uses, ex: showing a change over time.
This feature does not include any potentially sensitive data. 

Closing Price: All values here can be seen to be unique closing prices, and are floating numbers that represent USD currency. There is no default value, all values are greater than zero. This attribute is not a unique identifier and should not be used as one.
These prices will be one of the central components of our analysis as we are looking into the correlation of evaluation and other commodities statuses., ex: showing a change over time.
This feature does not include any potentially sensitive data. 

Percent Change: All values are very precise float determinations of the change in percent value of a firms value with respect to the previous value. There is no default value, and the values range from a max change percent of 0.7391 to a minimum of -0.431. This attribute is not a unique identifier and should not be used as one.
These changes will be one of the central components of our analysis as we are looking into the correlation of evaluation and other commodities statuses., ex: showing a change over time.
This feature does not include any potentially sensitive data. 
