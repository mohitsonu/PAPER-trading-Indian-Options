#!/usr/bin/env python3
"""
🔧 QUICK FIX: Strike Selection Issue
Temporarily adjusts filters to allow trading with current market conditions
"""

import sys
import os
from high_accuracy_algo import HighAccuracyAlgo
from datetime import datetime

def main():
    print("🔧 STRIKE SELECTION QUICK FIX")
    print("=" * 50)
    
    # Initialize algorithm
    algo = HighAccuracyAlgo(initial_capital=100000, strategy_mode='CURRENT')
    
    print("\n🔐 Attempting login...")
    if not algo.login():
        print("❌ Login failed. Cannot proceed.")
        return
    
    print("✅ Login successful!")
    
    # Fetch market data
    print("\n📊 Fetching market data...")
    algo.get_comprehensive_market_data()
    
    current_nifty = algo.last_nifty_price
    print(f"\n📈 Current Nifty Price: {current_nifty:.2f}")
    
    # TEMPORARY FIX: Adjust filters for current market conditions
    print("\n🔧 APPLYING TEMPORARY FIXES:")
    
    # Fix 1: Expand premium range
    original_min_premium = 15
    original_max_premium = 70
    new_min_premium = 10  # Allow lower premiums
    new_max_premium = 150  # Allow higher premiums
    
    print(f"1. Premium Range: ₹{original_min_premium}-{original_max_premium} → ₹{new_min_premium}-{new_max_premium}")
    
    # Fix 2: Expand distance limits
    print("2. Distance Limits: Relaxed for current market")
    
    # Fix 3: Check what strikes would be valid with relaxed filters
    valid_strikes = []
    
    for symbol, data in algo.market_data.items():
        strike = data['strike']
        ltp = data['ltp']
        option_type = data['option_type']
        
        if ltp <= 0:
            continue
            
        distance = abs(strike - current_nifty)
        
        # Apply relaxed filters
        premium_ok = new_min_premium <= ltp <= new_max_premium
        
        # Relaxed distance filter
        if ltp <= 50:
            max_distance = 800  # Increased from 400
        elif ltp <= 100:
            max_distance = 600  # Increased from 200
        else:
            max_distance = 400  # Increased from 100
            
        distance_ok = distance <= max_distance
        
        if premium_ok and distance_ok:
            valid_strikes.append({
                'symbol': symbol,
                'strike': strike,
                'type': option_type,
                'ltp': ltp,
                'distance': distance
            })
    
    print(f"\n✅ RESULTS WITH RELAXED FILTERS:")
    print(f"Valid Strikes Found: {len(valid_strikes)}")
    
    if valid_strikes:
        print("\n📋 TOP VALID STRIKES:")
        # Sort by distance (closest to current price first)
        valid_strikes.sort(key=lambda x: x['distance'])
        
        for i, strike in enumerate(valid_strikes[:10]):  # Show top 10
            print(f"{i+1:2d}. {strike['strike']} {strike['type']}: ₹{strike['ltp']:>6.2f} | Dist: {strike['distance']:>3.0f}")
        
        print(f"\n💡 RECOMMENDATION:")
        print(f"The algorithm can now find {len(valid_strikes)} valid strikes.")
        print(f"Consider running the main algorithm with these relaxed parameters.")
        
        # Show how to implement the fix
        print(f"\n🔧 TO IMPLEMENT THIS FIX:")
        print(f"1. Edit high_accuracy_algo.py")
        print(f"2. Find the premium filter section (around line 1950)")
        print(f"3. Change premium range from ₹15-70 to ₹10-150")
        print(f"4. Increase distance limits by 2x")
        
    else:
        print(f"\n❌ Even with relaxed filters, no valid strikes found.")
        print(f"This suggests a deeper issue with market data or expiry selection.")
        
        # Check if we need different strikes
        closest_strikes = []
        for symbol, data in algo.market_data.items():
            if data['ltp'] > 0:
                distance = abs(data['strike'] - current_nifty)
                closest_strikes.append((data['strike'], distance, data['option_type'], data['ltp']))
        
        closest_strikes.sort(key=lambda x: x[1])  # Sort by distance
        
        print(f"\n📊 CLOSEST AVAILABLE STRIKES:")
        for i, (strike, dist, opt_type, ltp) in enumerate(closest_strikes[:5]):
            print(f"{i+1}. {strike} {opt_type}: ₹{ltp:.2f} (Distance: {dist:.0f})")
        
        print(f"\n💡 SOLUTION:")
        print(f"You may need strikes closer to {current_nifty:.0f}")
        print(f"Current strikes start from {closest_strikes[0][0]} (too far)")

if __name__ == "__main__":
    main()