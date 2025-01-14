from fastapi import HTTPException, Response
from typing import Dict, List, Tuple, Union, Optional
from src.Utils.param_model import Params, CustomParams
import datetime

def validate_period(period, min_val, max_val, data_length): 
    errors = [] 
    if period < min_val or period > max_val: 
        errors.append(f"Period {period} is out of bounds. Must be between {min_val} and {max_val}.") 
    if period >= data_length: errors.append(f"Period {period} cannot be greater than or equal to the length of the data {data_length}.") 
    return { "is_valid": not errors, "errors": errors }

def validate_params(key : int, paramets : Union[Params,CustomParams] ):    
    # Fetch the validation function based on the key
    validate_fn = input_validations.get(key)
    
    if validate_fn:
        # Pass the parameters along with the length of the data
        # Assuming paramets contains a dictionary of the relevant parameters for the strategy
        print("data_length==>",paramets.asset_params.data_length)
        if isinstance(paramets, Params):
            result = validate_fn(*paramets.strategy_params.get_optional_params_tuple(), data_length=paramets.asset_params.data_length)
        elif isinstance(paramets, CustomParams):
            if key == 7:
                result = validate_fn(*paramets.strategy_params[1].get_optional_params_tuple())
            elif key == 8:
                result = validate_fn(*paramets.strategy_params[0].get_optional_params_tuple())
        print("result==>",result)
        return result
    else:
        return {"error": f"Invalid strategy key: {key}"}


def validate_rsi_inputs(rsi_time, rsi_upper, rsi_lower, data_length):
    errors = []

    # Validate RSI period using the generalized function
    rsi_period_validation = validate_period(rsi_time, 2, 50, data_length)
    if not rsi_period_validation["is_valid"]:
        errors.extend(rsi_period_validation["errors"])

    # Validate RSI limits
    if not (0 <= rsi_upper <= 100 and 0 <= rsi_lower <= 100):
        errors.append("RSI limits must be between 0 and 100.")
    elif rsi_upper <= rsi_lower:
        errors.append("RSI upper limit must be greater than the lower limit.")

    return {
        "is_valid": not errors,
        "errors": errors
    }

def validate_sma_crossover_inputs(fast_period, slow_period, data_length):
    errors = []

    # Validate fast period using the generalized function
    fast_period_validation = validate_period(fast_period, 1, 50, data_length)
    if not fast_period_validation["is_valid"]:
        errors.extend(fast_period_validation["errors"])

    # Validate slow period using the generalized function
    slow_period_validation = validate_period(slow_period, 10, 200, data_length)
    if not slow_period_validation["is_valid"]:
        errors.extend(slow_period_validation["errors"])

    return {
        "is_valid": not errors,
        "errors": errors
    }

def validate_macd_inputs(fast_period, slow_period, signal_period, data_length):
    errors = []

    # Validate fast period
    fast_period_validation = validate_period(fast_period, 1, 50, data_length)
    if not fast_period_validation["is_valid"]:
        errors.extend(fast_period_validation["errors"])

    # Validate slow period
    slow_period_validation = validate_period(slow_period, 10, 200, data_length)
    if not slow_period_validation["is_valid"]:
        errors.extend(slow_period_validation["errors"])

    # Validate signal period
    signal_period_validation = validate_period(signal_period, 1, 50, data_length)
    if not signal_period_validation["is_valid"]:
        errors.extend(signal_period_validation["errors"])

    return {
        "is_valid": not errors,
        "errors": errors
    }

def validate_ema_crossover_inputs(fast_period, slow_period, data_length):
    errors = []

    # Validate fast period
    fast_period_validation = validate_period(fast_period, 1, 50, data_length)
    if not fast_period_validation["is_valid"]:
        errors.extend(fast_period_validation["errors"])

    # Validate slow period
    slow_period_validation = validate_period(slow_period, 10, 200, data_length)
    if not slow_period_validation["is_valid"]:
        errors.extend(slow_period_validation["errors"])

    return {
        "is_valid": not errors,
        "errors": errors
    }

