#!/usr/bin/env python3
"""
🔍 CHECK CURRENT STRIKES
Verify what strikes should be available for current Nifty level
"""

def main():
    current_nifty = 25041
    print(f"🔍 CURRENT NIFTY ANALYSIS")
    print(f"📈 Current Nifty: {current_nifty}")
    print("=" * 50)
    
    # Calculate ideal strike range
    atm_strike = round(current_nifty / 50) * 50  # Round to nearest 50
    
    print(f"\n📊 IDEAL STRIKE RANGE:")
    print(f"ATM Strike: {atm_strike}")
    
    # Show strikes that should be available
    strikes_needed = []
    for i in range(-10, 11):  # 10 strikes above and below ATM
        strike = atm_strike + (i * 50)
        distance = abs(strike - current_nifty)
        
        if distance <= 500:  # Within 500 points
            strikes_needed.append(strike)
            
    print(f"\n✅ STRIKES THAT SHOULD BE AVAILABLE:")
    for strike in strikes_needed:
        distance = abs(strike - current_nifty)
        if distance <= 100:
            status = "🎯 ATM"
        elif distance <= 200:
            status = "✅ Near ATM"
        elif distance <= 300:
            status = "⚠️ OTM"
        else:
            status = "❌ Far OTM"
            
        print(f"  {strike}: Distance {distance:3.0f} pts | {status}")
    
    print(f"\n🚨 CURRENT ALGORITHM STRIKES:")
    current_strikes = list(range(25400, 26900, 50))
    print(f"Available: {current_strikes[0]} to {current_strikes[-1]}")
    print(f"Closest to Nifty: {current_strikes[0]} (Distance: {current_strikes[0] - current_nifty} pts)")
    
    print(f"\n💡 SOLUTION:")
    print(f"The algorithm needs strikes around {atm_strike-250} to {atm_strike+250}")
    print(f"Current strikes start from {current_strikes[0]} - too far!")
    
    # Check if we need to change expiry or strike range
    print(f"\n🔧 RECOMMENDATIONS:")
    print(f"1. Check if there are strikes below 25400 available")
    print(f"2. The algorithm should look for strikes: 24800, 24850, 24900, 24950, 25000, 25050, 25100, 25150, 25200")
    print(f"3. Current closest strike (25400) is {current_strikes[0] - current_nifty} points away - too far for good trading")

if __name__ == "__main__":
    main()