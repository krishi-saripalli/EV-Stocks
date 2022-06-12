# Tech Report
This is where you can type out your tech report.

### Where is the data from?
* *Oil Prices*: This data is from the [US Energy Information Administration](https://www.eia.gov/dnav/pet/pet_pri_spt_s1_d.htm). 
We scraped data from both the WTI and Brent spot indexes.
* *Lithium Prices*: This data is from [investing.com](https://www.investing.com/commodities/lithium-carbonate-99-min-china-futures-historical-data)
* *Gold Prices*: This data is from [World Gold Council](https://www.gold.org/goldhub/data/gold-prices)
* *Historical Stock Prices*: This data is from [IEX Cloud API](https://iexcloud.io/docs/api/)


### How did you collect your data?
* *Oil Prices*: Data was collected from a handy but lengthy excel sheet that can be downloaded from the US Energy Information
Agency's website. This data was read with pandas and scraped into a dataframe, which was then directly input to a database.
* *Lithium Prices*: Data was collected from a CSV file that was download from investing.com. This data was scraped with a csv reader in python and then directly input to a database.
* *Gold Prices*: Data was collected from a spreadsheet (XLS file) containing daily records of gold prices, which was then coverted and cleaned in a dataframe and placed in the gold.db file
* *Historical Stock Prices EV Market*: Data was collected from the IEX cloud API method for historical stock pricing, using the pyEx python library. This data was then entered into an SQLite database.


### Is the source reputable?
* *Oil Prices*: I believe that the US Energy Information Administration, being a government agency responsible for analyzing
impartial energy information for policymaking, is a reputable source for this data.
* *Lithium Prices*: I believe that investing.com is a reputable source because this site is widely known as being the go-to source for stock and company info, and in addition, this website was used in the previous homework assignment.
* *Gold Prices* Yes, the World Gold Council is the premier source of information and statistics concerning the economics and trade of gold.
* *Historical Stock Prices EV Market*: Yes, this API is one of the leading financial markets data sources!


### How did you generate the sample? Is it comparably small or large? Is it representative or is it likely to exhibit some kind of sampling bias?
Our sample consists of daily price data from March 22, 2020 to February 28th, 2022 for all datasets: oil prices, precious
metals (including lithium), and stock prices/data. This sample was the largest for which we could collect daily data
for all of our metrics, so we selected this. Further, our sample begins **after** the COVID stock market crash, so our analysis
of EV stock prices will not be affected by a sudden substantial drop in stock prices that has nothing to do with precious metals or oil. 
Overall, our sample data consists of many data points, so it's large in that regard, however it may be small in terms of the time
frame over which we'll be analyzing: a little less than two years. This could show some sampling bias, since we aren't
analyzing the entire trend of electric vehicles. However, the last two years have seen unprecedented levels of interest
in electric vehicles, so this would be the best time to analyze what affects their stock price now that people have begun
to pay more attention to them.

### Are there any other considerations you took into account when collecting your data? This is open-ended based on your data; feel free to leave this blank. (Example: If it's user data, is it public/are they consenting to have their data used? Is the data potentially skewed in any direction?)


### How clean is the data? Does this data contain what you need in order to complete the project you proposed to do? (Each team will have to go about answering this question differently, but use the following questions as a guide. Graphs and tables are highly encouraged if they allow you to answer these questions more succinctly.)
* *Oil Prices*: This data was mostly clean. There were a few entries (< 3) where a negative spot price was recorded, which is
impossible, so they were removed from the dataset. 
our data.
* *Lithium Prices*: This data was mostly clean. The only cleaning that needed to be done was that the volume column had no data in it, and the prices needed to be converted from CNY to USD. In addition, commas needed to be deleted from the prices, and % needed to be deleted from the change percentages.
* *Gold Prices*: The data is fully cleaned after removing commas from prices and changing value types. Later we may need to join table on dates, in which case dates that are not found in common will be excluded in the join table.
* *Historical EV Stock Data*: The data was very clean when received from the API call. The only adjustments made were the removal of incomplete rows of data, we did not want partially filled information.


### How many data points are there total? How many are there in each group you care about (e.g. if you are dividing your data into positive/negative examples, are they split evenly)? Do you think this is enough data to perform your analysis later on?
* *Oil Prices*: there are 478 rows in this dataset, with each row corresponding to a date and containing both the WTI
and Brent spot price indexes.
* *Lithium Prices*: there are 462 rows in this dataset, with each row corresponding to a date and containing the high price, open price, low price, and percentage change in price.
* *Gold Prices*: There are 503 rows with a column for the date of the recorded prices and another column for the price in US Dollars per Ounce.
* *Historical EV Stock Data*: There are 19903 rows, accounting for five years of daily entries for 20 EV companies.     For this portion of the data, there are only seven attributes (date, closing price, trading volume, total change, changePercent, changeOverTime, and trading symbol)



### Are there missing values? Do these occur in fields that are important for your project's goals?
* *Oil Prices*: A fair amount of dates were missing in this dataset, so there are some days where there is no oil spot price data. 
Still, the general trend is retained. These missing prices may affect our project's goals, since there is
less data to work with. If we try to do a daily analysis of correlation, we won't be able to for some days. 
* *Lithium Prices*: A few dates here and there are missing, for example, March 2 doesn't have any data. This shouldn't be significant however, since it is only a few dates.
* *Gold Prices*: There are missing values, presumably for days where commodities exchanges were not open and thus, no price data was available.
* *Historical EV Stock Data*: there were missing fields initially, however, the removal of rows with missing fields was a portion of the data cleaning conducted. As a result, we do not have missing fields in this table.


### Are there duplicates? Do these occur in fields that are important for your project's goals?
Since all of our data, stock or spot commodity prices, are sequential, there aren't any duplicates. 

### How is the data distributed? Is it uniform or skewed? Are there outliers? What are the min/max values? (focus on the fields that are most relevant to your project goals)
* *Oil Prices:* These prices seem to be generally uniformly distributed (specifically moreso a log-normal distribution; more details in data spec). There aren't any outliers. For oil prices, we have a minimum ~$23 and maximum ~$100 USD.
* *Lithium Prices*: The prices are generally increasing, and the minimum price is about 6000 USD/metric ton and the max price goes up to about 68000/metric ton.
* *Gold Prices*: Prices tend to steadily increase over time with some changes.
* *Historical EV Stock Data*: More specifics regarding the distribution, minimum, and maximum of the historical data table are outlined in the historical table specs. However, this data's distribution is not critical 
to our conclusion. We are not looking at this data's aggregate appearance, we are interested in it's change over time and response to global trends.


### Are there any data type issues (e.g. words in fields that were supposed to be numeric)? Where are these coming from? (E.g. a bug in your scraper? User input?) How will you fix them?
* *Oil Prices*: I thought that the date field, as recorded in Excel, would be a large issue. However, when importing into a Pandas dataframe, it was automatically recognized
as a date and reformatted without any further interference. The other issues was when importing data from excel, float numbers were recognized as strings. This was solved by a quick df.astype(float) command to convert the strings to their appropriate floats.
* *Lithium Prices*: There aren't any data type issues like this in the lithium prices data. Numbers appear as numbers and text appears as text in our database.
* *Gold Prices*: There are no data type issues.
* *Historical EV Stock Data*: There are not! This data came from an API that is very professional and reliable. 


### Do you need to throw any data away? What data? Why? Any reason this might affect the analyses you are able to run or the conclusions you are able to draw?
* *Oil Prices*: For some dates, there were also missing values for either the WTI or Brent spot price index, but not both,
so these entries were removed from the dataset too. This is because we may end up neeting both spot prices indices. However,
if we decide to use one or the other independently, we can change this removal easily by removing a line of code.
* *Lithium Prices*: We don't need to throw any data away for the lithium data.
* *Gold Prices*: As of now, no data was thrown, however, once tables are joined for analysis, some data may need to be removed.
* *Historical EV Stock Data*: A minimal amount of data was thrown when rows were seen to be incomplete or lacking data. This was limited to four lines.  


### Summarize any challenges or observations you have made since collecting your data. Then, discuss your next steps and how your data collection has impacted the type of analysis you will perform. (approximately 3-5 sentences)
* *Oil Prices*: A challenge I had with this is how to filter out the date's we aren't using. The original dataset of oil prices went daily all the way from the late 1900's so there was a *lot* of information (thousands of data points); I had to somehow limit it to only March 2020 and beyond, removing a large portion of the data. Ultimately, I decided the easiest way wasn't to remove this by code, but to manually select the irrelevant time periods and remove them from the excel sheet altogether. Since this is a pre-processing step, it won't affect our analysis at all!
* *Lithium Prices:* One challenge I had when collecting this data was that prices were in CNY but we needed to convert to USD. However, exchange rates are always changing from day to day, so I found the average exchange rate in the last 2 years and used that to convert each of the CNY prices to USD prices. Next steps will include using the data in our database to perform statistical tests for analysis.
* *Gold Prices*: The only notable challenges came from sourcing data. Initially, we intended on sourcing metal price data from API's where it would have been mostly cleaned for us. However, we immediatley realized that when trying to source enough data, our API call limit on a free account was reached. From there, we decided that searching for recorded spreadsheet data was the better option. Because of this, we had to drop some metals from our analysis because of a lack of available (or affordable) data.
* *Historical EV Stock Data*: Data sourcing was a challenge. There are limits on the number of free API calls that restricted the scope and breadth of our financial analysis.  
