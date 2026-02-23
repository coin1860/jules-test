# User Stories

## Overview
This document outlines the user stories for the USD/CNY Quantitative Trading Proof of Concept (POC). The primary users are the **Trader**, the **Quant**, and the **System Administrator**.

---

## 1. Trader Persona
*As a Trader, I want to execute trades based on reliable data and strategies so that I can profit from USD/CNY price movements.*

### US-01: Real-Time Market Data Monitoring
**As a** Trader,
**I want** to see the current USD/CNY exchange rate in real-time,
**So that** I can make informed decisions or verify the automated system's actions.

**Acceptance Criteria:**
- The system fetches the latest `CNY=X` price from Yahoo Finance.
- The price is displayed in the logs or console output.
- The timestamp of the price update is visible.

### US-02: Automated Trade Execution (Paper Trading)
**As a** Trader,
**I want** the system to automatically execute "Buy" and "Sell" orders when a strategy signal is generated,
**So that** I don't miss trading opportunities due to latency or absence.

**Acceptance Criteria:**
- When a "BUY" signal is generated, the system simulates buying USD with available CNY.
- When a "SELL" signal is generated, the system simulates selling USD for CNY.
- Trades are rejected if there is insufficient balance.
- All trade executions are logged with Price, Quantity, and Timestamp.

### US-03: Portfolio Balance Tracking
**As a** Trader,
**I want** to view my current holdings in both USD and CNY, as well as my total equity in CNY,
**So that** I can track my profit and loss (P&L).

**Acceptance Criteria:**
- The system maintains a ledger of USD and CNY balances.
- After every trade, the balances are updated correctly.
- Total Equity is calculated as `Balance_CNY + (Balance_USD * Current_Price)`.
- The equity value is logged after each trade or market tick.

---

## 2. Quant Persona
*As a Quant, I want to design and test trading strategies so that I can identify profitable algorithms.*

### US-04: Strategy Definition (SMA Crossover)
**As a** Quant,
**I want** to define a Simple Moving Average (SMA) Crossover strategy with configurable windows,
**So that** I can capture trend-following opportunities.

**Acceptance Criteria:**
- The strategy accepts `short_window` and `long_window` parameters.
- A "BUY" signal is generated when the Short SMA crosses above the Long SMA (Golden Cross).
- A "SELL" signal is generated when the Short SMA crosses below the Long SMA (Death Cross).
- A "HOLD" signal is returned otherwise.

### US-05: Strategy Configuration
**As a** Quant,
**I want** to easily adjust strategy parameters (e.g., window sizes) without changing the code,
**So that** I can optimize the strategy for different market conditions.

**Acceptance Criteria:**
- Parameters can be passed via command-line arguments or a configuration file.
- The system validates that `short_window < long_window`.

---

## 3. System Administrator Persona
*As a System Admin, I want to ensure the system is robust, secure, and auditable.*

### US-06: Robust Error Handling
**As a** System Admin,
**I want** the system to handle network errors (e.g., Yahoo Finance API downtime) gracefully,
**So that** the application doesn't crash unexpectedly.

**Acceptance Criteria:**
- If the data provider fails, the system retries or logs an error without crashing.
- Critical errors are logged with stack traces for debugging.

### US-07: Comprehensive Logging
**As a** System Admin,
**I want** detailed logs of all system activities (Tick, Signal, Trade, Error),
**So that** I can audit the system's behavior and diagnose issues.

**Acceptance Criteria:**
- Logs include timestamps, log levels (INFO, ERROR), and message details.
- Logs are written to both the console and a file (e.g., `trading.log`).

### US-08: Code Quality & Reliability
**As a** Developer/Admin,
**I want** the codebase to have 100% test coverage,
**So that** I can be confident that changes won't introduce regressions.

**Acceptance Criteria:**
- `pytest` suite passes all tests.
- `pytest-cov` report shows 100% coverage for core modules (`src/`).
