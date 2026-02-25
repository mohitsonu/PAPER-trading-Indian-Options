#!/usr/bin/env python3
"""
🧪 TEST SCHEDULER
Quick test to verify the auto trader scheduler works correctly
"""

import sys
from datetime import datetime, time as dt_time

def test_scheduler():
    print("🧪 TESTING AUTO TRADER SCHEDULER")
    print("=" * 50)
    
    # Test 1: Import check
    print("\n1️⃣ Testing imports...")
    try:
        import schedule
        print("   ✅ schedule library installed")
    except ImportError:
        print("   ❌ schedule library missing - run: pip install schedule")
        return False
    
    try:
        from auto_trader_scheduler import AutoTrader
        print("   ✅ AutoTrader class imported")
    except Exception as e:
        print(f"   ❌ Failed to import AutoTrader: {e}")
        return False
    
    # Test 2: Check trading day logic
    print("\n2️⃣ Testing trading day detection...")
    trader = AutoTrader()
    is_trading_day = trader.is_trading_day()
    today = datetime.now()
    day_name = today.strftime('%A')
    
    if today.weekday() < 5:
        print(f"   ✅ Today is {day_name} - Trading day: {is_trading_day}")
    else:
        print(f"   ✅ Today is {day_name} - Weekend (No trading): {not is_trading_day}")
    
    # Test 3: Check market hours logic
    print("\n3️⃣ Testing market hours detection...")
    is_market_hours = trader.is_market_hours()
    current_time = datetime.now().strftime('%H:%M:%S')
    
    print(f"   Current time: {current_time}")
    print(f"   Market hours: 09:15:00 - 15:30:00")
    print(f"   In market hours: {is_market_hours}")
    
    if is_market_hours:
        print("   ✅ Currently in market hours")
    else:
        print("   ℹ️ Currently outside market hours")
    
    # Test 4: Check if algorithm file exists
    print("\n4️⃣ Testing algorithm file...")
    import os
    if os.path.exists("run_high_accuracy.py"):
        print("   ✅ run_high_accuracy.py found")
    else:
        print("   ❌ run_high_accuracy.py not found")
        return False
    
    # Test 5: Check .env file
    print("\n5️⃣ Testing environment configuration...")
    if os.path.exists(".env"):
        print("   ✅ .env file found")
    else:
        print("   ⚠️ .env file not found - credentials may be missing")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    if is_trading_day and is_market_hours:
        print("✅ All systems ready!")
        print("🚀 The scheduler will START the algorithm NOW")
    elif is_trading_day and not is_market_hours:
        print("✅ All systems ready!")
        print("⏰ The scheduler will start the algorithm at 9:15 AM")
    elif not is_trading_day:
        print("✅ All systems ready!")
        print("📅 The scheduler will start on the next trading day")
    
    print("\n💡 To start the scheduler, run:")
    print("   python auto_trader_scheduler.py")
    print("   OR double-click START_AUTO_TRADER.bat")
    
    return True

if __name__ == "__main__":
    success = test_scheduler()
    sys.exit(0 if success else 1)
