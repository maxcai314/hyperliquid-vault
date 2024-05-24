from data import *
from signal import *

data = DataSeries.from_csv('resources/eth-usd-max.csv')


def test_accuracy(predictor) -> float:
    num_correct = 0

    for i in range(7, len(data)-1):
        history = data[i-7:i]
        today = data[i].price
        tomorrow = data[i+1].price

        actual_result = tomorrow > today
        prediction = predictor.predict_price(history)

        if actual_result == prediction:
            num_correct += 1

    return num_correct / (len(data) - 8)


print(f'Always Bullish: {test_accuracy(ALWAYS_BULLISH)}')
print(f'Always Bearish: {test_accuracy(ALWAYS_BEARISH)}')