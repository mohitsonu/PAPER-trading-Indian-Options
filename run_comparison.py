#!/usr/bin/env python3
"""
🎯 STRATEGY COMPARISON RUNNER
Run both strategies side-by-side to compare performance
"""

import sys
import os
from datetime import datetime

print("=" * 80)
print("🎯 STRATEGY COMPARISON RUNNER")
print("=" * 80)
print()
print("Which strategy do you want to run?")
print()
print("1. Current Strategy (Complex - 12 indicators, 260 points)")
print("2. Simplified Strategy (Price Action - 6 components, 100 points)")
print("3. Run BOTH (Compare side-by-side)")
print()

choice = input("Enter your choice (1/2/3): ").strip()

if choice == "1":
    print("\n✅ Running CURRENT STRATEGY...")
    print("   File: high_accuracy_algo.py")
    print("   Scoring: 12 components, 260 points")
    print("   Min Score: 90")
    print()
    os.system("python run_high_accuracy.py")

elif choice == "2":
    print("\n✅ Running SIMPLIFIED STRATEGY...")
    print("   File: simplified_hybrid_algo.py")
    print("   Scoring: 6 components, 100 points")
    print("   Min Score: 70")
    print()
    # Need to create run file for simplified
    print("⚠️ Simplified strategy needs integration first!")
    print("   Run: python integrate_simplified.py")

elif choice == "3":
    print("\n✅ Running BOTH STRATEGIES...")
    print()
    print("📊 STRATEGY 1: Current (Complex)")
    print("   Will save to: current_trades_YYYYMMDD.csv")
    print()
    print("📊 STRATEGY 2: Simplified (Price Action)")
    print("   Will save to: simplified_trades_YYYYMMDD.csv")
    print()
    print("⚠️ This feature needs implementation!")
    print("   I'll create it now...")

else:
    print("\n❌ Invalid choice!")
    sys.exit(1)
