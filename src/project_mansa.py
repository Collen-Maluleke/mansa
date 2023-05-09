import backtrader as bt
import backtrader.indicators as btind

class PsychLevels(bt.Indicator):
    lines = ('support_level', 'resistance_level', 'strength')

    def __init__(self):
        self.support_level = 0
        self.resistance_level = 0
        self.strength = 0

    def next(self):
        close = self.data.close[0]
        if close % 10 == 0:
            self.support_level = close
            self.strength = close % 100 // 10 + 1
        else:
            self.support_level = 0
            self.resistance_level = 0
            self.strength = 0

class EMABot(bt.Strategy):
    params = (
        ('daily_fast_ema', 20),
        ('daily_slow_ema', 50),
        ('intraday_fast_ema', 9),
        ('intraday_slow_ema', 21),
        ('daily_timeframe', bt.TimeFrame.Days),
        ('intraday_timeframe', bt.TimeFrame.Hours),
        ('daily_compression', 1),
        ('intraday_compression', 4),
        ('oscillator', btind.RSI),
        ('oscillator_period', 14),
        ('oscillator_upper', 70),
        ('oscillator_lower', 30),
        ('psych_level_strength_threshold', 2),
        ('risk_reward_ratio', 4),
        ('max_risk_pct', 1),
        ('max_concurrent_trades', 3),
        ('convergence_threshold', 0.05),
    )

    def __init__(self):
        self.daily_data = self.datas[0].resample(
            timeframe=self.params.daily_timeframe,
            compression=self.params.daily_compression,
        )
        self.intraday_data = self.datas[0].resample(
            timeframe=self.params.intraday_timeframe,
            compression=self.params.intraday_compression,
        )

        self.daily_fast_ema = btind.ExponentialMovingAverage(
            self.daily_data.close, period=self.params.daily_fast_ema
        )
        self.daily_slow_ema = btind.ExponentialMovingAverage(
            self.daily_data.close, period=self.params.daily_slow_ema
        )
        self.intraday_fast_ema = btind.ExponentialMovingAverage(
            self.intraday_data.close, period=self.params.intraday_fast_ema
        )
        self.intraday_slow_ema = btind.ExponentialMovingAverage(
            self.intraday_data.close, period=self.params.intraday_slow_ema
        )
        self.psych_levels = PsychLevels()
        self.oscillator = self.params.oscillator(self.datas[0].close, period=self.params.oscillator_period)
        self.previous_psych_level = None
        self.previous_price_action = None
        self.order = None
        self.open_orders = []

    def next(self):
        if self.num_of_open_trades >= self.params.max_number_of_trades:
            return  
       # Check if daily EMAs are bullish or bearish
        daily_trend = None
        if self.daily_fast_ema[0] > self.daily_slow_ema[0]:
            daily_trend = 'bullish'
        elif self.daily_fast_ema[0] < self.daily_slow_ema[0]:
            daily_trend = 'bearish'