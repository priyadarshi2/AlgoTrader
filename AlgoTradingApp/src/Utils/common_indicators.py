import backtrader as bt
import talib as ta
import numpy as np
from enum import Enum
from typing import Optional

class CommonTaLibRSI(bt.Indicator):    #Common TA-Lib RSI Indicator 
    lines = ('rsi',)
    params = (('rsi_period',14),)

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, value)
        self.addminperiod(int(self.params.rsi_period))
    
    def next(self):
        #Extract close prices
        close_prices = np.array(self.data.close.get(size=len(self.data)))

        #Compute RSI
        if len(close_prices) >= self.params.rsi_period:
            rsi_values = ta.RSI(close_prices, timeperiod=self.params.rsi_period)
            self.lines.rsi[0] = rsi_values[-1]
        else:
            self.lines.rsi[0] = float('nan')

class CommonTaLibSMA(bt.Indicator):
    lines = ('sma',)
    params = (('period', 14),)

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, value)
        self.addminperiod(int(self.params.period))

    def next(self):
        close_prices = np.array(self.data.close.get(size=len(self.data)))

        if len(close_prices) >= self.params.period:
            sma_values = ta.SMA(close_prices, timeperiod=self.params.period)
            self.lines.sma[0] = sma_values[-1]
        else:
            self.lines.sma[0] = float('nan')

class CommonTaLibEMA(bt.Indicator):
    lines = ('ema',)
    params = (('period', 14),)

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, value)
        self.addminperiod(int(self.params.period))

    def next(self):
        close_prices = np.array(self.data.close.get(size=len(self.data)))

        if len(close_prices) >= self.params.period:
            ema_values = ta.EMA(close_prices, timeperiod=self.params.period)
            self.lines.ema[0] = ema_values[-1]
        else:
            self.lines.ema[0] = float('nan')

class CommonTaLibMACD(bt.Indicator):
    lines = ('macd', 'macdsignal', 'macdhist',)
    params = (('fastperiod', 12), ('slowperiod', 26), ('signalperiod', 9),)

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, value)
        self.addminperiod(int(self.params.slowperiod) + int(self.params.signalperiod))

    def next(self):
        close_prices = np.array(self.data.close.get(size=len(self.data)))

        if len(close_prices) >= self.params.slowperiod:
            macd, macdsignal, macdhist = ta.MACD(
                close_prices,
                fastperiod=self.params.fastperiod,
                slowperiod=self.params.slowperiod,
                signalperiod=self.params.signalperiod
            )
            self.lines.macd[0] = macd[-1]
            self.lines.macdsignal[0] = macdsignal[-1]
            self.lines.macdhist[0] = macdhist[-1]
        else:
            self.lines.macd[0] = float('nan')
            self.lines.macdsignal[0] = float('nan')
            self.lines.macdhist[0] = float('nan')

class CommonTaLibBBANDS(bt.Indicator):
    lines = ('upperband', 'middleband', 'lowerband',)
    params = (
        ('period', 20),
        ('nbdevup', 2),
        ('nbdevdn', 2),
        ('matype', 0),
        ('dev_factor', 2),
    )

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, value)
        self.addminperiod(int(self.params.period))

    def next(self):
        close_prices = np.array(self.data.close.get(size=len(self.data)))

        if len(close_prices) >= self.params.period:
            upperband, middleband, lowerband = ta.BBANDS(
                close_prices,
                timeperiod=self.params.period,
                nbdevup=self.params.nbdevup * self.params.dev_factor,
                nbdevdn=self.params.nbdevdn * self.params.dev_factor,
                matype=self.params.matype
            )
            self.lines.upperband[0] = upperband[-1]
            self.lines.middleband[0] = middleband[-1]
            self.lines.lowerband[0] = lowerband[-1]
        else:
            self.lines.upperband[0] = float('nan')
            self.lines.middleband[0] = float('nan')
            self.lines.lowerband[0] = float('nan')

