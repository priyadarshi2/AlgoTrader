import backtrader as bt
import talib as ta
import numpy as np
from enum import Enum
from typing import Optional
from src.Utils.param_model import CustomParams, StrategyParams

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
    params = CustomParams.get_params_detail('Patterns')

    def __init__(self, strategy_params : StrategyParams = None):
        if strategy_params: 
            self._update_params(strategy_params)
        super(CombinedPatternIndicator, self).__init__()
        print("Pattern params", self.params)
        self.addminperiod(self.params.pattern_lookback)
    
    def _update_params(self, strategy_params: StrategyParams):
        """Update strategy parameters with provided values."""
        updated_params = []

        # Convert params tuple to a dictionary for easier update
        params_dict = dict(CustomParams.get_params_detail('Patterns'))

        # Update the params dictionary with the provided strategy parameters
        for param, value in strategy_params.optional_params.items():
            if param in params_dict:
                params_dict[param] = value

        # Append the updated params to self.params
        for param, value in updated_params:
            setattr(self.params, param, value)

    def next(self):
        high, low, close = [np.array(getattr(self.data, attr).get(size=self.params.pattern_lookback)) for attr in ['high', 'low', 'close']]
        if len(high) >= self.params.pattern_lookback:
            self.pattern_type = self._detect_patterns()

    def _detect_patterns(self) -> Optional[PatternOccurrence]:
        high, low, close = [np.array(getattr(self.data, attr).get(size=self.params.pattern_lookback)) for attr in ['high', 'low', 'close']]
        for pattern in [self._is_rbr_pattern, self._is_rbd_pattern, self._is_dbr_pattern, self._is_dbd_pattern]:
            if pattern(high, low, close):
                pattern_type = pattern.__name__.split('_')[2].upper()
                properties = {
                    'base_size': high[-1] - low[-1],
                    'risk': high[-1] - min(low) if 'RBD' in pattern_type else low[-1] - min(low),
                    'reward': max(high) - high[-1]
                }
                print(f"Pattern detected: {pattern_type}")
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

