# 🎯 START HERE - How to Run Your Algo

## ⚠️ IMPORTANT: Only ONE File to Run

**DO NOT run these old files:**
- ~~`simplified_hybrid_algo.py`~~ ❌ DELETED (old file)
- ~~`run_comparison.py`~~ ❌ (old file)
- ~~`run_dual_comparison.py`~~ ❌ (old file)

---

## ✅ CORRECT Way to Run

### Run BOTH Strategies (Recommended):
```cmd
python run_high_accuracy.py
```

This automatically runs:
1. **CURRENT Strategy** (Complex, Min Score 90)
2. **SIMPLIFIED Strategy** (Price Action, Min Score 70)

Both run simultaneously until 3:30 PM.

---

## 📊 Output Files

After running, you'll get:
- `current_trades_20251203.csv` - CURRENT strategy trades
- `simplified_trades_20251203.csv` - SIMPLIFIED strategy trades

---

## 🔧 Compare Results

After trading ends:
```cmd
python compare_strategies.py
```

---

## 📁 Key Files (Keep These)

### Core:
- `high_accuracy_algo.py` - Main algorithm (both modes)
- `adaptive_market_engine.py` - Market detection
- `priority_features.py` - Advanced filters
- `trailing_stop_manager.py` - Smart stops
- `trade_state_persistence.py` - Position recovery
- `brokerage_calculator.py` - Charges

### Runners:
- `run_high_accuracy.py` - **Main runner (BOTH strategies)** ⭐
- `run_single_strategy.py` - Run only one strategy
- `run_both_strategies.py` - Alternative dual runner

### Utilities:
- `compare_strategies.py` - Compare results
- `generate_dynamic_report.py` - Visual reports
- `view_high_accuracy_results.py` - View results
- `expiry_config.json` - Update expiry here

### Batch Files (Windows):
- `run_high_accuracy_unbuffered.bat` - Easy launcher ⭐
- `run_single.bat` - Single strategy launcher

---

## 🔧 Update Expiry

Edit `expiry_config.json`:
```json
{
  "current_expiry": "09DEC25"
}
```

---

## ❓ Troubleshooting

### "No market data available"
- Check if market is open (9:15 AM - 3:30 PM)
- Verify expiry date in `expiry_config.json`
- Wait 2-3 minutes after market opens

### "Login failed"
- Check `.env` file has correct credentials
- Verify TOTP key is correct

### Want to run only ONE strategy?
```cmd
python run_single_strategy.py
```
Then choose: 1 (CURRENT) or 2 (SIMPLIFIED)

---

## 📈 What to Expect

**CURRENT Strategy:**
- Fewer trades (stricter filters)
- Min score: 90/100
- More conservative

**SIMPLIFIED Strategy:**
- More trades (relaxed filters)
- Min score: 70/100
- More aggressive

Both strategies will:
- ✅ Auto-login
- ✅ Fetch live market data
- ✅ Find high-quality trades
- ✅ Exit at targets/stop-loss
- ✅ Send Telegram notifications
- ✅ Generate reports

---

## 🚀 Quick Start

1. **Update expiry** (if needed):
   ```cmd
   notepad expiry_config.json
   ```

2. **Run algo**:
   ```cmd
   python run_high_accuracy.py
   ```

3. **Let it run** until 3:30 PM

4. **Compare results**:
   ```cmd
   python compare_strategies.py
   ```

That's it! 🎉
