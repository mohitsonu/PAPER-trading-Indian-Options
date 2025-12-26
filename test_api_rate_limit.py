#!/usr/bin/env python3
"""
Test if API rate limit fix works
"""

from high_accuracy_algo import HighAccuracyAlgo
import time

print("=" * 70)
print("🧪 TESTING API RATE LIMIT FIX")
print("=" * 70)
print()

print("Initializing algo...")
algo = HighAccuracyAlgo(initial_capital=100000)

print("\n✅ Algo initialized")
print("\nLogging in...")

if algo.login():
    print("✅ Login successful")
    
    print("\n🔍 Testing market data fetch (Cycle 1)...")
    start = time.time()
    data1 = algo.get_comprehensive_market_data()
    elapsed1 = time.time() - start
    
    if data1:
        print(f"✅ Cycle 1: Got {len(data1)} options in {elapsed1:.1f}s")
    else:
        print(f"❌ Cycle 1: No data (took {elapsed1:.1f}s)")
    
    print("\n⏳ Waiting 10 seconds before Cycle 2...")
    time.sleep(10)
    
    print("\n🔍 Testing market data fetch (Cycle 2)...")
    start = time.time()
    data2 = algo.get_comprehensive_market_data()
    elapsed2 = time.time() - start
    
    if data2:
        print(f"✅ Cycle 2: Got {len(data2)} options in {elapsed2:.1f}s")
    else:
        print(f"❌ Cycle 2: No data (took {elapsed2:.1f}s)")
    
    print("\n" + "=" * 70)
    if data1 and data2:
        print("✅ TEST PASSED: API rate limit fix working!")
    else:
        print("❌ TEST FAILED: Still hitting rate limits")
    print("=" * 70)
else:
    print("❌ Login failed")
