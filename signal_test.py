from data import *
from signal import *

data = DataSeries.from_csv('resources/eth-usd-max.csv')


def test_accuracy(predictor) -> float:
    num_correct = 0
    num_true = 0

    for i in range(7, len(data)-1):
        history = data[i-7:i+1]
        today = history[-1].price
        tomorrow = data[i+1].price

        actual_result = tomorrow > today
        prediction = predictor.predict_price(history)
        if prediction:
            num_true += 1

        if actual_result == prediction:
            num_correct += 1

    print(f'Predicted Bullish: {num_true / (len(data) - 8)}')
    return num_correct / (len(data) - 8)


print(f'Always Bullish: {test_accuracy(ALWAYS_BULLISH)}')
print(f'Always Bearish: {test_accuracy(ALWAYS_BEARISH)}')
print()
print(f'Yesterday\'s News: {test_accuracy(YESTERDAYS_NEWS)}')
print(f'Three Days Ago: {test_accuracy(PointSignal(time_step=3))}')
print()
print(f'Linear Trend (7): {test_accuracy(LinearSignal(days_to_consider=7))}')
print(f'Quadratic Trend (7): {test_accuracy(QuadraticSignal(days_to_consider=7))}')
print()
print(f'Linear Trend (4): {test_accuracy(LinearSignal(days_to_consider=4))}')
print(f'Quadratic Trend (4): {test_accuracy(QuadraticSignal(days_to_consider=4))}')
