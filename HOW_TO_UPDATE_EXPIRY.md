# 📅 HOW TO UPDATE EXPIRY DATE

## 🎯 SIMPLE METHOD

### Step 1: Open the config file
```
expiry_config.json
```

### Step 2: Change the current_expiry
```json
{
  "current_expiry": "28NOV25",  ← Change this line
  "next_expiry": "02DEC25",
  ...
}
```

### Step 3: Save the file

### Step 4: Run the algo
```bash
python run_high_accuracy.py
```

**That's it!** The algo will automatically use the new expiry.

---

## 📋 UPCOMING EXPIRY DATES

### November 2025:
- ✅ 25NOV25 (Monday) - Current
- 📅 28NOV25 (Thursday) - Monthly expiry

### December 2025:
- 📅 02DEC25 (Monday)
- 📅 05DEC25 (Thursday)
- 📅 09DEC25 (Monday)
- 📅 12DEC25 (Thursday)
- 📅 16DEC25 (Monday)
- 📅 19DEC25 (Thursday)
- 📅 23DEC25 (Monday)
- 📅 26DEC25 (Thursday) - Monthly expiry
- 📅 30DEC25 (Monday)

### January 2026:
- 📅 02JAN26 (Thursday)
- 📅 06JAN26 (Monday)
- And so on...

---

## 🔄 WHEN TO UPDATE

### Every Monday Morning (9:00 AM):
1. Check if today is expiry day
2. If yes, update to next Monday's date
3. Save and run

### Example:
```
Monday 25 Nov → Use 25NOV25
After 3:30 PM → Update to 28NOV25 (Thursday monthly)
Thursday 28 Nov → Use 28NOV25
After 3:30 PM → Update to 02DEC25 (next Monday)
```

---

## 📝 FORMAT

**Always use this format:**
```
DDMMMYY
```

**Examples:**
- ✅ 25NOV25 (correct)
- ✅ 02DEC25 (correct)
- ❌ 25-NOV-25 (wrong)
- ❌ 25Nov25 (wrong - must be uppercase)
- ❌ 2DEC25 (wrong - must be 02DEC25)

---

## 🎯 QUICK REFERENCE

### To change expiry:
1. Open `expiry_config.json`
2. Change `"current_expiry": "25NOV25"` to new date
3. Save
4. Run algo

### Current expiry:
```json
"current_expiry": "25NOV25"
```

### Next expiry:
```json
"current_expiry": "28NOV25"
```

---

## 💡 TIPS

1. **Update on Monday morning** before market opens
2. **Check the calendar** for correct dates
3. **Use uppercase** for month (NOV, DEC, JAN)
4. **Use 2 digits** for day (02, 05, 09)
5. **Use 2 digits** for year (25, 26)

---

## 🚀 THAT'S IT!

No need to edit Python code anymore!
Just update the JSON file and you're good to go! 📅
