# 📊 How to Update Your Trading Report

## 🎯 AUTOMATIC MODE (Recommended!)

**Your trading bot now auto-generates the report!**

When you run your trading bot:
```bash
python run_high_accuracy.py
```

After trading ends (3:30 PM), it will:
1. ✅ Save all trades to CSV
2. ✅ **Automatically generate the report**
3. ✅ **Open it in your browser**
4. ✅ Done! No manual steps needed!

---

## Manual Methods (If Needed)

### Option 1: Double-Click Method
1. **Double-click** `update_report.bat`
2. Wait a few seconds while it processes your trades
3. The report will automatically open in your browser
4. Done! ✅

### Option 2: Command Line Method
```bash
python generate_dynamic_report.py
```

The report will auto-open in your browser.

### Option 3: Just View Report
```bash
python open_report.py
```

Opens the existing report without regenerating.

---

## What Happens Automatically?

The script automatically:
- ✅ Reads ALL your `high_accuracy_trades_*.csv` files
- ✅ Combines them into one dataset
- ✅ Generates fresh charts and metrics
- ✅ Creates a new `trading_report.html` with today's data
- ✅ Opens it in your browser

---

## Daily Workflow

**NEW AUTOMATIC WORKFLOW:**
1. Run your trading bot: `python run_high_accuracy.py`
2. Bot trades automatically during market hours
3. At 3:30 PM, bot stops and auto-generates report
4. Report opens in your browser automatically
5. Done! 🎉

**No manual steps required!**

---

## Features

Your dynamic report includes:
- 📈 **Equity Curve** - See your account growth over time
- 📉 **Drawdown Chart** - Monitor risk
- 🎯 **Strategy Performance** - Which strategies work best
- 💰 **Daily P&L** - Day-by-day breakdown
- 📊 **Win/Loss Distribution** - Statistical analysis
- 📋 **Trade Log** - Recent 50 trades
- 🔍 **Date Filter** - View specific days or all-time

---

## Troubleshooting

**Problem:** Script doesn't run
- **Solution:** Make sure Python is installed and in your PATH

**Problem:** No data shows up
- **Solution:** Check that you have `high_accuracy_trades_*.csv` files in the same folder

**Problem:** Report looks old
- **Solution:** Make sure you ran `update_report.bat` AFTER today's trading

---

## Automation (Optional)

Want it to update automatically every day?

### Windows Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 4:00 PM (after market close)
4. Action: Start a program
5. Program: `C:\path\to\update_report.bat`
6. Done!

Now your report updates automatically every day! 🎉

---

## Need Help?

If something isn't working:
1. Check that all CSV files are in the same folder as the script
2. Make sure Python is installed (`python --version`)
3. Try running from command line to see error messages
