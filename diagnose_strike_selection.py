#!/usr/bin/env python3
"""
🔍 STRIKE SELECTION DIAGNOSTIC TOOL
Helps identify why no strikes are being selected
"""

import sys
import os
from high_accuracy_algo import HighAccuracyAlgo
from datetime import datetime
import json

def main():
    print("🔍 STRIKE SELECTION DIAGNOSTIC TOOL")
    print("=" * 60)
    
    # Initialize algorithm
    algo = HighAccuracyAlgo(initial_capital=100000, strategy_mode='CURRENT')
    
    print("\n🔐 Attempting login...")
    if not algo.login():
        print("❌ Login failed. Cannot proceed with diagnosis.")
        return
    
    print("✅ Login successful!")
    
    # Fetch market data
    print("\n📊 Fetching market data...")
    algo.get_comprehensive_market_data()
    
    print(f"\n📈 Current Nifty Price: {algo.last_nifty_price:.2f}")
    print(f"📊 Market Data Points: {len(algo.market_data)}")
    
    if not algo.market_data:
        print("❌ No market data available. Check your connection or market hours.")
        return
    
    print("\n" + "=" * 60)
    print("📋 DETAILED STRIKE ANALYSIS")
    print("=" * 60)
    
    # Analyze each strike
    valid_strikes = 0
    total_strikes = 0
    
    for symbol, data in algo.market_data.items():
        total_strikes += 1
        strike = data['strike']
        ltp = data['ltp']
        option_type = data['option_type']
        
        # Calculate distance from current price
        distance = abs(strike - algo.last_nifty_price)
        
        # Check if it has valid data
        has_data = ltp > 0
        
        # Apply algorithm's filtering logic
        if has_data:
            # Premium filter (updated to match algorithm changes)
            premium_ok = 10 <= ltp <= 150  # Changed from 15-70 to 10-150
            
            # Distance filter based on premium (updated to match algorithm changes)
            if ltp <= 40:
                max_distance = 800  # Increased from 400
                category = "Optimal"
            elif ltp <= 50:
                max_distance = 600  # Increased from 200
                category = "Acceptable"
            elif ltp <= 70:
                max_distance = 400  # Increased from 100
                category = "Risky"
            else:
                max_distance = 200  # Increased from 50
                category = "Rejected"
            
            distance_ok = distance <= max_distance
            
            if premium_ok and distance_ok:
                valid_strikes += 1
                status = "✅ VALID"
            else:
                status = "❌ FILTERED"
                if not premium_ok:
                    status += f" (Premium: ₹{ltp:.2f} not in ₹10-150 range)"
                if not distance_ok:
                    status += f" (Distance: {distance:.0f} > {max_distance} for {category})"
        else:
            status = "⚠️ NO DATA"
        
        print(f"{strike:>5} {option_type}: ₹{ltp:>6.2f} | Dist: {distance:>3.0f} | {status}")
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total Strikes: {total_strikes}")
    print(f"Valid Strikes: {valid_strikes}")
    print(f"Success Rate: {(valid_strikes/total_strikes*100):.1f}%")
    
    if valid_strikes == 0:
        print("\n🚨 DIAGNOSIS: NO VALID STRIKES FOUND")
        print("\nPossible reasons:")
        print("1. Current Nifty price calculation is incorrect")
        print("2. All strikes are too far OTM (out of the money)")
        print("3. Premium levels are outside the ₹10-150 range")
        print("4. Market data is stale or incomplete")
        
        print(f"\n💡 SUGGESTIONS:")
        print(f"• Current calculated Nifty: {algo.last_nifty_price:.2f}")
        print(f"• Check if this matches actual Nifty 50 index price")
        print(f"• If incorrect, the CE-PE parity calculation may be failing")
        print(f"• Try running during active market hours (9:15 AM - 3:30 PM)")
    else:
        print(f"\n✅ Found {valid_strikes} valid strikes for trading")
    
    # Show recent price history
    if algo.price_history:
        print(f"\n📈 RECENT PRICE HISTORY:")
        for i, price_data in enumerate(algo.price_history[-5:]):
            print(f"  {i+1}. {price_data['timestamp'].strftime('%H:%M:%S')}: ₹{price_data['nifty']:.2f}")

if __name__ == "__main__":
    main()