import csv
import os
from datetime import datetime


class TradeLogger:    
    def __init__(self, log_file="result/alpaca_trades.csv"):
        self.log_file = log_file
        self._initialize_log()
    
    def _initialize_log(self):
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Create file with headers if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'symbol', 'side', 'qty', 'price', 
                    'strategy', 'order_id', 'status', 'error'
                ])
    
    def log_trade(self, symbol, side, qty, price, strategy_name, 
                  order_id=None, status='submitted', error=None):
        """
        Log a trade to CSV file
        
        Args:
            symbol: Trading symbol (e.g., 'BTC/USD')
            side: Order side ('BUY' or 'SELL')
            qty: Order quantity
            price: Order price
            strategy_name: Name of strategy generating the signal
            order_id: Alpaca order ID (if successful)
            status: Order status ('submitted', 'failed', etc.)
            error: Error message (if failed)
        """
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                symbol,
                side,
                qty,
                price,
                strategy_name,
                order_id,
                status,
                error
            ])
    
    def log_success(self, symbol, side, qty, price, strategy_name, order_response):
        """Log a successful order submission"""
        order_id = order_response.id if hasattr(order_response, 'id') else None
        self.log_trade(
            symbol=symbol,
            side=side,
            qty=qty,
            price=price,
            strategy_name=strategy_name,
            order_id=order_id,
            status='submitted'
        )
    
    def log_failure(self, symbol, side, qty, price, strategy_name, error):
        """Log a failed order submission"""
        self.log_trade(
            symbol=symbol,
            side=side,
            qty=qty,
            price=price,
            strategy_name=strategy_name,
            status='failed',
            error=str(error)
        )
