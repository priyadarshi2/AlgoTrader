import backtrader as bt 
import src.Utils.common_indicators as cind
import src.Utils.standard as std
import src.Utils.custom_strategies as cstm

class RSIStrategy(bt.Strategy):
    params = (
        ('rsi_time', 14),
        ('rsi_upper', 70),
        ('rsi_lower', 30),
    )

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, int(value))
            else:
                print(f"Warning: Unrecognized parameter '{key}' for RSIStrategy.")
        self.rsi = cind.CommonTaLibRSI(self.data, rsi_period=int(self.params.rsi_time))
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}
    
    def get_param(self):
        # Create a dictionary of current parameters
        self.param_dict = {key: getattr(self.params, key) for key in self.params._getkeys()}
        return self.param_dict
    
    def next(self):
        if self.rsi.lines.rsi[0] < int(self.params.rsi_lower):
            self.trade_manager.execute_trade('buy')
        elif self.rsi.lines.rsi[0] > int(self.params.rsi_upper):
            self.trade_manager.execute_trade('sell')

    def stop(self):
        self.trade_manager.finalize_portfolio()
    
       
class SMACrossoverStrategy(bt.Strategy):
    params = (
        ('fast_period', 10),
        ('slow_period', 30),
    )

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, int(value))
            else:
                print(f"Warning: Unrecognized parameter '{key}' for RSIStrategy.")
        self.fast_sma = cind.CommonTaLibSMA(self.data, period=int(self.params.fast_period))
        self.slow_sma = cind.CommonTaLibSMA(self.data, period=int(self.params.slow_period))
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}
    
    def get_param(self):
        # Create a dictionary of current parameters
        self.param_dict = {key: getattr(self.params, key) for key in self.params._getkeys()}
        return self.param_dict


    def next(self):
        if not self.position:  # Not in position
            if self.fast_sma.lines.sma[0] > self.slow_sma.lines.sma[0]:
                self.trade_manager.execute_trade('buy')
        else:  # In position
            if self.fast_sma.lines.sma[0] < self.slow_sma.lines.sma[0]:
                self.trade_manager.execute_trade('sell')
    
    def stop(self):
        self.trade_manager.finalize_portfolio()

class MACDStrategy(bt.Strategy):
    params = (
        ('fast_period', 12),
        ('slow_period', 26),
        ('signal_period', 9),
    )

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, int(value))
            else:
                print(f"Warning: Unrecognized parameter '{key}' for RSIStrategy.")
        self.macd = cind.CommonTaLibMACD(
            self.data,
            fastperiod=int(self.params.fast_period),
            slowperiod=int(self.params.slow_period),
            signalperiod=int(self.params.signal_period)
        )
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}
    
    def get_param(self):
        # Create a dictionary of current parameters
        self.param_dict = {key: getattr(self.params, key) for key in self.params._getkeys()}
        return self.param_dict


    def next(self):
        if not self.position:
            if self.macd.lines.macd[0] > self.macd.lines.macdsignal[0]:
                self.trade_manager.execute_trade('buy')
        else:
            if self.macd.lines.macd[0] < self.macd.lines.macdsignal[0]:
                self.trade_manager.execute_trade('sell')
        
    def stop(self):
        self.trade_manager.finalize_portfolio()

class BollingerBandsStrategy(bt.Strategy):
    params = (
        ('period', 20),
        ('nbdevup', 2),
        ('nbdevdn', 2),
    )

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, int(value))
            else:
                print(f"Warning: Unrecognized parameter '{key}' for RSIStrategy.")
        self.bb = cind.CommonTaLibBBANDS(
            self.data,
            period=int(self.params.period),
            nbdevup=int(self.params.nbdevup),
            nbdevdn=int(self.params.nbdevdn)
        )
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}
    
    def get_param(self):
        # Create a dictionary of current parameters
        self.param_dict = {key: getattr(self.params, key) for key in self.params._getkeys()}
        return self.param_dict


    def next(self):
        if not self.position:
            if self.data.close[0] < self.bb.lines.lowerband[0]:
                self.trade_manager.execute_trade('buy')
        else:
            if self.data.close[0] > self.bb.lines.upperband[0]:
                self.trade_manager.execute_trade('sell')
    
    def stop(self):
        self.trade_manager.finalize_portfolio()

class EMACrossoverStrategy(bt.Strategy):
    params = (
        ('fast_period', 10),
        ('slow_period', 30),
    )

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, int(value))
            else:
                print(f"Warning: Unrecognized parameter '{key}' for RSIStrategy.")

        self.fast_ema = cind.CommonTaLibEMA(self.data, period=self.params.fast_period)
        self.slow_ema = cind.CommonTaLibEMA(self.data, period=self.params.slow_period)
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}
    
    def get_param(self):
        # Create a dictionary of current parameters
        self.param_dict = {key: getattr(self.params, key) for key in self.params._getkeys()}
        return self.param_dict

    def next(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, value)
            else:
                print(f"Warning: Unrecognized parameter '{key}' for RSIStrategy.")

        if not self.position:
            if self.fast_ema.lines.ema[0] > self.slow_ema.lines.ema[0]:
                self.trade_manager.execute_trade('buy')
        else:
            if self.fast_ema.lines.ema[0] < self.slow_ema.lines.ema[0]:
                self.trade_manager.execute_trade('sell')
    
    def stop(self):
        self.trade_manager.finalize_portfolio()

class OBVStrategy(bt.Strategy):
    params = ()
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, int(value))
            else:
                print(f"Warning: Unrecognized parameter '{key}' for RSIStrategy.")
        self.obv = cind.CommonTaLibOBV(self.data, )
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}
    
    def get_param(self):

        # Create a dictionary of current parameters
        self.param_dict = {key: getattr(self.params, key) for key in self.params._getkeys()}
        return self.param_dict
        


    def next(self):
        if not self.position:
            if self.data.close[0] > self.data.close[-1] and self.obv.lines.obv[0] > self.obv.lines.obv[-1]:
                self.trade_manager.execute_trade('buy')
        else:
            if self.data.close[0] < self.data.close[-1] and self.obv.lines.obv[0] < self.obv.lines.obv[-1]:
                self.trade_manager.execute_trade('sell')
    
    def stop(self):
        self.trade_manager.finalize_portfolio()

class ATRStrategy(bt.Strategy):
    params = (
        ('atr_time', 14),
        ('atr_threshold', 2.0),  # Example threshold value
    )

    def __init__(self, **kwargs):
        # Dynamically update parameters
        for key, value in kwargs.items():
            if key in self.params._getkeys():
                setattr(self.params, key, int(value))
            else:
                print(f"Warning: Unrecognized parameter '{key}' for RSIStrategy.")
        self.atr = cind.CommonTaLibATR(self.data, atr_period=self.params.atr_time)
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}
    
    def get_param(self):
        # Create a dictionary of current parameters
        self.param_dict = {key: getattr(self.params, key) for key in self.params._getkeys()}
        return self.param_dict


    def next(self):
        if self.atr.lines.atr[0] > self.params.atr_threshold:
            self.trade_manager.execute_trade('buy')
        elif self.atr.lines.atr[0] < self.params.atr_threshold:
            self.trade_manager.execute_trade('sell')

    def stop(self):
        self.trade_manager.finalize_portfolio()

common_strats = {
    0 : RSIStrategy,
    1 : SMACrossoverStrategy,
    2 : MACDStrategy,
    3 : BollingerBandsStrategy,
    4 : EMACrossoverStrategy,
    6 : OBVStrategy,
    7 : ATRStrategy
}
