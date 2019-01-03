### Script to get daily exchange rates from the European Central Bank
### Stores file as fxrates_YYYYMMDD.csv
### 2019.01.03 MH 

from urllib.request import urlopen
from datetime import date
import xmltodict
import pandas as pd

file = urlopen('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
data = file.read()
file.close()

xml = xmltodict.parse(data)

### Get the date from the XML-file and store it as 'update'
xmldate = xml["gesmes:Envelope"]
root_elements = xmldate["Cube"]["Cube"] if type(xmldate["Cube"]["Cube"]) == list else [xmldate["Cube"]["Cube"]]
for element in root_elements:
    update = element['@time']

### Create columns for dataframe
cols = ['Currency','EUR_Rate']

### Create the empty list and then fill it with the currencies and rates (as float)
lst = []

### Add EUR manually
lst.append(['EUR', float(1)])

currencies = xml["gesmes:Envelope"]
root_elements = currencies["Cube"]["Cube"]["Cube"] if type(currencies["Cube"]["Cube"]["Cube"]) == list else [currencies["Cube"]["Cube"]["Cube"]]
for element in root_elements:
    lst.append([element['@currency'], float(element['@rate'])])

### create DF
df = pd.DataFrame(lst, columns=cols)

### Insert the date (called 'update') as the first value for all rows
df.insert(0, 'Date', update)

### find USD-rate
usdrate = df.loc[df['Currency'].isin(['USD'])]
usd = usdrate['EUR_Rate']

### Create the empty list and then fill it with the currencies and rates (as float)
lst_usd = []

### for each currency divide the EUR rate by USD rate and add as a column to original df
for i in range(len(df)):
    lst_usd.append(float(df['EUR_Rate'][i] / usd))
df.insert(3, 'USD_Rate', lst_usd)

### Save file as fxrates_yyyymmdd.csv
save_date = str(date.today().strftime('%Y%m%d'))
df.to_csv('fxrates_%s.csv' % save_date, sep=',', index=False)