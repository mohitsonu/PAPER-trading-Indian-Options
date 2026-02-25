# 🤖 AUTO TRADER SETUP GUIDE

This guide will help you set up the trading algorithm to run automatically during market hours.

## 📋 What You Get

- **Automatic Start**: Algorithm starts at 9:15 AM on trading days
- **Automatic Stop**: Algorithm stops at 3:30 PM
- **Auto-Restart**: If algorithm crashes, it restarts automatically
- **Weekend Skip**: No trading on Saturday/Sunday
- **Health Monitoring**: Checks every 5 minutes

---

## 🚀 OPTION 1: Manual Start (Recommended for Testing)

### Step 1: Test the Scheduler
1. Double-click `START_AUTO_TRADER.bat`
2. The scheduler will start and show status messages
3. It will automatically start trading at 9:15 AM (if during market hours)
4. Press `Ctrl+C` to stop when needed

### Pros:
- ✅ Easy to start/stop
- ✅ See logs in real-time
- ✅ Full control

### Cons:
- ❌ Must start manually each day
- ❌ Stops if you close the window

---

## 🔧 OPTION 2: Windows Task Scheduler (Fully Automatic)

This will start the scheduler automatically when Windows starts.

### Step 1: Open Task Scheduler
1. Press `Win + R`
2. Type `taskschd.msc` and press Enter
3. Task Scheduler window opens

### Step 2: Create New Task
1. Click **"Create Task"** (not "Create Basic Task")
2. In **General** tab:
   - Name: `Auto Trading Scheduler`
   - Description: `Runs trading algorithm during market hours`
   - ✅ Check **"Run whether user is logged on or not"**
   - ✅ Check **"Run with highest privileges"**
   - Configure for: **Windows 10**

### Step 3: Set Triggers
1. Go to **Triggers** tab
2. Click **"New"**
3. Begin the task: **At startup**
4. ✅ Check **"Enabled"**
5. Click **OK**

### Step 4: Set Actions
1. Go to **Actions** tab
2. Click **"New"**
3. Action: **Start a program**
4. Program/script: Browse to `START_AUTO_TRADER.bat`
5. Start in: Browse to your project folder (e.g., `E:\SHOONYS PAPER`)
6. Click **OK**

### Step 5: Configure Conditions
1. Go to **Conditions** tab
2. ❌ Uncheck **"Start the task only if the computer is on AC power"**
3. ❌ Uncheck **"Stop if the computer switches to battery power"**

### Step 6: Configure Settings
1. Go to **Settings** tab
2. ✅ Check **"Allow task to be run on demand"**
3. ✅ Check **"Run task as soon as possible after a scheduled start is missed"**
4. ✅ Check **"If the task fails, restart every: 5 minutes"**
5. Set **"Attempt to restart up to: 3 times"**
6. If running task does not end when requested: **Do not start a new instance**

### Step 7: Save and Test
1. Click **OK**
2. Enter your Windows password if prompted
3. Right-click the task → **Run** to test
4. Check `auto_trader_scheduler.log` for status

### Pros:
- ✅ Fully automatic - starts on Windows boot
- ✅ Runs in background
- ✅ Restarts if computer reboots

### Cons:
- ❌ Harder to see real-time logs
- ❌ Requires Windows password

---

## 📊 Monitoring

### Check if Scheduler is Running
1. Open Task Manager (`Ctrl + Shift + Esc`)
2. Look for `python.exe` running `auto_trader_scheduler.py`

### View Logs
- **Scheduler Log**: `auto_trader_scheduler.log`
- **Trading Log**: Check the CSV files and console output

### Stop the Scheduler
- **Manual Mode**: Press `Ctrl+C` in the window
- **Task Scheduler Mode**: 
  1. Open Task Scheduler
  2. Find "Auto Trading Scheduler"
  3. Right-click → **End**

---

## 🎯 How It Works

```
8:00 AM  - Scheduler running, waiting...
9:15 AM  - ✅ Market opens - Start trading algorithm
9:20 AM  - ✅ Health check - Algorithm running fine
11:00 AM - ✅ Health check - Algorithm running fine
3:30 PM  - 🛑 Market closes - Stop trading algorithm
3:35 PM  - Scheduler running, waiting for next day...
```

---

## 🔍 Troubleshooting

### Scheduler doesn't start algorithm
1. Check `auto_trader_scheduler.log` for errors
2. Verify it's a weekday (Monday-Friday)
3. Verify time is between 9:15 AM - 3:30 PM
4. Check if `.env` file has correct credentials

### Algorithm crashes repeatedly
1. Check `high_accuracy_trades_YYYYMMDD.csv` for errors
2. Verify internet connection
3. Check Shoonya API status
4. Review login credentials in `.env`

### Task Scheduler doesn't run
1. Verify task is **Enabled**
2. Check **History** tab for error messages
3. Ensure path to `.bat` file is correct
4. Try running task manually (right-click → Run)

---

## 📝 Important Notes

1. **Keep Computer On**: The scheduler needs your computer running
2. **Internet Connection**: Required for trading
3. **Login Credentials**: Must be valid in `.env` file
4. **Market Holidays**: Currently doesn't skip holidays (you can add this)
5. **Logs**: Check logs regularly to ensure everything is working

---

## 🛡️ Safety Features

- ✅ Only runs during market hours
- ✅ Skips weekends automatically
- ✅ Auto-restarts if algorithm crashes
- ✅ Stops at market close
- ✅ Health checks every 5 minutes
- ✅ All activities logged

---

## 📞 Quick Commands

### Start Scheduler (Manual)
```bash
python auto_trader_scheduler.py
```

### View Logs
```bash
type auto_trader_scheduler.log
```

### Check if Running
```bash
tasklist | findstr python
```

### Stop All Python Processes (Emergency)
```bash
taskkill /F /IM python.exe
```

---

## 🎉 You're All Set!

The scheduler is now ready to run your trading algorithm automatically during market hours. Just start it once and forget about it!

**Recommended**: Start with **Option 1 (Manual)** for a few days to ensure everything works, then switch to **Option 2 (Task Scheduler)** for full automation.
