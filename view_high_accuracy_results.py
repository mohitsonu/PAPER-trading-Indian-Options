#!/usr/bin/env python3
"""
📊 High Accuracy Trading Results Viewer
Detailed analysis of quality-focused trading performance
"""

import pandas as pd
import json
from datetime import datetime
import os

def view_high_accuracy_results():
    """View and analyze high accuracy trading results"""
    
    print("🎯 HIGH ACCURACY OPTIONS TRADING RESULTS")
    print("=" * 70)
    
    csv_file = f"high_accuracy_trades_{datetime.now().strftime('%Y%m%d')}.csv"
    json_file = f"high_accuracy_updates_{datetime.now().strftime('%Y%m%d')}.json"
    
    # Read CSV file
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
        
        if not df.empty:
            entries = df[df['action'] == 'ENTRY']
            exits = df[df['action'] == 'EXIT']
            
            print(f"\n📋 TRADE SUMMARY:")
            print(f"Total Entries: {len(entries)}")
            print(f"Total Exits: {len(exits)}")
            print(f"Open Positions: {len(entries) - len(exits)}")
            
            if len(exits) > 0:
                # Calculate performance metrics
                winning_trades = len(exits[exits['pnl_after_charges'] > 0])
                losing_trades = len(exits[exits['pnl_after_charges'] <= 0])
                win_rate = (winning_trades / len(exits)) * 100
                
                total_pnl = exits['pnl_after_charges'].sum()
                avg_score = exits['accuracy_score'].mean()
                avg_holding = exits['holding_time_minutes'].mean()
                
                print(f"\n📈 PERFORMANCE METRICS:")
                print(f"Win Rate: {win_rate:.1f}% ({winning_trades}W / {losing_trades}L)")
                print(f"Total Net P&L: ₹{total_pnl:+,.2f}")
                print(f"Average Accuracy Score: {avg_score:.0f}/100")
                print(f"Average Holding Time: {avg_holding:.0f} minutes")
                
                if winning_trades > 0:
                    avg_win = exits[exits['pnl_after_charges'] > 0]['pnl_after_charges'].mean()
                    print(f"Average Win: ₹{avg_win:.2f}")
                
                if losing_trades > 0:
                    avg_loss = exits[exits['pnl_after_charges'] <= 0]['pnl_after_charges'].mean()
                    print(f"Average Loss: ₹{avg_loss:.2f}")
            
            # Show recent trades
            print(f"\n🔄 RECENT TRADES:")
            recent_trades = df.tail(10)
            for _, trade in recent_trades.iterrows():
                action = trade['action']
                symbol = trade['symbol']
                
                if action == 'ENTRY':
                    score = trade['accuracy_score']
                    price = trade['entry_price']
                    print(f"   🟢 ENTRY: {symbol} @ ₹{price:.2f} | Score: {score:.0f}/100")
                else:
                    pnl = trade['pnl_after_charges']
                    price = trade['exit_price']
                    reason = trade['reason']
                    holding = trade['holding_time_minutes']
                    print(f"   🔴 EXIT: {symbol} @ ₹{price:.2f} | P&L: ₹{pnl:+.2f} | {reason} | {holding:.0f}min")
        else:
            print("❌ No trades found in CSV")
    
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_file}")
    
    # Read JSON file
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        print(f"\n💰 CAPITAL SUMMARY:")
        print(f"Initial Capital: ₹{data['initial_capital']:,}")
        print(f"Current Capital: ₹{data['current_capital']:,.2f}")
        
        net_pnl = data['current_capital'] - data['initial_capital']
        net_return = (net_pnl / data['initial_capital']) * 100
        
        print(f"Net P&L: ₹{net_pnl:+,.2f} ({net_return:+.2f}%)")
        print(f"Broker Charges per Trade: ₹{data['broker_charges_per_trade']}")
        
        perf = data['performance']
        print(f"\n📊 DETAILED PERFORMANCE:")
        print(f"Total Trades: {perf['total_trades']}")
        print(f"Win Rate: {perf['win_rate']:.1f}%")
        print(f"Total Gross P&L: ₹{perf['total_gross_pnl']:+,.2f}")
        print(f"Total Charges: ₹{perf['total_charges']:.2f}")
        print(f"Total Net P&L: ₹{perf['total_net_pnl']:+,.2f}")
        print(f"Average Accuracy Score: {perf['avg_accuracy_score']:.0f}/100")
        print(f"Average Holding Time: {perf['avg_holding_time_minutes']:.0f} minutes")
        
        if perf['total_charges'] > 0:
            profit_factor = abs(perf['total_gross_pnl'] / perf['total_charges'])
            print(f"Profit Factor: {profit_factor:.2f}")
        
        if data['positions']:
            print(f"\n🔄 OPEN POSITIONS:")
            for pos in data['positions']:
                print(f"   {pos['symbol']} @ ₹{pos['entry_price']:.2f} x {pos['quantity']}")
                print(f"   Score: {pos['accuracy_score']:.0f}/100 | Strategy: {pos['strategy']}")
        
        if data['recent_trades']:
            print(f"\n📈 RECENT COMPLETED TRADES:")
            for trade in data['recent_trades']:
                net_pnl = trade['net_pnl']
                score = trade['accuracy_score']
                reason = trade['exit_reason']
                holding = trade['holding_minutes']
                charges = trade['charges']
                print(f"   {trade['symbol']}: ₹{net_pnl:+.2f} (after ₹{charges:.0f} charges)")
                print(f"   Score: {score:.0f}/100 | {reason} | {holding:.0f}min")
    
    except FileNotFoundError:
        print(f"❌ JSON file not found: {json_file}")

