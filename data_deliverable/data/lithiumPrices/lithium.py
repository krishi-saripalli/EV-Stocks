import sqlite3
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv
import datetime

conn = sqlite3.connect('../project_data.db')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS "lithium";')

c.execute("""CREATE TABLE lithium (
	date TIMESTAMP PRIMARY KEY NOT NULL,
	price REAL NOT NULL,
	open REAL NOT NULL,
	high REAL NOT NULL,
	low REAL NOT NULL,
	change_pct REAL NOT NULL
)""")

conn.commit()

# use avg rate of 0.15 USD = 1 CNY
# csv file name
filename = "Lithium_Data.csv"

# initializing the titles and rows list
fields = []
rows = []

# reading csv file
# https://stackoverflow.com/questions/41585078/how-do-i-read-and-write-csv-files-with-python
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        row.pop(5)
        row[1] = float(row[1].replace(',', ''))
        row[2] = float(row[2].replace(',', ''))
        row[3] = float(row[3].replace(',', ''))
        row[4] = float(row[4].replace(',', ''))
        row[5] = float(row[5].replace('%', ''))

        row[1] = row[1] / (20/3)
        row[2] = row[2] / (20/3)
        row[3] = row[3] / (20/3)
        row[4] = row[4] / (20/3)
        row[0] = datetime.datetime.strptime(row[0], "%b %d, %Y").strftime("%Y-%m-%d")

        rows.append(row)


for eachRow in rows:
    c.execute('INSERT INTO lithium VALUES (?,?,?,?,?,?)', (eachRow[0], eachRow[1],
                                                           eachRow[2],eachRow[3],eachRow[4],eachRow[5]))

conn.commit()

# TODO: LITHIUM PRICE DATA IS NOW IN FORMAT: USD/METRIC TON. Convert to USD/ounce to match gold?
# optional; we can discuss later
