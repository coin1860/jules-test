# Implementation Plan

## Phase 1: Project Setup & Infrastructure
- [ ] Initialize Python environment and `requirements.txt`.
- [ ] Configure `pytest` and `pytest-cov` for coverage reporting.
- [ ] Create basic project structure (`src/`, `tests/`).

## Phase 2: Core Components Implementation (TDD)
- [ ] **Market Data Provider:**
    - [ ] Create `MarketDataProvider` interface.
    - [ ] Implement `MockProvider` for testing.
    - [ ] Implement `YFinanceProvider` for real data (USD/CNY).
    - [ ] Write unit tests for data fetching and error handling.
- [ ] **Account Manager:**
    - [ ] Create `AccountManager` class.
    - [ ] Implement `deposit`, `withdraw`, `buy_usd`, `sell_usd`.
    - [ ] Implement `get_equity_cny`.
    - [ ] Write unit tests for balance updates and invalid operations.
- [ ] **Strategy Engine:**
    - [ ] Create `StrategyModule` class (SMA Crossover).
    - [ ] Implement signal generation logic (`on_tick`).
    - [ ] Write unit tests with known price sequences to verify signals.

## Phase 3: Integration & Execution
- [ ] **Trading Engine:**
    - [ ] Create `TradingEngine` class to orchestrate Data -> Strategy -> Account.
    - [ ] Implement the main loop with configurable intervals.
    - [ ] Write integration tests simulating a full trading session.

## Phase 4: Finalization
- [ ] Verify 100% test coverage using `pytest --cov`.
- [ ] Add basic logging/reporting to console.
- [ ] Final code review and cleanup.
