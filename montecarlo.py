import numpy as np
from numpy.random import randn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def monte_carlo_simulation(model, X, y, games, simulations=1000):
    over_count = 0
    under_count = 0
    exact_count = 0
    mse = mean_squared_error(y, model.predict(X))
    std_dev = np.std(y)
    predictions = []

    for _ in range(simulations):
        noise = randn() * std_dev
        prediction = model.predict([[games + 1]])[0][0] + noise
        prediction = round(prediction)
        predictions.append(prediction)
        if prediction > games:
            over_count += 1
        elif prediction < games:
            under_count += 1
        else:
            exact_count += 1

    over_percentage = over_count / simulations
    under_percentage = under_count / simulations
    exact_percentage = exact_count / simulations

    return over_percentage, under_percentage, exact_percentage, predictions
