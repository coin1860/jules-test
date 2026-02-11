import pytest
from src.account import AccountManager

@pytest.fixture
def account():
    return AccountManager(initial_cny=10000.0, initial_usd=1000.0)

def test_initial_balance(account):
    assert account.balance_cny == 10000.0
    assert account.balance_usd == 1000.0

def test_deposit_cny(account):
    account.deposit(5000.0, "CNY")
    assert account.balance_cny == 15000.0

def test_deposit_usd(account):
    account.deposit(500.0, "USD")
    assert account.balance_usd == 1500.0

def test_deposit_invalid_currency(account):
    with pytest.raises(ValueError):
        account.deposit(100.0, "EUR")

def test_deposit_invalid_amount(account):
    with pytest.raises(ValueError):
        account.deposit(-100.0, "CNY")

def test_withdraw_cny(account):
    account.withdraw(5000.0, "CNY")
    assert account.balance_cny == 5000.0

def test_withdraw_usd(account):
    account.withdraw(500.0, "USD")
    assert account.balance_usd == 500.0

def test_withdraw_insufficient_cny(account):
    with pytest.raises(ValueError):
        account.withdraw(20000.0, "CNY")

def test_withdraw_insufficient_usd(account):
    with pytest.raises(ValueError):
        account.withdraw(2000.0, "USD")

def test_withdraw_invalid_currency(account):
    with pytest.raises(ValueError):
        account.withdraw(100.0, "EUR")

def test_withdraw_invalid_amount(account):
    with pytest.raises(ValueError):
        account.withdraw(-100.0, "CNY")

def test_buy_usd_success(account):
    # Buy 100 USD at 7.0 CNY/USD
    account.buy_usd(100.0, 7.0)
    assert account.balance_usd == 1100.0
    assert account.balance_cny == 10000.0 - 700.0

def test_buy_usd_insufficient_cny(account):
    with pytest.raises(ValueError):
        account.buy_usd(2000.0, 7.0) # Costs 14000 CNY, only have 10000

def test_buy_usd_invalid_args(account):
    with pytest.raises(ValueError):
        account.buy_usd(-100.0, 7.0)
    with pytest.raises(ValueError):
        account.buy_usd(100.0, -7.0)

def test_sell_usd_success(account):
    # Sell 100 USD at 7.0 CNY/USD
    account.sell_usd(100.0, 7.0)
    assert account.balance_usd == 900.0
    assert account.balance_cny == 10000.0 + 700.0

def test_sell_usd_insufficient_usd(account):
    with pytest.raises(ValueError):
        account.sell_usd(2000.0, 7.0) # Have 1000

def test_sell_usd_invalid_args(account):
    with pytest.raises(ValueError):
        account.sell_usd(-100.0, 7.0)
    with pytest.raises(ValueError):
        account.sell_usd(100.0, -7.0)

def test_get_equity_cny(account):
    # 10000 CNY + 1000 USD * 7.0 = 17000 CNY
    equity = account.get_equity_cny(7.0)
    assert equity == 17000.0

def test_get_equity_invalid_price(account):
    with pytest.raises(ValueError):
        account.get_equity_cny(-1.0)