class CommonTaLibOBV(bt.Indicator):
    lines = ('obv',)
    params = (('timeperiod', 18),)

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, value)
        self.addminperiod(int(self.params.timeperiod))

    def next(self):
        close_prices = np.array(self.data.close.get(size=len(self.data)))
        volumes = np.array(self.data.volume.get(size=len(self.data)))

        if len(close_prices) >= 2:  # OBV requires at least 2 data points
            obv_values = ta.OBV(close_prices, volumes)
            self.lines.obv[0] = obv_values[-1]
        else:
            self.lines.obv[0] = float('nan')

class CommonTaLibATR(bt.Indicator):
    # Common TA-Lib ATR Indicator
    lines = ('atr',)
    params = (('atr_period', 14),)

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, value)
        self.addminperiod(int(self.params.atr_period))

    def next(self):
        # Extract high, low, and close prices
        high_prices = np.array(self.data.high.get(size=len(self.data)))
        low_prices = np.array(self.data.low.get(size=len(self.data)))
        close_prices = np.array(self.data.close.get(size=len(self.data)))

        # Compute ATR
        if len(close_prices) >= self.params.atr_period:
            atr_values = ta.ATR(high_prices, low_prices, close_prices, timeperiod=self.params.atr_period)
            self.lines.atr[0] = atr_values[-1]
        else:
            self.lines.atr[0] = float('nan')


class PatternType(Enum):
    RBD = "RBD"
    RBR = "RBR"
    DBR = "DBR"
    DBD = "DBD"

class PatternOccurrence:
    def __init__(self, pattern_type: PatternType, time: int, properties: dict):
        self.pattern_type = pattern_type
        self.time = time
        self.properties = properties

class CombinedPatternIndicator(bt.Indicator):
    lines = ('pattern',)
    params = (('pattern_lookback', 14), ('min_base_size', 1), ('max_base_size', 5))

    def __init__(self):
        self.addminperiod(self.params.pattern_lookback)
        self.lines.pattern = None

    def next(self):
        high, low, close = [np.array(getattr(self.data, attr).get(size=self.params.pattern_lookback)) for attr in ['high', 'low', 'close']]
        if len(high) >= self.params.pattern_lookback:
            self.lines.pattern[0] = self._detect_patterns(high, low, close)

    def _detect_patterns(self, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> Optional[PatternOccurrence]:
        for pattern in [self._is_rbr_pattern, self._is_rbd_pattern, self._is_dbr_pattern, self._is_dbd_pattern]:
            if pattern(high, low, close):
                pattern_type = pattern.__name__.split('_')[1].upper()
                properties = {
                    'base_size': high[-1] - low[-1],
                    'risk': high[-1] - min(low) if 'RBD' in pattern_type else low[-1] - min(low),
                    'reward': max(high) - high[-1]
                }
                return PatternOccurrence(PatternType[pattern_type], len(self.data), properties)
        return None

    def _is_base_pattern(self, high, low, close, trend, check_fn):
        base_range = high[-1] - low[-1]
        return (self.p.min_base_size <= base_range <= self.p.max_base_size and check_fn(close) and 
                all(close[i-1] > close[i] for i in range(trend[0], trend[1], trend[2])))

    def _is_rbr_pattern(self, high, low, close): return self._is_base_pattern(high, low, close, (-3, -6, -1), lambda c: c[-1] > max(high[-3:]))
    def _is_rbd_pattern(self, high, low, close): return self._is_base_pattern(high, low, close, (-3, -6, -1), lambda c: c[-1] < min(low[-3:]))
    def _is_dbr_pattern(self, high, low, close): return self._is_base_pattern(high, low, close, (8, 5, -1), lambda c: max(high[-3:]) > min(low[-8:-5]))
    def _is_dbd_pattern(self, high, low, close): return self._is_base_pattern(high, low, close, (8, 5, -1), lambda c: min(low[-3:]) < max(high[-8:-5]))
