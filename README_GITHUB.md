# 🎯 High Accuracy Options Trading Algorithm

An intelligent options trading algorithm for NIFTY index options, designed for high-accuracy trades with strict risk management.

## 📊 Features

### Core Strategies
- **CONTRARIAN Strategy**: Counter-trend trading with high win rate (66.7%+)
- **TREND_RIDER Strategy**: Trend-following for strong market moves
- **Adaptive Market Engine**: Auto-detects market conditions (TRENDING/RANGING/CHOPPY/VOLATILE)

### Risk Management
- Smart trailing stops with dynamic profit protection
- Position sizing based on capital and risk tolerance
- Maximum trades per day limit (8 trades)
- Strike diversity filter (max 2 trades per strike)

### Technical Analysis
- Multi-timeframe analysis (1min, 5min, 15min)
- Price action trend detection
- Candlestick pattern recognition
- EMA trend confirmation
- RSI momentum analysis
- Market condition filtering

### Advanced Features
- Priority features (OI analysis, Stochastic, Greeks)
- Smart premium selection based on market level
- Trend direction filter (prevents counter-trend trades)
- Real-time position monitoring
- Telegram notifications (optional)

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip install -r requirements.txt
```

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd <repo-name>
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file with your credentials:
```env
SHOONYA_USER_ID=your_user_id
SHOONYA_PASSWORD=your_password
SHOONYA_TOTP_KEY=your_totp_key
SHOONYA_VENDOR_CODE=your_vendor_code
SHOONYA_API_SECRET=your_api_secret

# Optional: Telegram notifications
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
TELEGRAM_ENABLED=True
```

5. **Update expiry date**
Edit `expiry_config.json`:
```json
{
  "current_expiry": "02DEC25"
}
```

6. **Run the algorithm**
```bash
python run_high_accuracy.py
```

## 📁 Project Structure

```
├── high_accuracy_algo.py          # Main algorithm
├── run_high_accuracy.py           # Entry point
├── priority_features.py           # Market condition, OI, Stochastic, Greeks
├── adaptive_market_engine.py      # Smart market mode detection
├── trailing_stop_manager.py       # Dynamic profit protection
├── trade_state_persistence.py     # Position recovery on restart
├── brokerage_calculator.py        # Realistic cost calculation
├── expiry_config.json             # Easy expiry date management
├── .env.example                   # Environment variables template
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## ⚙️ Configuration

### Expiry Date
Update `expiry_config.json`:
```json
{
  "current_expiry": "02DEC25",
  "next_expiry": "05DEC25"
}
```

### Trading Parameters
Edit `high_accuracy_algo.py`:
```python
self.initial_capital = 100000      # Starting capital
self.max_positions = 3             # Max concurrent positions
self.stop_loss_pct = 0.25          # 25% stop loss
self.target_profit_pct = 0.50      # 50% target
self.min_accuracy_score = 90       # Min score for CURRENT strategy
```

### Strategy Selection
The algorithm runs both strategies by default:
- **CURRENT**: Complex scoring (12 components)
- **SIMPLIFIED**: Price action focused (6 components)

Results are saved to separate CSV files for comparison.

## 📊 Performance Metrics

### Recent Results (Nov 27, 2025)
- **Win Rate**: 83.3% (5W / 1L)
- **P&L**: +₹1,332 (+1.37%)
- **Trades**: 6 trades
- **Strategy**: CONTRARIAN + TREND_RIDER

### Key Improvements
- SCALPER strategy disabled (was 31% WR, -₹23,201)
- Max trades enforced (8 per day)
- Market condition filter (sits out choppy markets)
- Strike diversity (max 2 per strike)

## 🛡️ Risk Management

### Position Sizing
- Risk per trade: 3% of capital
- Max positions: 3 concurrent
- Dynamic lot sizing: 150-300 lots based on market mode

### Stop Loss & Targets
- Stop Loss: 25% of entry price
- Target: 50% of entry price (2:1 R:R)
- Trailing stops: Lock profits at 5%, 10%, 20%+ levels

### Filters
1. **Trend Direction**: Blocks counter-trend trades
2. **Market Condition**: Sits out CHOPPY/VOLATILE markets
3. **Strike Diversity**: Max 2 trades per strike
4. **Max Trades**: 8 trades per day limit
5. **Time Filter**: No trading before 9:30 AM or after 2:30 PM

## 📈 Strategies

### CONTRARIAN (Primary)
- Counter-trend trading
- Works best in ranging/reversal markets
- Win Rate: 66.7%+
- Holding time: 20-80 minutes

### TREND_RIDER
- Trend-following strategy
- Works best in strong trending markets
- Win Rate: 100% (limited data)
- Holding time: 60-120 minutes

### SCALPER (Disabled)
- Quick scalping strategy
- **Disabled due to poor performance** (31% WR, -₹23,201 loss)

## 🔧 Troubleshooting

### Common Issues

**1. Login Failed**
- Check credentials in `.env` file
- Verify TOTP key is correct
- Ensure API secret is valid

**2. No Trades Taken**
- Check market condition (might be CHOPPY)
- Verify expiry date in `expiry_config.json`
- Check if max trades limit reached

**3. Position Not Exiting**
- Check stop loss and target levels
- Verify trailing stop is working
- Check market data feed

## 📝 Output Files

### Trade Logs
- `current_trades_YYYYMMDD.csv` - CURRENT strategy trades
- `simplified_trades_YYYYMMDD.csv` - SIMPLIFIED strategy trades
- `daily_capital_tracking.csv` - Daily P&L summary

### State Files
- `capital_persistence.json` - Capital tracking
- `trade_state_YYYYMMDD.json` - Position recovery data

## 🤝 Contributing

This is a personal trading algorithm. Feel free to fork and modify for your own use.

## ⚠️ Disclaimer

**This software is for educational purposes only.**

- Trading involves substantial risk of loss
- Past performance does not guarantee future results
- Use at your own risk
- Always test with paper trading first
- Never risk more than you can afford to lose

## 📄 License

MIT License - See LICENSE file for details

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Happy Trading! 🚀**
