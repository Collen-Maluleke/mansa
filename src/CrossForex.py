import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Forex price data into a pandas DataFrame
df = pd.read_csv('forex_prices.csv')

# Compute the short- and long-term moving averages
short_window = 20
long_window = 50
df['short_ma'] = df['Close'].rolling(window=short_window).mean()
df['long_ma'] = df['Close'].rolling(window=long_window).mean()

# Create a signal to buy (1) or sell (-1) based on the crossover
df['signal'] = np.where(df['short_ma'] > df['long_ma'], 1, -1)

# Set initial capital
initial_capital = 10000

# Buy or sell the currency pair based on the signal
units = 0
capital = initial_capital
for i in range(len(df)):
    if df['signal'][i] == 1:
        units += capital / df['Close'][i]
        capital = 0
    elif df['signal'][i] == -1 and units > 0:
        capital = units * df['Close'][i]
        units = 0

# Plot the Forex prices and moving averages
plt.plot(df['Close'], label='Close')
plt.plot(df['short_ma'], label='Short MA')
plt.plot(df['long_ma'], label='Long MA')
plt.legend()
plt.show()

# Print the final capital
print('Final capital:', capital + units * df['Close'][-1])
