#!/usr/bin/env python3
"""
🎯 Single Strategy Runner
Run only ONE strategy (CURRENT or SIMPLIFIED)
"""

import sys
from high_accuracy_algo import HighAccuracyAlgo
from datetime import datetime
import json
import os

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None

def main():
    """Main runner for single strategy"""
    
    print("🎯 SINGLE STRATEGY RUNNER", flush=True)
    print("=" * 70, flush=True)
    sys.stdout.flush()
    
    print("\nWhich strategy do you want to run?", flush=True)
    print(flush=True)
    print("1. CURRENT (Complex - Min Score 90)", flush=True)
    print("2. SIMPLIFIED (Price Action - Min Score 70)", flush=True)
    print(flush=True)
    
    choice = input("Enter your choice (1/2): ").strip()
    
    if choice == "1":
        strategy_mode = "CURRENT"
        strategy_name = "CURRENT Strategy (Complex)"
    elif choice == "2":
        strategy_mode = "SIMPLIFIED"
        strategy_name = "SIMPLIFIED Strategy (Price Action)"
    else:
        print("❌ Invalid choice!", flush=True)
        return
    
    print(f"\n✅ Running {strategy_name}", flush=True)
    print("=" * 70, flush=True)
    sys.stdout.flush()
    
    # Check for persisted capital
    capital_file = "capital_persistence.json"
    persisted_capital = None
    
    if os.path.exists(capital_file):
        try:
            with open(capital_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                persisted_capital = data.get('current_capital')
                total_pnl = data.get('total_pnl', 0)
                session_date = data.get('session_date', 'Unknown')
                
                print(f"\n💾 CAPITAL PERSISTENCE FOUND:", flush=True)
                print(f"📅 Last Session: {session_date}", flush=True)
                print(f"💰 Previous Capital: ₹{persisted_capital:,.2f}", flush=True)
                print(f"📈 Total P&L: ₹{total_pnl:+,.2f}", flush=True)
        except:
            pass
    
    capital = 100000  # Fixed ₹1,00,000 capital
    
    print(f"\n🚀 STARTING {strategy_name.upper()}", flush=True)
    print(f"💰 Capital: ₹{capital:,}", flush=True)
    print(f"⏰ Trading Hours: 9:15 AM to 3:30 PM (Automatic)", flush=True)
    print(f"📅 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    sys.stdout.flush()
    
    print(f"\n⏳ Initializing algorithm...", flush=True)
    sys.stdout.flush()
    
    # Initialize and run algorithm
    algo = HighAccuracyAlgo(initial_capital=capital, strategy_mode=strategy_mode)
    
    print(f"\n✅ Algorithm initialized! Starting trading session...", flush=True)
    sys.stdout.flush()
    
    try:
        algo.run_high_accuracy_session()
    except KeyboardInterrupt:
        print(f"\n🛑 Session stopped by user", flush=True)
    except Exception as e:
        print(f"\n❌ Error occurred: {e}", flush=True)
    
    print(f"\n📊 Session completed!", flush=True)
    print(f"Check results: python view_high_accuracy_results.py", flush=True)

if __name__ == "__main__":
    main()
