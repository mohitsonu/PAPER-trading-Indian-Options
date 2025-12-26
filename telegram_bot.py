#!/usr/bin/env python3
"""Telegram Bot Integration for Trading Summaries"""
import requests
import json
from datetime import datetime
import pandas as pd
import os

class TelegramBot:
    def __init__(self, bot_token=None, chat_id=None):
        self.bot_token = bot_token or self._load_config().get('bot_token')
        self.chat_id = chat_id or self._load_config().get('chat_id')
        
        if not self.bot_token or not self.chat_id:
            print("⚠️ Telegram not configured. Create telegram_config.json")
            self.enabled = False
        else:
            self.enabled = True
    
    def _load_config(self):
        try:
            if os.path.exists('telegram_config.json'):
                with open('telegram_config.json', 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
        return {}
    
    def send_message(self, message, parse_mode='HTML'):
        if not self.enabled:
            print("Telegram not configured")
            return False
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': parse_mode
        }
        
        try:
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                print("✅ Telegram message sent")
                return True
            else:
                print(f"❌ Telegram error: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Send failed: {e}")
            return False
    
    def send_daily_summary(self, csv_file=None, capital_start=100000):
        if not self.enabled:
            return False
        
        try:
            if not csv_file:
                today = datetime.now().strftime("%Y%m%d")
                csv_file = f"high_accuracy_trades_{today}.csv"
            
            if not os.path.exists(csv_file):
                message = f"""
🤖 <b>HIGH ACCURACY TRADING - DAILY SUMMARY</b>
📅 Date: {datetime.now().strftime('%Y-%m-%d')}

❌ <b>No trades file found</b>
📁 Looking for: {csv_file}
💡 No trades were taken today
                """
                return self.send_message(message.strip())
            
            df = pd.read_csv(csv_file)
            
            if df.empty:
                message = f"""
🤖 <b>HIGH ACCURACY TRADING - DAILY SUMMARY</b>
📅 Date: {datetime.now().strftime('%Y-%m-%d')}

📊 <b>No trades taken today</b>
🎯 Algorithm waited for high accuracy setups
                """
                return self.send_message(message.strip())
            
            exits = df[df['action'] == 'EXIT']
            
            if exits.empty:
                total_pnl = 0
                win_rate = 0
                total_trades = 0
                wins = 0
                losses = 0
            else:
                pnl_col = None
                for col in ['net_pnl_after_charges', 'pnl_after_charges', 'pnl', 'gross_pnl']:
                    if col in exits.columns:
                        pnl_col = col
                        break
                
                if pnl_col:
                    total_pnl = exits[pnl_col].sum()
                    wins = len(exits[exits[pnl_col] > 0])
                    losses = len(exits[exits[pnl_col] < 0])
                    total_trades = len(exits)
                    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
                else:
                    total_pnl = 0
                    win_rate = 0
                    total_trades = len(exits)
                    wins = 0
                    losses = 0
            
            ending_capital = capital_start + total_pnl
            return_pct = (total_pnl / capital_start * 100) if capital_start > 0 else 0
            
            pnl_emoji = "🟢" if total_pnl > 0 else "🔴" if total_pnl < 0 else "⚪"
            trend_emoji = "📈" if total_pnl > 0 else "📉" if total_pnl < 0 else "➡️"
            
            message = f"""
🤖 <b>HIGH ACCURACY TRADING - DAILY SUMMARY</b>
📅 Date: {datetime.now().strftime('%Y-%m-%d')}

💰 <b>PERFORMANCE</b>
{pnl_emoji} Net P&L: ₹{total_pnl:,.2f}
{trend_emoji} Return: {return_pct:+.2f}%
💼 Capital: ₹{ending_capital:,.2f}

📊 <b>STATISTICS</b>
🎯 Total Trades: {total_trades}
✅ Wins: {wins}
❌ Losses: {losses}
📈 Win Rate: {win_rate:.1f}%

🔍 <b>STRATEGY</b>
🎯 High Accuracy Algorithm
⏰ Market Hours: 9:15 AM - 3:30 PM
🛡️ Risk Management: Active
            """
            
            if not exits.empty and len(exits) <= 5 and pnl_col:
                message += "\n📋 <b>TODAY'S TRADES</b>\n"
                for _, trade in exits.iterrows():
                    symbol = trade.get('symbol', 'Unknown')
                    pnl = trade.get(pnl_col, 0)
                    pnl_emoji = "✅" if pnl > 0 else "❌"
                    message += f"{pnl_emoji} {symbol}: ₹{pnl:+.2f}\n"
            
            return self.send_message(message.strip())
            
        except Exception as e:
            error_message = f"""
🤖 <b>HIGH ACCURACY TRADING - ERROR</b>
📅 Date: {datetime.now().strftime('%Y-%m-%d')}

❌ <b>Error generating summary</b>
🔧 Error: {str(e)}
            """
            print(f"Error: {e}")
            return self.send_message(error_message.strip())
