#!/usr/bin/env python3
"""
🎯 High Accuracy Options Trading Algorithm Runner
Quick start script for quality-focused trading
"""

from high_accuracy_algo import HighAccuracyAlgo
from datetime import datetime
import json

def main():
    """Main runner for high accuracy trading"""
    
    print("🎯 HIGH ACCURACY OPTIONS TRADING ALGORITHM")
    print("=" * 70)
    print("🎪 DESIGNED FOR QUALITY TRADES WITH ₹20 BROKER CHARGES")
    print("=" * 70)
    
    # Configuration is built into the algorithm
    print("✅ Using built-in high accuracy configuration")
    
    # Check for persisted capital
    import os
    capital_file = "capital_persistence.json"
    persisted_capital = None
    
    if os.path.exists(capital_file):
        try:
            with open(capital_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                persisted_capital = data.get('current_capital')
                total_pnl = data.get('total_pnl', 0)
                session_date = data.get('session_date', 'Unknown')
                
                print(f"\n💾 CAPITAL PERSISTENCE FOUND:")
                print(f"📅 Last Session: {session_date}")
                print(f"💰 Previous Capital: ₹{persisted_capital:,.2f}")
                print(f"📈 Total P&L: ₹{total_pnl:+,.2f}")
                print(f"🔄 Will continue with persisted capital")
        except:
            pass
    
    if not persisted_capital:
        print(f"\n🆕 FIRST SESSION - Starting with fresh capital")
    
    print(f"\n📋 ALGORITHM SETTINGS:")
    print(f"💰 Capital: {'₹{:,.2f} (Persisted)'.format(persisted_capital) if persisted_capital else '₹1,00,000 (Initial)'}")
    print(f"💸 Broker Charges: ₹20 per trade")
    print(f"🎯 Min Accuracy Score: 85/100")
    print(f"📊 Max Positions: 3")
    print(f"🛡️ Risk per Trade: 3%")
    print(f"📈 Target R:R: 2.67:1 (30% SL, 80% Target)")
    print(f"⏰ Max Holding: 4 hours")
    print(f"🎪 Target: 1-10 quality trades per day")
    
    print(f"\n🔍 STRICT ENTRY CRITERIA:")
    print(f"• Minimum ₹30 premium (covers broker charges)")
    print(f"• Minimum 5 lakh OI for liquidity")
    print(f"• Minimum 1000 volume")
    print(f"• Maximum ₹5 bid-ask spread")
    print(f"• 70% trend strength required")
    print(f"• 70% market confidence required")
    
    # Default settings
    capital = 100000  # Fixed ₹1,00,000 capital
    
    print(f"\n🚀 STARTING HIGH ACCURACY TRADING SESSION")
    print(f"💰 Capital: ₹{capital:,} (Fixed)")
    print(f"⏰ Trading Hours: 9:15 AM to 3:30 PM (Automatic)")
    print(f"📅 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize and run algorithm
    algo = HighAccuracyAlgo(initial_capital=capital)
    
    try:
        algo.run_high_accuracy_session()  # No duration needed - automatic trading hours
    except KeyboardInterrupt:
        print(f"\n🛑 Session stopped by user")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
    
    print(f"\n📊 Session completed. Check results with:")
    print(f"   python view_high_accuracy_results.py")

if __name__ == "__main__":
    main()