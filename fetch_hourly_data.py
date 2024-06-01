from data import DataSeries
import cryptocompare
import pandas as pd
from datetime import datetime

endTime = datetime(year=2024, month=6, day=1)

# needs env var CRYPTOCOMPARE_API_KEY
result = cryptocompare.get_historical_price_hour('ETH', currency='USD', limit=2000, toTs=endTime)

df = pd.DataFrame.from_records(result)
df['time'] = pd.to_datetime(df['time'], unit='s')
df['volume'] = df['volumefrom'].multiply(df['close']).add(df['volumeto'])

data = DataSeries.from_df(df)
print(data)

data.to_csv('resources/eth-usd-hourly.csv')

data = DataSeries.from_csv('resources/eth-usd-hourly.csv')
print(data)
