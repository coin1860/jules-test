import time
import logging
from .market_data import MarketDataProvider
from .account import AccountManager
from .strategy import StrategyModule

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TradingEngine:
    def __init__(self,
                 market_data: MarketDataProvider,
                 account: AccountManager,
                 strategy: StrategyModule,
                 symbol: str = "CNY=X",
                 trade_amount_usd: float = 100.0):
        self.market_data = market_data
        self.account = account
        self.strategy = strategy
        self.symbol = symbol
        self.trade_amount_usd = trade_amount_usd
        self.is_running = False

    def run_step(self):
        try:
            current_price = self.market_data.get_current_price(self.symbol)
            logger.info(f"Current Price for {self.symbol}: {current_price}")

            signal = self.strategy.on_tick(current_price)
            logger.info(f"Signal: {signal}")

            if signal == "BUY":
                # Buy USD (Sell CNY)
                try:
                    self.account.buy_usd(self.trade_amount_usd, current_price)
                    logger.info(f"EXECUTED BUY: {self.trade_amount_usd} USD @ {current_price}")
                except ValueError as e:
                    logger.error(f"Failed to BUY: {e}")

            elif signal == "SELL":
                # Sell USD (Buy CNY)
                try:
                    self.account.sell_usd(self.trade_amount_usd, current_price)
                    logger.info(f"EXECUTED SELL: {self.trade_amount_usd} USD @ {current_price}")
                except ValueError as e:
                    logger.error(f"Failed to SELL: {e}")

            equity = self.account.get_equity_cny(current_price)
            logger.info(f"Total Equity (CNY): {equity:.2f}")

        except Exception as e:
            logger.error(f"Error in run_step: {e}")

    def run(self, interval: int = 60):
        self.is_running = True
        logger.info("Starting Trading Engine...")
        try:
            while self.is_running:
                self.run_step()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Stopping Trading Engine...")
            self.is_running = False
