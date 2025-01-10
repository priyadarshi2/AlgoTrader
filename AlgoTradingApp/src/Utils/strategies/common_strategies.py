import backtrader as bt 
import src.Utils.indicators.common_indicators as cind
import src.Utils.standard as std
from src.Utils.param_model import Params

class RSIStrategy(bt.Strategy):
    params = Params.get_params_detail('RSI')
    def __init__(self):
        print("RSI params", self.params)
        self.rsi = cind.CommonTaLibRSI(self.data, rsi_period=int(self.params.rsi_time))
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}
    
    def next(self):
        if self.rsi.lines.rsi[0] < int(self.params.rsi_lower):
            self.trade_manager.execute_trade('buy')
        elif self.rsi.lines.rsi[0] > int(self.params.rsi_upper):
            self.trade_manager.execute_trade('sell')

    def stop(self):
        self.trade_manager.finalize_portfolio()
    
    def validate_params(self, params):
        """
        Function to validate the parameters for the strategy.
        Raise ValueError if any parameter is invalid.
        """
        # Validate that RSI period is positive and within a reasonable range
        if params['rsi_time'] <= 0:
            raise ValueError(f"Invalid RSI period: {params['rsi_time']}. It must be a positive integer.")
        if params['rsi_time'] < 5 or params['rsi_time'] > 100:
            raise ValueError(f"RSI period: {params['rsi_time']} is too short or too long. It should be between 5 and 100.")

        # Validate that upper and lower RSI levels are within logical bounds
        if not (0 <= params['rsi_lower'] < params['rsi_upper'] <= 100):
            raise ValueError(f"Invalid RSI levels: rsi_lower should be less than rsi_upper, and both should be between 0 and 100.")
        
        # Ensure that RSI levels are within typical ranges (optional, can be customized)
        if params['rsi_upper'] >= 100 or params['rsi_lower'] <= 0:
            raise ValueError(f"Invalid RSI levels: RSI values should be between 0 and 100. rsi_upper: {params['rsi_upper']}, rsi_lower: {params['rsi_lower']}")

        # Optional: Add more checks depending on other conditions specific to the strategy
        # For example, checking if 'rsi_upper' and 'rsi_lower' are in a reasonable range (e.g., avoiding overly tight levels)
        if params['rsi_upper'] - params['rsi_lower'] < 10:
            raise ValueError(f"RSI range between upper and lower values is too tight. Consider widening the gap.")
    
       
class SMACrossoverStrategy(bt.Strategy):
    params = Params.get_params_detail('SMACrossOver')
    def __init__(self):
        self.fast_sma = cind.CommonTaLibSMA(self.data, period=int(self.params.fast_period))
        self.slow_sma = cind.CommonTaLibSMA(self.data, period=int(self.params.slow_period))
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}
    
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
    params = Params.get_params_detail('MACD')
    def __init__(self):
        self.macd = cind.CommonTaLibMACD(
            self.data,
            fastperiod=int(self.params.fast_period),
            slowperiod=int(self.params.slow_period),
            signalperiod=int(self.params.signal_period)
        )
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}
    
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
    params = Params.get_params_detail('BBands')
    def __init__(self):
        self.bb = cind.CommonTaLibBBANDS(
            self.data,
            period=int(self.params.period),
            nbdevup=int(self.params.nbdevup),
            nbdevdn=int(self.params.nbdevdn)
        )
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}
    
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
    params = Params.get_params_detail('EMACrossOver')
    def __init__(self):
        self.fast_ema = cind.CommonTaLibEMA(self.data, period=self.params.fast_period)
        self.slow_ema = cind.CommonTaLibEMA(self.data, period=self.params.slow_period)
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}

    def next(self):
        if not self.position:
            if self.fast_ema.lines.ema[0] > self.slow_ema.lines.ema[0]:
                self.trade_manager.execute_trade('buy')
        else:
            if self.fast_ema.lines.ema[0] < self.slow_ema.lines.ema[0]:
                self.trade_manager.execute_trade('sell')
    
    def stop(self):
        self.trade_manager.finalize_portfolio()

class OBVStrategy(bt.Strategy):
    params = Params.get_params_detail('OBV')
    def __init__(self):
        self.obv = cind.CommonTaLibOBV(self.data)
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}

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
    params = Params.get_params_detail('ATR')
    def __init__(self):
        self.atr = cind.CommonTaLibATR(self.data, atr_period=self.params.atr_time)
        self.trade_manager = std.TradeManager(self)
        self.param_dict = {}
    
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
    5 : OBVStrategy,
    6 : ATRStrategy
}
