#!/usr/bin/env python3
"""
Analyze SCALPER strategy performance across all trading days
"""

import pandas as pd
import glob
from datetime import datetime

# Find all trade CSV files
csv_files = sorted(glob.glob("high_accuracy_trades_*.csv"))

print("=" * 80)
print("🔍 SCALPER STRATEGY ANALYSIS - ALL DAYS")
print("=" * 80)
print()

all_scalper_trades = []
daily_results = []

for csv_file in csv_files:
    try:
        # Read CSV
        df = pd.read_csv(csv_file)
        
        # Filter for SCALPER strategy and EXIT actions only
        scalper_trades = df[(df['strategy'] == 'SCALPER') & (df['action'] == 'EXIT')]
        
        if len(scalper_trades) == 0:
            continue
        
        # Extract date from filename
        date_str = csv_file.split('_')[-1].replace('.csv', '')
        date = datetime.strptime(date_str, '%Y%m%d').strftime('%b %d')
        
        # Calculate metrics
        total_trades = len(scalper_trades)
        wins = len(scalper_trades[scalper_trades['net_pnl_after_charges'] > 0])
        losses = total_trades - wins
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = scalper_trades['net_pnl_after_charges'].sum()
        
        # Store daily results
        daily_results.append({
            'date': date,
            'trades': total_trades,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'pnl': total_pnl
        })
        
        # Store all trades
        for _, trade in scalper_trades.iterrows():
            all_scalper_trades.append({
                'date': date,
                'symbol': trade['symbol'],
                'entry': trade['entry_price'],
                'exit': trade['exit_price'],
                'pnl': trade['net_pnl_after_charges'],
                'holding_time': trade['holding_time_minutes']
            })
        
    except Exception as e:
        print(f"Error processing {csv_file}: {e}")
        continue

# Print daily breakdown
print("📊 DAILY BREAKDOWN:")
print("-" * 80)
print(f"{'Date':<10} {'Trades':<8} {'Wins':<6} {'Loss':<6} {'Win Rate':<10} {'P&L':<15}")
print("-" * 80)

total_trades_all = 0
total_wins_all = 0
total_losses_all = 0
total_pnl_all = 0

for result in daily_results:
    print(f"{result['date']:<10} {result['trades']:<8} {result['wins']:<6} {result['losses']:<6} {result['win_rate']:>6.1f}%   ₹{result['pnl']:>12,.0f}")
    total_trades_all += result['trades']
    total_wins_all += result['wins']
    total_losses_all += result['losses']
    total_pnl_all += result['pnl']

print("-" * 80)
overall_win_rate = (total_wins_all / total_trades_all * 100) if total_trades_all > 0 else 0
print(f"{'TOTAL':<10} {total_trades_all:<8} {total_wins_all:<6} {total_losses_all:<6} {overall_win_rate:>6.1f}%   ₹{total_pnl_all:>12,.0f}")
print("=" * 80)

# Summary
print()
print("📈 OVERALL SCALPER PERFORMANCE:")
print("-" * 80)
print(f"Total Trades:     {total_trades_all}")
print(f"Winning Trades:   {total_wins_all} ({overall_win_rate:.1f}%)")
print(f"Losing Trades:    {total_losses_all} ({100-overall_win_rate:.1f}%)")
print(f"Total P&L:        ₹{total_pnl_all:,.0f}")
print(f"Avg P&L per trade: ₹{total_pnl_all/total_trades_all:,.0f}" if total_trades_all > 0 else "N/A")
print()

# Verdict
if overall_win_rate >= 60 and total_pnl_all > 0:
    verdict = "✅ GOOD - Keep SCALPER strategy"
    color = "🟢"
elif overall_win_rate >= 50 and total_pnl_all > 0:
    verdict = "⚠️ OKAY - SCALPER needs improvement"
    color = "🟡"
else:
    verdict = "❌ BAD - DISABLE SCALPER strategy"
    color = "🔴"

print(f"{color} VERDICT: {verdict}")
print()

# Winning days vs losing days
winning_days = len([r for r in daily_results if r['pnl'] > 0])
losing_days = len([r for r in daily_results if r['pnl'] < 0])
print(f"Winning Days: {winning_days}/{len(daily_results)} ({winning_days/len(daily_results)*100:.1f}%)")
print(f"Losing Days:  {losing_days}/{len(daily_results)} ({losing_days/len(daily_results)*100:.1f}%)")
print()

# Best and worst days
if daily_results:
    best_day = max(daily_results, key=lambda x: x['pnl'])
    worst_day = min(daily_results, key=lambda x: x['pnl'])
    print(f"Best Day:  {best_day['date']} → ₹{best_day['pnl']:+,.0f} ({best_day['trades']} trades, {best_day['win_rate']:.0f}% WR)")
    print(f"Worst Day: {worst_day['date']} → ₹{worst_day['pnl']:+,.0f} ({worst_day['trades']} trades, {worst_day['win_rate']:.0f}% WR)")

print("=" * 80)
