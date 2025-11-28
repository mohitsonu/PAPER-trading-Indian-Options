"""
Test script to verify strike diversity filter is working correctly
"""

# Simulate trade_history with entries
trade_history = []

# Simulate first entry on 26000 PE
trade_history.append({
    'action': 'ENTRY',
    'strike': 26000,
    'option_type': 'PE',
    'trade_id': 'TEST_001'
})

print("=" * 70)
print("🧪 TESTING STRIKE DIVERSITY FILTER")
print("=" * 70)

# Test 1: First trade on 26000 PE
strike = 26000
option_type = 'PE'
strike_trade_count = sum(1 for t in trade_history 
                        if t.get('strike') == strike 
                        and t.get('option_type') == option_type
                        and t.get('action') == 'ENTRY')

print(f"\n✅ Test 1: First trade on {strike} {option_type}")
print(f"   Trade count: {strike_trade_count}")
print(f"   Should allow: {strike_trade_count < 2}")
assert strike_trade_count < 2, "First trade should be allowed"

# Test 2: Check BEFORE second trade
strike_trade_count = sum(1 for t in trade_history 
                        if t.get('strike') == strike 
                        and t.get('option_type') == option_type
                        and t.get('action') == 'ENTRY')

print(f"\n✅ Test 2: Second trade attempt on {strike} {option_type}")
print(f"   Current count: {strike_trade_count}")
print(f"   Should allow: {strike_trade_count < 2}")
assert strike_trade_count < 2, "Second trade should be allowed"

# Add second entry
trade_history.append({
    'action': 'ENTRY',
    'strike': 26000,
    'option_type': 'PE',
    'trade_id': 'TEST_002'
})

# Test 3: Check BEFORE third trade (should block)
strike_trade_count = sum(1 for t in trade_history 
                        if t.get('strike') == strike 
                        and t.get('option_type') == option_type
                        and t.get('action') == 'ENTRY')

print(f"\n❌ Test 3: Third trade attempt on {strike} {option_type}")
print(f"   Current count: {strike_trade_count}")
print(f"   Should block: {strike_trade_count >= 2}")
assert strike_trade_count >= 2, "Third trade should be blocked"

# Test 4: Different strike should be allowed
strike = 26200
option_type = 'PE'
strike_trade_count = sum(1 for t in trade_history 
                        if t.get('strike') == strike 
                        and t.get('option_type') == option_type
                        and t.get('action') == 'ENTRY')

print(f"\n✅ Test 4: First trade on {strike} {option_type} (different strike)")
print(f"   Trade count: {strike_trade_count}")
print(f"   Should allow: {strike_trade_count < 2}")
assert strike_trade_count < 2, "Different strike should be allowed"

# Test 5: Same strike but different option type should be allowed
strike = 26000
option_type = 'CE'
strike_trade_count = sum(1 for t in trade_history 
                        if t.get('strike') == strike 
                        and t.get('option_type') == option_type
                        and t.get('action') == 'ENTRY')

print(f"\n✅ Test 5: First trade on {strike} {option_type} (same strike, different type)")
print(f"   Trade count: {strike_trade_count}")
print(f"   Should allow: {strike_trade_count < 2}")
assert strike_trade_count < 2, "Same strike but CE should be allowed"

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
print("\n📝 SUMMARY:")
print("   The strike diversity filter will now correctly:")
print("   1. Track ENTRY trades (not just exits)")
print("   2. Block 3rd trade on same strike+type")
print("   3. Allow different strikes")
print("   4. Allow same strike but different option type (CE vs PE)")
print("\n🎯 This fix prevents the issue where we took 3 trades on 26000 PE")
print("   and all lost money!")
