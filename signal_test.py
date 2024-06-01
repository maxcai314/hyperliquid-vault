from data import *
import numpy as np
import matplotlib.pyplot as plt

data = DataSeries.from_csv('resources/eth-usd-hourly.csv')[-365 * 24:]  # only use data from the past year

HISTORY_LENGTH = 24

def test_signal(predictor, name='Investment Strategy', plot_price=True, plot_normalized=False):
    num_correct = 0
    num_true = 0

    eth_prices = np.array([entry.price for entry in data])
    t = np.arange(len(data), dtype=int)
    portfolio = np.zeros_like(t, dtype=float)
    portfolio[0:HISTORY_LENGTH] = data[0:HISTORY_LENGTH].price  # first week doesn't count

    leverage = 1

    # leverage changes
    increase_leverage = [0]
    decrease_leverage = []

    for i in range(HISTORY_LENGTH, len(data) - 1):
        history = data[i - HISTORY_LENGTH:i + 1]
        prediction = predictor.predict_price(history)

        yesterday = eth_prices[i - 1]
        today = eth_prices[i]

        price_change = today - yesterday
        yesterday_portfolio = portfolio[i - 1]
        num_eth = yesterday_portfolio / yesterday
        portfolio[i] = yesterday_portfolio + (num_eth * price_change * leverage)

        tomorrow = eth_prices[i + 1]
        actual_result = tomorrow > today

        if prediction:
            if leverage != 1:
                increase_leverage.append(i)
            leverage = 1
        else:
            if leverage != 0.5:
                decrease_leverage.append(i)
            leverage = 0.5

        if prediction:
            num_true += 1

        if actual_result == prediction:
            num_correct += 1

    increase_leverage.append(len(data) - 1)
    decrease_leverage.append(len(data) - 1)

    if plot_price:
        plt.figure()
        plt.title(name)
        plt.xlabel('Hours Passed')
        plt.ylabel('Value ($)')
        plt.plot(t, eth_prices, label='Eth Price')
        plt.plot(t[HISTORY_LENGTH:len(data) - 1], portfolio[HISTORY_LENGTH:len(data) - 1], label='Portfolio Value')
        for start, end in zip(increase_leverage, decrease_leverage):
            plt.axvspan(start, end, color='g', alpha=0.2)
        for start, end in zip(decrease_leverage, increase_leverage[1:]):
            plt.axvspan(start, end, color='r', alpha=0.2)
        plt.legend(loc='upper left')
        plt.show()

    if plot_normalized:
        plt.figure()
        plt.title(name)
        plt.xlabel('Hours Passed')
        plt.ylabel('Value (ETH)')
        plt.plot(t, eth_prices / eth_prices, label='Eth Price')
        plt.plot(t[HISTORY_LENGTH:len(data) - 1], (portfolio / eth_prices)[HISTORY_LENGTH:len(data) - 1], label='Portfolio Value')
        for start, end in zip(increase_leverage, decrease_leverage):
            plt.axvspan(start, end, color='g', alpha=0.2)
        for start, end in zip(decrease_leverage, increase_leverage[1:]):
            plt.axvspan(start, end, color='r', alpha=0.2)
        plt.legend(loc='upper left')
        plt.show()

    print(name)
    print(f'Bullish ratio: {num_true / (len(data) - HISTORY_LENGTH - 1)}')
    print(f'Accuracy: {num_correct / (len(data) - HISTORY_LENGTH - 1)}')
    print()


if __name__ == '__main__':
    from signals import *

    test_signal(ALWAYS_BULLISH, name='Always Bullish')
    test_signal(ALWAYS_BEARISH, name='Always Bearish')

    test_signal(YESTERDAYS_NEWS, name='Last Hour\'s News')
    test_signal(PointSignal(time_step=2), name='Two Hours Ago')

    test_signal(LinearSignal(measurements_to_consider=7), name='Linear Trend (7)')
    test_signal(QuadraticSignal(measurements_to_consider=7), name='Quadratic Trend (7)')

    test_signal(LinearSignal(measurements_to_consider=4), name='Linear Trend (4)')
    test_signal(QuadraticSignal(measurements_to_consider=4), name='Quadratic Trend (4)')
