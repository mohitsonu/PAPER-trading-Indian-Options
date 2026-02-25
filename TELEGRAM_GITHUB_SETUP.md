# 📱 Telegram Notifications in GitHub Actions

Your trading bot now sends Telegram notifications automatically when running on GitHub Actions!

## ✅ What's Already Done

1. ✅ GitHub Actions workflow updated to support Telegram
2. ✅ HTML report generation added to workflow
3. ✅ Code updated to read Telegram credentials from environment variables
4. ✅ Telegram notifications integrated into trading cycle

## 🔐 Setup GitHub Secrets (Required)

You need to add your Telegram credentials as GitHub Secrets:

### Step 1: Go to Repository Settings
1. Open your repository: https://github.com/mohitsonu/PAPER-trading
2. Click **Settings** (top menu)
3. Click **Secrets and variables** → **Actions** (left sidebar)

### Step 2: Add Telegram Secrets
Click **New repository secret** and add these TWO secrets:

**Secret 1:**
- Name: `TELEGRAM_BOT_TOKEN`
- Value: `8468449326:AAHCEko5T1squW5VFJjL4SdS0nr8h1JB-sU`

**Secret 2:**
- Name: `TELEGRAM_CHAT_ID`
- Value: `@optionsalgotesting`

### Step 3: Verify Existing Secrets
Make sure you already have these 5 Shoonya secrets (you added them before):
- ✅ SHOONYA_USER_ID
- ✅ SHOONYA_PASSWORD
- ✅ SHOONYA_TOTP_KEY
- ✅ SHOONYA_VENDOR_CODE
- ✅ SHOONYA_API_SECRET

**Total: You should have 7 secrets in GitHub**

## 📊 What You'll Get

### 1. Trade Signals (Real-time)
When a trade is executed, you'll receive:
```
🎯 TRADE SIGNAL

Symbol: NIFTY25400CE
Action: BUY
Price: ₹54.70
Score: 92/100
Strategy: CONTRARIAN

Reason: High accuracy opportunity (Score: 92/100)

⏰ 2026-02-25 10:30:15 IST
```

### 2. Daily Summary (Market Close)
At 3:25 PM, you'll receive:
```
📊 DAILY TRADING SUMMARY

Total Trades: 5
Winning Trades: 3
Win Rate: 60%

💰 Total P&L: +₹2,450
💼 Current Capital: ₹102,450

⏰ 2026-02-25 15:25:00 IST
```

### 3. HTML Report
- Generated after each trading cycle
- Available in GitHub Actions artifacts
- Shows detailed trade analysis, charts, and performance metrics

## 🚀 How It Works

1. **Every 5 minutes** during market hours (9:15 AM - 3:30 PM IST)
2. Bot checks for trading opportunities
3. If trade executed → **Telegram notification sent immediately**
4. At market close → **Daily summary sent**
5. HTML report generated and uploaded to GitHub

## 📥 Accessing HTML Reports

1. Go to your repository
2. Click **Actions** tab
3. Click on any workflow run
4. Scroll down to **Artifacts** section
5. Download `trading-results-XXX`
6. Extract and open `trading_report.html` in browser

## 🧪 Test Telegram (Optional)

To test if Telegram is working locally:
```bash
python telegram_signals/test_telegram.py
```

You should receive a test message on Telegram!

## ⚠️ Important Notes

- Telegram notifications work BOTH locally and on GitHub Actions
- GitHub Actions uses secrets (secure)
- Local runs use `telegram_signals/config.py` (already configured)
- HTML report is generated automatically
- Reports are saved as artifacts (30 days retention)

## 🎉 You're All Set!

Once you add the 2 Telegram secrets to GitHub:
1. Push this code to GitHub
2. Wait for next workflow run (every 5 minutes during market hours)
3. Check your Telegram channel for notifications!

---

**Need Help?**
- Test locally first: `python run_high_accuracy.py`
- Check GitHub Actions logs for errors
- Verify all 7 secrets are added correctly
