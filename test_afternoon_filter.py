"""
Test script to demonstrate afternoon trading filter logic
"""
from datetime import datetime

def test_afternoon_filter():
    """Simulate afternoon trading filter with different scenarios"""
    
    print("=" * 80)
    print("🧪 TESTING AFTERNOON TRADING FILTER")
    print("=" * 80)
    
    # Test scenarios
    scenarios = [
        # (hour, minute, market_condition, score, should_allow)
        (10, 30, 'TRENDING', 80, True, "Morning + Trending"),
        (11, 45, 'CHOPPY', 60, False, "Morning + Choppy (blocked by choppy filter)"),
        (13, 30, 'TRENDING', 75, True, "1:30 PM + Trending"),
        (14, 0, 'TRENDING', 70, False, "2:00 PM + Weak Trend (score < 75)"),
        (14, 0, 'STRONG_UPTREND', 80, True, "2:00 PM + Strong Uptrend"),
        (14, 15, 'STRONG_DOWNTREND', 78, True, "2:15 PM + Strong Downtrend"),
        (14, 15, 'TRENDING', 72, False, "2:15 PM + Normal Trend (not strong)"),
        (14, 15, 'RANGE_BOUND', 65, False, "2:15 PM + Range Bound"),
        (14, 15, 'CHOPPY', 60, False, "2:15 PM + Choppy"),
        (14, 30, 'STRONG_UPTREND', 85, False, "2:30 PM + Strong Trend (too late!)"),
        (14, 45, 'STRONG_UPTREND', 90, False, "2:45 PM + Strong Trend (market closing)"),
    ]
    
    print("\n📋 TEST SCENARIOS:\n")
    
    for hour, minute, condition, score, expected, description in scenarios:
        # Time check
        is_after_2pm = hour >= 14 and minute >= 0
        is_after_230pm = hour > 14 or (hour == 14 and minute >= 30)
        
        # Market condition check
        is_strong_trend = (
            condition in ['STRONG_UPTREND', 'STRONG_DOWNTREND'] and
            score >= 75
        )
        is_choppy = condition == 'CHOPPY'
        is_weak_range = condition == 'RANGE_BOUND' and score < 65
        
        # Decision logic
        if is_after_230pm:
            should_allow = False
            reason = "After 2:30 PM - Market closing"
        elif is_choppy:
            should_allow = False
            reason = "Choppy market"
        elif is_weak_range:
            should_allow = False
            reason = "Weak ranging market"
        elif is_after_2pm and not is_strong_trend:
            should_allow = False
            reason = "After 2 PM without strong trend"
        else:
            should_allow = True
            reason = "All filters passed"
        
        # Result
        result = "✅ ALLOW" if should_allow else "❌ BLOCK"
        match = "✓" if should_allow == expected else "✗ MISMATCH"
        
        print(f"{match} {result} | {hour:02d}:{minute:02d} | {condition:20s} | Score: {score:2d} | {description}")
        print(f"   Reason: {reason}")
        print()
    
    print("=" * 80)
    print("📊 FILTER LOGIC SUMMARY")
    print("=" * 80)
    print("""
🕐 TIME FILTERS:
   ✅ 9:30 AM - 2:00 PM: Normal trading (if market suitable)
   ⚠️  2:00 PM - 2:30 PM: Only STRONG trends (score ≥ 75)
   ❌ After 2:30 PM: NO TRADING (too close to close)
   ❌ Before 9:30 AM: NO TRADING (opening volatility)

📈 MARKET CONDITION FILTERS:
   ✅ STRONG_UPTREND (score ≥ 75): Allowed anytime before 2:30 PM
   ✅ STRONG_DOWNTREND (score ≥ 75): Allowed anytime before 2:30 PM
   ⚠️  TRENDING (score < 75): Only before 2:00 PM
   ❌ CHOPPY: Never allowed
   ❌ RANGE_BOUND (score < 65): Never allowed
   ⚠️  RANGE_BOUND (score ≥ 65): Only before 2:00 PM

🎯 AFTERNOON TRADING RULES (2:00 PM - 2:30 PM):
   Required: STRONG_UPTREND or STRONG_DOWNTREND
   Required: Score ≥ 75
   Reason: Afternoon sessions are choppy - only trade strong trends
    """)
    
    print("=" * 80)
    print("💡 TODAY'S ANALYSIS (NOV 28)")
    print("=" * 80)
    print("""
📉 WHAT HAPPENED:
   Trade 4: 2:15 PM - Lost ₹910 (STOP_LOSS in 18 mins)
   Trade 5: 2:09 PM - Lost ₹584 (END_OF_DAY)
   Total Afternoon Loss: ₹1,494

🔍 WHY THEY WOULD BE BLOCKED:
   - Market was CHOPPY/RANGING after 2 PM
   - Not a STRONG trend (score likely < 75)
   - Both trades on 26000 PE (same losing strike)

✅ WITH NEW FILTER:
   - Both trades would be BLOCKED
   - Would save ₹1,494
   - Final P&L: +₹1,721 instead of +₹226
    """)

if __name__ == "__main__":
    test_afternoon_filter()
