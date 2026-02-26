#!/usr/bin/env python3
"""
🤖 GITHUB ACTIONS RUNNER
Simplified runner for GitHub Actions environment
Runs a single trading cycle and exits
Includes Telegram notifications and HTML report generation
"""

import sys
import os
from datetime import datetime
from high_accuracy_algo import HighAccuracyAlgo

# Telegram integration
try:
    from telegram_signals.telegram_notifier import TelegramNotifier
    from telegram_signals.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ENABLED
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("⚠️ Telegram module not available")

# HTML Report generation
try:
    import generate_dynamic_report
    REPORT_AVAILABLE = True
except ImportError:
    REPORT_AVAILABLE = False
    print("⚠️ Report generation module not available")

def main():
    print("=" * 60)
    print("🤖 GITHUB ACTIONS - AUTO TRADING BOT")
    print("=" * 60)
    print(f"⏰ Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
    print("=" * 60)
    
    # Initialize Telegram if available
    telegram = None
    if TELEGRAM_AVAILABLE and TELEGRAM_ENABLED:
        try:
            # Check for environment variables first (GitHub Secrets)
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN', TELEGRAM_BOT_TOKEN)
            chat_id = os.getenv('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID)
            telegram = TelegramNotifier(bot_token, chat_id)
            print("✅ Telegram notifications enabled")
        except Exception as e:
            print(f"⚠️ Telegram initialization failed: {e}")
    
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
    
    # Check if this is the first run of the day (around market open)
    is_market_open_time = current_time.hour == 9 and current_time.minute <= 20
    
    try:
        # Login
        print("🔐 Logging in...")
        if not algo.login():
            print("❌ Login failed")
            sys.exit(1)
        
        print("✅ Login successful!")
        print()
        
        # Send session start notification (only at market open)
        if is_market_open_time and telegram:
            try:
                telegram.send_session_start(algo.current_capital)
                print("📱 Trading session start notification sent to Telegram")
            except Exception as e:
                print(f"⚠️ Session start notification failed: {e}")
        
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
                        
                        # Send Telegram notification
                        if telegram:
                            try:
                                trade_data = {
                                    'symbol': best_opp['symbol'],
                                    'strike': best_opp.get('strike', 'N/A'),
                                    'option_type': best_opp.get('option_type', 'N/A'),
                                    'entry_price': best_opp['ltp'],
                                    'quantity': best_opp.get('quantity', 15),
                                    'strategy': 'CONTRARIAN',
                                    'reason': f"High accuracy opportunity (Score: {best_opp['score_data']['score']}/100)"
                                }
                                telegram.send_entry_signal(trade_data)
                                print("📱 Entry signal sent to Telegram")
                            except Exception as e:
                                print(f"⚠️ Telegram notification failed: {e}")
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
        
        # Generate HTML report
        if REPORT_AVAILABLE:
            try:
                print()
                print("📊 Generating HTML trading report...")
                generate_dynamic_report.generate_dynamic_report()
                print("✅ Trading report generated: trading_report.html")
            except Exception as e:
                print(f"⚠️ Report generation failed: {e}")
        
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
            
            # Send daily summary via Telegram at market close (3:25 PM onwards)
            if telegram and current_time.hour >= 15 and current_time.minute >= 25:
                try:
                    wins = len([t for t in algo.trade_history if t.get('pnl', 0) > 0])
                    losses = len([t for t in algo.trade_history if t.get('pnl', 0) <= 0])
                    win_rate = (wins / len(algo.trade_history) * 100) if algo.trade_history else 0
                    
                    # Find today's CSV file
                    today = datetime.now().strftime('%Y%m%d')
                    csv_file = f"high_accuracy_trades_{today}.csv"
                    
                    summary_data = {
                        'starting_capital': capital,
                        'ending_capital': algo.current_capital,
                        'net_pnl': total_pnl,
                        'net_pnl_pct': (total_pnl / capital * 100),
                        'total_trades': len(algo.trade_history),
                        'win_rate': win_rate,
                        'wins': wins,
                        'losses': losses,
                        'csv_file': csv_file if os.path.exists(csv_file) else ''
                    }
                    
                    telegram.send_daily_summary(summary_data)
                    print("📱 Daily summary sent to Telegram")
                except Exception as e:
                    print(f"⚠️ Telegram summary failed: {e}")
        
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
