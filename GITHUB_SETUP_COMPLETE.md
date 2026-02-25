# 🚀 COMPLETE GITHUB ACTIONS SETUP GUIDE

## ⏱️ Total Time: 20 minutes
## 💰 Cost: FREE (Forever!)

---

## 📋 WHAT YOU'LL GET

- ✅ Bot runs automatically during market hours
- ✅ Checks every 5 minutes for trading opportunities
- ✅ No laptop needed
- ✅ 100% FREE
- ✅ Secure (credentials encrypted)
- ✅ Easy to monitor

---

## 🚀 STEP-BY-STEP SETUP

### STEP 1: Create GitHub Account (3 minutes)

1. Go to: **https://github.com/**
2. Click **"Sign up"**
3. Enter:
   - Email address
   - Password (strong password)
   - Username (e.g., "yourname-trading")
4. Verify email
5. Choose **"Free"** plan (no credit card needed!)

✅ **Account created!**

---

### STEP 2: Create Private Repository (2 minutes)

1. Click **"+"** icon (top right) → **"New repository"**
2. Fill in:
   - Repository name: **trading-bot**
   - Description: **Automated options trading bot**
   - ⚠️ **IMPORTANT**: Select **"Private"** (not Public!)
   - ✅ Check **"Add a README file"**
3. Click **"Create repository"**

✅ **Repository created!**

---

### STEP 3: Upload Your Code (5 minutes)

**Method 1: Web Upload (Easiest)**

1. In your repository, click **"Add file"** → **"Upload files"**

2. Drag and drop these files from your laptop:
   ```
   ✅ run_high_accuracy.py
   ✅ run_github_actions.py
   ✅ high_accuracy_algo.py
   ✅ priority_features.py
   ✅ adaptive_market_engine.py
   ✅ trailing_stop_manager.py
   ✅ trade_state_persistence.py
   ✅ brokerage_calculator.py
   ✅ expiry_config.json
   ✅ requirements.txt
   ✅ .github/workflows/trading-bot.yml
   ```

