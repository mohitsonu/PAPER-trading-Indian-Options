#!/usr/bin/env python3
"""
🤖 GITHUB ACTIONS RUNNER
Simplified runner for GitHub Actions environment
Runs a single trading cycle and exits
"""

import sys
import os
from datetime import datetime
from high_accuracy_algo import HighAccuracyAlgo

def main():
    print("=" * 60)
    print("🤖 GITHUB ACTIONS - AUTO TRADING BOT")
    print("=" * 60)
    print(f"⏰ Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print("=" * 60)
    
    # Check if it's a trading day and market hours
    now = datetime.now()
    is_weekday = now.weekday() < 5
    current_time = now.time()
    
    from datetime import time as dt_time
    market_open = dt_time(9, 15)
    market_close = dt_time(15, 30)
    is_market_hours = market_open <= current_time <= market_close
    
    if not is_weekday:
        print("📅 Weekend - No trading")
        return
    
    if not is_market_hours:
        print("⏰ Outside market hours (9:15 AM - 3:30 PM)")
        return
    
    print("✅ Market is open - Starting trading cycle...")
    print()
    
    # Initialize algorithm
    capital = 100000
    algo = HighAccuracyAlgo(initial_capital=capital, strategy_mode='CURRENT')
    
    try:
        # Login
        print("🔐 Logging in...")
        if not algo.login():
            print("❌ Login failed")
            sys.exit(1)
        
        print("✅ Login successful!")
        print()
        
        # Run single cycle
        print("📊 Fetching market data...")
        algo.get_comprehensive_market_data()
        
        if not algo.market_data:
            print("⚠️ No market data available")
            return
        
        print(f"✅ Fetched data for {len(algo.market_data)} options")
        print()
        
        # Analyze opportunities
        print("🔍 Analyzing trading opportunities...")
        opportunities = algo.find_high_accuracy_opportunities()
        
        if opportunities:
            print(f"✅ Found {len(opportunities)} opportunities")
            
            # Display top opportunities
            for i, opp in enumerate(opportunities[:3], 1):
                score = opp['score_data']['score']
                symbol = opp['symbol']
                ltp = opp['ltp']
                print(f"   {i}. {symbol}: Score {score}/100 @ ₹{ltp:.2f}")
            
            # Execute trades if score >= 90
            high_quality = [o for o in opportunities if o['score_data']['score'] >= 90]
            
            if high_quality:
                print()
                print(f"🎯 {len(high_quality)} opportunities meet 90+ score threshold")
                
                # Check positions and execute
                current_positions = len(algo.active_positions)
                max_positions = algo.max_positions
                
                if current_positions < max_positions:
                    print(f"💼 Current positions: {current_positions}/{max_positions}")
                    print("🚀 Executing trades...")
                    
                    # Execute top opportunity
                    best_opp = high_quality[0]
                    success = algo.execute_trade(best_opp)
                    
                    if success:
                        print(f"✅ Trade executed: {best_opp['symbol']}")
                    else:
                        print("❌ Trade execution failed")
                else:
                    print(f"⚠️ Max positions reached ({current_positions}/{max_positions})")
            else:
                print("ℹ️ No opportunities meet 90+ score threshold")
        else:
            print("ℹ️ No trading opportunities found")
        
        # Check and manage existing positions
        if algo.active_positions:
            print()
            print(f"📊 Managing {len(algo.active_positions)} active positions...")
            algo.manage_positions()
        
        # Display summary
        print()
        print("=" * 60)
        print("📊 CYCLE SUMMARY")
        print("=" * 60)
        print(f"💰 Capital: ₹{algo.current_capital:,.2f}")
        print(f"📈 Positions: {len(algo.active_positions)}/{algo.max_positions}")
        print(f"📊 Trades Today: {len(algo.trade_history)}")
        
        if algo.trade_history:
            total_pnl = sum(t.get('pnl', 0) for t in algo.trade_history)
            print(f"💵 Total P&L: ₹{total_pnl:+,.2f}")
        
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
