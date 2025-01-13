params_keys = {
    'RSI' : 0,
    'SMACrossOver' : 1,
    'MACD' : 2,
    'BBands' : 3,
    'EMACrossOver' : 4,
    'OBV' : 5,
    'ATR': 6,
    'Patterns' : 7,
    'UFO' : 8,
}

param_strat_modified = {
    0: [  # RSIStrategy
        ('rsi_time', 14, 2, 50, int), 
        ('rsi_upper', 70, 50, 100 ,int), 
        ('rsi_lower', 30, 0, 50,int)
    ],
    1: [  # SMACrossoverStrategy
        ('fast_period', 10, 1, 50,int), 
        ('slow_period', 30, 10, 200,int)
    ],
    2: [  # MACDStrategy
        ('fast_period', 12, 1, 50, int), 
        ('slow_period', 26, 10, 200, int), 
        ('signal_period', 9, 1, 50, int)
    ],
    3: [  # BollingerBandsStrategy
        ('period', 20, 5, 100, int), 
        ('nbdevup', 2, 1, 5, int), 
        ('nbdevdn', 2, 1, 5, int)
    ],
    4: [  # EMACrossoverStrategy
        ('fast_period', 10, 1, 50, int), 
        ('slow_period', 30, 10, 200, int)
    ],
    5: [  # OBVStrategy (No parameters defined)
    ],
    6: [  # ATRStrategy
        ('atr_time', 14, 1, 50, int), 
        ('atr_threshold', 2, 0, 5, float) ####this will be float#######
    ],
    7: [  # PatternIndicator
        ('pattern_lookback', 14, 1, 50, int), 
        ('min_base_size', 1, 1, 5, int), 
        ('max_base_size', 5, 1, 10, int)
    ],
    8 : [ #UFOStrategy
        ('risk_per_trade', 0.01, 0.01, 1.0, float),  # Risk per trade as a fraction of available cash
        ('stop_loss_atr', 2.0, 1.0, 3.0, float),    # ATR multiplier for stop loss
        ('take_profit_atr', 3.0, 1.0, 5.0, float)   # ATR multiplier for take profit
    
    ]
}

