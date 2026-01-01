# Binance Futures Order Bot (CLI-Based)
A CLI-based Python trading bot built for Binance USDT-M Futures, supporting basic and advanced order types with robust validation, structured logging, and modular architecture.

This project is developed as part of a Python Developer Internship Assignment and follows industry best practices for safety, reproducibility, and clean design.

---
## 📌 Key Features

### ✅ Core Orders (Mandatory)
- Market Orders
- Limit Orders
### ⭐ Advanced Orders (Bonus)
- Stop-Limit Orders
- OCO (One-Cancels-the-Other) (simulated for Futures)
- TWAP (Time-Weighted Average Price) Strategy
- Grid Trading Strategy
### 🛡 Validation & Reliability
- Symbol, quantity, and price validation
- Market-price range validation
- Minimum notional validation (Binance Futures rule: ≥ 100 USDT)
- Graceful error handling with detailed logs
### 🪵 Logging
- Timestamped, structured logs
- API request success/failure tracking
- Stack traces for debugging

---
## 🗂 Project Structure
```bash
binance-bot/
│
├── src/
│   ├── __init__.py
│   ├── config.py          # Loads API keys from environment
│   ├── client.py          # Binance Futures client wrapper
│   ├── validators.py      # Input validation utilities
│   ├── logger.py          # Centralized logging configuration
│
│   ├── market_orders.py   # Market order logic
│   ├── limit_orders.py    # Limit order logic
│
│   └── advanced/
│       ├── __init__.py
│       ├── stop_limit.py
│       ├── oco.py
│       ├── twap.py
│       └── grid_strategy.py
│
├── bot.log                # Runtime logs (included in ZIP, not GitHub)
├── requirements.txt
├── README.md
├── report.pdf
└── .env                   # Not committed
```
---
## ⚙️ Tech Stack
- Python 3.9+
- python-binance
- python-dotenv
- argparse
- logging
  
## 🔐 Binance API Setup (Testnet)

⚠️ This project uses Binance Futures Testnet to ensure:
- No real funds are used
- No KYC dependency
- Safe and reproducible execution

---
## 1️⃣ Create Testnet API Keys

Visit: https://testnet.binancefuture.com

Login → Profile → API Management

Create a new API key
- Enable: Futures Trading
- Disable: Withdrawals

## 2️⃣ Configure Environment Variables
Create a .env file in the project root:
```bash
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_secret_key
```
⚠️ Never commit .env to GitHub

---
## 🧪 Setup & Installation
### 1️⃣ Clone Repository
```bash
git clone <your-repo-url>
cd binance-bot
```
### 2️⃣ Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---
### ▶️ How to Run the Bot
All commands must be run from the project root using python -m

### 📌 Market Order
```bash
python -m src.market_orders BTCUSDT BUY 0.01
```
---
### 📌 Limit Order
```bash
python -m src.limit_orders BTCUSDT BUY 0.01 42000
```
---
### 📌 Stop-Limit Order
```bash
python -m src.advanced.stop_limit BTCUSDT BUY 0.01 41500 41600
```
---
### 📌 TWAP Strategy

Splits a large order into smaller chunks over time.
```bash
python -m src.advanced.twap BTCUSDT BUY 0.05 5 10
```
➡️ Places 5 market orders at 10-second intervals

---
### 📌 Grid Trading Strategy
Automated buy-low / sell-high within a defined price range.
```bash
python -m src.advanced.grid_strategy BTCUSDT 0.002 82000 86000 4
```

✔ Includes:
- Market price validation
- Minimum notional validation (≥ 100 USDT)

---
### 📌 OCO (Simulated)
Binance Futures does not support native OCO orders.

This implementation:
- Places Take-Profit and Stop-Loss orders
- Cancels the remaining order once one is executed
```bash
python -m src.advanced.oco
```
---
### 🪵 Logging
All activity is logged to bot.log:
- Order placements
- Validation failures
- Exchange-level API errors
- Debug stack traces

Sample Log Output
```bash
2026-01-01 14:18:32 | INFO | TWAP started: 5 orders
2026-01-01 14:19:23 | INFO | TWAP execution completed
2026-01-01 14:23:03 | ERROR | Grid strategy failed | Order notional too small
```
bot.log is intentionally excluded from GitHub and included only in the submission ZIP.

---

## 🧠 Design Decisions
- Testnet-only trading for safety
- Absolute package imports (src.module)
- Validation before API calls to prevent rejections
- Structured logging for real-world debugging

## 🚧 Known Limitations
- OCO is simulated (Futures API limitation)
- Grid strategy is static (no live rebalancing)
- No WebSocket-based price streaming
- No persistent state management

## 🚀 Future Enhancements
- WebSocket market data integration
- Dynamic grid rebalancing
- Position-aware OCO execution
- Risk management & leverage control
- Backtesting using historical datasets

## ✅ Submission Notes
- Uses Binance Futures Testnet
- .env and logs excluded from GitHub
- Logs and screenshots included in report.pdf
- Fully reproducible via README instructions

## ⭐ This project demonstrates:
- Clean Python architecture
- API integration skills
- Error handling & validation
- Understanding of real trading constraints
- Professional development practices