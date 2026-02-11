# Requirements Specification (POC)

## 1. Overview
A minimal quantitative trading Proof of Concept (POC) designed for a user with USD and CNY accounts in Mainland China.
The system will monitor the USD/CNY exchange rate, generate trading signals based on a simple trend-following strategy, and simulate the execution to track potential profit/loss.

## 2. Constraints & Assumptions
*   **Market:** USD/CNY (Onshore/Offshore proxy).
*   **Execution:** Due to regulatory restrictions on retail API access for Chinese bank accounts, the POC will operate in **Paper Trading Mode** (Simulation). It will generate signals that the user can manually execute or log for analysis.
*   **Capital:** The system will track a virtual portfolio starting with a user-defined amount of CNY and USD.
*   **Compliance:** The system does not interface with real banking APIs (to avoid security/legal risks in this POC phase).

## 3. User Stories
*   **US-01:** As a user, I want to see the current USD/CNY exchange rate so I can know the market status.
*   **US-02:** As a user, I want the system to automatically generate "Buy USD" or "Sell USD" signals based on a Moving Average Crossover strategy.
*   **US-03:** As a user, I want the system to track my virtual portfolio value (CNY + USD converted to CNY) over time.
*   **US-04:** As a user, I want to ensure the code is robust, with 100% test coverage.

## 4. Functional Requirements
*   **FR-01 Data Ingestion:** Fetch USD/CNY exchange rate every X minutes (default: 1 min).
    *   *Source:* Yahoo Finance (`CNY=X`) or similar free public API.
*   **FR-02 Strategy Engine:** Implement a Simple Moving Average (SMA) Crossover strategy.
    *   *Parameters:* Short Window (e.g., 5 periods), Long Window (e.g., 20 periods).
    *   *Logic:*
        *   If Short SMA > Long SMA AND previous Short SMA <= previous Long SMA -> **BUY USD** (Sell CNY).
        *   If Short SMA < Long SMA AND previous Short SMA >= previous Long SMA -> **SELL USD** (Buy CNY).
*   **FR-03 Account Management:** Maintain a local ledger of holdings.
    *   Support `deposit`, `withdraw`, `trade` operations.
    *   Calculate total equity in CNY.
*   **FR-04 Reporting:** Log all actions (Signal, Trade, Balance Update) to a file/console.

## 5. Non-Functional Requirements
*   **NFR-01 Reliability:** The system must handle network failures gracefully (retry logic).
*   **NFR-02 Quality:** 100% Unit Test Coverage required.
*   **NFR-03 Extensibility:** Modular design to swap Data Source or Strategy later.
