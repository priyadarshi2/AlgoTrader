import yfinance as yf
import src.Utils.common_strategies as cstr
import backtrader as bt

def get_stock_data(symb,start_date,end_date):
    stock = yf.Ticker(symb)
    data = stock.history(start=start_date, end=end_date)
    return data

def get_rsi_backtest(symb,start_date,end_date,amount, key):
    data = get_stock_data(symb,start_date,end_date)
    result = backtest(data,cstr.common_strats[key],amount)
    trades, summary = result.trade_manager.get_result()
    strategies = fetch_common_strategies()
    summary["Strategy"] = strategies[key]
    return {"name" : symb, "hist" : trades, "summary" : summary}

def backtest(data,strategy,amount):
    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro = bt.Cerebro()
    cerebro.adddata(data_feed)
    cerebro.addstrategy(strategy)
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