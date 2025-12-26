# ⚠️ IMPORTANT: API Rate Limit Issue

## Problem:
Running **BOTH strategies simultaneously** causes API rate limiting:
- CURRENT strategy: 60 API calls per cycle
- SIMPLIFIED strategy: 60 API calls per cycle
- **Total: 120 calls every 3 minutes** = Rate limited!

## Solution: Run ONE Strategy at a Time

### ✅ Option 1: Run CURRENT Strategy Only (Recommended)
```cmd
python run_current_only.py
```

**Benefits:**
- No rate limiting
- Min score: 90/100 (high quality trades)
- 30 strikes covered
- Stable and reliable

### ✅ Option 2: Run SIMPLIFIED Strategy Only
```cmd
python run_single_strategy.py
```
Then choose option 2 (SIMPLIFIED)

**Benefits:**
- No rate limiting
- Min score: 70/100 (more trades)
- 30 strikes covered

### ❌ Don't Use (Causes Rate Limiting):
```cmd
python run_high_accuracy.py  # Runs BOTH = Rate limited!
```

---

## Why This Happens:

**Shoonya API Limits:**
- ~40-50 calls per minute allowed
- Running 2 strategies = 120 calls per 3 minutes = 40 calls/min
- This triggers rate limiting

**Single Strategy:**
- 60 calls per 3 minutes = 20 calls/min
- Well within limits ✅

---

## Recommended Setup:

### For Today (Test):
```cmd
python run_current_only.py
```

Let it run until 3:30 PM and see results.

### For Tomorrow (Compare):
Run SIMPLIFIED strategy:
```cmd
python run_single_strategy.py
```
Choose option 2

Then compare results over multiple days.

---

## Files to Use:

✅ **run_current_only.py** - CURRENT strategy (Min score 90)
✅ **run_single_strategy.py** - Choose CURRENT or SIMPLIFIED
❌ **run_high_accuracy.py** - Runs BOTH (rate limited)
❌ **run_both_strategies.py** - Runs BOTH (rate limited)

---

## Summary:

**Problem:** Running 2 strategies = Too many API calls
**Solution:** Run 1 strategy at a time
**Recommended:** Use `run_current_only.py`

---

**Status:** Ready to trade with single strategy! 🎯
