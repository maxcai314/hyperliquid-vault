from data import Entry, DataSeries
from dataclasses import dataclass

@dataclass
class ConstantSignal:
    result: bool

    def predict_price(self, price_history: DataSeries) -> bool:
        """
        Predicts whether tomorrow's price will be higher than today's, given one week of historical data.
        :param price_history: the historical price data over one week (collected daily)
        :return: whether tomorrow's price will be higher than today's
        """
        return self.result


ALWAYS_BULLISH = ConstantSignal(result=True)
ALWAYS_BEARISH = ConstantSignal(result=False)
