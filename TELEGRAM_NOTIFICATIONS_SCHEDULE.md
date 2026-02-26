# 📱 Telegram Notifications Schedule

## ✅ What You'll Receive on Telegram

### 1. 🚀 Session Start (9:15-9:20 AM)
Sent once at market open:
```
🚀 TRADING SESSION STARTED 🚀

💰 Capital: ₹226,545.81
📅 Date: 26-Feb-2026
⏰ Time: 09:15:00 AM

🎯 High Accuracy Algorithm Active
📊 Monitoring market for quality setups...
```

### 2. 🟢 Entry Signals (When Trade Executes)
Sent immediately when a trade is placed:
```
🟢 ENTRY SIGNAL 🟢

📊 Symbol: NIFTY25400CE
🎯 Strike: 25400 CE
💰 Entry Price: ₹54.70
📦 Quantity: 15
📈 Strategy: CONTRARIAN

💡 Reason: High accuracy opportunity (Score: 92/100)

⏰ Time: 26-Feb-2026 10:30:15 AM
```

### 3. 🔴 Exit Signals (When Trade Closes)
Sent when position is closed:
```
🟢 EXIT SIGNAL - PROFIT 🟢

📊 Symbol: NIFTY25400CE
🎯 Strike: 25400 CE
💵 Entry: ₹54.70
💵 Exit: ₹62.30
📦 Quantity: 15
💰 Trade P&L: ₹+114.00 (+13.9%)
⏱️ Holding Time: 45 minutes
📋 Exit Reason: Target Hit

⏰ Time: 26-Feb-2026 11:15:20 AM
```

### 4. 📊 Daily Summary (3:25-3:30 PM)
Sent once at market close with CSV file:
```
🎉 DAILY SUMMARY 🎉

📅 Date: 26-Feb-2026

💰 Starting Capital: ₹226,545.81
💰 Ending Capital: ₹228,995.81
📊 Net Profit (After Charges): ₹+2,450.00 (+1.08%)

📋 Total Trades: 5
🎯 Win Rate: 60.0% (3W / 2L)

⏰ Session End: 03:30:00 PM

📎 [Trade Journal CSV File Attached]
```

## ⏰ Notification Timing

| Time | Notification | Frequency |
|------|-------------|-----------|
| 9:15-9:20 AM | Session Start | Once per day |
| 9:15 AM - 3:30 PM | Entry Signals | When trade executes |
| 9:15 AM - 3:30 PM | Exit Signals | When position closes |
| 3:25-3:30 PM | Daily Summary | Once per day |

## 🔄 How It Works

1. **GitHub Actions runs every 5 minutes** during market hours
2. **At 9:15 AM**: First run sends "Session Start" message
3. **During trading**: Entry/Exit signals sent in real-time
4. **At 3:25 PM**: Last run sends "Daily Summary" with CSV

## 📱 Your Telegram Channel

All messages go to: `@optionsalgotesting`

## ✅ Status

- ✅ Telegram secrets added to GitHub
- ✅ Code updated and pushed
- ✅ Notifications will start from tomorrow's market open (9:15 AM)

## 🧪 Test Now (Optional)

To test Telegram locally:
```bash
python telegram_signals/test_telegram.py
```

This will send test messages to verify everything works!

---

**Next Market Open**: You'll receive the "🚀 TRADING SESSION STARTED" message at 9:15 AM!
