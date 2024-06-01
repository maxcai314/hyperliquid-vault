from data import DataSeries
import cryptocompare
import pandas as pd
from datetime import datetime

end_time = datetime(year=2024, month=6, day=1)

data = DataSeries.empty()

for i in range(10):
    # avoid timezones using timestamps
    result = cryptocompare.get_historical_price_hour('ETH', currency='USD', limit=2000, toTs=end_time)
    df = pd.DataFrame.from_records(result)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['volume'] = df['volumefrom'].multiply(df['close']).add(df['volumeto'])
    new_data = DataSeries.from_df(df)

    data = new_data.concat(data)
    end_time = datetime.fromtimestamp(data.time[0].timestamp())

destination = 'resources/eth-usd-hourly.csv'
data.to_csv(destination)

if __name__ == '__main__':
    loaded_data = DataSeries.from_csv(destination)  # attempt to load from file
    print(loaded_data)