def analyze_quality_metrics():
    """Analyze the quality of trades based on accuracy scores"""
    
    print(f"\n🏆 QUALITY ANALYSIS")
    print("=" * 50)
    
    csv_file = f"high_accuracy_trades_{datetime.now().strftime('%Y%m%d')}.csv"
    
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
        exits = df[df['action'] == 'EXIT']
        
        if len(exits) > 0:
            # Score-based analysis
            high_score_trades = exits[exits['accuracy_score'] >= 90]
            medium_score_trades = exits[(exits['accuracy_score'] >= 80) & (exits['accuracy_score'] < 90)]
            low_score_trades = exits[exits['accuracy_score'] < 80]
            
            print(f"High Score Trades (90+): {len(high_score_trades)}")
            print(f"Medium Score Trades (80-89): {len(medium_score_trades)}")
            print(f"Low Score Trades (<80): {len(low_score_trades)}")
            
            # Success rates by score category
            if len(high_score_trades) > 0:
                high_score_wins = len(high_score_trades[high_score_trades['pnl_after_charges'] > 0])
                high_score_win_rate = (high_score_wins / len(high_score_trades)) * 100
                print(f"High Score Win Rate: {high_score_win_rate:.1f}%")
            
            if len(medium_score_trades) > 0:
                medium_score_wins = len(medium_score_trades[medium_score_trades['pnl_after_charges'] > 0])
                medium_score_win_rate = (medium_score_wins / len(medium_score_trades)) * 100
                print(f"Medium Score Win Rate: {medium_score_win_rate:.1f}%")
            
            # Strategy analysis
            print(f"\n📊 STRATEGY BREAKDOWN:")
            strategy_stats = exits.groupby('strategy').agg({
                'pnl_after_charges': ['count', 'sum', 'mean'],
                'accuracy_score': 'mean'
            }).round(2)
            
            for strategy in strategy_stats.index:
                count = strategy_stats.loc[strategy, ('pnl_after_charges', 'count')]
                total_pnl = strategy_stats.loc[strategy, ('pnl_after_charges', 'sum')]
                avg_pnl = strategy_stats.loc[strategy, ('pnl_after_charges', 'mean')]
                avg_score = strategy_stats.loc[strategy, ('accuracy_score', 'mean')]
                
                print(f"{strategy}: {count} trades, ₹{total_pnl:+.2f} total, ₹{avg_pnl:+.2f} avg, {avg_score:.0f} avg score")
            
            # Time-based analysis
            print(f"\n⏰ HOLDING TIME ANALYSIS:")
            short_holds = exits[exits['holding_time_minutes'] <= 60]  # <= 1 hour
            medium_holds = exits[(exits['holding_time_minutes'] > 60) & (exits['holding_time_minutes'] <= 180)]  # 1-3 hours
            long_holds = exits[exits['holding_time_minutes'] > 180]  # > 3 hours
            
            for category, data in [("Short (≤1h)", short_holds), ("Medium (1-3h)", medium_holds), ("Long (>3h)", long_holds)]:
                if len(data) > 0:
                    wins = len(data[data['pnl_after_charges'] > 0])
                    win_rate = (wins / len(data)) * 100
                    avg_pnl = data['pnl_after_charges'].mean()
                    print(f"{category}: {len(data)} trades, {win_rate:.1f}% win rate, ₹{avg_pnl:+.2f} avg P&L")
        
        else:
            print("❌ No completed trades found for analysis")
    
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_file}")

