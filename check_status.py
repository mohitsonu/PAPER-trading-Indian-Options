#!/usr/bin/env python3
"""
📊 STATUS CHECKER
Quick check to see if auto trader is running and view recent activity
"""

import os
import sys
from datetime import datetime
import psutil

def check_status():
    print("📊 AUTO TRADER STATUS CHECK")
    print("=" * 60)
    print(f"⏰ Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check if scheduler is running
    print("\n1️⃣ SCHEDULER STATUS:")
    scheduler_running = False
    algo_running = False
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'python' in proc.info['name'].lower():
                cmdline_str = ' '.join(cmdline)
                
                if 'auto_trader_scheduler.py' in cmdline_str:
                    scheduler_running = True
                    print(f"   ✅ Scheduler running (PID: {proc.info['pid']})")
                
                if 'run_high_accuracy.py' in cmdline_str:
                    algo_running = True
                    print(f"   ✅ Trading algorithm running (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if not scheduler_running:
        print("   ❌ Scheduler NOT running")
        print("   💡 Start with: START_AUTO_TRADER.bat")
    
    if not algo_running and scheduler_running:
        print("   ℹ️ Algorithm not running (may be outside market hours)")
    
    # Check scheduler log
    print("\n2️⃣ RECENT SCHEDULER ACTIVITY:")
    if os.path.exists("auto_trader_scheduler.log"):
        with open("auto_trader_scheduler.log", "r", encoding='utf-8') as f:
            lines = f.readlines()
            recent_lines = lines[-10:] if len(lines) > 10 else lines
            
            if recent_lines:
                for line in recent_lines:
                    print(f"   {line.strip()}")
            else:
                print("   ℹ️ No log entries yet")
    else:
        print("   ℹ️ No log file found (scheduler hasn't run yet)")
    
    # Check today's trades
    print("\n3️⃣ TODAY'S TRADING ACTIVITY:")
    today = datetime.now().strftime('%Y%m%d')
    trade_file = f"high_accuracy_trades_{today}.csv"
    
    if os.path.exists(trade_file):
        with open(trade_file, "r", encoding='utf-8') as f:
            lines = f.readlines()
            trade_count = len(lines) - 1  # Subtract header
            
            if trade_count > 0:
                print(f"   ✅ {trade_count} trades executed today")
                print(f"   📄 File: {trade_file}")
            else:
                print("   ℹ️ No trades executed yet today")
    else:
        print("   ℹ️ No trading activity today")
    
    # Market hours check
    print("\n4️⃣ MARKET STATUS:")
    now = datetime.now()
    current_time = now.time()
    is_weekday = now.weekday() < 5
    
    from datetime import time as dt_time
    market_open = dt_time(9, 15)
    market_close = dt_time(15, 30)
    is_market_hours = market_open <= current_time <= market_close
    
    day_name = now.strftime('%A')
    
    if not is_weekday:
        print(f"   📅 Today is {day_name} (Weekend - No trading)")
    elif is_market_hours:
        print(f"   ✅ Market is OPEN (9:15 AM - 3:30 PM)")
        print(f"   ⏰ Current: {current_time.strftime('%H:%M:%S')}")
    else:
        if current_time < market_open:
            print(f"   ⏰ Market opens at 9:15 AM")
            print(f"   ⏳ Current: {current_time.strftime('%H:%M:%S')}")
        else:
            print(f"   🔒 Market closed (3:30 PM)")
            print(f"   ⏰ Current: {current_time.strftime('%H:%M:%S')}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    
    if scheduler_running and algo_running:
        print("✅ Everything is running perfectly!")
    elif scheduler_running and not algo_running:
        if is_market_hours and is_weekday:
            print("⚠️ Scheduler running but algorithm not active")
            print("   Check logs for issues")
        else:
            print("✅ Scheduler running, waiting for market hours")
    else:
        print("❌ Scheduler not running")
        print("💡 Start with: START_AUTO_TRADER.bat")
    
    print("\n")

if __name__ == "__main__":
    try:
        check_status()
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        sys.exit(1)
