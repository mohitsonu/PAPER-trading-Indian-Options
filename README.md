# 🎯 High Accuracy Options Trading Algorithm

A sophisticated high-accuracy paper trading system for NIFTY options designed for quality trades with ₹20 broker charges consideration.

## 🎪 Key Features

- **Quality Over Quantity**: 1-10 high-accuracy trades per day
- **Strict Entry Criteria**: Minimum 85/100 accuracy score
- **Broker Charges Integration**: ₹20 per trade factored into P&L
- **Live Option Chain Display**: Real-time data for all strikes
- **Enhanced Risk Management**: 2.67:1 risk-reward ratio
- **Advanced Market Analysis**: Trend confirmation and structure analysis

## 📊 Strike Coverage

Monitors all strikes: [25400, 25450, 25500, 25550, 25600, 25650, 25700, 25750, 25800, 25850, 25900, 25950, 26000]

## 🚀 Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Setup credentials in `.env` file:**
```
SHOONYA_USER_ID=your_user_id
SHOONYA_PASSWORD=your_password
SHOONYA_TOTP_KEY=your_totp_key
SHOONYA_VENDOR_CODE=your_vendor_code
SHOONYA_API_SECRET=your_api_secret
```

3. **Run high accuracy trading:**
```bash
python run_high_accuracy.py
```

4. **View live option chain (separate window):**
```bash
python show_option_chain.py
```

5. **View results:**
```bash
python view_high_accuracy_results.py
```

## 📁 Project Files

### Core Files
- `high_accuracy_algo.py` - Main high accuracy trading algorithm
- `run_high_accuracy.py` - Easy runner script
- `show_option_chain.py` - Live option chain viewer
- `view_high_accuracy_results.py` - Results analysis

### Configuration
- `high_accuracy_config.json` - Algorithm parameters
- `.env` - API credentials (create from .env.example)

### Generated Files
- `high_accuracy_trades_YYYYMMDD.csv` - Trade journal
- `high_accuracy_updates_YYYYMMDD.json` - Real-time updates

## ⚙️ Algorithm Settings

### Entry Criteria
- **Minimum Premium**: ₹30 (covers broker charges)
- **Minimum OI**: 5 lakh (liquidity)
- **Minimum Volume**: 1000
- **Maximum Spread**: ₹5
- **Accuracy Score**: 85/100 minimum

### Risk Management
- **Stop Loss**: 30%
- **Target**: 80% (2.67:1 R:R)
- **Max Holding**: 4 hours
- **Max Positions**: 2
- **Risk per Trade**: 3%

### Market Analysis
- **Trend Confirmation**: 10 periods
- **Market Confidence**: 70% minimum
- **Update Frequency**: 2 minutes
- **Opportunity Check**: Every 15 minutes

## 📊 Display Features

### Option Chain Shows
- Real-time LTP, Volume, OI
- Bid/Ask prices and spreads
- Accuracy scores (0-100)
- Trading signals
- Market sentiment (PCR ratios)

### Trading Signals
- 🟢 **CE HIGH** - High accuracy call opportunity
- 🔴 **PE HIGH** - High accuracy put opportunity
- 🎯 **ATM WATCH** - At-the-money monitoring
- 📈 **CE HEAVY** - Call heavy OI
- 📉 **PE HEAVY** - Put heavy OI

## 🎯 Quality Metrics

- **Target Win Rate**: 70%+
- **Profit Factor**: 2.0+
- **Average Score**: 85+/100
- **Max Trades/Day**: 10
- **Focus**: High probability setups only

## 💡 Usage Tips

1. **Monitor Option Chain**: Run `show_option_chain.py` in separate terminal
2. **Quality Focus**: Algorithm waits for 85+ score opportunities
3. **Broker Charges**: All P&L calculations include ₹20 charges
4. **Patience Required**: May have periods with no trades (by design)
5. **Results Analysis**: Use `view_high_accuracy_results.py` for detailed metrics