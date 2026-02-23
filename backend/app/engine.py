import time
import logging
import threading
from typing import Dict, Any, Optional

from .market_data import MarketDataProvider
from .account import AccountManager
from .strategy import StrategyModule

logger = logging.getLogger(__name__)

class TradingEngine:
    def __init__(self,
                 market_data: MarketDataProvider,
                 account: AccountManager,
                 strategy: StrategyModule,
                 symbol: str = "CNY=X",
                 trade_amount_usd: float = 100.0,
                 interval: int = 5): # Default faster interval for testing/demo
        self.market_data = market_data
        self.account = account
        self.strategy = strategy
        self.symbol = symbol
        self.trade_amount_usd = trade_amount_usd
        self.interval = interval

        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

        # State for API
        self.last_price = 0.0
        self.last_signal = "HOLD"
        self.is_running = False

    def start(self):
        with self._lock:
            if self.is_running:
                logger.warning("Engine already running")
                return

            self._stop_event.clear()
            self.is_running = True
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()
            logger.info("Trading Engine Started")

    def stop(self):
        with self._lock:
            if not self.is_running:
                return

            self._stop_event.set()
            # Wait for thread, but do not block forever
            if self._thread and self._thread.is_alive():
                 # No join here to keep API responsive, thread will exit soon
                 pass

            self.is_running = False
            logger.info("Trading Engine Stopping...")

    def update_strategy_parameters(self, short_window: int, long_window: int):
        with self._lock:
            logger.info(f"Updating strategy parameters: short={short_window}, long={long_window}")
            self.strategy.update_parameters(short_window, long_window)

    def _run_loop(self):
        logger.info(f"Engine Loop Started for {self.symbol}")
        while not self._stop_event.is_set():
            try:
                self._run_step()
            except Exception as e:
                logger.error(f"Error in trading loop: {e}")

            # Sleep with check for stop event
            if self._stop_event.wait(self.interval):
                break

        logger.info("Engine Loop Exited")

    def _run_step(self):
        # Fetch Price
        try:
            current_price = self.market_data.get_current_price(self.symbol)
            with self._lock:
                self.last_price = current_price
        except Exception as e:
            logger.error(f"Failed to fetch price: {e}")
            return

        # Strategy Signal
        with self._lock:
            try:
                signal = self.strategy.on_tick(current_price)
                self.last_signal = signal
            except Exception as e:
                logger.error(f"Strategy Error: {e}")
                return

        logger.info(f"Price: {current_price}, Signal: {signal}")

        # Execute Trade
        # Note: AccountManager is thread-safe now
        if signal == "BUY":
            try:
                self.account.buy_usd(self.trade_amount_usd, current_price)
                logger.info(f"EXECUTED BUY: {self.trade_amount_usd} USD @ {current_price}")
            except ValueError as e:
                logger.error(f"Failed to BUY: {e}")

        elif signal == "SELL":
            try:
                self.account.sell_usd(self.trade_amount_usd, current_price)
                logger.info(f"EXECUTED SELL: {self.trade_amount_usd} USD @ {current_price}")
            except ValueError as e:
                logger.error(f"Failed to SELL: {e}")

    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            equity = 0.0
            # Calculate equity if we have a price
            if self.last_price > 0:
                try:
                    equity = self.account.get_equity_cny(self.last_price)
                except:
                    pass
            elif self.account.balance_usd == 0:
                 equity = self.account.balance_cny

            return {
                "running": self.is_running,
                "symbol": self.symbol,
                "price": self.last_price,
                "signal": self.last_signal,
                "equity_cny": equity,
                "balances": {
                    "cny": self.account.balance_cny,
                    "usd": self.account.balance_usd
                },
                "strategy": {
                    "short_window": self.strategy.short_window,
                    "long_window": self.strategy.long_window
                }
            }
