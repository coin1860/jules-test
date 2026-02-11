from typing import List, Dict, Any
from datetime import datetime

class AccountManager:
    def __init__(self, initial_cny: float = 0.0, initial_usd: float = 0.0):
        self.balance_cny = initial_cny
        self.balance_usd = initial_usd
        self.transactions: List[Dict[str, Any]] = []

    def deposit(self, amount: float, currency: str):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        if currency == "CNY":
            self.balance_cny += amount
        elif currency == "USD":
            self.balance_usd += amount
        else:
            raise ValueError(f"Unsupported currency: {currency}")

        self._log_transaction("DEPOSIT", currency, amount, 0.0)

    def withdraw(self, amount: float, currency: str):
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")

        if currency == "CNY":
            if self.balance_cny < amount:
                raise ValueError("Insufficient CNY balance")
            self.balance_cny -= amount
        elif currency == "USD":
            if self.balance_usd < amount:
                raise ValueError("Insufficient USD balance")
            self.balance_usd -= amount
        else:
            raise ValueError(f"Unsupported currency: {currency}")

        self._log_transaction("WITHDRAW", currency, amount, 0.0)

    def buy_usd(self, amount_usd: float, price_cny_per_usd: float):
        """Buys USD using CNY."""
        if amount_usd <= 0 or price_cny_per_usd <= 0:
            raise ValueError("Amount and price must be positive")

        cost_cny = amount_usd * price_cny_per_usd
        if self.balance_cny < cost_cny:
            raise ValueError("Insufficient CNY balance to buy USD")

        self.balance_cny -= cost_cny
        self.balance_usd += amount_usd
        self._log_transaction("BUY_USD", "USD", amount_usd, price_cny_per_usd)

    def sell_usd(self, amount_usd: float, price_cny_per_usd: float):
        """Sells USD for CNY."""
        if amount_usd <= 0 or price_cny_per_usd <= 0:
            raise ValueError("Amount and price must be positive")

        if self.balance_usd < amount_usd:
            raise ValueError("Insufficient USD balance to sell")

        revenue_cny = amount_usd * price_cny_per_usd
        self.balance_usd -= amount_usd
        self.balance_cny += revenue_cny
        self._log_transaction("SELL_USD", "USD", amount_usd, price_cny_per_usd)

    def get_equity_cny(self, current_price_cny_per_usd: float) -> float:
        if current_price_cny_per_usd < 0:
             raise ValueError("Price must be non-negative")
        return self.balance_cny + (self.balance_usd * current_price_cny_per_usd)

    def _log_transaction(self, action: str, currency: str, amount: float, price: float):
        self.transactions.append({
            "timestamp": datetime.now(),
            "action": action,
            "currency": currency,
            "amount": amount,
            "price": price,
            "balance_cny": self.balance_cny,
            "balance_usd": self.balance_usd
        })
