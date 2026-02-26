#!/usr/bin/env python3
"""
🤖 GITHUB ACTIONS RUNNER
Runs the FULL trading session exactly like local execution
Includes Telegram notifications and HTML report generation
"""

import sys
import os
from datetime import datetime
from high_accuracy_algo import HighAccuracyAlgo

def main():
    print("=" * 60)
    print("🤖 GITHUB ACTIONS - AUTO TRADING BOT")
    print("=" * 60)
    print(f"⏰ Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print("=" * 60)
    
    # Check if it's a trading day and market hours
    now = datetime.now()
    is_weekday = now.weekday() < 5
    current_time = now.time()
    
    from datetime import time as dt_time
    market_open = dt_time(9, 15)
    market_close = dt_time(15, 30)
    is_market_hours = market_open <= current_time <= market_close
    
    if not is_weekday:
        print("📅 Weekend - No trading")
        return
    
    if not is_market_hours:
        print("⏰ Outside market hours (9:15 AM - 3:30 PM)")
        return
    
    print("✅ Market is open - Starting FULL trading session...")
    print()
    
    # Initialize algorithm with CURRENT strategy (same as local)
    capital = 100000
    strategy_mode = "CURRENT"  # High accuracy mode (score >= 90)
    
    print(f"🎯 HIGH ACCURACY OPTIONS TRADING ALGORITHM")
    print(f"💰 Capital: ₹{capital:,}")
    print(f"📊 Strategy: {strategy_mode} (Min Score: 90/100)")
    print(f"⏰ Session: 9:15 AM - 3:30 PM")
    print("=" * 60)
    print()
    
    algo = HighAccuracyAlgo(initial_capital=capital, strategy_mode=strategy_mode)
    
    try:
        # Run the FULL session (exactly like local run)
        print("🚀 Starting full trading session (continuous monitoring)...")
        algo.run_high_accuracy_session()
        
        print()
        print("=" * 60)
        print("✅ TRADING SESSION COMPLETED")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
