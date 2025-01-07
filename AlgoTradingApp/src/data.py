from src.Utils.common_strategies import common_strats

common_strategies = common_strats

param_strats = {
    0: ['rsi_time', 'rsi_upper', 'rsi_lower'],
    1: ['fast_period', 'slow_period'],           # SMACrossoverStrategy
    2: ['fast_period', 'slow_period', 'signal_period'], # MACDStrategy
    3: ['period', 'nbdevup', 'nbdevdn'],         # BollingerBandsStrategy
    4: ['fast_period', 'slow_period'],           # EMACrossoverStrategy
    6: [],                                       # OBVStrategy (No parameters defined)
    7: ['atr_time', 'atr_threshold']             # ATRStrategy
}

