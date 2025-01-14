import src.Utils.strategies.common_strategies as common 
import src.Utils.strategies.custom_strategies as custom 
import src.Utils.indicators.custom_indicators as indicators 
import src.Utils.validatators as valids
from src.param_definitions import params_keys, param_strat_modified

strats_inds = {
    0 : common.RSIStrategy,
    1 : common.SMACrossoverStrategy,
    2 : common.MACDStrategy,
    3 : common.BollingerBandsStrategy,
    4 : common.EMACrossoverStrategy,
    5 : common.OBVStrategy,
    6 : common.ATRStrategy,
    7 : indicators.CombinedPatternIndicator,
    8 : custom.UFOStrategy
}

input_valids = {
    0 : valids.validate_rsi_inputs,
    1 : valids.validate_sma_crossover_inputs,
    2 : valids.validate_macd_inputs,
    3 : valids.validate_bollinger_bands_inputs,
    4 : valids.validate_ema_crossover_inputs,
    5 : valids.validate_obv_inputs,
    6 : valids.validate_atr_inputs
}

custom_input_valids = {
    7 : valids.validate_combined_pattern_params,
    8 : valids.validate_ufo_params
}
