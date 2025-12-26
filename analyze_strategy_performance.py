#!/usr/bin/env python3
"""
Analyze strategy performance across all trades
"""

import pandas as pd
import glob
from datetime import datetime

def analyze_strategies():
    print("=" * 80)
    print("📊 STRATEGY PERFORMANCE ANALYSIS")
    print("=" * 80)
    
    # Load all trade files
    trade_files = glob.glob("high_accuracy_trades_*.csv")
    
    if not trade_files:
        print("❌ No trade files found!")
        return
    
    print(f"\n✅ Found {len(trade_files)} trade files")
    
    # Combine all trades
    all_trades = []
    for file in sorted(trade_files):
        try:
            df = pd.read_csv(file)
            all_trades.append(df)
        except Exception as e:
            print(f"⚠️ Error reading {file}: {e}")
    
    if not all_trades:
        print("❌ No trades loaded!")
        return
    
    # Combine all dataframes
    df_all = pd.concat(all_trades, ignore_index=True)
    
    # Filter only EXIT records (completed trades)
    exits = df_all[df_all['action'] == 'EXIT'].copy()
    
    if exits.empty:
        print("❌ No completed trades found!")
        return
    
    print(f"✅ Loaded {len(exits)} completed trades")
    
    # Find P&L column
    pnl_col = None
    for col in ['net_pnl_after_charges', 'pnl_after_charges', 'net_pnl', 'pnl', 'gross_pnl']:
        if col in exits.columns:
            pnl_col = col
            break
    
    if not pnl_col:
        print("❌ No P&L column found!")
        return
    
    print(f"📊 Using P&L column: {pnl_col}")
    
    # Check if strategy column exists
    if 'strategy' not in exits.columns:
        print("\n⚠️ No 'strategy' column found in trades!")
        print("   Strategies might not be tracked in older trades")
        return
    
    # Analyze by strategy
    print("\n" + "=" * 80)
    print("📊 PERFORMANCE BY STRATEGY")
    print("=" * 80)
    
    strategies = exits['strategy'].unique()
    
    strategy_stats = []
    
    for strategy in strategies:
        if pd.isna(strategy) or strategy == '' or strategy == 'UNKNOWN':
            continue
        
        strategy_trades = exits[exits['strategy'] == strategy]
        
        total_trades = len(strategy_trades)
        wins = len(strategy_trades[strategy_trades[pnl_col] > 0])
        losses = len(strategy_trades[strategy_trades[pnl_col] <= 0])
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = strategy_trades[pnl_col].sum()
        avg_pnl = strategy_trades[pnl_col].mean()
        
        avg_win = strategy_trades[strategy_trades[pnl_col] > 0][pnl_col].mean() if wins > 0 else 0
        avg_loss = strategy_trades[strategy_trades[pnl_col] <= 0][pnl_col].mean() if losses > 0 else 0
        
        risk_reward = abs(avg_win / avg_loss) if avg_loss != 0 else 0
        
        strategy_stats.append({
            'strategy': strategy,
            'total_trades': total_trades,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_pnl': avg_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'risk_reward': risk_reward
        })
    
    # Sort by total P&L
    strategy_stats.sort(key=lambda x: x['total_pnl'], reverse=True)
    
    # Display results
    for i, stats in enumerate(strategy_stats, 1):
        emoji = "✅" if stats['total_pnl'] > 0 else "❌"
        
        print(f"\n{i}. {emoji} {stats['strategy']}")
        print(f"   {'─' * 70}")
        print(f"   Total Trades: {stats['total_trades']}")
        print(f"   Win Rate: {stats['win_rate']:.1f}% ({stats['wins']}W / {stats['losses']}L)")
        print(f"   Total P&L: ₹{stats['total_pnl']:+,.2f}")
        print(f"   Avg P&L per Trade: ₹{stats['avg_pnl']:+,.2f}")
        print(f"   Avg Win: ₹{stats['avg_win']:+,.2f}")
        print(f"   Avg Loss: ₹{stats['avg_loss']:+,.2f}")
        print(f"   Risk:Reward: 1:{stats['risk_reward']:.2f}")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY & RECOMMENDATIONS")
    print("=" * 80)
    
    profitable = [s for s in strategy_stats if s['total_pnl'] > 0]
    unprofitable = [s for s in strategy_stats if s['total_pnl'] <= 0]
    
    print(f"\n✅ Profitable Strategies: {len(profitable)}")
    for s in profitable:
        print(f"   • {s['strategy']}: ₹{s['total_pnl']:+,.2f} ({s['win_rate']:.1f}% WR)")
    
    print(f"\n❌ Unprofitable Strategies: {len(unprofitable)}")
    for s in unprofitable:
        print(f"   • {s['strategy']}: ₹{s['total_pnl']:+,.2f} ({s['win_rate']:.1f}% WR)")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    print("   " + "─" * 70)
    
    for stats in unprofitable:
        print(f"\n   ⚠️ {stats['strategy']}:")
        
        if stats['win_rate'] < 40:
            print(f"      • Very low win rate ({stats['win_rate']:.1f}%)")
            print(f"      • Recommendation: DISABLE or increase entry criteria")
        
        if stats['risk_reward'] < 1.5:
            print(f"      • Poor risk:reward ratio (1:{stats['risk_reward']:.2f})")
            print(f"      • Recommendation: Increase targets or tighten stops")
        
        if stats['total_trades'] < 5:
            print(f"      • Too few trades ({stats['total_trades']}) for reliable analysis")
            print(f"      • Recommendation: Collect more data before deciding")
        else:
            print(f"      • Recommendation: DISABLE this strategy")
    
    for stats in profitable:
        if stats['win_rate'] > 60 and stats['total_pnl'] > 5000:
            print(f"\n   ✅ {stats['strategy']}:")
            print(f"      • Excellent performance!")
            print(f"      • Recommendation: KEEP and possibly increase allocation")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    analyze_strategies()
