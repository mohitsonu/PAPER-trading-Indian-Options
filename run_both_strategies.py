#!/usr/bin/env python3
"""
🎯 DUAL STRATEGY RUNNER
Run BOTH strategies simultaneously for easy comparison
"""

import threading
import time
from datetime import datetime
from high_accuracy_algo import HighAccuracyAlgo

def run_strategy(strategy_name, strategy_mode, capital):
    """Run a single strategy in its own thread"""
    print(f"\n🚀 Starting {strategy_name}...")
    
    try:
        algo = HighAccuracyAlgo(
            initial_capital=capital,
            strategy_mode=strategy_mode
        )
        
        # Override CSV filename to separate strategies
        algo.csv_file = f"{strategy_mode.lower()}_trades_{datetime.now().strftime('%Y%m%d')}.csv"
        algo.json_file = f"{strategy_mode.lower()}_updates_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Reinitialize files with new names
        algo.initialize_files()
        
        print(f"✅ {strategy_name} initialized")
        print(f"   📄 CSV: {algo.csv_file}")
        print(f"   📄 JSON: {algo.json_file}")
        
        # Run the strategy
        algo.run_high_accuracy_session()
        
    except Exception as e:
        print(f"❌ Error in {strategy_name}: {e}")

def main():
    print("=" * 80)
    print("🎯 DUAL STRATEGY RUNNER - Run Both Strategies Simultaneously")
    print("=" * 80)
    print()
    print("This will run BOTH strategies at the same time:")
    print()
    print("📊 STRATEGY 1: CURRENT (Complex)")
    print("   - 12 components, 260 points, min score 90")
    print("   - File: current_trades_YYYYMMDD.csv")
    print()
    print("📊 STRATEGY 2: SIMPLIFIED (Price Action)")
    print("   - 6 components, 100 points, min score 70")
    print("   - File: simplified_trades_YYYYMMDD.csv")
    print()
    print("Both will trade the same market data and you can compare results!")
    print("=" * 80)
    print()
    
    confirm = input("Start both strategies? (y/n, default=y): ").strip().lower() or 'y'
    
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    capital = 100000  # ₹1,00,000 for each strategy
    
    print("\n🚀 Starting both strategies...")
    print("=" * 80)
    
    # Create threads for each strategy
    thread1 = threading.Thread(
        target=run_strategy,
        args=("CURRENT Strategy", "CURRENT", capital),
        daemon=False
    )
    
    thread2 = threading.Thread(
        target=run_strategy,
        args=("SIMPLIFIED Strategy", "SIMPLIFIED", capital),
        daemon=False
    )
    
    # Start both threads
    thread1.start()
    time.sleep(2)  # Small delay to avoid API conflicts
    thread2.start()
    
    print("\n✅ Both strategies are running!")
    print("📊 Check the CSV files to compare results:")
    print(f"   - current_trades_{datetime.now().strftime('%Y%m%d')}.csv")
    print(f"   - simplified_trades_{datetime.now().strftime('%Y%m%d')}.csv")
    print()
    print("⏳ Waiting for both strategies to complete...")
    print("=" * 80)
    
    # Wait for both threads to complete
    thread1.join()
    thread2.join()
    
    print("\n" + "=" * 80)
    print("✅ Both strategies completed!")
    print("=" * 80)
    print()
    print("📊 COMPARE RESULTS:")
    print(f"   1. Open: current_trades_{datetime.now().strftime('%Y%m%d')}.csv")
    print(f"   2. Open: simplified_trades_{datetime.now().strftime('%Y%m%d')}.csv")
    print(f"   3. Compare: Trades, Win Rate, P&L")
    print()
    print("💡 TIP: Use Excel or a diff tool to compare side-by-side!")
    print("=" * 80)

if __name__ == "__main__":
    main()
