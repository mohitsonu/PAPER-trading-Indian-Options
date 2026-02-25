# 📊 Trade Journal

This folder contains all your trading records, automatically saved by the GitHub Actions bot.

## 📁 Folder Structure

```
trade_journal/
├── csv/                          # Trade records in CSV format
│   ├── high_accuracy_trades_20260121.csv
│   ├── high_accuracy_trades_20260122.csv
│   └── ...
│
├── json/                         # Trade updates and capital tracking
│   ├── high_accuracy_updates_20260121.json
│   ├── high_accuracy_updates_20260122.json
│   ├── capital_persistence.json
│   └── ...
│
└── logs/                         # Bot execution logs
    ├── auto_trader_scheduler.log
    └── ...
```

## 📋 File Descriptions

### CSV Files (`csv/` folder)
- **Format**: `high_accuracy_trades_YYYYMMDD.csv`
- **Contains**: Complete trade records for each day
- **Columns**: 
  - Trade ID
  - Symbol
  - Entry/Exit prices
  - Quantity
  - P&L
  - Strategy
  - Timestamps
  - And more...

### JSON Files (`json/` folder)
- **Trade Updates**: `high_accuracy_updates_YYYYMMDD.json`
  - Real-time trade updates
  - Position changes
  - Market conditions
  
- **Capital Tracking**: `capital_persistence.json`
  - Current capital
  - Total P&L
  - Session date
  - Performance metrics

### Log Files (`logs/` folder)
- **Scheduler Logs**: `auto_trader_scheduler.log`
  - Bot execution history
  - Market open/close times
  - Errors and warnings
  - System messages

## 📊 How to Use

### View Trade History
1. Go to `trade_journal/csv/` folder
2. Click on any CSV file
3. GitHub will display it as a table

### Download for Analysis
1. Click on any file
2. Click "Download" button
3. Open in Excel, Google Sheets, or Python

### Track Performance
1. Open `capital_persistence.json` to see current capital
2. Compare CSV files across dates to track progress

## 🔄 Auto-Update

Files are automatically saved after each trading session:
- ✅ New files created daily during market hours
- ✅ Committed to repository automatically
- ✅ No manual download needed
- ✅ Permanent storage (never expires)

## 📈 Analysis Tips

### Daily Review
```python
import pandas as pd

# Load today's trades
df = pd.read_csv('trade_journal/csv/high_accuracy_trades_20260121.csv')

# View summary
print(df.describe())
print(f"Total P&L: ₹{df['pnl'].sum():.2f}")
print(f"Win Rate: {(df['pnl'] > 0).mean() * 100:.1f}%")
```

### Monthly Analysis
```python
import pandas as pd
import glob

# Load all January trades
files = glob.glob('trade_journal/csv/high_accuracy_trades_202601*.csv')
df = pd.concat([pd.read_csv(f) for f in files])

# Monthly summary
print(f"Total Trades: {len(df)}")
print(f"Total P&L: ₹{df['pnl'].sum():.2f}")
print(f"Win Rate: {(df['pnl'] > 0).mean() * 100:.1f}%")
```

## 🎯 Quick Stats

To get quick stats, you can use GitHub's built-in CSV viewer:
1. Click on any CSV file
2. GitHub shows it as a table
3. Use browser search (Ctrl+F) to find specific trades

## 📞 Notes

- Files are saved in IST timezone
- Each trading day creates new files
- Old files are never deleted (permanent history)
- You can download entire folder as ZIP anytime
