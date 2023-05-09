import ccxt
import talib
import numpy as np

exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
    'enableRateLimit': True,
})

# Define symbols to trade
symbols = ['EUR/USD', 'US30', 'US100']

# Define timeframes to trade
timeframes = ['4h', '1d']

since = exchange.parse8601('2022-01-01T00:00:00Z')
limit = None
params = {}

for symbol in symbols:
    for timeframe in timeframes:
        bars = exchange.fetch_ohlcv(symbol, timeframe, since, limit, params)
        ticks = exchange.fetch_ticker(symbol)

        # Map candlesticks to np array
        closes = np.asarray([x[4] for x in bars])

        # Define SMA indicators
        sma20 = talib.SMA(closes, timeperiod=20)
        sma50 = talib.SMA(closes, timeperiod=50)
        sma200 = talib.SMA(closes, timeperiod=200)

        # Define EMA indicators
        ema20 = talib.EMA(closes, timeperiod=20)
        ema50 = talib.EMA(closes, timeperiod=50)
        ema200 = talib.EMA(closes, timeperiod=200)

        # Identify trend direction
        if sma20[-1] > sma50[-1] > sma200[-1]:
            print(f"{symbol} ({timeframe}): Bullish trend")

        elif sma20[-1] < sma50[-1] < sma200[-1]:
            print(f"{symbol} ({timeframe}): Bearish trend")

        else:
            print(f"{symbol} ({timeframe}): Ranging trend")

        # Identify key levels based on trend
        if sma20[-1] > sma50[-1] > sma200[-1]:
            support_level = np.min(closes)
            print(f"{symbol} ({timeframe}): Strong support level: {support_level}")

        elif sma20[-1] < sma50[-1] < sma200[-1]:
            resistance_level = np.max(closes)
            print(f"{symbol} ({timeframe}): Strong resistance level: {resistance_level}")

        # Identify breakout after ranging period
        if sma20[-1] == sma50[-1] == sma200[-1]:
            print(f"{symbol} ({timeframe}): Waiting for breakout")

        # Enter trade based on trend and key levels
        if sma20[-1] > sma50[-1] > sma200[-1]:
            if ticks['last'] < support_level:
                print(f"{symbol} ({timeframe}): Enter long position")

        elif sma20[-1] < sma50[-1] < sma200[-1]:
            if ticks['last'] > resistance_level:
                print(f"{symbol} ({timeframe}): Enter short position")
# Define symbols to trade
symbols = ['EUR/USD', 'US30', 'US100']

# Define timeframes to trade
timeframes = ['4h', '1d']

since = exchange.parse8601('2022-01-01T00:00:00Z')
limit = None
params = {}

for symbol in symbols:
    for timeframe in timeframes:
        bars = exchange.fetch_ohlcv(symbol, timeframe, since, limit, params)
        ticks = exchange.fetch_ticker(symbol)

        # Map candlesticks to np array
        closes = np.asarray([x[4] for x in bars])

        # Define SMA indicators
        sma20 = talib.SMA(closes, timeperiod=20)
        sma50 = talib.SMA(closes, timeperiod=50)
        sma200 = talib.SMA(closes, timeperiod=200)

        # Define EMA indicators
        ema20 = talib.EMA(closes, timeperiod=20)
        ema50 = talib.EMA(closes, timeperiod=50)
        ema200 = talib.EMA(closes, timeperiod=200)

        # Identify trend direction
        if sma20[-1] > sma50[-1] > sma200[-1]:
            print(f"{symbol} ({timeframe}): Bullish trend")

        elif sma20[-1] < sma50[-1] < sma200[-1]:
            print(f"{symbol} ({timeframe}): Bearish trend")

        else:
            print(f"{symbol} ({timeframe}): Ranging trend")

        # Identify key levels based on trend
        if sma20[-1] > sma50[-1] > sma200[-1]:
            support_level = np.min(closes)
            print(f"{symbol} ({timeframe}): Strong support level: {support_level}")

        elif sma20[-1] < sma50[-1] < sma200[-1]:
            resistance_level = np.max(closes)
            print(f"{symbol} ({timeframe}): Strong resistance level: {resistance_level}")

        # Identify breakout after ranging period
        if sma20[-1] == sma50[-1] == sma200[-1]:
            print(f"{symbol} ({timeframe}): Waiting for breakout")

        # Enter trade based on trend and key levels
        if sma20[-1] > sma50[-1] > sma200[-1]:
            if ticks['last'] < support_level:
                print(f"{symbol} ({timeframe}): Enter long position")

        elif sma20[-1] < sma50[-1] < sma200[-1]:
            if ticks['last'] > resistance_level:
                print(f"{symbol} ({timeframe}): Enter short position")

# Part 3: Enter trades at specified times
for symbol in symbols:
    if symbol == 'EUR/USD':
        start_time = exchange.parse8601('2023-04-26T15:00:00Z')
        end_time = exchange.parse8601('2023-04-26T18:00:00Z')
    elif symbol == 'US30':
        start_time = exchange.parse8601('2023-04-26T14:00:00Z')
        end_time = exchange.parse8601('2023-04-26T19:00:00Z')
    elif symbol == 'US100':
        start_time = exchange.parse8601('2023-04-26T14:00:00Z')
        end_time = exchange.parse8601('2023-04-26T19:00:00Z')
    else:
        print(f"Invalid symbol: {symbol}")
        continue

    now = exchange.milliseconds()
    if start_time <= now <= end_time:
        for timeframe in timeframes:
            bars = exchange.fetch_ohlcv(symbol, timeframe, since, limit, params)
            ticks = exchange.fetch_ticker(symbol)

            # Map candlesticks to np array
            closes = np.asarray([x[4] for x in bars])

            # Define SMA indicators
            sma20 = talib.SMA(closes, timeperiod=20)
            sma50 = talib.SMA(closes, timeperiod=50)
            sma200 = talib.SMA(closes, timeperiod=200)

            # Define EMA indicators
            ema20 = talib.EMA(closes, timeperiod=20)
            ema50 = talib.EMA(closes, timeperiod=50)
            ema200 = talib.EMA(closes, timeperiod=200)

            # Identify trend direction
            if sma20[-1] > sma50[-1] > sma200[-1]:
                print(f"{symbol} ({timeframe}): Bullish trend")

            elif sma20[-1] < sma50[-1] < sma200[-1]:
                print(f"{symbol} ({timeframe}): Bearish trend")

            else:
                print(f"{symbol} ({timeframe}): Ranging trend")

            # Identify key levels based on trend
            if sma20[-1] > sma50[-1] > sma200[-1]:
                support_level = np.min(closes)
                print(f"{symbol} ({timeframe}): Strong support level: {support_level}")

            elif sma20[-1] < sma50[-1] < sma200[-1]:
                resistance_level = np.max(closes)
                print(f"{symbol} ({timeframe}): Strong resistance level: {resistance_level}")

            # Identify breakout after ranging period
            if sma20[-1] == sma50[-1] == sma200[-1]:
                print(f"{symbol} ({timeframe}): Waiting for breakout")

            # Enter trade based on trend and key levels
            if sma20[-1] > sma50[-1] > sma200[-1]:
                if ticks['last'] < support_level:
                    print(f"{symbol} ({timeframe}): Enter long position")

            elif sma20[-1] < sma50[-1] < sma200[-1]:
                if ticks['last'] > resistance_level:
                    print(f"{symbol} ({timeframe}): Enter short position")
    else:
        print(f"{symbol} markets are currently closed.")
