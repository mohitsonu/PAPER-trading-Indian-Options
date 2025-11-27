#!/usr/bin/env python3
"""
📊 COMPLETE TRADING HISTORY ANALYSIS
Analyzes all CSV files to determine if algorithm is profitable
"""

import pandas as pd
import glob
from datetime import datetime

print("=" * 80)
print("📊 COMPLETE TRADING HISTORY ANALYSIS")
print("=" * 80)
print()

# Find all CSV files
csv_files = glob.glob("high_accuracy_trades_*.csv")
csv_files.sort()

print(f"Found {len(csv_files)} trading days")
print()

total_pnl = 0
total_trades = 0
winning_days = 0
losing_days = 0
daily_results = []

for csv_file in csv_files:
    try:
        df = pd.read_csv(csv_file)
        
        # Get date from filename
        date_str = csv_file.replace("high_accuracy_trades_", "").replace(".csv", "")
        date = datetime.strptime(date_str, "%Y%m%d").strftime("%b %d")
        
        # Count trades (only exits)
        exits = df[df['action'] == 'EXIT']
        num_trades = len(exits)
        
        # Calculate P&L
        if 'net_pnl_after_charges' in df.columns:
            day_pnl = exits['net_pnl_after_charges'].sum()
        elif 'pnl_after_charges' in df.columns:
            day_pnl = exits['pnl_after_charges'].sum()
        elif 'gross_pnl' in df.columns:
            day_pnl = exits['gross_pnl'].sum() - (num_trades * 40)  # Estimate charges
        else:
            day_pnl = 0
        
        # Get final capital if available
        final_capital = df['capital'].iloc[-1] if 'capital' in df.columns else 100000
        
        # Count wins/losses
        if 'net_pnl_after_charges' in df.columns:
            wins = len(exits[exits['net_pnl_after_charges'] > 0])
            losses = len(exits[exits['net_pnl_after_charges'] < 0])
        elif 'pnl_after_charges' in df.columns:
            wins = len(exits[exits['pnl_after_charges'] > 0])
            losses = len(exits[exits['pnl_after_charges'] < 0])
        else:
            wins = losses = 0
        
        win_rate = (wins / num_trades * 100) if num_trades > 0 else 0
        
        total_pnl += day_pnl
        total_trades += num_trades
        
        if day_pnl > 0:
            winning_days += 1
            status = "✅ WIN"
        else:
            losing_days += 1
            status = "❌ LOSS"
        
        daily_results.append({
            'date': date,
            'trades': num_trades,
            'pnl': day_pnl,
            'capital': final_capital,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'status': status
        })
        
        print(f"{status} {date}: {num_trades:2d} trades | P&L: ₹{day_pnl:+8,.0f} | WR: {win_rate:5.1f}% | Capital: ₹{final_capital:,.0f}")
        
    except Exception as e:
        print(f"❌ Error reading {csv_file}: {e}")

print()
print("=" * 80)
print("📊 OVERALL SUMMARY")
print("=" * 80)
print()

print(f"📅 Trading Days: {len(csv_files)}")
print(f"✅ Winning Days: {winning_days}")
print(f"❌ Losing Days: {losing_days}")
print(f"📊 Win Rate (Days): {winning_days/len(csv_files)*100:.1f}%")
print()

print(f"📈 Total Trades: {total_trades}")
print(f"💰 Total P&L: ₹{total_pnl:+,.2f}")
print(f"📊 Average P&L per Day: ₹{total_pnl/len(csv_files):+,.2f}")
print(f"📊 Average Trades per Day: {total_trades/len(csv_files):.1f}")
print()

# Calculate overall win rate
total_wins = sum(r['wins'] for r in daily_results)
total_losses = sum(r['losses'] for r in daily_results)
overall_win_rate = (total_wins / (total_wins + total_losses) * 100) if (total_wins + total_losses) > 0 else 0

print(f"🎯 Overall Win Rate (Trades): {overall_win_rate:.1f}%")
print(f"✅ Winning Trades: {total_wins}")
print(f"❌ Losing Trades: {total_losses}")
print()

# Best and worst days
if daily_results:
    best_day = max(daily_results, key=lambda x: x['pnl'])
    worst_day = min(daily_results, key=lambda x: x['pnl'])
    
    print(f"🏆 Best Day: {best_day['date']} - ₹{best_day['pnl']:+,.0f}")
    print(f"💔 Worst Day: {worst_day['date']} - ₹{worst_day['pnl']:+,.0f}")
    print()

# Final verdict
print("=" * 80)
print("🎯 VERDICT")
print("=" * 80)
print()

if total_pnl > 0:
    print(f"✅ ALGORITHM IS PROFITABLE")
    print(f"   Total Profit: ₹{total_pnl:+,.2f}")
    print(f"   Return: {total_pnl/100000*100:+.2f}%")
else:
    print(f"❌ ALGORITHM IS LOSING MONEY")
    print(f"   Total Loss: ₹{total_pnl:+,.2f}")
    print(f"   Drawdown: {total_pnl/100000*100:+.2f}%")

print()

# Analysis
print("=" * 80)
print("💡 KEY INSIGHTS")
print("=" * 80)
print()

if overall_win_rate < 50:
    print(f"⚠️ Win rate is LOW ({overall_win_rate:.1f}%)")
    print(f"   Need: Better entry signals or tighter filters")
    print()

if total_trades / len(csv_files) > 20:
    print(f"⚠️ Too many trades per day ({total_trades/len(csv_files):.1f})")
    print(f"   Need: Stricter filters to reduce overtrading")
    print()

if losing_days > winning_days:
    print(f"⚠️ More losing days ({losing_days}) than winning days ({winning_days})")
    print(f"   Need: Better market condition filter")
    print()

# Recommendations
print("=" * 80)
print("🎯 RECOMMENDATIONS")
print("=" * 80)
print()

if total_pnl < 0:
    print("Based on your trading history:")
    print()
    print("1. 🚫 STOP LIVE TRADING IMMEDIATELY")
    print("   - Algorithm is not profitable yet")
    print("   - Need to fix issues before risking real money")
    print()
    print("2. 📊 ANALYZE WHAT WORKED")
    print("   - Look at winning days vs losing days")
    print("   - What was different on profitable days?")
    print("   - Market conditions? Trade count? Strategy?")
    print()
    print("3. 🔧 SIMPLIFY THE ALGORITHM")
    print("   - Remove complex indicators")
    print("   - Focus on 2-3 simple rules that work")
    print("   - Test with paper trading first")
    print()
    print("4. 💪 CONSIDER MANUAL TRADING")
    print("   - You mentioned capital doubled before")
    print("   - What was different then?")
    print("   - Maybe simpler approach worked better")
    print()
else:
    print("✅ Algorithm is profitable!")
    print("   Continue with current approach")
    print("   Monitor daily performance")
    print("   Adjust position sizing if needed")
    print()

print("=" * 80)
