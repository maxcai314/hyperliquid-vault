import pandas as pd
from dataclasses import dataclass

@dataclass
class Entry:
    time: pd.Timestamp
    price: float
    market_cap: float
    total_volume: float

    def __repr__(self):
        return f'{self.time} - {self.price} - {self.market_cap} - {self.total_volume}'

@dataclass
class DataSeries:
    time: pd.DataFrame
    price: pd.DataFrame
    market_cap: pd.DataFrame
    total_volume: pd.DataFrame

    @staticmethod
    def from_csv(file_path: str):
        df = pd.read_csv(file_path)
        df['snapped_at'] = pd.to_datetime(df['snapped_at'])

        return DataSeries(
            time=df['snapped_at'],
            price=df['price'],
            market_cap=df['market_cap'],
            total_volume=df['total_volume']
        )

    def __len__(self):
        return len(self.time)

    def __getitem__(self, key):
        if isinstance(key, slice):
            time = self.time[key].reset_index(drop=True)
            price = self.price[key].reset_index(drop=True)
            market_cap = self.market_cap[key].reset_index(drop=True)
            total_volume = self.total_volume[key].reset_index(drop=True)

            return DataSeries(
                time=time,
                price=price,
                market_cap=market_cap,
                total_volume=total_volume
            )
        elif isinstance(key, int):
            index = key % len(self)
            return Entry(
                time=self.time[index],
                price=self.price[index],
                market_cap=self.market_cap[index],
                total_volume=self.total_volume[index]
            )

    def __repr__(self):
        return pd.DataFrame({
            'time': self.time,
            'price': self.price,
            'market_cap': self.market_cap,
            'total_volume': self.total_volume
        }).__repr__()


if __name__ == '__main__':
    data = DataSeries.from_csv('resources/eth-usd-max.csv')
    print(data)

    print('first value:')
    print(data[0])

    print('last value:')
    print(data[-1])

    print('first values:')
    print(data[5:10])
