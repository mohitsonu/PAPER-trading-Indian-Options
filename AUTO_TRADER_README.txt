================================================================================
🤖 AUTOMATIC TRADING SCHEDULER - QUICK START
================================================================================

WHAT IT DOES:
- Automatically starts trading at 9:15 AM (Monday-Friday)
- Automatically stops trading at 3:30 PM
- Restarts if algorithm crashes
- Skips weekends automatically
- Monitors health every 5 minutes

================================================================================
🚀 HOW TO USE
================================================================================

OPTION 1: MANUAL START (Easiest)
---------------------------------
1. Double-click: START_AUTO_TRADER.bat
2. Leave the window open
3. Press Ctrl+C to stop

OPTION 2: AUTOMATIC START (Best for daily use)
-----------------------------------------------
1. Read: SETUP_AUTO_START.md
2. Follow Windows Task Scheduler setup
3. Runs automatically on computer startup

================================================================================
📊 MONITORING
================================================================================

Check if running:
- Look for black window with "AUTO TRADER SCHEDULER" title
- Check Task Manager for "python.exe"

View logs:
- Open: auto_trader_scheduler.log
- Shows all start/stop/error messages

Check trades:
- Open: high_accuracy_trades_YYYYMMDD.csv
- Shows all executed trades

================================================================================
🛑 HOW TO STOP
================================================================================

Manual mode:
- Press Ctrl+C in the scheduler window

Task Scheduler mode:
- Open Task Manager
- Find "python.exe" 
- Right-click → End Task

================================================================================
⚠️ IMPORTANT NOTES
================================================================================

1. Keep your computer ON during market hours
2. Ensure stable internet connection
3. Check logs daily to verify it's working
4. The scheduler needs to run continuously
5. Don't close the window if running manually

================================================================================
🔧 TROUBLESHOOTING
================================================================================

Scheduler not starting algorithm:
→ Check if it's a weekday (Mon-Fri)
→ Check if time is 9:15 AM - 3:30 PM
→ Check auto_trader_scheduler.log for errors

Algorithm keeps crashing:
→ Check internet connection
→ Verify .env credentials are correct
→ Check Shoonya API status

Can't see the window:
→ Check Task Manager for python.exe
→ Check auto_trader_scheduler.log

================================================================================
📞 QUICK COMMANDS
================================================================================

Test scheduler:
    python test_scheduler.py

Start scheduler:
    python auto_trader_scheduler.py

View logs:
    type auto_trader_scheduler.log

Stop all Python:
    taskkill /F /IM python.exe

================================================================================
✅ YOU'RE ALL SET!
================================================================================

The scheduler will now handle everything automatically. Just start it once
and it will trade during market hours every weekday.

For detailed setup instructions, see: SETUP_AUTO_START.md
