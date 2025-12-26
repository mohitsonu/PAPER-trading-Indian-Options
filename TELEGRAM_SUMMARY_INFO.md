# 📱 Telegram Summary - How It Works

## ✅ Automatic Sending

The Telegram summary is **automatically sent** when the trading session ends at **3:30 PM**.

### What Gets Sent:

1. **Daily Summary Message:**
   - Starting/Ending Capital
   - Net P&L (with percentage)
   - Total Trades
   - Win Rate (Wins/Losses)
   - Session End Time

2. **Trade Journal (CSV File):**
   - Complete list of all trades
   - Entry/Exit prices
   - P&L for each trade
   - Strategy used
   - Timestamps

### When It's Sent:

- ✅ At 3:30 PM when market closes
- ✅ When you stop the algo manually (Ctrl+C)
- ✅ Only if there are completed trades (EXIT records)

---

## 🔧 Manual Sending

If the automatic summary didn't send, you can send it manually:

```cmd
python send_telegram_summary_now.py
```

This will:
1. ✅ Find today's trades file
2. ✅ Calculate all metrics
3. ✅ Send summary message
4. ✅ Send CSV file

---

## ⚠️ Troubleshooting

### Summary Not Sent?

**Possible Reasons:**

1. **No Completed Trades**
   - Only ENTRY records, no EXIT records
   - Trades still open
   - Solution: Wait for trades to close or send manually

2. **Telegram Disabled**
   - Check `telegram_signals/config.py`
   - Make sure `TELEGRAM_ENABLED = True`

3. **Session Didn't End Properly**
   - Algo crashed before 3:30 PM
   - Solution: Run manual sender

4. **Network Issue**
   - Telegram API unreachable
   - Solution: Check internet, retry manual sender

### How to Check:

1. **Check if trades file exists:**
   ```
   high_accuracy_trades_20251203.csv
   ```

2. **Check if there are EXIT records:**
   Open CSV and look for rows with `action = EXIT`

3. **Check Telegram config:**
   ```cmd
   python telegram_signals/test_telegram.py
   ```

---

## 📊 What You Saw Yesterday

```
😔 DAILY SUMMARY 😔
📅 Date: 02-Dec-2025
💰 Starting Capital: ₹110,167.47
💰 Ending Capital: ₹105,829.25
📊 Net Profit (After Charges): ₹-4,338.22 (-3.94%)
📋 Total Trades: 5
🎯 Win Rate: 40.0% (2W / 3L)
⏰ Session End: 05:54:33 PM

📊 Trade Journal - 02-Dec-2025
[CSV file attached]
```

This means:
- ✅ Automatic sending worked
- ✅ Summary was sent at 5:54 PM
- ✅ CSV file was attached

---

## 🎯 Expected Behavior

### During Trading (9:15 AM - 3:30 PM):
- Entry signals sent immediately when trade is taken
- Exit signals sent immediately when trade is closed
- No summary yet

### At Session End (3:30 PM):
- All positions closed
- Final P&L calculated
- Summary message sent
- CSV file sent

### If You Stop Early (Ctrl+C):
- Session ends immediately
- Summary sent if there are completed trades
- CSV file sent

---

## 💡 Tips

1. **Don't worry if summary isn't sent during trading**
   - It only sends at end of session
   - Entry/exit signals are sent in real-time

2. **If you want to check progress during day**
   - Use: `python view_high_accuracy_results.py`
   - Or check the CSV file directly

3. **If summary doesn't send automatically**
   - Run: `python send_telegram_summary_now.py`
   - It will send immediately

4. **CSV file is always created**
   - Even if Telegram fails
   - You can always check the file manually

---

## ✅ Summary

**Automatic:** Sent at 3:30 PM when session ends
**Manual:** Run `send_telegram_summary_now.py` anytime
**Requirements:** Must have completed trades (EXIT records)

Your Telegram integration is working correctly! 🎉

---

**Last Updated:** December 3, 2025
