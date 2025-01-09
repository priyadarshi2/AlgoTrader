from fastapi import HTTPException, Response
import datetime

def validate_period(period, min_val, max_val, data_length): 
    errors = [] 
    if period < min_val or period > max_val: 
        errors.append(f"Period {period} is out of bounds. Must be between {min_val} and {max_val}.") 
    if period >= data_length: errors.append(f"Period {period} cannot be greater than or equal to the length of the data {data_length}.") 
    return { "is_valid": not errors, "errors": errors }

def validate_params(key, paramets):    
    # Fetch the validation function based on the key
    validate_fn = input_validations.get(key)
    
    if validate_fn:
        # Pass the parameters along with the length of the data
        # Assuming paramets contains a dictionary of the relevant parameters for the strategy
        result = validate_fn(**paramets)
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


input_validations = {
    0 : validate_rsi_inputs,
    1 : validate_sma_crossover_inputs,
    2 : validate_macd_inputs,
    3 : validate_bollinger_bands_inputs,
    4 : validate_ema_crossover_inputs,
    5 : validate_obv_inputs,
    6 : validate_atr_inputs
}
