from data import Entry, DataSeries
from dataclasses import dataclass
from scipy import stats, odr

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

@dataclass
class PointSignal:
    time_step: int

    def predict_price(self, price_history: DataSeries) -> bool:
        """
        Predicts by comparing the price time_step days ago to the current price.
        """
        return price_history[-1].price > price_history[-1 - self.time_step].price


YESTERDAYS_NEWS = PointSignal(time_step=1)

@dataclass
class LinearSignal:
    days_to_consider: int

    def predict_price(self, price_history: DataSeries) -> bool:
        """
        Predicts by fitting a linear regression to the price data and extrapolating the next day's price.
        """
        x = range(-1 - self.days_to_consider, 0)
        y = [price_history[i].price for i in x]

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        return slope > 0 and r_value > 0.4

@dataclass
class QuadraticSignal:
    days_to_consider: int

    def predict_price(self, price_history: DataSeries) -> bool:
        """
        Predicts by fitting a quadratic regression to the price data and extrapolating the next day's price.
        """
        x = range(-1 - self.days_to_consider, 0)
        y = [price_history[i].price for i in x]

        data = odr.Data(x, y)
        odr_obj = odr.ODR(data, odr.quadratic)
        output = odr_obj.run()
        coeffs = output.beta
        next_price = coeffs[2]

        return next_price > price_history[-1].price
