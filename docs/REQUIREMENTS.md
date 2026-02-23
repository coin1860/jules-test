# Product Requirements Document (PRD)

## 1. Introduction
This document outlines the product requirements for the **USD/CNY Quantitative Trading Proof of Concept (POC)**. The goal of this POC is to validate the feasibility of a Python-based trading system that monitors the USD/CNY exchange rate, executes automated trades based on a Simple Moving Average (SMA) crossover strategy, and tracks portfolio performance in a simulated "Paper Trading" environment.

---

## 2. Functional Requirements

### 2.1 Market Data Ingestion
**FR-01: Real-Time Price Monitoring**
- The system MUST fetch the current USD/CNY exchange rate from a public data provider (e.g., Yahoo Finance).
- The default symbol is `CNY=X`.
- The fetch interval MUST be configurable (default: 60 seconds).

**FR-02: Data Handling**
- The system MUST handle invalid or missing data points gracefully.
- The system MUST store historical price data in memory (or a lightweight database) to calculate technical indicators.

### 2.2 Trading Strategy
**FR-03: Simple Moving Average (SMA) Crossover**
- The system MUST implement an SMA Crossover strategy.
- Inputs:
    - `short_window` (default: 5 periods)
    - `long_window` (default: 20 periods)
- Logic:
    - **BUY Signal:** When Short SMA crosses ABOVE Long SMA.
    - **SELL Signal:** When Short SMA crosses BELOW Long SMA.
    - **HOLD Signal:** Otherwise.

**FR-04: Strategy Configuration**
- Strategy parameters (windows) MUST be configurable via command-line arguments.
- The system MUST validate that `short_window < long_window`.

### 2.3 Order Execution (Paper Trading)
**FR-05: Simulated Execution**
- The system MUST simulate trade execution without connecting to a real broker.
- Trades MUST be executed at the last known price.
- **BUY Logic:** Decrease CNY balance, Increase USD balance.
- **SELL Logic:** Decrease USD balance, Increase CNY balance.

**FR-06: Balance Validation**
- The system MUST validate sufficient funds before executing a trade.
- If funds are insufficient, the trade MUST be rejected and logged.

### 2.4 Portfolio Management
**FR-07: Balance Tracking**
- The system MUST maintain separate balances for USD and CNY.
- The initial balances MUST be configurable via command-line arguments (default: 10,000 CNY, 1,000 USD).

**FR-08: Equity Calculation**
- The system MUST calculate the Total Equity in CNY at each step.
- Formula: `Total Equity (CNY) = Balance_CNY + (Balance_USD * Current_Price_CNY_per_USD)`.

### 2.5 Reporting & Logging
**FR-09: Activity Logging**
- The system MUST log all major events (Price Update, Signal Generation, Trade Execution, Error) to:
    - Console (Standard Output)
    - File (`trading.log`)
- Log format MUST include timestamp, log level, and message.

---

## 3. Non-Functional Requirements

### 3.1 Performance
**NFR-01: Latency**
- The system SHOULD process a market tick and generate a signal within 100ms (excluding network latency).

### 3.2 Reliability
**NFR-02: Error Handling**
- The system MUST NOT crash due to transient network errors (e.g., API timeout).
- The system MUST retry failed data fetches with exponential backoff (if applicable) or skip the tick.

### 3.3 Quality Assurance
**NFR-03: Test Coverage**
- The codebase MUST maintain **100% unit test coverage** for all core logic modules (`src/`).
- The system MUST follow Test-Driven Development (TDD) principles.

### 3.4 Usability
**NFR-04: Command Line Interface (CLI)**
- The system MUST provide a user-friendly CLI with help documentation (`--help`).
- Arguments SHOULD include: Symbol, Initial Capital, Interval.

---

## 4. Technical Constraints
- **Language:** Python 3.9+
- **Data Provider:** `yfinance` library.
- **Testing Framework:** `pytest`, `pytest-cov`.
- **Operating System:** Cross-platform (Linux/macOS/Windows).

---

## 5. Future Scope (Out of Scope for POC)
- Persistent database (SQL/NoSQL) for trade history.
- Real broker API integration.
- Advanced strategy optimization (backtesting engine).
- Web-based Dashboard/UI.
