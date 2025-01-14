import src.Utils.indicators.custom_indicators as cind
import backtrader as bt
import src.Utils.standard as std 
from src.Utils.param_model import CustomParams, StrategyParams
from typing import List

class UFOStrategy(bt.Strategy):
    params = CustomParams.get_params_detail('UFO')
    def __init__(self, strategy_params :  List[StrategyParams] = None):
        """Initialize strategy."""
        super(UFOStrategy, self).__init__()

        if strategy_params: 
            self._update_params(strategy_params[0])
        
        self.order = None
        self.trades = []
        self.metrics = {}
        self._last_portfolio_value = self.broker.getvalue()
        self.initialized = False
        self.consecutive_losses = 0
        self.patterns = []  # List to store detected patterns
        print("UFO", self.params.stop_loss_atr)
        self.pattern = cind.CombinedPatternIndicator(self.data, strategy_params=strategy_params[1])
        self.trade_manager = std.TradeManager(self)

    def _update_params(self, strategy_params: StrategyParams):
        """Update strategy parameters with provided values."""
        updated_params = []

        # Convert params tuple to a dictionary for easier update
        params_dict = dict(CustomParams.get_params_detail('UFO'))

        # Update the params dictionary with the provided strategy parameters
        for param, value in strategy_params.optional_params.items():
            if param in params_dict:
                params_dict[param] = value
        # Append the updated params to self.params
        for param, value in updated_params:
            setattr(self.params, param, value)
      

    def next(self):
        # Update metrics
        self._update_metrics()
        
        # Detect patterns
        pattern = self.pattern._detect_patterns()
        if pattern:
            self.patterns.append(pattern)
            
            # Get current price and calculate position size
            price = self.data.close[0]
            risk_amount = self.broker.get_cash() * self.p.risk_per_trade
            
            # Calculate position size based on pattern properties
            stop_distance = pattern.properties['risk']
            position_size = risk_amount / stop_distance if stop_distance > 0 else 0
            
            # Execute trades based on pattern type
            if pattern.pattern_type in [cind.PatternType.RBR, cind.PatternType.DBR]:
                if not self.position:  # Only enter if no position exists
                    self.trade_manager.execute_trade('buy', size=position_size)
            elif pattern.pattern_type in [cind.PatternType.RBD, cind.PatternType.DBD]:
                if not self.position:  # Only enter if no position exists
                    self.trade_manager.execute_trade('sell', size=position_size)
            print(f"Pattern detected: {pattern.pattern_type}, Position size: {position_size}, position {self.position}, Time: {self.data.datetime.datetime(0)}")
        
        # Manage existing positions
        if self.position:
            # Calculate stop loss and take profit levels
            if self.position.size > 0:  # Long position
                stop_price = self.position.price * (1 - self.p.stop_loss_atr)
                take_profit = self.position.price * (1 + self.p.take_profit_atr)
            else:  # Short position
                stop_price = self.position.price * (1 + self.p.stop_loss_atr)
                take_profit = self.position.price * (1 - self.p.take_profit_atr)
            
            # Check for exit conditions
            current_price = self.data.close[0]
            if ((self.position.size > 0 and current_price <= stop_price) or
                (self.position.size < 0 and current_price >= stop_price) or
                (self.position.size > 0 and current_price >= take_profit) or
                (self.position.size < 0 and current_price <= take_profit)):
                self.close()

            print(f"Current price: {current_price}, Stop price: {stop_price}, Take profit: {take_profit} psosition size : {self.position.size} time: {self.data.datetime.datetime(0)}")
    
    def _update_metrics(self):
        current_value = self.broker.getvalue()
        daily_pnl = ((current_value - self._last_portfolio_value) / self._last_portfolio_value) if self._last_portfolio_value > 0 else 0
        self._last_portfolio_value = current_value

        # Update metrics dictionary
        self.metrics.update({
            'daily_pnl': daily_pnl,
        })

    def stop(self):
        self.trade_manager.addTradeData(tradedata=self.metrics)
        self.trade_manager.finalize_portfolio()
    

custom_strats = {
    0 : UFOStrategy
}
            
