import matplotlib.pyplot as plt

from data import *
from signal import *
import numpy as np
import matplotlib.pyplot as plt

data = DataSeries.from_csv('resources/eth-usd-max.csv')[1000:] # ignore first few years


def test_accuracy(predictor, name='Investment Strategy') -> float:
    num_correct = 0
    num_true = 0

    t = np.arange(len(data))
    portfolio = np.zeros_like(t, dtype=float)
    portfolio[0:7] = data[0].price  # first week doesn't count

    leverage = 1

    for idx in range(7, len(data)-1):
        i = int(t[idx])
        history = data[i-7:i+1]
        yesterday = history[-2].price
        today = history[-1].price
        prediction = predictor.predict_price(history)

        price_change = today - yesterday
        yesterday_portfolio = portfolio[idx - 1]
        num_eth = yesterday_portfolio / yesterday
        portfolio[idx] = yesterday_portfolio + (num_eth * price_change * leverage)

        tomorrow = data[i + 1].price
        actual_result = tomorrow > today

        if prediction:
            leverage = 1
        else:
            leverage = 0.5

        if prediction:
            num_true += 1

        if actual_result == prediction:
            num_correct += 1

    plt.figure()
    plt.title(name)
    plt.xlabel('Days Passed')
    plt.ylabel('Value ($)')
    plt.plot(t, np.array([entry.price for entry in data]), label='Eth Price')
    plt.plot(t[7:len(data)-1], portfolio[7:len(data)-1], label='Portfolio Value')
    plt.legend()
    plt.show()

    print(name)
    print(f'Bullish ratio: {num_true / (len(data) - 8)}')
    print(f'Accuracy: {num_correct / (len(data) - 8)}')
    print()

    return num_correct / (len(data) - 8)


test_accuracy(ALWAYS_BULLISH, name='Always Bullish')
test_accuracy(ALWAYS_BEARISH, name='Always Bearish')

test_accuracy(YESTERDAYS_NEWS, name='Yesterday\'s News')
test_accuracy(PointSignal(time_step=2), name='Two Days Ago')

test_accuracy(LinearSignal(days_to_consider=7), name='Linear Trend (7)')
test_accuracy(QuadraticSignal(days_to_consider=7), name='Quadratic Trend (7)')

test_accuracy(LinearSignal(days_to_consider=4), name='Linear Trend (4)')
test_accuracy(QuadraticSignal(days_to_consider=4), name='Quadratic Trend (4)')
