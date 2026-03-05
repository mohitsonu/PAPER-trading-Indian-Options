# 📂 How to View GitHub Actions Trading Files

## 🔍 Understanding Where Files Are

**IMPORTANT:** When GitHub Actions runs, it runs on **GitHub's cloud servers**, NOT on your laptop!

```
Your Laptop (Local)          GitHub Cloud (Remote)
─────────────────           ──────────────────────
❌ No CSV files             ✅ CSV files created here
❌ No updates               ✅ Trading happens here
❌ Report not updated       ✅ Report generated here
```

## 📥 How to Get Files to Your Laptop

### Method 1: Pull from GitHub (After Session Ends)

**When:** After 3:30 PM (when trading session ends)

**Steps:**
```bash
git pull origin main
```

This will download:
- Today's CSV file in `trade_journal/csv/`
- Today's JSON file in `trade_journal/json/`
- Updated `capital_persistence.json`
- Updated `trading_report.html`

### Method 2: Download from GitHub Actions Artifacts

**When:** Anytime during or after the session

**Steps:**
1. Go to: https://github.com/mohitsonu/PAPER-trading/actions
2. Click on today's workflow run (the one "In progress" or completed)
3. Scroll down to **Artifacts** section
4. Download `trading-results-XXX.zip`
5. Extract the ZIP file
6. You'll find:
   - `high_accuracy_trades_YYYYMMDD.csv`
   - `high_accuracy_updates_YYYYMMDD.json`
   - `capital_persistence.json`
   - `trading_report.html`

### Method 3: View on GitHub Website

**When:** After session ends (files are committed)

**Steps:**
1. Go to: https://github.com/mohitsonu/PAPER-trading
2. Navigate to `trade_journal/csv/` folder
3. Click on today's CSV file to view online
4. Click "Raw" to download

## 📊 Real-Time Monitoring

### Option 1: Telegram (BEST)
✅ Real-time notifications
✅ No need to check GitHub
✅ Entry/Exit signals instantly
✅ Daily summary with CSV at 3:30 PM

### Option 2: GitHub Actions Logs
1. Go to: https://github.com/mohitsonu/PAPER-trading/actions
2. Click on today's workflow run
3. Click on "Run trading bot" step
4. View live logs as trading happens

### Option 3: Wait for Session End
- At 3:30 PM, all files are committed to GitHub
- Run `git pull origin main` to get them locally
- Open `trading_report.html` in browser

## 🔄 Workflow Timeline

```
9:15 AM  → GitHub Actions starts on cloud
9:15 AM  → Session start notification on Telegram
9:15-3:30 PM → Trading happens on GitHub cloud
             → CSV files created on GitHub cloud
             → You see notifications on Telegram
3:30 PM  → Session ends
3:30 PM  → Files committed to GitHub repository
3:30 PM  → Daily summary sent to Telegram with CSV
3:31 PM  → Run `git pull` to get files locally
```

## 📱 What You Get on Telegram

Even though files are on GitHub cloud, you get everything on Telegram:

1. **Session Start** (9:15 AM)
2. **Entry Signals** (when trades open)
3. **Exit Signals** (when trades close)
4. **Daily Summary** (3:30 PM) **← Includes CSV file!**

So you don't need to check GitHub or pull files - everything is on Telegram!

## 💡 Key Points

1. ✅ **GitHub Actions runs on cloud** - not your laptop
2. ✅ **Files created on cloud** - not in your local folder
3. ✅ **Telegram shows everything** - real-time updates
4. ✅ **CSV sent to Telegram** - at 3:30 PM daily summary
5. ✅ **Pull to get locally** - after 3:30 PM if needed

## 🎯 Recommended Workflow

**During Trading Day:**
- Monitor Telegram for all updates
- No need to check local files
- Everything is real-time on Telegram

**After 3:30 PM:**
- Check Telegram for daily summary (includes CSV)
- If you want files locally: `git pull origin main`
- Open `trading_report.html` for detailed analysis

## ❓ FAQ

**Q: Why don't I see CSV files in my local folder?**
A: Because GitHub Actions runs on cloud, not your laptop. Files are on GitHub.

**Q: How do I see today's trades?**
A: Check Telegram notifications or wait for 3:30 PM summary with CSV.

**Q: When will files appear locally?**
A: After you run `git pull origin main` (after 3:30 PM when session ends).

**Q: Can I see live updates?**
A: Yes! On Telegram (best) or GitHub Actions logs.

**Q: Do I need to do anything?**
A: No! Just monitor Telegram. Everything is automatic.

---

**Bottom Line:** You don't need local files during the day. Telegram gives you everything in real-time! 📱