def validate_bollinger_bands_inputs(period, nbdevup, nbdevdn, data_length):
    errors = []

    # Validate period
    period_validation = validate_period(period, 5, 100, data_length)
    if not period_validation["is_valid"]:
        errors.extend(period_validation["errors"])

    # Validate nbdevup and nbdevdn
    if not (1 <= nbdevup <= 5):
        errors.append(f"nbdevup must be between 1 and 5. Provided value: {nbdevup}")
    if not (1 <= nbdevdn <= 5):
        errors.append(f"nbdevdn must be between 1 and 5. Provided value: {nbdevdn}")

    return {
        "is_valid": not errors,
        "errors": errors
    }

def validate_obv_inputs(data_length):
    errors = []

    # Ensure there's enough data to calculate OBV (at least 2 data points)
    if data_length < 2:
        errors.append("Not enough data points to calculate OBV. At least 2 data points are required.")

    return {
        "is_valid": not errors,
        "errors": errors
    }

def validate_atr_inputs(atr_time, atr_threshold, data_length):
    errors = []

    # Validate atr_time
    atr_time_validation = validate_period(atr_time, 1, 50, data_length)
    if not atr_time_validation["is_valid"]:
        errors.extend(atr_time_validation["errors"])

    # Validate atr_threshold
    if not (0 < atr_threshold <= 5):
        errors.append(f"ATR threshold must be a float between 0 and 5. Provided value: {atr_threshold}")

    return {
        "is_valid": not errors,
        "errors": errors
    }

def validate_combined_pattern_params(pattern_lookback, min_base_size, max_base_size):
    """
    Validates the parameters for the CombinedPatternIndicator.
    
    Args:
        pattern_lookback (int): Number of lookback periods for pattern detection.
        min_base_size (float): Minimum size of the pattern's base.
        max_base_size (float): Maximum size of the pattern's base.
    
    Returns:
        dict: A dictionary indicating whether the parameters are valid and any errors.
    """
    print("pattern_lookback",pattern_lookback)
    print("min_base_size",min_base_size)
    print("max_base_size",max_base_size)
    errors = []

    # Validate pattern_lookback
    if not isinstance(pattern_lookback, int) or pattern_lookback < 1:
        errors.append("pattern_lookback must be a positive integer greater than 0.")

    # Validate min_base_size
    if not isinstance(min_base_size, (int, float)) or min_base_size <= 0:
        errors.append("min_base_size must be a positive number.")

    # Validate max_base_size
    if not isinstance(max_base_size, (int, float)) or max_base_size <= 0:
        errors.append("max_base_size must be a positive number.")

    # Ensure min_base_size is less than or equal to max_base_size
    if min_base_size > max_base_size:
        errors.append("min_base_size must be less than or equal to max_base_size.")

    return {
        "is_valid": not errors,
        "errors": errors
    }


def validate_ufo_params(risk_per_trade, stop_loss_atr, take_profit_atr):
    """
    Validates the parameters for the UFO strategy.
    
    Args:
        stop_loss_atr (float): ATR multiplier for stop-loss.
        take_profit_atr (float): ATR multiplier for take-profit.
        risk_per_trade (float): Fraction of capital to risk per trade.
    
    Returns:
        dict: A dictionary indicating whether the parameters are valid and any errors.
    """
    print("stop_loss_atr",stop_loss_atr)
    print("take_profit_atr",take_profit_atr)
    print("risk_per_trade",risk_per_trade)

    errors = []

    # Validate stop_loss_atr
    if stop_loss_atr <= 0:
        errors.append("stop_loss_atr must be a positive float.")

    # Validate take_profit_atr
    if take_profit_atr <= 0:
        errors.append("take_profit_atr must be a positive float.")

    # Ensure take_profit_atr > stop_loss_atr for a positive risk-reward ratio
    if take_profit_atr <= stop_loss_atr:
        errors.append("take_profit_atr must be greater than stop_loss_atr for a positive risk-reward ratio.")

    # Validate risk_per_trade
    if not (0 < risk_per_trade <= 1):
        errors.append("risk_per_trade must be a float between 0 and 1 (exclusive).")

    return {
        "is_valid": not errors,
        "errors": errors
    }


input_validations = {
    0 : validate_rsi_inputs,
    1 : validate_sma_crossover_inputs,
    2 : validate_macd_inputs,
    3 : validate_bollinger_bands_inputs,
    4 : validate_ema_crossover_inputs,
    5 : validate_obv_inputs,
    6 : validate_atr_inputs,
    7 : validate_combined_pattern_params,
    8 : validate_ufo_params
}
