from src.Utils.common_strategies import common_strats

common_strategies = common_strats

param_strats = {
    0: ['rsi_time', 'rsi_upper', 'rsi_lower'],
    1: ['fast_period', 'slow_period'],           # SMACrossoverStrategy
    2: ['fast_period', 'slow_period', 'signal_period'], # MACDStrategy
    3: ['period', 'nbdevup', 'nbdevdn'],         # BollingerBandsStrategy
    4: ['fast_period', 'slow_period'],           # EMACrossoverStrategy
    5: [],                                       # OBVStrategy (No parameters defined)
    6: ['atr_time', 'atr_threshold']             # ATRStrategy
}

param_strat_modified = {
    0: [  # RSIStrategy
        ('rsi_time', 14, 2, 50), 
        ('rsi_upper', 70, 50, 100), 
        ('rsi_lower', 30, 0, 50)
    ],
    1: [  # SMACrossoverStrategy
        ('fast_period', 10, 1, 50), 
        ('slow_period', 30, 10, 200)
    ],
    2: [  # MACDStrategy
        ('fast_period', 12, 1, 50), 
        ('slow_period', 26, 10, 200), 
        ('signal_period', 9, 1, 50)
    ],
    3: [  # BollingerBandsStrategy
        ('period', 20, 5, 100), 
        ('nbdevup', 2, 1, 5), 
        ('nbdevdn', 2, 1, 5)
    ],
    4: [  # EMACrossoverStrategy
        ('fast_period', 10, 1, 50), 
        ('slow_period', 30, 10, 200)
    ],
    5: [  # OBVStrategy (No parameters defined)
    ],
    6: [  # ATRStrategy
        ('atr_time', 14, 1, 50), 
        ('atr_threshold', 2, 0, 5) ####this will be float#######
    ]
}



