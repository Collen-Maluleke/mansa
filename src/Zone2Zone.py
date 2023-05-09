import pandas as pd
import numpy as np
import talib

# Constants for strategy parameters
PAIRS = ['EURUSD', 'USDJPY', 'AUDUSD', 'US100', 'US30', 'XAUUSD']
SESSIONS = ['London', 'New York']
CAPITAL = 1.0 # total capital, assuming 1.0 as an example
RISK = 0.03 # maximum risk per trade, 3%

# Define the trading logic
def trade_signal(data, pair, session):
    # Check if the current session is within the allowed sessions
    if session not in SESSIONS:
        return 0
    
    # Calculate support and resistance levels using Bollinger Bands
    upper, middle, lower = talib.BBANDS(data['close'], timeperiod=20, nbdevup=2, nbdevdn=2)
    
    # Check for breakouts from significant price levels
    if data['close'][-1] > upper[-1]:
        signal = 1 # buy signal
    elif data['close'][-1] < lower[-1]:
        signal = -1 # sell signal
    else:
        return 0 # no trade signal
    
    # Confirm the breakout by checking for a retest and rejection of the broken level
    retest = False
    for i in range(-2, -6, -1):
        if (signal == 1 and data['close'][i] < upper[i]) or (signal == -1 and data['close'][i] > lower[i]):
            retest = True
            break
    
    # Trade execution only if there is rejection from the broken level
    if retest:
        return 0
    else:
        return signal

# Define the strategy
def zone_to_zone_strategy(data, pair, session):
    # Get the trade signal
    signal = trade_signal(data, pair, session)
    
    # Calculate the position size
    position_size = int(CAPITAL * RISK / data['close'][-1])
    
    # Return the position size for the trade signal
    return signal * position_size

# Backtest the strategy on historical data
def backtest(data, pair, session):
    # Calculate the strategy for each bar
    data['strategy'] = np.vectorize(zone_to_zone_strategy)(data, pair, session)
    
    # Calculate the cumulative return
    data['return'] = data['close'].pct_change() * data['strategy'].shift(1)
    data['cumulative_return'] = (1 + data['return']).cumprod() - 1
    
    # Plot the cumulative return
    data[['close', 'cumulative_return']].plot()

# Load the historical data for each pair and session
for pair in PAIRS:
    for session in SESSIONS:
        data = pd.read_csv(f"{pair}_{session}.csv")
        backtest(data, pair, session)
