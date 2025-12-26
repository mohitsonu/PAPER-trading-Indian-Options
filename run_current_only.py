#!/usr/bin/env python3
"""
🎯 Run HIGH ACCURACY Strategy Only (No Rate Limits)
Single strategy = Half the API calls
"""

import sys
from high_accuracy_algo import HighAccuracyAlgo
from datetime import datetime

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None

def main():
    """Run HIGH ACCURACY strategy only"""
    
    print("🎯 HIGH ACCURACY TRADING - HIGH ACCURACY STRATEGY", flush=True)
    print("=" * 70, flush=True)
    print("📊 Running single strategy to avoid API rate limits", flush=True)
    print("=" * 70, flush=True)
    sys.stdout.flush()
    
    capital = 100000
    
    print(f"\n🚀 STARTING CURRENT STRATEGY", flush=True)
    print(f"💰 Capital: ₹{capital:,}", flush=True)
    print(f"⏰ Trading Hours: 9:15 AM to 3:30 PM", flush=True)
    print(f"📅 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print(f"🎯 Min Score: 90/100", flush=True)
    print("=" * 70, flush=True)
    sys.stdout.flush()
    
    print(f"\n⏳ Initializing algorithm...", flush=True)
    sys.stdout.flush()
    
    # Initialize with CURRENT mode
    algo = HighAccuracyAlgo(initial_capital=capital, strategy_mode='CURRENT')
    
    print(f"\n✅ Algorithm initialized! Starting trading...", flush=True)
    sys.stdout.flush()
    
    try:
        algo.run_high_accuracy_session()
    except KeyboardInterrupt:
        print(f"\n🛑 Session stopped by user", flush=True)
    except Exception as e:
        print(f"\n❌ Error occurred: {e}", flush=True)
        import traceback
        traceback.print_exc()
    
    print(f"\n📊 Session completed!", flush=True)

if __name__ == "__main__":
    main()
