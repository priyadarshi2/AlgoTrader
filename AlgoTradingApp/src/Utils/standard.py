from datetime import datetime

class TradeManager:
    def __init__(self, strategy):
        """
        Initialize the TradeManager with the parent strategy.
        :param strategy: The strategy object using this trade manager.
        """
        self.strategy = strategy

        # Portfolio tracking
        self.portfolio = {
            'Start': None,
            'End': None,
            'Net': None,
            'Net Percentage': None,
            'Total trades' : None,
            'Winning trades' : None,
            'Losing trades' : None,
        }


        # Trade log
        self.trades = {
            'Action': [],
            'Price': [],
            'DateTime': [],
        }

        self.actions = []
        self.start_cash = None
        self.end_cash = None
        self.profit = None
        self.profit_perc = None
    
    def execute_trade(self, signal, size=None):
        """
        Executes a trade based on the given signal and logs it.
        :param signal: 'buy' or 'sell'
        :param size: The size of the trade. If None, uses the default size.
        """
        if signal == 'buy':
            if not self.strategy.position:  # Only buy if not in position
                self.strategy.buy(size=size)
                self._log_trade('Buy')
        elif signal == 'sell':
            if self.strategy.position:  # Only sell if in position
                self.strategy.sell(size=size)
                self._log_trade('Sell')

    def _log_trade(self, action):
        """
        Logs trade details into the trades dictionary.
        :param action: 'Buy' or 'Sell'
        """
        trade = {
            'Action': action,
            'Price': self.strategy.data.close[0],
            'DateTime': self.strategy.data.datetime.datetime(0),
        }
        for key, value in trade.items():
            self.trades[key].append(value)
        self.actions.append(trade)
    

    def finalize_portfolio(self):
        """
        Calculates portfolio performance at the end of the strategy.
        """
        self.start_cash = self.strategy.broker.startingcash
        self.end_cash = self.strategy.broker.getvalue()
        self.profit = self.end_cash - self.start_cash
        self.profit_perc = (self.profit/self.start_cash)*100

        self.portfolio['Start'] = f"{round(self.start_cash, 3)}"
        self.portfolio['End'] = f"{round(self.end_cash, 3)}"
        self.portfolio['Net'] = "{0}{1}".format('+' if self.profit > 0 else '', round(self.profit,3))
        self.portfolio['Net Percentage'] = f"{round(self.profit_perc, 3)}%"
        self.portfolio['Total trades'] = len(self.trades['Action'])
        self.portfolio['Winning trades'] = len([trade for trade in self.trades['Action'] if trade == 'Buy'])
        self.portfolio['Losing trades'] = len([trade for trade in self.trades['Action'] if trade == 'Sell'])
    
    def get_result(self):
        return self.actions, self.portfolio
    
    def get_result_df(self):
        return self.trades, self.portfolio
    
    def addTradeData(self, tradedata):
        self.portfolio.update(tradedata)
    

class Leg:
    def __init__(self, **kwargs):
        default_params = {
            'target_profit': None,
            'trail_sl': None,
            'stop_loss': None,
            're_entry_sl': None,
            're_entry_tgt': None,
            'simple_momentum': None,
            'range_breakout': None
        }
        self.params = {**default_params, **kwargs}

    def __repr__(self):
        return f"Leg({self.params})"

    def get_param(self, key):
        return self.params.get(key, None)

    def set_param(self, key, value):
        self.params[key] = value

class Legs:
    def __init__(self, quantity, position, *legs):
        self.quantity = quantity
        self.position = position
        self.legs = legs

    def __repr__(self):
        return (f"Legs(quantity={self.quantity}, position={self.position}, "
                f"legs={self.legs})")

    def get_leg(self, index):
        if 0 <= index < len(self.legs):
            return self.legs[index]
        else:
            return None

