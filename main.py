import logging
import argparse
from src.market_data import YFinanceProvider
from src.account import AccountManager
from src.strategy import StrategyModule
from src.engine import TradingEngine

def main():
    parser = argparse.ArgumentParser(description="Simple Quant POC")
    parser.add_argument("--symbol", type=str, default="CNY=X", help="Trading Symbol")
    parser.add_argument("--cny", type=float, default=10000.0, help="Initial CNY Balance")
    parser.add_argument("--usd", type=float, default=1000.0, help="Initial USD Balance")
    parser.add_argument("--interval", type=int, default=60, help="Trading Interval (seconds)")
    args = parser.parse_args()

    # Setup Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("trading.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger("Main")

    logger.info("Initializing Components...")

    market_data = YFinanceProvider()
    account = AccountManager(initial_cny=args.cny, initial_usd=args.usd)
    strategy = StrategyModule(short_window=5, long_window=20)

    engine = TradingEngine(
        market_data=market_data,
        account=account,
        strategy=strategy,
        symbol=args.symbol
    )

    logger.info(f"Starting Engine for {args.symbol} with Interval {args.interval}s")
    engine.run(interval=args.interval)

if __name__ == "__main__":
    main()