def show_algorithm_improvements():
    """Show what improvements were made for high accuracy"""
    
    print(f"\n🚀 HIGH ACCURACY ALGORITHM FEATURES")
    print("=" * 60)
    
    improvements = [
        "✅ Strict Entry Criteria (Min 85/100 score)",
        "✅ Broker Charges Integration (₹20 per trade)",
        "✅ Quality over Quantity Focus (1-10 trades/day)",
        "✅ Enhanced Market Analysis:",
        "   • 10-period trend confirmation",
        "   • Market structure analysis",
        "   • Confidence scoring",
        "✅ Advanced Scoring System:",
        "   • Liquidity scoring (25 points)",
        "   • Premium quality (20 points)", 
        "   • Trend alignment (25 points)",
        "   • Strike selection (15 points)",
        "   • Market structure (15 points)",
        "✅ Risk Management Enhancements:",
        "   • 30% stop loss, 80% target (2.67:1 R:R)",
        "   • Trailing stops for profitable trades",
        "   • Maximum 4-hour holding time",
        "   • Position sizing based on accuracy",
        "✅ Comprehensive Filtering:",
        "   • Minimum ₹30 premium (covers charges)",
        "   • Minimum 5L OI for liquidity",
        "   • Minimum 1000 volume",
        "   • Maximum ₹5 bid-ask spread",
        "✅ Extended Market Coverage:",
        "   • 13 strike prices monitored",
        "   • Enhanced NIFTY estimation",
        "   • Confidence-based decisions",
        "✅ Quality Metrics Tracking:",
        "   • Win rate by accuracy score",
        "   • Strategy performance analysis",
        "   • Holding time optimization",
        "   • Profit factor calculation"
    ]
    
    for feature in improvements:
        print(f"  {feature}")
    
    print(f"\n💡 KEY DIFFERENCES FROM BASIC ALGO:")
    print("=" * 60)
    print("1. 🎯 Higher minimum score (85 vs 60)")
    print("2. 💸 Broker charges factored into P&L")
    print("3. ⏰ Longer cycles (2min vs 30sec) for quality")
    print("4. 🔍 Opportunity checks every 15 minutes")
    print("5. 📊 Enhanced market structure analysis")
    print("6. 🛡️ Better risk-reward ratio (2.67:1 vs 2:1)")
    print("7. 📈 Trailing stops for profit protection")
    print("8. 🎪 Maximum 3 positions for better diversification")
    print("9. 📋 Detailed quality metrics tracking")
    print("10. ⚡ Focus on 1-10 quality trades per day")

def compare_with_basic_algo():
    """Compare results with basic algorithm if available"""
    
    print(f"\n⚖️ COMPARISON WITH BASIC ALGORITHM")
    print("=" * 60)
    
    # Check if basic algo files exist
    basic_csv = f"trade_journal_{datetime.now().strftime('%Y%m%d')}.csv"
    high_acc_csv = f"high_accuracy_trades_{datetime.now().strftime('%Y%m%d')}.csv"
    
    try:
        basic_df = pd.read_csv(basic_csv, encoding='utf-8')
        high_acc_df = pd.read_csv(high_acc_csv, encoding='utf-8')
        
        basic_exits = basic_df[basic_df['action'] == 'EXIT']
        high_acc_exits = high_acc_df[high_acc_df['action'] == 'EXIT']
        
        if len(basic_exits) > 0 and len(high_acc_exits) > 0:
            # Basic algo stats
            basic_trades = len(basic_exits)
            basic_wins = len(basic_exits[basic_exits['pnl'] > 0])
            basic_win_rate = (basic_wins / basic_trades) * 100
            basic_total_pnl = basic_exits['pnl'].sum()
            
            # High accuracy algo stats
            ha_trades = len(high_acc_exits)
            ha_wins = len(high_acc_exits[high_acc_exits['pnl_after_charges'] > 0])
            ha_win_rate = (ha_wins / ha_trades) * 100
            ha_total_pnl = high_acc_exits['pnl_after_charges'].sum()
            
            print(f"📊 BASIC ALGORITHM:")
            print(f"   Trades: {basic_trades} | Win Rate: {basic_win_rate:.1f}% | P&L: ₹{basic_total_pnl:+.2f}")
            
            print(f"🎯 HIGH ACCURACY ALGORITHM:")
            print(f"   Trades: {ha_trades} | Win Rate: {ha_win_rate:.1f}% | P&L: ₹{ha_total_pnl:+.2f}")
            
            print(f"\n📈 IMPROVEMENT:")
            if ha_trades < basic_trades:
                print(f"✅ Fewer trades: {basic_trades - ha_trades} less trades (quality focus)")
            if ha_win_rate > basic_win_rate:
                print(f"✅ Better win rate: +{ha_win_rate - basic_win_rate:.1f}%")
            if ha_total_pnl > basic_total_pnl:
                print(f"✅ Better P&L: +₹{ha_total_pnl - basic_total_pnl:.2f}")
        
        else:
            print("❌ Insufficient data for comparison")
    
    except FileNotFoundError:
        print("❌ Basic algorithm files not found for comparison")

if __name__ == "__main__":
    view_high_accuracy_results()
    analyze_quality_metrics()
    show_algorithm_improvements()
    compare_with_basic_algo()