3. **⚠️ DO NOT upload .env file** (we'll add credentials as secrets)

4. Click **"Commit changes"**

✅ **Code uploaded!**

---

### STEP 4: Add Your Credentials as Secrets (5 minutes)

**IMPORTANT**: This keeps your credentials secure!

1. In your repository, click **"Settings"** (top menu)

2. In left sidebar, click **"Secrets and variables"** → **"Actions"**

3. Click **"New repository secret"**

4. Add each secret one by one:

**Secret 1: User ID**
- Name: `SHOONYA_USER_ID`
- Secret: `FA318285` (your actual user ID)
- Click **"Add secret"**

**Secret 2: Password**
- Name: `SHOONYA_PASSWORD`
- Secret: Your Shoonya password
- Click **"Add secret"**

**Secret 3: TOTP Key**
- Name: `SHOONYA_TOTP_KEY`
- Secret: Your TOTP key
- Click **"Add secret"**

**Secret 4: Vendor Code**
- Name: `SHOONYA_VENDOR_CODE`
- Secret: Your vendor code
- Click **"Add secret"**

**Secret 5: API Secret**
- Name: `SHOONYA_API_SECRET`
- Secret: Your API secret
- Click **"Add secret"**

✅ **Credentials secured!**

---

### STEP 5: Enable GitHub Actions (2 minutes)

1. In your repository, click **"Actions"** (top menu)

2. If you see "Workflows aren't being run on this repository":
   - Click **"I understand my workflows, go ahead and enable them"**

3. You should see your workflow: **"Auto Trading Bot"**

✅ **Actions enabled!**

---

### STEP 6: Test the Setup (3 minutes)

**Manual Test:**

1. Go to **"Actions"** tab
2. Click **"Auto Trading Bot"** workflow (left sidebar)
3. Click **"Run workflow"** button (right side)
4. Click green **"Run workflow"** button
5. Wait 10-20 seconds, then refresh page
6. Click on the workflow run (yellow dot → green checkmark)
7. Click **"trading-bot"** job
8. See the logs!

✅ **Working!**

---

## 📊 HOW IT WORKS

### Automatic Schedule

The bot runs automatically:

```
Monday-Friday:
├─ 9:15 AM  → Check market
├─ 9:20 AM  → Check market
├─ 9:25 AM  → Check market
├─ ...
├─ 3:25 PM  → Check market
└─ 3:30 PM  → Final check, then stop

Saturday-Sunday:
└─ No runs (weekend)
```

### What Happens Each Run

1. ✅ Check if market is open
2. ✅ Login to Shoonya
3. ✅ Fetch market data
4. ✅ Analyze opportunities
5. ✅ Execute trades if score ≥ 90
6. ✅ Manage existing positions
7. ✅ Save results

---

## 📈 MONITORING YOUR BOT

### View Live Logs

1. Go to **"Actions"** tab
2. Click on any running workflow (yellow dot)
3. Click **"trading-bot"** job
4. See real-time logs!

### Download Trade Results

1. After workflow completes (green checkmark)
2. Scroll down to **"Artifacts"**
3. Click **"trading-results-XXX"** to download
4. Extract ZIP file
5. Open CSV files to see trades!

### Check Status

- **Green checkmark** ✅ = Success
- **Yellow dot** 🟡 = Running
- **Red X** ❌ = Failed (check logs)

---

## 💰 USAGE & LIMITS

### GitHub Free Tier

- ✅ 2,000 minutes/month FREE
- ✅ Private repositories
- ✅ Unlimited public repositories

### Your Usage

- Trading hours: 6.25 hours/day
- Trading days: ~22 days/month
- Runs every 5 minutes: ~82 runs/day
- Each run: ~2-3 minutes
- **Total: ~400-500 minutes/month**

### Remaining

- 2,000 - 500 = **1,500 minutes free for other projects!**

✅ **Well within free tier!**

---

## 🔒 SECURITY

Your setup is secure:

- ✅ Repository is **private** (only you can see)
- ✅ Credentials stored as **encrypted secrets**
- ✅ Secrets never appear in logs
- ✅ GitHub's enterprise-grade security
- ✅ 2FA available (recommended)

**Enable 2FA:**
1. Click your profile picture → Settings
2. Password and authentication
3. Enable two-factor authentication

---

## 🎯 ADVANTAGES vs OTHER SOLUTIONS

| Feature | GitHub Actions | AWS EC2 | Laptop |
|---------|---------------|---------|--------|
| Cost | FREE ✅ | ₹600/month | ₹500/month |
| Setup Time | 20 min | 45 min | 5 min |
| Laptop Needed | NO ✅ | NO ✅ | YES ❌ |
| Credit Card | NO ✅ | YES ❌ | NO ✅ |
| Maintenance | None ✅ | Some | Some |
| Reliability | Excellent | Excellent | Fair |

---

## 🆘 TROUBLESHOOTING

### Workflow not running

**Check:**
1. Is it a weekday (Mon-Fri)?
2. Is it market hours (9:15 AM - 3:30 PM IST)?
3. Are Actions enabled? (Settings → Actions → Allow all actions)

### Workflow failing

**Check logs:**
1. Go to Actions → Click failed run
2. Click "trading-bot" job
3. Look for error message
4. Common issues:
   - Wrong credentials → Update secrets
   - Missing file → Re-upload files
   - API issue → Check Shoonya status

### No trades executing

**This is normal if:**
- No opportunities meet 90+ score threshold
- Market conditions not favorable
- Already at max positions (3)

**Check:**
- View logs to see opportunities found
- Check if scores are below 90
- Verify market is actually open

---

## 📱 MOBILE MONITORING

### GitHub Mobile App

1. Download "GitHub" app (iOS/Android)
2. Login with your account
3. Go to your repository
4. Click "Actions"
5. Monitor from anywhere!

### Email Notifications

1. Settings → Notifications
2. Enable "Actions" notifications
3. Get email when workflow fails

---

## 🔄 UPDATING YOUR BOT

### Update Code

1. Go to repository
2. Click on file to update
3. Click pencil icon (Edit)
4. Make changes
5. Click "Commit changes"
6. Next run will use new code!

### Update Credentials

1. Settings → Secrets and variables → Actions
2. Click on secret to update
3. Click "Update secret"
4. Enter new value
5. Click "Update secret"

---

## 📊 VIEWING RESULTS

### Daily Summary

After each trading day:

1. Go to Actions
2. Click last workflow run of the day
3. Scroll to "Artifacts"
4. Download "trading-results-XXX"
5. Extract and view CSV files

### Capital Tracking

The bot saves:
- `capital_persistence.json` - Current capital
- `high_accuracy_trades_YYYYMMDD.csv` - All trades
- `high_accuracy_updates_YYYYMMDD.json` - Trade updates

---

## 🎉 YOU'RE DONE!

Your trading bot is now running on GitHub Actions!

**What happens now:**
- ✅ Bot runs automatically Mon-Fri, 9:15 AM - 3:30 PM
- ✅ Checks market every 5 minutes
- ✅ Executes high-accuracy trades (score ≥ 90)
- ✅ You can monitor from anywhere
- ✅ Completely FREE!

**Next steps:**
1. Monitor first few days
2. Check logs regularly
3. Download trade results
4. Adjust strategy if needed

---

## 💡 PRO TIPS

1. **Check logs daily** - Ensure bot is running smoothly
2. **Download results weekly** - Keep track of performance
3. **Enable 2FA** - Extra security for your account
4. **Star your repo** - Easy to find later
5. **Add README** - Document your strategy

---

## 🆚 FINAL COMPARISON

### GitHub Actions vs AWS vs Laptop

**For your situation (sometimes won't open laptop):**

🏆 **WINNER: GitHub Actions**

Why?
- ✅ 100% FREE (no credit card needed)
- ✅ Easy 20-minute setup
- ✅ No laptop needed
- ✅ Perfect for high-accuracy strategy
- ✅ Secure and reliable
- ✅ Easy to monitor

**When to use AWS instead:**
- Need truly continuous monitoring (every second)
- Need more than 2,000 minutes/month
- Want to run multiple bots

**When to use Laptop:**
- Testing new strategies
- Short-term trading
- Don't want to setup cloud

---

## 📞 NEED HELP?

If you get stuck:

1. Check the logs (Actions → Click run → View logs)
2. Read error message carefully
3. Check troubleshooting section above
4. Verify all secrets are correct
5. Ensure all files are uploaded

Common issues are usually:
- Wrong credentials
- Missing files
- Timezone confusion

---

## ✅ CHECKLIST

Before you start:
- [ ] GitHub account created
- [ ] Repository created (PRIVATE!)
- [ ] All files uploaded
- [ ] All 5 secrets added
- [ ] Actions enabled
- [ ] Test run successful

After setup:
- [ ] Monitor first day
- [ ] Check logs
- [ ] Download results
- [ ] Verify trades
- [ ] Enable 2FA (recommended)

---

## 🎊 CONGRATULATIONS!

You now have a professional, cloud-based trading bot running 24/7 (during market hours) - completely FREE!

No laptop needed. No credit card needed. Just pure automation! 🚀
