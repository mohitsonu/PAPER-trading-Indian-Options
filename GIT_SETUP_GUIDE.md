# 🚀 Git Setup Guide

## 📋 Quick Setup

### Step 1: Initialize Git
```bash
git init
```

### Step 2: Add files
```bash
git add .
```

### Step 3: Commit
```bash
git commit -m "Initial commit - High Accuracy Trading Algorithm"
```

### Step 4: Create GitHub repo
1. Go to https://github.com/new
2. Create a new repository
3. Copy the repository URL

### Step 5: Push to GitHub
```bash
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
```

---

## 🛡️ What's Protected by .gitignore

### ✅ Sensitive Data (NEVER committed):
- `.env` - API credentials, passwords, TOTP keys
- `capital_persistence.json` - Your capital data
- `daily_capital_tracking.csv` - Your P&L history
- All trade CSV files (`*_trades_*.csv`)
- All trade JSON files (`*_updates_*.json`)
- Trade state files (`trade_state_*.json`)
- Trading reports (`trading_report*.html`)

### ✅ System Files (NEVER committed):
- `__pycache__/` - Python cache
- `.venv/` - Virtual environment
- `*.pyc` - Compiled Python files

### ✅ Backup Files (NEVER committed):
- `*_BACKUP_*.py` - Your backup files
- `*.bak` - Backup files

---

## 📁 What WILL Be Committed

### ✅ Code Files:
- `high_accuracy_algo.py`
- `run_high_accuracy.py`
- `priority_features.py`
- `adaptive_market_engine.py`
- `trailing_stop_manager.py`
- `trade_state_persistence.py`
- `brokerage_calculator.py`
- All other `.py` files

### ✅ Config Files:
- `expiry_config.json` (safe - no sensitive data)
- `high_accuracy_config.json` (if exists)
- `.env.example` (template only, no real credentials)
- `requirements.txt`

### ✅ Documentation:
- `README.md`
- All `.md` files (analysis, guides, etc.)

---

## 🔒 Security Checklist

Before pushing to GitHub, verify:

- [ ] `.env` file is in `.gitignore`
- [ ] No API keys in code
- [ ] No passwords in code
- [ ] No TOTP keys in code
- [ ] No real trading data in repo
- [ ] `.env.example` has placeholder values only

---

## 🚨 If You Accidentally Commit Sensitive Data

### Remove from Git history:
```bash
# Remove file from Git but keep locally
git rm --cached .env

# Commit the removal
git commit -m "Remove sensitive file"

# Force push (if already pushed to GitHub)
git push -f origin main
```

### If credentials were exposed:
1. **IMMEDIATELY change all passwords**
2. **Regenerate API keys**
3. **Create new TOTP key**
4. **Update `.env` file**

---

## 📝 Recommended Commit Messages

### Good commit messages:
```bash
git commit -m "Add market condition filter"
git commit -m "Fix strike diversity bug"
git commit -m "Disable SCALPER strategy (31% WR)"
git commit -m "Update expiry to 02DEC25"
```

### Bad commit messages:
```bash
git commit -m "fix"
git commit -m "update"
git commit -m "changes"
```

---

## 🌿 Branching Strategy (Optional)

### For testing new features:
```bash
# Create feature branch
git checkout -b feature/new-strategy

# Make changes and commit
git add .
git commit -m "Add new strategy"

# Push to GitHub
git push origin feature/new-strategy

# Merge to main when tested
git checkout main
git merge feature/new-strategy
git push origin main
```

---

## 🔄 Daily Workflow

### Morning (before trading):
```bash
# Pull latest changes (if working from multiple machines)
git pull origin main

# Update expiry if needed
# Edit expiry_config.json

# Commit expiry change
git add expiry_config.json
git commit -m "Update expiry to 02DEC25"
git push origin main
```

### Evening (after trading):
```bash
# Commit any code changes
git add *.py
git commit -m "Fix: Improve trend detection"
git push origin main

# Note: Trade data is NOT committed (in .gitignore)
```

---

## 📊 What Others Will See

When someone clones your repo, they will get:
- ✅ All Python code
- ✅ Configuration templates
- ✅ Documentation
- ✅ Setup instructions

They will NOT get:
- ❌ Your API credentials
- ❌ Your trading data
- ❌ Your P&L history
- ❌ Your capital information

---

## 🎯 Ready to Push!

**Your repo is now safe to push to GitHub!**

All sensitive data is protected by `.gitignore`.

```bash
git init
git add .
git commit -m "Initial commit - High Accuracy Trading Algorithm"
git remote add origin <your-github-url>
git push -u origin main
```

**Happy coding!** 🚀
