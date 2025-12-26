# 🎯 High Accuracy Trading Algorithm - Final Setup

## ✅ SIMPLIFIED Integration Complete!

The SIMPLIFIED strategy is now fully integrated into the main algorithm. You can choose which strategy to run at startup.

---

## 🚀 How to Run

### Method 1: Python (Recommended)
```cmd
python run_high_accuracy.py
```

You'll be prompted to choose:
1. **CURRENT** (Complex, Min Score 90)
2. **SIMPLIFIED** (Price Action, Min Score 70)

### Method 2: Batch File
Double-click: **`run_high_accuracy_unbuffered.bat`**

---

## 📊 Strategy Comparison

### CURRENT Strategy (Option 1)
- **Scoring:** 12 indicators, 260 points
- **Min Score:** 90/100
- **Approach:** Complex multi-indicator analysis
- **Trades:** Fewer, higher quality
- **Best For:** Conservative trading, high accuracy

### SIMPLIFIED Strategy (Option 2)
- **Scoring:** 6 components, 100 points
- **Min Score:** 70/100
- **Approach:** Price action focused
- **Trades:** More frequent
- **Best For:** Aggressive trading, more opportunities

---

## 📁 Output Files

Both strategies use the same file format:
- `high_accuracy_trades_YYYYMMDD.csv` - Trade log
- `high_accuracy_updates_YYYYMMDD.json` - Session data
- `capital_persistence.json` - Capital tracking
- `trading_report.html` - Visual report

---

## 🔧 Configuration

### Update Expiry
Edit `expiry_config.json`:
```json
{
  "current_expiry": "09DEC25"
}
```

### Check Expiry
```cmd
python check_expiry.py
```

---

## 📈 Features (Both Strategies)

✅ **Adaptive Market Engine**
- Auto-detects market conditions (TRENDING/RANGING/CHOPPY)
- Adjusts strategy based on market mode

✅ **Smart Trailing Stops**
- Dynamic trailing based on profit level
- Breakeven protection at 5% profit
- Profit lock-in at 10%, 20%, 30%+

✅ **Priority Features**
- Market condition filter
- OI change analysis
- Stochastic oscillator
- Greeks analysis

✅ **Position Recovery**
- Saves position state
- Restores on restart
- No lost positions

✅ **Telegram Notifications**
- Entry/exit signals
- Daily summary
- Real-time updates

---

## 🛠️ Utilities

### View Results
```cmd
python view_high_accuracy_results.py
```

### Generate Report
```cmd
python generate_dynamic_report.py
```

### View Capital
```cmd
python view_capital.py
```

---

## ⚠️ Important Notes

### API Rate Limits
- Run **ONE strategy at a time**
- Don't run multiple instances
- 3-minute cycle time prevents rate limiting

### Trading Hours
- Auto-starts at 9:15 AM (or immediately if after)
- Auto-stops at 3:30 PM
- Exits all positions at 3:15 PM

### Capital Management
- Starting capital: ₹1,00,000
- Capital persists across sessions
- Risk per trade: 3%
- Max positions: 3

---

## 📋 Quick Start Checklist

1. ✅ Update expiry in `expiry_config.json`
2. ✅ Check `.env` file has correct credentials
3. ✅ Run: `python run_high_accuracy.py`
4. ✅ Choose strategy (1 or 2)
5. ✅ Let it trade until 3:30 PM
6. ✅ Check results: `python view_high_accuracy_results.py`

---

## 🎯 Recommended Approach

### Week 1: Test CURRENT
```cmd
python run_high_accuracy.py
```
Choose option 1 (CURRENT)

### Week 2: Test SIMPLIFIED
```cmd
python run_high_accuracy.py
```
Choose option 2 (SIMPLIFIED)

### Week 3+: Use Best Performer
Based on results, stick with the strategy that performs better for your trading style.

---

## 📞 Support Files

- `README_FINAL.md` - This file
- `IMPORTANT_READ_THIS.md` - API rate limit info
- `API_RATE_LIMIT_FIX.md` - Technical details
- `FIXES_APPLIED_DEC03.md` - Recent fixes
- `QUICK_START_DUAL.md` - Old dual strategy guide (deprecated)

---

## ✅ Status

**Ready to Trade!** 🎉

- ✅ SIMPLIFIED strategy integrated
- ✅ Single instance (no rate limits)
- ✅ Choose strategy at startup
- ✅ All features working
- ✅ Telegram notifications enabled
- ✅ Position recovery active

---

**Last Updated:** December 3, 2025, 10:30 AM
**Version:** 2.0 (Integrated SIMPLIFIED)
