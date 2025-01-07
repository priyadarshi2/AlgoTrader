import yfinance as yf
import src.Utils.common_strategies as cstr
import backtrader as bt
import src.source_metadata as dta
import src.Utils.validatators as vdtr
from src.source_metadata import param_strat_modified

def get_stock_data(symb,start_date,end_date):
    stock = yf.Ticker(symb)
    data = stock.history(start=start_date, end=end_date)
    return data

def get_backtest(symb,start_date,end_date,amount, key, paramets):
    data = get_stock_data(symb,start_date,end_date)
    result = backtest(data,cstr.common_strats[key],amount, paramets)
    trades, summary = result.trade_manager.get_result()
    strategies = fetch_common_strategies()
    summary["Strategy"] = strategies[key]
    return {"name" : symb, "hist" : trades, "summary" : summary}

def backtest(data,strategy,amount, paramets):
    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro = bt.Cerebro()
    cerebro.adddata(data_feed)
    cerebro.addstrategy(strategy, **paramets)
    cerebro.broker.set_cash(amount)
    cerebro.broker.setcommission(commission=0.001)
    backtest_result = cerebro.run()
    result = backtest_result[0]
    return result

def isValidBacktestKey(key):
    if key in cstr.common_strats.keys():
        return True
    else:
        return False
    
def get_common_strategies():
    str_dct = fetch_common_strategies()
    return {"data" : str_dct}

def fetch_common_strategies():
    str_dct = {}
    for key, class_obj in cstr.common_strats.items():
        str_dct[key] = class_obj.__name__
    return str_dct

def get_parameters(key):
    strats = dta.param_strat_modified
    return {"data" : strats[key]}

def get_validate_params(symb, start_date, end_date, key, paramets):
    # Fetch stock data
    data = get_stock_data(symb, start_date, end_date)
    # Fetch default values from param_strat_modified for the given strategy (key)
    default_params = {param[0]: param[1] for param in param_strat_modified.get(key, [])}
    print(default_params)
    # Combine the default parameters with the user-supplied parameters (paramets)
    paramets.update(default_params)
    paramets["data_length"] = len(data)
    
    # Call validate_params with data and parameters
    result = vdtr.validate_params(key=key, paramets=paramets)
    
    return {"data": result}
