import pandas as pd
from dataclasses import dataclass

@dataclass
class Entry:
    time: pd.Timestamp
    high: float
    low: float
    open: float
    close: float
    volume: float

    def __repr__(self):
        return f'{self.time}: {self.close}'

    @property
    def price(self):
        return self.close

@dataclass
class DataSeries:
    time: pd.Series
    high: pd.Series
    low: pd.Series
    open: pd.Series
    close: pd.Series
    volume: pd.Series

    @property
    def price(self):
        return self.close

    @staticmethod
    def empty():
        return DataSeries(
            time=pd.Series(dtype='datetime64[ns]'),
            high=pd.Series(dtype='float'),
            low=pd.Series(dtype='float'),
            open=pd.Series(dtype='float'),
            close=pd.Series(dtype='float'),
            volume=pd.Series(dtype='float')
        )

    @staticmethod
    def from_df(df: pd.DataFrame):
        return DataSeries(
            time=df['time'],
            high=df['high'],
            low=df['low'],
            open=df['open'],
            close=df['close'],
            volume=df['volume']
        )

    def to_df(self):
        return pd.DataFrame({
            'time': self.time,
            'high': self.high,
            'low': self.low,
            'open': self.open,
            'close': self.close,
            'volume': self.volume
        })

    @staticmethod
    def from_csv(file_path: str):
        df = pd.read_csv(file_path)
        df['time'] = pd.to_datetime(df['time'])

        return DataSeries.from_df(df)

    def to_csv(self, file_path: str):
        self.to_df().to_csv(file_path, index=False)

    def concat(self, new_data):
        return DataSeries.from_df(pd.concat([self.to_df(), new_data.to_df()], ignore_index=True))

    def __len__(self):
        return len(self.time)

    def __getitem__(self, key):
        if isinstance(key, slice):
            # wrap negative numbers using modulo
            start = key.start % len(self) if key.start is not None else None
            stop = key.stop % len(self) if key.stop is not None else None
            key = slice(start, stop, key.step)

            return DataSeries(
                time=self.time[key].reset_index(drop=True),
                high=self.high[key].reset_index(drop=True),
                low=self.low[key].reset_index(drop=True),
                open=self.open[key].reset_index(drop=True),
                close=self.close[key].reset_index(drop=True),
                volume=self.volume[key].reset_index(drop=True)
            )
        elif isinstance(key, int):
            index = key % len(self)
            return Entry(
                time=self.time[index],
                high=self.high[index],
                low=self.low[index],
                open=self.open[index],
                close=self.close[index],
                volume=self.volume[index]
            )

    def __iter__(self):
        return iter([Entry(
            time=self.time[i],
            high=self.high[i],
            low=self.low[i],
            open=self.open[i],
            close=self.close[i],
            volume=self.volume[i]
        ) for i in range(len(self))])

    def __repr__(self):
        return self.to_df().__repr__()


if __name__ == '__main__':
    data = DataSeries.from_csv('resources/eth-usd-hourly.csv')
    print(data)

    print('first value:')
    print(data[0])

    print('last value:')
    print(data[-1])

    print('first values:')
    print(data[5:10])
