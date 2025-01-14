import yfinance as yf
import src.Utils.strategies.common_strategies as cstr
import backtrader as bt
import src.source_metadata as dta
import src.Utils.validatators as vdtr
from src.Utils.param_model import CustomParams, StrategyParams, Params 
from src.source_metadata import strats_inds, params_keys, param_strat_modified

def get_stock_data(symb,start_date,end_date, time_delta):
    stock = yf.Ticker(symb)
    data = stock.history(start=start_date, end=end_date, interval=time_delta)
    return data

def get_backtest(param : Params):
    print("===============>get_backtest")
    stock_details = param.asset_params.get_params_tuple()
    data = get_stock_data(*stock_details)
    param.set_asset_data_length(len(data))
    print("===============>param_set_length")
    result = backtest(data,param)
    trades, summary = result.trade_manager.get_result()
    summary["Strategy"] = param.strategy_params.name
    return {"name" : param.asset_params.ticker_symbol, "hist" : trades, "summary" : summary}

def backtest(data, param : Params):
    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro = bt.Cerebro()
    cerebro.adddata(data_feed)
    strategy = cstr.common_strats[params_keys[param.strategy_params.name]]
    cerebro.addstrategy(strategy)
    cerebro.broker.set_cash(param.asset_params.amount)
    cerebro.broker.setcommission(commission=0.001)
    backtest_result = cerebro.run()
    result = backtest_result[0]
    return result

def isValidBacktestKey(key):
    if key in params_keys.keys():
        return True
    else:
        return False
    
def get_common_strategies():
    return {"data" : params_keys}

def get_parameters(key):
    param_list = param_strat_modified[params_keys[key]]  
    result = [param[:4] for param in param_list] 
    return {"data" : result}

def get_validate_params(paramets : Params):
    
    # Fetch stock data
    data = get_stock_data(*paramets.asset_params.get_params_tuple())
    paramets.set_asset_data_length(len(data))
    key = params_keys[paramets.strategy_params.name]
    # Call validate_params with data and parameters
    result = vdtr.validate_params(key=key, paramets=paramets)
    
    return {"data": result}

def get_custom_backtest(param : CustomParams):
    print("===============>get_custom_backtest")
    stock_details = param.asset_params.get_params_tuple()
    data = get_stock_data(*stock_details)
    param.set_asset_data_length(len(data))
    print("===============>param_set_length")
    result = customBacktest(data,param)
    trades, summary = result.trade_manager.get_result()
    summary["Strategy"] = param.strategy_params[0].name
    return {"name" : param.asset_params.ticker_symbol, "hist" : trades, "summary" : summary}

def get_validate_custom_params(paramets : CustomParams):
    
    # Fetch stock data
    data = get_stock_data(*paramets.asset_params.get_params_tuple())
    paramets.set_asset_data_length(len(data))

    key1 = params_keys[paramets.strategy_params[0].name]
    key2 = params_keys[paramets.strategy_params[1].name]
    # Call validate_params with data and parameter
    result = [None, None]
    result[0] = vdtr.validate_params(key=key1, paramets=paramets)
    result[1] = vdtr.validate_params(key=key2, paramets=paramets)
    return {"data": result}

def customBacktest(data, param : CustomParams):
    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro = bt.Cerebro()
    cerebro.adddata(data_feed)
    strategy = strats_inds[params_keys[param.strategy_params[0].name]]
    cerebro.addstrategy(strategy, param.strategy_params)
    cerebro.broker.set_cash(param.asset_params.amount)
    cerebro.broker.setcommission(commission=0.001)
    backtest_result = cerebro.run()
    result = backtest_result[0]
    return result

def get_custom_backtest_df(param : CustomParams):
    print("===============>get_custom_backtest_df")
    stock_details = param.asset_params.get_params_tuple()
    data = get_stock_data(*stock_details)
    param.set_asset_data_length(len(data))
    print("===============>param_set_length")
    result = customBacktest(data,param)
    trades, summary = result.trade_manager.get_result_df()
    summary["Strategy"] = param.strategy_params[0].name
    return {"name" : param.asset_params.ticker_symbol, "hist" : trades, "summary" : summary}