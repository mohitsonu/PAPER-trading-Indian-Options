"""
🔔 Telegram Signal Notifier for High Accuracy Trading
Sends real-time trade signals to Telegram channel/group
"""

import requests
import json
import os
from datetime import datetime

class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        """
        Initialize Telegram notifier
        
        Args:
            bot_token: Your Telegram bot token from @BotFather
            chat_id: Your channel/group chat ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
    def send_message(self, message, parse_mode='HTML'):
        """Send message to Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            response = requests.post(url, data=data, timeout=10)
            return response.json()
        except Exception as e:
            print(f"❌ Telegram send failed: {e}")
            return None
    
    def send_entry_signal(self, trade_data):
        """Send entry signal"""
        symbol = trade_data['symbol']
        strike = trade_data.get('strike', 'N/A')
        option_type = trade_data.get('option_type', 'N/A')
        entry_price = trade_data['entry_price']
        quantity = trade_data['quantity']
        strategy = trade_data.get('strategy', 'N/A')
        reason = trade_data.get('reason', '')
        
        message = f"""
🟢 <b>ENTRY SIGNAL</b> 🟢

📊 <b>Symbol:</b> {symbol}
🎯 <b>Strike:</b> {strike} {option_type}
💰 <b>Entry Price:</b> ₹{entry_price:.2f}
📦 <b>Quantity:</b> {quantity}
📈 <b>Strategy:</b> {strategy}

💡 <b>Reason:</b> {reason}

⏰ <b>Time:</b> {datetime.now().strftime('%d-%b-%Y %I:%M:%S %p')}
"""
        return self.send_message(message)
    
    def send_exit_signal(self, trade_data):
        """Send exit signal with P&L"""
        symbol = trade_data['symbol']
        strike = trade_data.get('strike', 'N/A')
        option_type = trade_data.get('option_type', 'N/A')
        entry_price = trade_data['entry_price']
        exit_price = trade_data['exit_price']
        quantity = trade_data['quantity']
        net_pnl = trade_data.get('net_pnl', 0)
        gross_pnl = trade_data.get('gross_pnl', 0)
        pnl_pct = ((exit_price - entry_price) / entry_price) * 100
        reason = trade_data.get('exit_reason', 'EXIT')
        holding_time = trade_data.get('holding_time_minutes', 0)
        
        # Emoji based on profit/loss
        emoji = "🟢" if net_pnl > 0 else "🔴"
        status = "PROFIT" if net_pnl > 0 else "LOSS"
        
        message = f"""
{emoji} <b>EXIT SIGNAL - {status}</b> {emoji}

📊 <b>Symbol:</b> {symbol}
🎯 <b>Strike:</b> {strike} {option_type}
💵 <b>Entry:</b> ₹{entry_price:.2f}
💵 <b>Exit:</b> ₹{exit_price:.2f}
📦 <b>Quantity:</b> {quantity}
💰 <b>Trade P&L:</b> ₹{net_pnl:+,.2f} ({pnl_pct:+.1f}%)
⏱️ <b>Holding Time:</b> {holding_time:.0f} minutes
📋 <b>Exit Reason:</b> {reason}

⏰ <b>Time:</b> {datetime.now().strftime('%d-%b-%Y %I:%M:%S %p')}
"""
        return self.send_message(message)
    
    def send_daily_summary(self, summary_data):
        """Send simple end of day summary with CSV file"""
        starting_capital = summary_data.get('starting_capital', 0)
        ending_capital = summary_data.get('ending_capital', 0)
        net_pnl = summary_data.get('net_pnl', 0)
        net_pnl_pct = summary_data.get('net_pnl_pct', 0)
        total_trades = summary_data.get('total_trades', 0)
        win_rate = summary_data.get('win_rate', 0)
        wins = summary_data.get('wins', 0)
        losses = summary_data.get('losses', 0)
        csv_file = summary_data.get('csv_file', '')
        
        # Emoji based on profit/loss
        emoji = "🎉" if net_pnl > 0 else "😔"
        
        # Simple, clean message
        message = f"""
{emoji} <b>DAILY SUMMARY</b> {emoji}

📅 <b>Date:</b> {datetime.now().strftime('%d-%b-%Y')}

💰 <b>Starting Capital:</b> ₹{starting_capital:,.2f}
💰 <b>Ending Capital:</b> ₹{ending_capital:,.2f}
📊 <b>Net Profit (After Charges):</b> ₹{net_pnl:+,.2f} ({net_pnl_pct:+.2f}%)

📋 <b>Total Trades:</b> {total_trades}
🎯 <b>Win Rate:</b> {win_rate:.1f}% ({wins}W / {losses}L)

⏰ <b>Session End:</b> {datetime.now().strftime('%I:%M:%S %p')}
"""
        
        # Send message first
        self.send_message(message)
        
        # Send CSV file if available
        if csv_file and os.path.exists(csv_file):
            try:
                self.send_document(csv_file, f"📊 Trade Journal - {datetime.now().strftime('%d-%b-%Y')}")
            except Exception as e:
                print(f"⚠️ Failed to send CSV file: {e}")
        
        return True
    
    def send_document(self, file_path, caption=""):
        """Send a document/file to Telegram"""
        try:
            url = f"{self.base_url}/sendDocument"
            
            with open(file_path, 'rb') as file:
                files = {'document': file}
                data = {
                    'chat_id': self.chat_id,
                    'caption': caption,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, data=data, files=files, timeout=30)
                
                if response.json().get('ok'):
                    return True
                else:
                    print(f"❌ Failed to send document: {response.json()}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error sending document: {e}")
            return False
    
    def send_session_start(self, capital):
        """Send session start notification"""
        message = f"""
🚀 <b>TRADING SESSION STARTED</b> 🚀

💰 <b>Capital:</b> ₹{capital:,.2f}
📅 <b>Date:</b> {datetime.now().strftime('%d-%b-%Y')}
⏰ <b>Time:</b> {datetime.now().strftime('%I:%M:%S %p')}

🎯 High Accuracy Algorithm Active
📊 Monitoring market for quality setups...
"""
        return self.send_message(message)
    
    def test_connection(self):
        """Test Telegram connection"""
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            if response.json().get('ok'):
                print("✅ Telegram connection successful!")
                return True
            else:
                print("❌ Telegram connection failed!")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
