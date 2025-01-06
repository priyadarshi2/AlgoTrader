import backtrader as bt
import talib as ta
import numpy as np

class CommonTaLibRSI(bt.Indicator):    #Common TA-Lib RSI Indicator 
    lines = ('rsi',)
    params = (('rsi_period',14),)

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, value)
        self.addminperiod(self.params.rsi_period)
    
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
        self.addminperiod(self.params.period)

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
        self.addminperiod(self.params.period)

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
        self.addminperiod(self.params.slowperiod + self.params.signalperiod)

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
    params = (('period', 20), ('nbdevup', 2), ('nbdevdn', 2), ('matype', 0),)

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, value)
        self.addminperiod(self.params.period)

    def next(self):
        close_prices = np.array(self.data.close.get(size=len(self.data)))

        if len(close_prices) >= self.params.period:
            upperband, middleband, lowerband = ta.BBANDS(
                close_prices,
                timeperiod=self.params.period,
                nbdevup=self.params.nbdevup,
                nbdevdn=self.params.nbdevdn,
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
        self.addminperiod(self.params.timeperiod)

    def next(self):
        close_prices = np.array(self.data.close.get(size=len(self.data)))
        volumes = np.array(self.data.volume.get(size=len(self.data)))

        if len(close_prices) >= 2:  # OBV requires at least 2 data points
            obv_values = ta.OBV(close_prices, volumes)
            self.lines.obv[0] = obv_values[-1]
        else:
            self.lines.obv[0] = float('nan')
