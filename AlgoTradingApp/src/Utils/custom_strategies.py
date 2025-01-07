import src.Utils.common_indicators as cind
import backtrader as bt
import src.Utils.standard as std 

class UFOStrategy(bt.Strategy):
    params = (
        ('risk_per_trade', 0.01),  # Risk per trade as a fraction of available cash
        ('stop_loss_atr', 2.0),    # ATR multiplier for stop loss
        ('take_profit_atr', 3.0),  # ATR multiplier for take profit
    )

    def __init__(self):
        """Initialize strategy."""
        super(UFOStrategy, self).__init__()
        self.order = None
        self.trades = []
        self.metrics = {}
        self._last_portfolio_value = self.broker.getvalue()
        self.initialized = False
        self.consecutive_losses = 0
        self.patterns = []  # List to store detected patterns
        self.pattern = cind.CombinedPatternIndicator(self.data)
        self.trade_manager = std.TradeManager(self)

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
                    self.trade_manager.execute_trade('buy')
            elif pattern.pattern_type in [cind.PatternType.RBD, cind.PatternType.DBD]:
                if not self.position:  # Only enter if no position exists
                    self.trade_manager.execute_trade('sell')
        
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
    
    def _update_metrics(self):
        current_value = self.broker.getvalue()
        daily_pnl = ((current_value - self._last_portfolio_value) / self._last_portfolio_value) if self._last_portfolio_value > 0 else 0
        self._last_portfolio_value = current_value
            
        # Update metrics dictionary
        self.metrics.update({
            'portfolio_value': current_value,
            'daily_pnl': daily_pnl,
            'total_trades': len(self.trades),
            'winning_trades': len([t for t in self.trades if t['pnl'] > 0]),
            'losing_trades': len([t for t in self.trades if t['pnl'] < 0])
        })

    def stop(self):
        self.trade_manager.finalize_portfolio()
    


            
