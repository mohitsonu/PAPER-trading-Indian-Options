#!/usr/bin/env python3
"""
🎯 Options Trading Algorithm
Choose your strategy: CONTRARIAN, SCALPER, or TREND RIDER
"""

import sys
from high_accuracy_algo import HighAccuracyAlgo
from datetime import datetime
import json
import os

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None

def main():
    """Main runner for high accuracy trading"""
    
    print("🎯 HIGH ACCURACY OPTIONS TRADING ALGORITHM", flush=True)
    print("=" * 70, flush=True)
    sys.stdout.flush()
    
    # Multi-strategy mode - Only profitable strategies enabled!
    print("\n📊 OPTIMIZED STRATEGY (Based on Performance Analysis):", flush=True)
    print(flush=True)
    print("   ✅ CONTRARIAN - Counter-trend trades (ONLY PROFITABLE STRATEGY)", flush=True)
    print("      • Win Rate: 41.3% | Total P&L: +₹23,346", flush=True)
    print("      • 121 trades analyzed | Risk:Reward: 1:1.24", flush=True)
    print(flush=True)
    print("   ❌ DISABLED (All losing strategies removed):", flush=True)
    print("      • SCALPER: -₹23,201 (31% WR)", flush=True)
    print("      • TREND_BEAR_PE: -₹22,151 (26.7% WR)", flush=True)
    print("      • SUPPORT_BOUNCE: -₹9,285 (12.5% WR)", flush=True)
    print("      • TREND_BULL_CE: -₹8,794 (27.3% WR)", flush=True)
    print("      • TREND_RIDER: -₹3,471 (33.3% WR)", flush=True)
    print("      • RESISTANCE_BOUNCE: -₹1,165 (0% WR)", flush=True)
    print(flush=True)
    print("💡 Algorithm now uses ONLY CONTRARIAN strategy", flush=True)
    print("   All losing strategies have been disabled based on data analysis.", flush=True)
    print(flush=True)
    
    strategy_mode = "CURRENT"  # Use CURRENT mode for higher quality (score 90)
    strategy_name = "HIGH ACCURACY"
    min_score = 90  # Minimum score 90 for quality trades
    
    print(f"\n✅ Selected: {strategy_name}", flush=True)
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
    
    # Default settings
    capital = 100000  # Fixed ₹1,00,000 capital
    
    print(f"\n🚀 STARTING {strategy_name.upper()}", flush=True)
    print(f"💰 Capital: ₹{capital:,}", flush=True)
    print(f"🎯 Min Score: {min_score}/100", flush=True)
    print(f"⏰ Trading Hours: 9:15 AM to 3:30 PM (Automatic)", flush=True)
    print(f"📅 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print("=" * 70, flush=True)
    sys.stdout.flush()
    
    print(f"\n⏳ Initializing algorithm...", flush=True)
    sys.stdout.flush()
    
    # Initialize and run algorithm
    algo = HighAccuracyAlgo(initial_capital=capital, strategy_mode=strategy_mode)
    
    print(f"\n✅ Algorithm initialized! Starting trading session...", flush=True)
    sys.stdout.flush()
    
    try:
        # Try to login first
        if algo.login():
            print("🚀 Starting live trading session...")
            algo.run_high_accuracy_session()
        else:
            print("⚠️ Login failed - This could be due to:")
            print("   1. Temporary Shoonya server issues")
            print("   2. Account status (check web login)")
            print("   3. Network connectivity")
            print("   4. API changes by Shoonya")
            print("\n💡 Suggestions:")
            print("   • Try again in a few minutes")
            print("   • Check your Shoonya web login")
            print("   • Contact Shoonya support if issue persists")
            print("   • Check if your account has sufficient balance")
            
    except KeyboardInterrupt:
        print(f"\n🛑 Session stopped by user", flush=True)
    except Exception as e:
        print(f"\n❌ Error occurred: {e}", flush=True)
        import traceback
        traceback.print_exc()
    
    print(f"\n📊 Session completed. Check results with:", flush=True)
    print(f"   python view_high_accuracy_results.py", flush=True)


if __name__ == "__main__":
    main()