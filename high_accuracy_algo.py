#!/usr/bin/env python3
"""
🎯 HIGH ACCURACY OPTIONS TRADING ALGORITHM
Quality over Quantity - Designed for 1-10 high-accuracy trades per day
Broker Charges: ₹20 per trade | Focus: High probability setups only
"""

from NorenRestApiPy.NorenApi import NorenApi
import pyotp
import os
import pandas as pd
import json
import csv
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import math
import numpy as np

# Telegram integration
try:
    from telegram_signals.telegram_notifier import TelegramNotifier
    from telegram_signals.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ENABLED
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("⚠️ Telegram module not found - signals disabled")

# Priority Features (Market Condition, OI Analysis, Stochastic, Greeks)
try:
    from priority_features import PriorityFeatures
    PRIORITY_FEATURES_AVAILABLE = True
except ImportError:
    PRIORITY_FEATURES_AVAILABLE = False
    print("⚠️ Priority features not found - using basic filters only")

# Adaptive Market Engine (Smart mode selection)
try:
    from adaptive_market_engine import AdaptiveMarketEngine
    ADAPTIVE_ENGINE_AVAILABLE = True
except ImportError:
    ADAPTIVE_ENGINE_AVAILABLE = False
    print("⚠️ Adaptive engine not found - using fixed strategy")

# Trailing Stop Manager (Smart profit protection)
try:
    from trailing_stop_manager import TrailingStopManager, StrategyTrailingStops, ProfitProtection
    TRAILING_STOP_AVAILABLE = True
except ImportError:
    TRAILING_STOP_AVAILABLE = False
    print("⚠️ Trailing stop manager not found - using basic stops")

# Trade state persistence
from trade_state_persistence import TradeStatePersistence

# Realistic brokerage calculator
from brokerage_calculator import BrokerageCalculator, calculate_tax_on_profit

load_dotenv()

class HighAccuracyAlgo:
    def __init__(self, initial_capital=100000, strategy_mode='CURRENT'):
        self.api = NorenApi(host='https://api.shoonya.com/NorenWClientTP/', 
                           websocket='wss://api.shoonya.com/NorenWSTP/')
        
        # Credentials
        self.user_id = os.getenv('SHOONYA_USER_ID')
        self.password = os.getenv('SHOONYA_PASSWORD')
        self.totp_key = os.getenv('SHOONYA_TOTP_KEY')
        self.vendor_code = os.getenv('SHOONYA_VENDOR_CODE')
        self.api_secret = os.getenv('SHOONYA_API_SECRET')
        
        # 🆕 STRATEGY MODE SELECTOR
        self.strategy_mode = strategy_mode  # 'CURRENT' or 'SIMPLIFIED'
        
        # HIGH ACCURACY PARAMETERS
        self.initial_capital = initial_capital
        self.capital_persistence_file = "capital_persistence.json"
        
        # Load persisted capital or use initial capital
        self.current_capital = self.load_persisted_capital() or initial_capital
        self.broker_charges = 20  # ₹20 per trade
        self.max_risk_per_trade = 0.03  # 3% risk per trade (higher for fewer trades)
        self.max_positions = 3  # Maximum 3 positions at a time
        
        # OPTIMIZED ENTRY CRITERIA (Better Strike Selection)
        if strategy_mode == 'SIMPLIFIED':
            self.min_accuracy_score = 70   # Lower for simplified (more trades)
        else:
            self.min_accuracy_score = 90   # Higher for current (fewer trades)
        
        self.min_premium = 20   # Minimum ₹20 premium
        self.max_premium = 150  # Reduced to ₹150 (avoid expensive options)
        self.min_oi = 100000    # Reduced from 500000 to 100000 (1 lakh OI)
        self.min_volume = 500   # Reduced from 1000 to 500 (more tradeable)
        
        # RISK MANAGEMENT
        self.stop_loss_pct = 0.25  # 25% stop loss (tighter)
        self.target_profit_pct = 0.50  # 50% target (2:1 R:R, more realistic)
        self.max_holding_time = 2  # Maximum 2 hours holding (reduced from 4)
        
        # TREND CONFIRMATION REQUIREMENTS
        self.trend_confirmation_periods = 10  # Need 10 data points for trend
        self.min_trend_strength = 0.7  # 70% directional moves required
        
        # Data Storage
        self.positions = []
        self.trade_history = []
        self.market_data = {}
        self.price_history = []
        self.last_nifty_price = 0
        self.trend_data = []
        self.candlestick_data = []  # Store OHLC data for pattern analysis
        self.current_patterns = []  # Store detected patterns
        
        # Brokerage Calculator (Realistic charges)
        self.brokerage_calc = BrokerageCalculator(broker_type='discount')
        
        # Live P&L Tracking
        self.daily_gross_pnl = 0  # Total gross P&L for the day
        self.daily_charges = 0  # Total charges for the day
        self.daily_net_pnl = 0  # Total net P&L after charges (before tax)
        
        # Telegram Notifier
        self.telegram = None
        if TELEGRAM_AVAILABLE and TELEGRAM_ENABLED:
            try:
                self.telegram = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
                print("✅ Telegram notifications enabled")
            except Exception as e:
                print(f"⚠️ Telegram initialization failed: {e}")
                self.telegram = None
        
        # Priority Features (4 critical filters)
        self.priority_features = None
        if PRIORITY_FEATURES_AVAILABLE:
            try:
                self.priority_features = PriorityFeatures()
                print("✅ Priority features enabled:")
                print("   1. Market Condition Filter (prevents overtrading)")
                print("   2. OI Change Analysis (smart money tracking)")
                print("   3. Stochastic Oscillator (precise timing)")
                print("   4. Greeks Analysis (risk assessment)")
            except Exception as e:
                print(f"⚠️ Priority features initialization failed: {e}")
                self.priority_features = None
        
        # Adaptive Market Engine (Smart strategy selection)
        self.adaptive_engine = None
        if ADAPTIVE_ENGINE_AVAILABLE:
            try:
                self.adaptive_engine = AdaptiveMarketEngine()
                print("✅ Adaptive Market Engine enabled:")
                print("   🎯 Auto-detects: TRENDING/RANGING/CHOPPY/VOLATILE")
                print("   🎯 Auto-selects: Best strategy for market condition")
                print("   🎯 Dynamic sizing: 150-300 lots based on confidence")
                print("   🎯 Smart limits: Max trades per mode")
                print("   🎯 Sits out: When market is unfavorable")
            except Exception as e:
                print(f"⚠️ Adaptive engine initialization failed: {e}")
                self.adaptive_engine = None
        
        # Trailing Stop Manager (Smart profit protection)
        self.trailing_stop_manager = None
        if TRAILING_STOP_AVAILABLE:
            try:
                self.trailing_stop_manager = TrailingStopManager()
                print("✅ Smart Trailing Stops enabled:")
                print("   📈 Dynamic trailing based on profit level")
                print("   📈 Adaptive to market mode (trending/ranging)")
                print("   📈 Breakeven protection at 5% profit")
                print("   📈 Profit lock-in at 10%, 20%, 30%+ levels")
            except Exception as e:
                print(f"⚠️ Trailing stop manager initialization failed: {e}")
                self.trailing_stop_manager = None
        
        # Multi-Timeframe Technical Indicators Data
        self.nifty_ohlc_1min = []   # 1-minute bars for precise timing
        self.nifty_ohlc_5min = []   # 5-minute bars for current analysis
        self.nifty_ohlc_15min = []  # 15-minute bars for trend filter
        self.nifty_ohlc_data = []   # Legacy OHLC data for compatibility
        
        self.indicators_1min = {}   # 1-minute indicators
        self.indicators_5min = {}   # 5-minute indicators  
        self.indicators_15min = {}  # 15-minute indicators
        self.current_indicators = {}  # Current indicators (for ATR, etc.)
        
        # Files
        self.csv_file = f"high_accuracy_trades_{datetime.now().strftime('%Y%m%d')}.csv"
        self.json_file = f"high_accuracy_updates_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Trade state persistence
        self.persistence = TradeStatePersistence()
        
        self.initialize_files()
    
    def initialize_files(self):
        """Initialize CSV and JSON files for high accuracy tracking"""
        
        csv_headers = [
            'timestamp', 'trade_id', 'action', 'symbol', 'strike', 'option_type',
            'entry_price', 'exit_price', 'quantity', 'capital_invested',
            'gross_pnl', 'total_charges', 'net_pnl_after_charges', 'capital',
            'reason', 'accuracy_score', 'trend_strength', 'nifty_level', 'iv_rank',
            'oi', 'volume', 'strategy', 'holding_time_minutes', 'candlestick_patterns',
            'running_daily_pnl'
        ]
        
        # Only create CSV if it doesn't exist (append mode for existing)
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(csv_headers)
            print(f"📄 Created new CSV file: {self.csv_file}")
        else:
            print(f"📄 Using existing CSV file: {self.csv_file}")
        
        # Load existing JSON data if file exists, otherwise create new
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r', encoding='utf-8') as file:
                    existing_data = json.load(file)
                
                # Load existing trades and positions
                self.trade_history = existing_data.get('trades', [])
                self.positions = existing_data.get('positions', [])
                
                print(f"✅ Loaded existing session data:")
                print(f"   📊 Trades: {len(self.trade_history)}")
                print(f"   📈 Open Positions: {len(self.positions)}")
                
                # Update start time to show session resumed
                existing_data['last_resumed'] = datetime.now().isoformat()
                existing_data['session_count'] = existing_data.get('session_count', 0) + 1
                
                # Save updated data
                with open(self.json_file, 'w', encoding='utf-8') as file:
                    json.dump(existing_data, file, indent=2, ensure_ascii=False)
                
            except Exception as e:
                print(f"⚠️ Error loading existing data: {e}")
                print(f"   Creating fresh session...")
                self._create_fresh_json()
        else:
            print(f"📄 Creating new JSON file: {self.json_file}")
            self._create_fresh_json()
        
        # 🔄 RESTORE ACTIVE POSITIONS FROM PERSISTENCE
        self._restore_active_positions()
        
        print(f"✅ High Accuracy Algo initialized")
        print(f"💰 Capital: ₹{self.current_capital:.2f} (Persisted from previous session)")
    
    def _restore_active_positions(self):
        """Restore active positions from persistence on restart"""
        try:
            # Load state from persistence module
            state = self.persistence.load_state()
            
            if not state or not state.get('positions'):
                print(f"ℹ️ No active positions to restore")
                return
            
            restored_positions = state.get('positions', [])
            
            if not restored_positions:
                return
            
            print(f"\n🔄 RESTORING {len(restored_positions)} ACTIVE POSITIONS:")
            
            for pos in restored_positions:
                # Convert entry_time string back to datetime
                if isinstance(pos.get('entry_time'), str):
                    try:
                        pos['entry_time'] = datetime.fromisoformat(pos['entry_time'])
                    except:
                        pos['entry_time'] = datetime.now()
                
                # Add to positions list
                self.positions.append(pos)
                
                # Calculate holding time
                entry_time = pos['entry_time']
                if isinstance(entry_time, str):
                    try:
                        entry_time = datetime.fromisoformat(entry_time)
                        pos['entry_time'] = entry_time  # Update to datetime object
                    except:
                        entry_time = datetime.now()
                        pos['entry_time'] = entry_time
                
                holding_time = datetime.now() - entry_time
                holding_minutes = int(holding_time.total_seconds() / 60)
                
                print(f"   ✅ {pos['symbol']}")
                print(f"      Entry: ₹{pos['entry_price']:.2f} x {pos['quantity']} lots")
                print(f"      SL: ₹{pos['stop_loss']:.2f} | Target: ₹{pos['target']:.2f}")
                print(f"      Holding: {holding_minutes} minutes")
                print(f"      Score: {pos['accuracy_score']:.0f}/100")
            
            print(f"\n✅ Successfully restored {len(restored_positions)} positions")
            print(f"💡 Monitoring will continue from where it stopped\n")
            
        except Exception as e:
            print(f"⚠️ Error restoring positions: {e}")
            print(f"   Starting with fresh session...")
    
    def _save_position_state(self):
        """Save current positions to persistence (called after every position change)"""
        try:
            # Prepare positions for saving (convert datetime to ISO format)
            positions_to_save = []
            for pos in self.positions:
                pos_copy = pos.copy()
                # Convert entry_time to ISO format if it's a datetime object
                entry_time = pos_copy.get('entry_time')
                if isinstance(entry_time, datetime):
                    pos_copy['entry_time'] = entry_time.isoformat()
                elif isinstance(entry_time, str):
                    # Already a string, keep it as is
                    pass
                else:
                    # If it's neither, use current time
                    pos_copy['entry_time'] = datetime.now().isoformat()
                positions_to_save.append(pos_copy)
            
            # Save to persistence
            metadata = {
                'last_nifty_price': self.last_nifty_price,
                'trade_count': len(self.trade_history),
                'session_date': datetime.now().strftime('%Y-%m-%d')
            }
            
            success = self.persistence.save_state(
                positions=positions_to_save,
                capital=self.current_capital,
                metadata=metadata
            )
            
            if success:
                print(f"💾 Position state saved ({len(positions_to_save)} active positions)")
            
        except Exception as e:
            print(f"⚠️ Error saving position state: {e}")
    
    def _create_fresh_json(self):
        """Create a fresh JSON file with initial data"""
        initial_data = {
            'start_time': datetime.now().isoformat(),
            'initial_capital': self.initial_capital,
            'broker_charges_per_trade': self.broker_charges,
            'min_accuracy_score': self.min_accuracy_score,
            'target_trades_per_day': '1-10',
            'focus': 'High Accuracy Quality Trades',
            'session_count': 1,
            'trades': [],
            'positions': [],
            'performance': {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_pnl': 0,
                'total_charges': 0,
                'net_pnl': 0,
                'win_rate': 0,
                'avg_accuracy_score': 0,
                'avg_holding_time': 0
            }
        }
        
        with open(self.json_file, 'w', encoding='utf-8') as file:
            json.dump(initial_data, file, indent=2, ensure_ascii=False)
    
    def load_persisted_capital(self):
        """Load capital from previous session"""
        try:
            if os.path.exists(self.capital_persistence_file):
                with open(self.capital_persistence_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    return data.get('current_capital', None)
        except Exception as e:
            print(f"⚠️ Could not load persisted capital: {e}")
        return None
    
    def save_capital_persistence(self):
        """Save current capital with daily P&L tracking"""
        try:
            # Load existing data to preserve daily sessions
            existing_data = {}
            if os.path.exists(self.capital_persistence_file):
                with open(self.capital_persistence_file, 'r', encoding='utf-8') as file:
                    existing_data = json.load(file)
            
            # Get session start capital (capital at beginning of today)
            today = datetime.now().strftime('%Y-%m-%d')
            daily_sessions = existing_data.get('daily_sessions', {})
            
            # If this is first save of the day, record starting capital
            if today not in daily_sessions:
                session_start_capital = existing_data.get('current_capital', self.initial_capital)
                daily_sessions[today] = {
                    'start_capital': session_start_capital,
                    'end_capital': self.current_capital,
                    'daily_pnl': self.current_capital - session_start_capital,
                    'trades_count': len(self.trade_history),
                    'session_start': datetime.now().isoformat(),
                    'last_update': datetime.now().isoformat()
                }
            else:
                # Update existing session
                daily_sessions[today].update({
                    'end_capital': self.current_capital,
                    'daily_pnl': self.current_capital - daily_sessions[today]['start_capital'],
                    'trades_count': len(self.trade_history),
                    'last_update': datetime.now().isoformat()
                })
            
            # Calculate total P&L from original initial capital
            original_initial = existing_data.get('initial_capital', self.initial_capital)
            total_pnl = self.current_capital - original_initial
            
            persistence_data = {
                'current_capital': self.current_capital,
                'initial_capital': original_initial,
                'total_pnl': total_pnl,
                'pnl_percentage': (total_pnl / original_initial * 100) if original_initial > 0 else 0,
                'last_updated': datetime.now().isoformat(),
                'session_date': today,
                'trades_completed': len(self.trade_history),
                'positions_count': len(self.positions),
                'daily_sessions': daily_sessions
            }
            
            with open(self.capital_persistence_file, 'w', encoding='utf-8') as file:
                json.dump(persistence_data, file, indent=2, ensure_ascii=False)
            
            # Save to daily capital CSV
            self.save_daily_capital_csv(daily_sessions[today])
            
            # Show daily P&L
            daily_pnl = daily_sessions[today]['daily_pnl']
            print(f"💾 Capital persisted: ₹{self.current_capital:.2f}")
            print(f"📅 Today's P&L: ₹{daily_pnl:+.2f} | Total P&L: ₹{total_pnl:+.2f}")
            
        except Exception as e:
            print(f"❌ Error saving capital persistence: {e}")
    
    def save_daily_capital_csv(self, session_data):
        """Save daily capital data to CSV file"""
        try:
            csv_file = "daily_capital_tracking.csv"
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Check if CSV exists, if not create with headers
            file_exists = os.path.exists(csv_file)
            
            with open(csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write headers if new file
                if not file_exists:
                    headers = [
                        'date', 'start_capital', 'end_capital', 'daily_pnl', 
                        'daily_pnl_pct', 'trades_count', 'session_start_time', 
                        'session_end_time', 'total_capital_from_start', 'cumulative_pnl'
                    ]
                    writer.writerow(headers)
                
                # Calculate values
                start_capital = session_data['start_capital']
                end_capital = session_data['end_capital']
                daily_pnl = session_data['daily_pnl']
                daily_pnl_pct = (daily_pnl / start_capital * 100) if start_capital > 0 else 0
                trades_count = session_data['trades_count']
                session_start = session_data['session_start']
                session_end = session_data['last_update']
                
                # Calculate cumulative P&L from original ₹100,000
                original_capital = 100000
                cumulative_pnl = end_capital - original_capital
                
                # Check if today's row already exists
                rows_to_keep = []
                if file_exists:
                    with open(csv_file, 'r', encoding='utf-8') as read_file:
                        reader = csv.reader(read_file)
                        rows_to_keep = [row for row in reader if len(row) > 0 and row[0] != today]
                
                # Rewrite file with updated data
                with open(csv_file, 'w', newline='', encoding='utf-8') as write_file:
                    writer = csv.writer(write_file)
                    
                    # Write headers
                    headers = [
                        'date', 'start_capital', 'end_capital', 'daily_pnl', 
                        'daily_pnl_pct', 'trades_count', 'session_start_time', 
                        'session_end_time', 'total_capital_from_start', 'cumulative_pnl'
                    ]
                    writer.writerow(headers)
                    
                    # Write existing rows (excluding today if it existed)
                    for row in rows_to_keep[1:]:  # Skip header row
                        if len(row) >= 4:  # Valid row
                            writer.writerow(row)
                    
                    # Write today's row
                    row = [
                        today,
                        f"{start_capital:.2f}",
                        f"{end_capital:.2f}",
                        f"{daily_pnl:+.2f}",
                        f"{daily_pnl_pct:+.2f}%",
                        trades_count,
                        session_start,
                        session_end,
                        f"{end_capital:.2f}",
                        f"{cumulative_pnl:+.2f}"
                    ]
                    writer.writerow(row)
                
                print(f"📊 Daily capital CSV updated: {csv_file}")
                
        except Exception as e:
            print(f"❌ Error saving daily capital CSV: {e}")
    
    def login(self):
        """Login to Shoonya API"""
        totp = pyotp.TOTP(self.totp_key).now()
        
        try:
            result = self.api.login(
                userid=self.user_id,
                password=self.password,
                twoFA=totp,
                vendor_code=self.vendor_code,
                api_secret=self.api_secret,
                imei='abc1234'
            )
            
            if result and result.get('stat') == 'Ok':
                print("✅ Login successful!")
                return True
            else:
                print(f"❌ Login failed: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def get_current_expiry(self):
        """Get current expiry date from config file"""
        try:
            # Read from expiry_config.json
            with open('expiry_config.json', 'r') as f:
                config = json.load(f)
                expiry = config.get('current_expiry', '25NOV25')
                print(f"📅 Using expiry from config: {expiry}")
                return expiry
        except FileNotFoundError:
            print("⚠️ expiry_config.json not found, using default: 25NOV25")
            return "25NOV25"
        except Exception as e:
            print(f"⚠️ Error reading expiry config: {e}, using default: 25NOV25")
            return "25NOV25"
    
    def get_comprehensive_market_data(self):
        """Get comprehensive market data with extended analysis"""
        
        # Dynamic strike range - Extended to 27000
        strikes = [25200, 25250, 25300, 25350, 25400, 25450, 25500, 25550, 25600, 
                   25650, 25700, 25750, 25800, 25850, 25900, 25950, 26000, 26050,
                   26100, 26150, 26200, 26250, 26300, 26350, 26400, 26450, 26500,
                   26550, 26600, 26650, 26700, 26750, 26800, 26850, 26900, 26950, 27000]
        
        # Get expiry from config file
        expiry = self.get_current_expiry()
        
        market_data = []
        strikes_found = []
        
        print(f"🔍 Fetching data for {len(strikes)} strikes with expiry {expiry}...")
        
        # Debug: Show first matched symbol
        debug_shown = False
        
        for strike in strikes:
            ce_found = False
            pe_found = False
            
            # Try to find options for this strike
            search_result = self.api.searchscrip(exchange="NFO", searchtext=str(strike))
            
            if search_result and search_result.get('stat') == 'Ok':
                symbols = search_result.get('values', [])
                
                for symbol in symbols:
                    tsym = symbol.get('tsym', '')
                    optt = symbol.get('optt', '')
                    
                    # Strict validation: Must be NIFTY (not BANKNIFTY), must have exact expiry and strike
                    # Expected format: NIFTY25NOV2425900CE or NIFTY25NOV2425900PE
                    if (tsym.startswith('NIFTY') and 
                        not tsym.startswith('NIFTYBANK') and
                        expiry in tsym and 
                        str(strike) in tsym and 
                        optt in ['CE', 'PE'] and
                        len(tsym) < 25):  # Reasonable length check
                        try:
                            quotes = self.api.get_quotes(exchange="NFO", token=symbol.get('token'))
                            
                            if quotes and quotes.get('stat') == 'Ok':
                                ltp = float(quotes.get('lp', 0))
                                
                                # Debug: Show first matched symbol with timestamp
                                if not debug_shown and ltp > 0:
                                    ltt = quotes.get('ltt', 'N/A')  # Last trade time
                                    print(f"✅ Sample: {tsym} @ ₹{ltp} | Last trade: {ltt}")
                                    debug_shown = True
                                
                                data = {
                                    'symbol': tsym,
                                    'strike': strike,
                                    'option_type': optt,
                                    'token': symbol.get('token'),
                                    'ltp': ltp,
                                    'volume': int(quotes.get('v', 0)),
                                    'oi': int(quotes.get('oi', 0)),
                                    'bid': float(quotes.get('bp1', 0)),
                                    'ask': float(quotes.get('sp1', 0)),
                                    'high': float(quotes.get('h', 0)),
                                    'low': float(quotes.get('l', 0)),
                                    'change': float(quotes.get('c', 0)),
                                    'change_pct': (float(quotes.get('c', 0)) / ltp * 100) if ltp > 0 else 0,
                                    'bid_ask_spread': float(quotes.get('sp1', 0)) - float(quotes.get('bp1', 0)),
                                    'timestamp': datetime.now()
                                }
                                market_data.append(data)
                                
                                if optt == 'CE':
                                    ce_found = True
                                else:
                                    pe_found = True
                        except Exception as e:
                            continue
            
            # Track which strikes have data
            if ce_found or pe_found:
                strikes_found.append(f"{strike}({'CE' if ce_found else ''}{'PE' if pe_found else ''})")
        
        print(f"✅ Data found for {len(strikes_found)} strikes: {', '.join(strikes_found[:5])}{'...' if len(strikes_found) > 5 else ''}")
        
        # Store market data
        self.market_data = {item['symbol']: item for item in market_data}
        
        if market_data:
            self.estimate_nifty_level()
            self.analyze_market_structure()
        else:
            print(f"❌ No market data available. Possible reasons:")
            print(f"   • Market just opened (wait 2-3 minutes)")
            print(f"   • API rate limiting")
            print(f"   • Network connectivity issues")
        
        return market_data
    
    def try_expiry(self, strikes, expiry):
        """Try to get data for specific expiry"""
        market_data = []
        
        for strike in strikes[:3]:  # Try only first 3 strikes for speed
            search_result = self.api.searchscrip(exchange="NFO", searchtext=str(strike))
            
            if search_result and search_result.get('stat') == 'Ok':
                symbols = search_result.get('values', [])
                
                for symbol in symbols:
                    tsym = symbol.get('tsym', '')
                    optt = symbol.get('optt', '')
                    
                    if (str(strike) in tsym and expiry in tsym and optt in ['CE', 'PE']):
                        try:
                            quotes = self.api.get_quotes(exchange="NFO", token=symbol.get('token'))
                            
                            if quotes and quotes.get('stat') == 'Ok':
                                ltp = float(quotes.get('lp', 0))
                                
                                if ltp > 0:  # Only add if has valid price
                                    data = {
                                        'symbol': tsym,
                                        'strike': strike,
                                        'option_type': optt,
                                        'token': symbol.get('token'),
                                        'ltp': ltp,
                                        'volume': int(quotes.get('v', 0)),
                                        'oi': int(quotes.get('oi', 0)),
                                        'bid': float(quotes.get('bp1', 0)),
                                        'ask': float(quotes.get('sp1', 0)),
                                        'high': float(quotes.get('h', 0)),
                                        'low': float(quotes.get('l', 0)),
                                        'change': float(quotes.get('c', 0)),
                                        'change_pct': (float(quotes.get('c', 0)) / ltp * 100) if ltp > 0 else 0,
                                        'bid_ask_spread': float(quotes.get('sp1', 0)) - float(quotes.get('bp1', 0)),
                                        'timestamp': datetime.now()
                                    }
                                    market_data.append(data)
                                    
                                    if len(market_data) >= 4:  # Found some data, return
                                        return market_data
                        except:
                            continue
        
        return market_data
    
    def estimate_nifty_level(self):
        """Enhanced NIFTY level estimation with confidence scoring"""
        
        atm_candidates = []
        strikes = set([item['strike'] for item in self.market_data.values()])
        
        for strike in strikes:
            ce_data = None
            pe_data = None
            
            for symbol, data in self.market_data.items():
                if data['strike'] == strike:
                    if data['option_type'] == 'CE':
                        ce_data = data
                    elif data['option_type'] == 'PE':
                        pe_data = data
            
            if ce_data and pe_data and ce_data['ltp'] > 0 and pe_data['ltp'] > 0:
                diff = abs(ce_data['ltp'] - pe_data['ltp'])
                estimated_nifty = strike + (ce_data['ltp'] - pe_data['ltp'])
                
                # Confidence based on liquidity and spread
                confidence = min(100, (ce_data['oi'] + pe_data['oi']) / 20000)  # Max confidence at 20L combined OI
                confidence *= max(0.5, 1 - (ce_data['bid_ask_spread'] + pe_data['bid_ask_spread']) / 20)  # Penalize wide spreads
                
                atm_candidates.append((strike, diff, estimated_nifty, confidence, ce_data['ltp'], pe_data['ltp']))
        
        if atm_candidates:
            # Find most confident ATM estimate
            best_estimate = min(atm_candidates, key=lambda x: x[1])  # Minimum CE-PE difference
            self.last_nifty_price = best_estimate[2]
            
            # Store enhanced price history
            self.price_history.append({
                'timestamp': datetime.now(),
                'nifty': best_estimate[2],
                'atm_strike': best_estimate[0],
                'confidence': best_estimate[3],
                'ce_ltp': best_estimate[4],
                'pe_ltp': best_estimate[5]
            })
            
            # Keep last 20 data points
            if len(self.price_history) > 20:
                self.price_history = self.price_history[-20:]
            
            # Update candlestick data
            self.update_candlestick_data()
            
            # Update multi-timeframe technical indicators
            self.update_multi_timeframe_indicators()
    
    def analyze_market_structure(self):
        """Analyze market structure for high accuracy signals"""
        
        if len(self.price_history) < self.trend_confirmation_periods:
            return {
                'trend': 'INSUFFICIENT_DATA',
                'strength': 0,
                'confidence': 0,
                'structure': 'UNKNOWN'
            }
        
        recent_prices = [p['nifty'] for p in self.price_history[-self.trend_confirmation_periods:]]
        
        # Calculate trend strength
        up_moves = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] > recent_prices[i-1])
        down_moves = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] < recent_prices[i-1])
        total_moves = up_moves + down_moves
        
        if total_moves == 0:
            trend_strength = 0
        else:
            trend_strength = max(up_moves, down_moves) / total_moves
        
        # Determine trend
        if trend_strength >= self.min_trend_strength:
            if up_moves > down_moves:
                trend = 'STRONG_BULLISH'
            else:
                trend = 'STRONG_BEARISH'
        elif trend_strength >= 0.6:
            if up_moves > down_moves:
                trend = 'BULLISH'
            else:
                trend = 'BEARISH'
        else:
            trend = 'SIDEWAYS'
        
        # Calculate price momentum
        if len(recent_prices) >= 5:
            momentum = (recent_prices[-1] - recent_prices[-5]) / recent_prices[-5] * 100
        else:
            momentum = 0
        
        # Market structure analysis
        highs = [p['nifty'] for p in self.price_history[-10:]]
        lows = [p['nifty'] for p in self.price_history[-10:]]
        
        if len(highs) >= 3:
            higher_highs = sum(1 for i in range(2, len(highs)) if highs[i] > highs[i-2])
            lower_lows = sum(1 for i in range(2, len(lows)) if lows[i] < lows[i-2])
            
            if higher_highs >= 2:
                structure = 'UPTREND'
            elif lower_lows >= 2:
                structure = 'DOWNTREND'
            else:
                structure = 'RANGE'
        else:
            structure = 'FORMING'
        
        analysis = {
            'trend': trend,
            'strength': trend_strength,
            'momentum': momentum,
            'structure': structure,
            'confidence': min(100, len(self.price_history) / self.trend_confirmation_periods * 100)
        }
        
        self.trend_data.append(analysis)
        if len(self.trend_data) > 10:
            self.trend_data = self.trend_data[-10:]
        
        return analysis
    
    def update_candlestick_data(self):
        """Update candlestick data from price history"""
        
        if len(self.price_history) < 2:
            return
        
        # Create OHLC data from price history (5-minute intervals)
        current_time = datetime.now()
        
        # Group price data into 5-minute candles
        if not self.candlestick_data or (current_time - self.candlestick_data[-1]['timestamp']).total_seconds() >= 300:  # 5 minutes
            
            # Get recent prices for this candle
            recent_prices = [p['nifty'] for p in self.price_history[-5:] if p['nifty'] > 0]
            
            if len(recent_prices) >= 2:
                candle = {
                    'timestamp': current_time,
                    'open': recent_prices[0],
                    'high': max(recent_prices),
                    'low': min(recent_prices),
                    'close': recent_prices[-1],
                    'volume': sum([p.get('volume', 0) for p in self.price_history[-5:]])
                }
                
                self.candlestick_data.append(candle)
                
                # Keep last 20 candles
                if len(self.candlestick_data) > 20:
                    self.candlestick_data = self.candlestick_data[-20:]
                
                # Analyze patterns after adding new candle
                self.analyze_candlestick_patterns()
    
    def analyze_candlestick_patterns(self):
        """Analyze candlestick patterns for trading signals"""
        
        if len(self.candlestick_data) < 3:
            self.current_patterns = []
            return
        
        patterns = []
        candles = self.candlestick_data[-5:]  # Analyze last 5 candles
        
        if len(candles) >= 1:
            # Single candle patterns
            patterns.extend(self.detect_single_candle_patterns(candles[-1]))
        
        if len(candles) >= 2:
            # Two candle patterns
            patterns.extend(self.detect_two_candle_patterns(candles[-2:]))
        
        if len(candles) >= 3:
            # Three candle patterns
            patterns.extend(self.detect_three_candle_patterns(candles[-3:]))
        
        self.current_patterns = patterns
    
    def detect_single_candle_patterns(self, candle):
        """Detect single candlestick patterns"""
        
        patterns = []
        
        open_price = candle['open']
        high = candle['high']
        low = candle['low']
        close = candle['close']
        
        body = abs(close - open_price)
        upper_shadow = high - max(open_price, close)
        lower_shadow = min(open_price, close) - low
        total_range = high - low
        
        if total_range == 0:
            return patterns
        
        # Doji - Small body, long shadows
        if body <= total_range * 0.1:
            if upper_shadow > body * 2 and lower_shadow > body * 2:
                patterns.append({
                    'name': 'DOJI',
                    'type': 'REVERSAL',
                    'strength': 'MEDIUM',
                    'signal': 'INDECISION',
                    'score': 15
                })
        
        # Hammer - Small body at top, long lower shadow
        if body <= total_range * 0.3 and lower_shadow >= body * 2 and upper_shadow <= body * 0.5:
            if close > open_price:  # Bullish hammer
                patterns.append({
                    'name': 'HAMMER',
                    'type': 'REVERSAL',
                    'strength': 'STRONG',
                    'signal': 'BULLISH',
                    'score': 20
                })
            else:  # Bearish hammer (hanging man)
                patterns.append({
                    'name': 'HANGING_MAN',
                    'type': 'REVERSAL',
                    'strength': 'STRONG',
                    'signal': 'BEARISH',
                    'score': 20
                })
        
        # Shooting Star - Small body at bottom, long upper shadow
        if body <= total_range * 0.3 and upper_shadow >= body * 2 and lower_shadow <= body * 0.5:
            patterns.append({
                'name': 'SHOOTING_STAR',
                'type': 'REVERSAL',
                'strength': 'STRONG',
                'signal': 'BEARISH',
                'score': 20
            })
        
        # Marubozu - No shadows, strong body
        if upper_shadow <= total_range * 0.05 and lower_shadow <= total_range * 0.05:
            if close > open_price:
                patterns.append({
                    'name': 'BULLISH_MARUBOZU',
                    'type': 'CONTINUATION',
                    'strength': 'STRONG',
                    'signal': 'BULLISH',
                    'score': 18
                })
            else:
                patterns.append({
                    'name': 'BEARISH_MARUBOZU',
                    'type': 'CONTINUATION',
                    'strength': 'STRONG',
                    'signal': 'BEARISH',
                    'score': 18
                })
        
        return patterns
    
    def detect_two_candle_patterns(self, candles):
        """Detect two candlestick patterns"""
        
        patterns = []
        
        if len(candles) < 2:
            return patterns
        
        prev_candle = candles[0]
        curr_candle = candles[1]
        
        prev_body = abs(prev_candle['close'] - prev_candle['open'])
        curr_body = abs(curr_candle['close'] - curr_candle['open'])
        
        # Bullish Engulfing
        if (prev_candle['close'] < prev_candle['open'] and  # Previous bearish
            curr_candle['close'] > curr_candle['open'] and  # Current bullish
            curr_candle['open'] < prev_candle['close'] and  # Opens below prev close
            curr_candle['close'] > prev_candle['open'] and  # Closes above prev open
            curr_body > prev_body * 1.2):  # Larger body
            
            patterns.append({
                'name': 'BULLISH_ENGULFING',
                'type': 'REVERSAL',
                'strength': 'VERY_STRONG',
                'signal': 'BULLISH',
                'score': 25
            })
        
        # Bearish Engulfing
        if (prev_candle['close'] > prev_candle['open'] and  # Previous bullish
            curr_candle['close'] < curr_candle['open'] and  # Current bearish
            curr_candle['open'] > prev_candle['close'] and  # Opens above prev close
            curr_candle['close'] < prev_candle['open'] and  # Closes below prev open
            curr_body > prev_body * 1.2):  # Larger body
            
            patterns.append({
                'name': 'BEARISH_ENGULFING',
                'type': 'REVERSAL',
                'strength': 'VERY_STRONG',
                'signal': 'BEARISH',
                'score': 25
            })
        
        # Piercing Pattern (Bullish)
        if (prev_candle['close'] < prev_candle['open'] and  # Previous bearish
            curr_candle['close'] > curr_candle['open'] and  # Current bullish
            curr_candle['open'] < prev_candle['low'] and  # Opens below prev low
            curr_candle['close'] > (prev_candle['open'] + prev_candle['close']) / 2):  # Closes above midpoint
            
            patterns.append({
                'name': 'PIERCING_PATTERN',
                'type': 'REVERSAL',
                'strength': 'STRONG',
                'signal': 'BULLISH',
                'score': 22
            })
        
        # Dark Cloud Cover (Bearish)
        if (prev_candle['close'] > prev_candle['open'] and  # Previous bullish
            curr_candle['close'] < curr_candle['open'] and  # Current bearish
            curr_candle['open'] > prev_candle['high'] and  # Opens above prev high
            curr_candle['close'] < (prev_candle['open'] + prev_candle['close']) / 2):  # Closes below midpoint
            
            patterns.append({
                'name': 'DARK_CLOUD_COVER',
                'type': 'REVERSAL',
                'strength': 'STRONG',
                'signal': 'BEARISH',
                'score': 22
            })
        
        return patterns
    
    def detect_three_candle_patterns(self, candles):
        """Detect three candlestick patterns"""
        
        patterns = []
        
        if len(candles) < 3:
            return patterns
        
        c1, c2, c3 = candles[0], candles[1], candles[2]
        
        # Three White Soldiers (Bullish)
        if (c1['close'] > c1['open'] and c2['close'] > c2['open'] and c3['close'] > c3['open'] and  # All bullish
            c2['close'] > c1['close'] and c3['close'] > c2['close'] and  # Rising closes
            c2['open'] > c1['open'] and c3['open'] > c2['open']):  # Rising opens
            
            patterns.append({
                'name': 'THREE_WHITE_SOLDIERS',
                'type': 'CONTINUATION',
                'strength': 'VERY_STRONG',
                'signal': 'BULLISH',
                'score': 28
            })
        
        # Three Black Crows (Bearish)
        if (c1['close'] < c1['open'] and c2['close'] < c2['open'] and c3['close'] < c3['open'] and  # All bearish
            c2['close'] < c1['close'] and c3['close'] < c2['close'] and  # Falling closes
            c2['open'] < c1['open'] and c3['open'] < c2['open']):  # Falling opens
            
            patterns.append({
                'name': 'THREE_BLACK_CROWS',
                'type': 'CONTINUATION',
                'strength': 'VERY_STRONG',
                'signal': 'BEARISH',
                'score': 28
            })
        
        # Morning Star (Bullish)
        if (c1['close'] < c1['open'] and  # First candle bearish
            abs(c2['close'] - c2['open']) < abs(c1['close'] - c1['open']) * 0.3 and  # Second candle small
            c3['close'] > c3['open'] and  # Third candle bullish
            c3['close'] > (c1['open'] + c1['close']) / 2):  # Third closes above first midpoint
            
            patterns.append({
                'name': 'MORNING_STAR',
                'type': 'REVERSAL',
                'strength': 'VERY_STRONG',
                'signal': 'BULLISH',
                'score': 30
            })
        
        # Evening Star (Bearish)
        if (c1['close'] > c1['open'] and  # First candle bullish
            abs(c2['close'] - c2['open']) < abs(c1['close'] - c1['open']) * 0.3 and  # Second candle small
            c3['close'] < c3['open'] and  # Third candle bearish
            c3['close'] < (c1['open'] + c1['close']) / 2):  # Third closes below first midpoint
            
            patterns.append({
                'name': 'EVENING_STAR',
                'type': 'REVERSAL',
                'strength': 'VERY_STRONG',
                'signal': 'BEARISH',
                'score': 30
            })
        
        return patterns
    
    def get_candlestick_score(self, option_type):
        """Calculate candlestick pattern score for option type"""
        
        if not self.current_patterns:
            return 0, []
        
        total_score = 0
        supporting_patterns = []
        
        for pattern in self.current_patterns:
            signal = pattern['signal']
            score = pattern['score']
            
            # Check if pattern supports the option type
            if option_type == 'CE' and signal == 'BULLISH':
                total_score += score
                supporting_patterns.append(pattern['name'])
            elif option_type == 'PE' and signal == 'BEARISH':
                total_score += score
                supporting_patterns.append(pattern['name'])
            elif signal == 'INDECISION':
                # Neutral patterns get half score
                total_score += score * 0.5
                supporting_patterns.append(pattern['name'])
        
        # Cap maximum candlestick score at 25 points
        return min(25, total_score), supporting_patterns
    
    def update_multi_timeframe_indicators(self):
        """Update technical indicators for multiple timeframes"""
        
        if len(self.price_history) < 2:
            return
        
        current_time = datetime.now()
        
        # Get recent prices for bar creation
        recent_prices = [p['nifty'] for p in self.price_history[-10:] if p['nifty'] > 0]
        
        if len(recent_prices) < 2:
            return
        
        # 1. Update 1-minute bars (60 seconds)
        if not self.nifty_ohlc_1min or (current_time - self.nifty_ohlc_1min[-1]['timestamp']).total_seconds() >= 60:
            self.create_ohlc_bar(self.nifty_ohlc_1min, recent_prices[-2:], current_time, 100)  # Keep 100 bars
            self.calculate_indicators_for_timeframe('1min', self.nifty_ohlc_1min)
        
        # 2. Update 5-minute bars (300 seconds) - KEEP CURRENT SYSTEM
        if not self.nifty_ohlc_5min or (current_time - self.nifty_ohlc_5min[-1]['timestamp']).total_seconds() >= 300:
            self.create_ohlc_bar(self.nifty_ohlc_5min, recent_prices[-5:], current_time, 50)   # Keep 50 bars
            self.calculate_indicators_for_timeframe('5min', self.nifty_ohlc_5min)
        
        # 3. Update 15-minute bars (900 seconds)
        if not self.nifty_ohlc_15min or (current_time - self.nifty_ohlc_15min[-1]['timestamp']).total_seconds() >= 900:
            self.create_ohlc_bar(self.nifty_ohlc_15min, recent_prices, current_time, 30)       # Keep 30 bars
            self.calculate_indicators_for_timeframe('15min', self.nifty_ohlc_15min)
    
    def create_ohlc_bar(self, ohlc_list, prices, timestamp, max_bars):
        """Create OHLC bar and manage list size"""
        
        if len(prices) >= 2:
            ohlc_bar = {
                'timestamp': timestamp,
                'open': prices[0],
                'high': max(prices),
                'low': min(prices),
                'close': prices[-1],
                'volume': 1000000  # Dummy volume
            }
            
            ohlc_list.append(ohlc_bar)
            
            # Keep only required number of bars
            if len(ohlc_list) > max_bars:
                ohlc_list[:] = ohlc_list[-max_bars:]
    
    def calculate_indicators_for_timeframe(self, timeframe, ohlc_data):
        """Calculate indicators for specific timeframe"""
        
        if len(ohlc_data) < 26:  # Need at least 26 periods for MACD
            return
        
        closes = [bar['close'] for bar in ohlc_data]
        
        try:
            # Calculate all indicators
            rsi = self.calculate_rsi(closes, 14)
            macd, macd_signal, macd_histogram = self.calculate_macd(closes, 12, 26, 9)
            bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(closes, 20, 2)
            ema_9 = self.calculate_ema(closes, 9)
            ema_21 = self.calculate_ema(closes, 21)
            
            # Store indicators for this timeframe
            indicators = {
                'rsi': rsi,
                'macd': macd,
                'macd_signal': macd_signal,
                'macd_histogram': macd_histogram,
                'bb_upper': bb_upper,
                'bb_middle': bb_middle,
                'bb_lower': bb_lower,
                'ema_9': ema_9,
                'ema_21': ema_21,
                'current_price': closes[-1],
                'bb_position': self.get_bb_position(closes[-1], bb_upper, bb_middle, bb_lower),
                'trend': self.get_trend_direction(closes[-1], ema_9, ema_21, rsi, macd, macd_signal)
            }
            
            # Store in appropriate timeframe
            if timeframe == '1min':
                self.indicators_1min = indicators
            elif timeframe == '5min':
                self.indicators_5min = indicators
                # Also update legacy nifty_ohlc_data and current_indicators for ATR
                self.nifty_ohlc_data = ohlc_data.copy()
                # Calculate ATR for 5min timeframe
                if len(ohlc_data) >= 15:
                    atr = self.calculate_atr(ohlc_data, 14)
                    indicators['atr'] = atr
                self.current_indicators = indicators.copy()
            elif timeframe == '15min':
                self.indicators_15min = indicators
                
        except Exception as e:
            print(f"⚠️ Error calculating {timeframe} indicators: {e}")
    
    def get_trend_direction(self, price, ema_9, ema_21, rsi, macd, macd_signal):
        """Determine trend direction for timeframe"""
        
        bullish_signals = 0
        bearish_signals = 0
        
        # EMA trend
        if price > ema_9 > ema_21:
            bullish_signals += 2
        elif price < ema_9 < ema_21:
            bearish_signals += 2
        
        # RSI momentum
        if rsi > 50:
            bullish_signals += 1
        else:
            bearish_signals += 1
        
        # MACD trend
        if macd > macd_signal:
            bullish_signals += 1
        else:
            bearish_signals += 1
        
        if bullish_signals >= 3:
            return 'BULLISH'
        elif bearish_signals >= 3:
            return 'BEARISH'
        else:
            return 'NEUTRAL'
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI without TA-Lib"""
        if len(prices) < period + 1:
            return 50.0
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_ema(self, prices, period):
        """Calculate EMA without TA-Lib"""
        if len(prices) < period:
            return prices[-1] if prices else 0
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD without TA-Lib"""
        if len(prices) < slow:
            return 0, 0, 0
        
        ema_fast = self.calculate_ema(prices, fast)
        ema_slow = self.calculate_ema(prices, slow)
        
        macd_line = ema_fast - ema_slow
        
        # For signal line, we need historical MACD values
        if len(prices) < slow + signal:
            macd_signal = macd_line
        else:
            # Simplified signal calculation
            macd_signal = macd_line * 0.8  # Approximation
        
        macd_histogram = macd_line - macd_signal
        
        return macd_line, macd_signal, macd_histogram
    
    def calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calculate Bollinger Bands without TA-Lib"""
        if len(prices) < period:
            current_price = prices[-1] if prices else 25800
            return current_price + 50, current_price, current_price - 50
        
        recent_prices = prices[-period:]
        middle = np.mean(recent_prices)
        std = np.std(recent_prices)
        
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        
        return upper, middle, lower
    
    def calculate_atr(self, ohlc_data, period=14):
        """Calculate Average True Range (ATR) for volatility measurement"""
        if len(ohlc_data) < period + 1:
            return 50  # Default ATR for NIFTY
        
        true_ranges = []
        
        for i in range(1, len(ohlc_data)):
            high = ohlc_data[i]['high']
            low = ohlc_data[i]['low']
            prev_close = ohlc_data[i-1]['close']
            
            # True Range = max of:
            # 1. Current High - Current Low
            # 2. abs(Current High - Previous Close)
            # 3. abs(Current Low - Previous Close)
            tr1 = high - low
            tr2 = abs(high - prev_close)
            tr3 = abs(low - prev_close)
            
            true_range = max(tr1, tr2, tr3)
            true_ranges.append(true_range)
        
        # Calculate ATR as average of true ranges
        if len(true_ranges) >= period:
            atr = np.mean(true_ranges[-period:])
        else:
            atr = np.mean(true_ranges)
        
        return atr
    
    def calculate_volume_profile(self, option_data):
        """Calculate volume profile metrics for entry confirmation"""
        
        volume = option_data.get('volume', 0)
        
        # Get historical volume data if available
        # For now, use simple volume analysis
        
        # Volume categories based on NIFTY options typical volumes
        if volume >= 100000:  # Very high volume
            volume_strength = 'VERY_HIGH'
            volume_score = 5
        elif volume >= 50000:  # High volume
            volume_strength = 'HIGH'
            volume_score = 4
        elif volume >= 10000:  # Good volume
            volume_strength = 'GOOD'
            volume_score = 3
        elif volume >= 5000:  # Medium volume
            volume_strength = 'MEDIUM'
            volume_score = 2
        elif volume >= 1000:  # Low volume
            volume_strength = 'LOW'
            volume_score = 1
        else:  # Very low volume
            volume_strength = 'VERY_LOW'
            volume_score = 0
        
        return {
            'volume': volume,
            'strength': volume_strength,
            'score': volume_score,
            'scalper_ready': volume >= 50000,  # High volume for scalper
            'breakout_ready': volume >= 100000  # Very high volume for breakouts
        }
    
    def get_dynamic_stop_loss(self, atr, strategy='CONTRARIAN'):
        """Calculate dynamic stop loss based on ATR and strategy"""
        
        # ATR-based volatility classification for NIFTY
        if atr < 30:
            volatility = 'LOW'
            base_sl = 0.15  # 15% for low volatility
        elif atr < 60:
            volatility = 'MEDIUM'
            base_sl = 0.25  # 25% for medium volatility
        else:
            volatility = 'HIGH'
            base_sl = 0.35  # 35% for high volatility
        
        # Strategy-specific adjustments
        if strategy == 'SCALPER':
            # Scalper uses tighter stops
            stop_loss = min(base_sl, 0.10)
        elif strategy == 'TREND_RIDER':
            # Trend rider uses wider stops
            stop_loss = max(base_sl, 0.25)
        elif strategy in ['SUPPORT_BOUNCE', 'RESISTANCE_BOUNCE']:
            # Bounce strategies use medium stops
            stop_loss = min(base_sl, 0.20)
        else:
            # CONTRARIAN uses base ATR-adjusted stops
            stop_loss = base_sl
        
        return {
            'stop_loss_pct': stop_loss,
            'volatility': volatility,
            'atr': atr
        }
    
    def calculate_technical_indicators(self):
        """Calculate RSI, MACD, Bollinger Bands, EMA, and ATR using custom functions"""
        
        if len(self.nifty_ohlc_data) < 26:  # Need at least 26 periods for MACD
            self.current_indicators = {}
            return
        
        # Extract price arrays
        closes = [bar['close'] for bar in self.nifty_ohlc_data]
        
        try:
            # 1. RSI (14-period)
            current_rsi = self.calculate_rsi(closes, 14)
            
            # 2. MACD (12, 26, 9)
            current_macd, current_macd_signal, current_macd_histogram = self.calculate_macd(closes, 12, 26, 9)
            
            # 3. Bollinger Bands (20, 2)
            current_bb_upper, current_bb_middle, current_bb_lower = self.calculate_bollinger_bands(closes, 20, 2)
            
            # 4. EMA (9 and 21)
            current_ema_9 = self.calculate_ema(closes, 9)
            current_ema_21 = self.calculate_ema(closes, 21)
            
            # 5. ATR (14-period) - NEW!
            current_atr = self.calculate_atr(self.nifty_ohlc_data, 14)
            
            # Store current indicator values
            self.current_indicators = {
                'rsi': current_rsi,
                'macd': current_macd,
                'macd_signal': current_macd_signal,
                'macd_histogram': current_macd_histogram,
                'bb_upper': current_bb_upper,
                'bb_middle': current_bb_middle,
                'bb_lower': current_bb_lower,
                'ema_9': current_ema_9,
                'ema_21': current_ema_21,
                'current_price': closes[-1],
                'bb_position': self.get_bb_position(closes[-1], current_bb_upper, current_bb_middle, current_bb_lower),
                'atr': current_atr  # NEW!
            }
            
        except Exception as e:
            print(f"⚠️ Error calculating indicators: {e}")
            self.current_indicators = {}
    
    def get_bb_position(self, price, bb_upper, bb_middle, bb_lower):
        """Determine price position within Bollinger Bands"""
        
        if price >= bb_upper:
            return "UPPER"
        elif price <= bb_lower:
            return "LOWER"
        elif price >= bb_middle:
            return "UPPER_HALF"
        else:
            return "LOWER_HALF"
    
    def get_multi_timeframe_signals(self, option_type):
        """Get multi-timeframe technical signals for option type"""
        
        if not self.indicators_5min:  # Need at least 5min data
            return 0, []
        
        signals = []
        total_score = 0
        
        # 1. 15-MINUTE TREND FILTER (30 points max) - Major trend direction
        trend_15min_score, trend_15min_signals = self.get_trend_filter_score(option_type)
        total_score += trend_15min_score
        signals.extend(trend_15min_signals)
        
        # 2. 5-MINUTE ANALYSIS (40 points max) - Current system (keep working logic)
        main_5min_score, main_5min_signals = self.get_timeframe_signals(option_type, self.indicators_5min, '5min')
        total_score += main_5min_score
        signals.extend(main_5min_signals)
        
        # 3. 1-MINUTE PRECISION (15 points max) - Fine-tune entry timing
        if self.indicators_1min:
            timing_1min_score, timing_1min_signals = self.get_timing_signals(option_type, self.indicators_1min)
            total_score += timing_1min_score
            signals.extend(timing_1min_signals)
        
        return min(85, total_score), signals
    
    def get_trend_filter_score(self, option_type):
        """15-minute trend filter - more lenient for more trades"""
        
        if not self.indicators_15min:
            return 20, ['15MIN_NEUTRAL']  # Higher neutral score
        
        trend_15min = self.indicators_15min['trend']
        signals = []
        score = 0
        
        if option_type == 'CE':  # Call options
            if trend_15min == 'BULLISH':
                score = 30
                signals.append('15MIN_BULLISH_TREND')
            elif trend_15min == 'NEUTRAL':
                score = 25  # Increased from 15 to 25
                signals.append('15MIN_NEUTRAL_TREND')
            else:  # BEARISH
                score = 15  # Increased from 5 to 15 (allow some counter-trend)
                signals.append('15MIN_AGAINST_TREND')
        
        elif option_type == 'PE':  # Put options
            if trend_15min == 'BEARISH':
                score = 30
                signals.append('15MIN_BEARISH_TREND')
            elif trend_15min == 'NEUTRAL':
                score = 25  # Increased from 15 to 25
                signals.append('15MIN_NEUTRAL_TREND')
            else:  # BULLISH
                score = 15  # Increased from 5 to 15 (allow some counter-trend)
                signals.append('15MIN_AGAINST_TREND')
        
        return score, signals
    
    def get_timeframe_signals(self, option_type, indicators, timeframe_name):
        """Get signals for specific timeframe (main 5min analysis)"""
        
        signals = []
        score = 0
        
        rsi = indicators['rsi']
        macd = indicators['macd']
        macd_signal = indicators['macd_signal']
        macd_histogram = indicators['macd_histogram']
        bb_position = indicators['bb_position']
        current_price = indicators['current_price']
        ema_9 = indicators['ema_9']
        ema_21 = indicators['ema_21']
        
        if option_type == 'CE':  # Call options - looking for bullish signals
            
            # RSI Signals (0-10 points for 5min)
            if 40 <= rsi <= 70:
                score += 10
                signals.append(f"{timeframe_name}_RSI_BULLISH")
            elif 30 <= rsi < 40:
                score += 8
                signals.append(f"{timeframe_name}_RSI_OVERSOLD")
            elif rsi > 70:
                score += 6
                signals.append(f"{timeframe_name}_RSI_MOMENTUM")
            else:
                score += 2
            
            # MACD Signals (0-10 points for 5min)
            if macd > macd_signal and macd_histogram > 0:
                score += 10
                signals.append(f"{timeframe_name}_MACD_STRONG")
            elif macd > macd_signal:
                score += 8
                signals.append(f"{timeframe_name}_MACD_BULLISH")
            elif macd_histogram > 0:
                score += 6
                signals.append(f"{timeframe_name}_MACD_HIST_POS")
            else:
                score += 2
            
            # Bollinger Bands (0-10 points for 5min)
            if bb_position == "LOWER":
                score += 10
                signals.append(f"{timeframe_name}_BB_LOWER")
            elif bb_position == "LOWER_HALF":
                score += 8
                signals.append(f"{timeframe_name}_BB_BELOW_MID")
            elif bb_position == "UPPER_HALF":
                score += 6
                signals.append(f"{timeframe_name}_BB_ABOVE_MID")
            else:
                score += 2
            
            # EMA Signals (0-10 points for 5min)
            if current_price > ema_9 > ema_21:
                score += 10
                signals.append(f"{timeframe_name}_EMA_UPTREND")
            elif current_price > ema_9:
                score += 8
                signals.append(f"{timeframe_name}_EMA_ABOVE_9")
            elif current_price > ema_21:
                score += 6
                signals.append(f"{timeframe_name}_EMA_ABOVE_21")
            else:
                score += 2
        
        elif option_type == 'PE':  # Put options - looking for bearish signals
            
            # RSI Signals (0-10 points for 5min)
            if 30 <= rsi <= 60:
                score += 10
                signals.append(f"{timeframe_name}_RSI_BEARISH")
            elif 60 < rsi <= 70:
                score += 8
                signals.append(f"{timeframe_name}_RSI_OVERBOUGHT")
            elif rsi < 30:
                score += 6
                signals.append(f"{timeframe_name}_RSI_MOMENTUM")
            else:
                score += 2
            
            # MACD Signals (0-10 points for 5min)
            if macd < macd_signal and macd_histogram < 0:
                score += 10
                signals.append(f"{timeframe_name}_MACD_STRONG")
            elif macd < macd_signal:
                score += 8
                signals.append(f"{timeframe_name}_MACD_BEARISH")
            elif macd_histogram < 0:
                score += 6
                signals.append(f"{timeframe_name}_MACD_HIST_NEG")
            else:
                score += 2
            
            # Bollinger Bands (0-10 points for 5min)
            if bb_position == "UPPER":
                score += 10
                signals.append(f"{timeframe_name}_BB_UPPER")
            elif bb_position == "UPPER_HALF":
                score += 8
                signals.append(f"{timeframe_name}_BB_ABOVE_MID")
            elif bb_position == "LOWER_HALF":
                score += 6
                signals.append(f"{timeframe_name}_BB_BELOW_MID")
            else:
                score += 2
            
            # EMA Signals (0-10 points for 5min)
            if current_price < ema_9 < ema_21:
                score += 10
                signals.append(f"{timeframe_name}_EMA_DOWNTREND")
            elif current_price < ema_9:
                score += 8
                signals.append(f"{timeframe_name}_EMA_BELOW_9")
            elif current_price < ema_21:
                score += 6
                signals.append(f"{timeframe_name}_EMA_BELOW_21")
            else:
                score += 2
        
        return min(40, score), signals  # Max 40 points for 5min analysis
    
    def get_timing_signals(self, option_type, indicators_1min):
        """1-minute precision timing signals"""
        
        signals = []
        score = 0
        
        rsi_1min = indicators_1min['rsi']
        trend_1min = indicators_1min['trend']
        
        # 1-minute timing confirmation
        if option_type == 'CE':
            if trend_1min == 'BULLISH' and 45 <= rsi_1min <= 65:
                score = 15
                signals.append('1MIN_PERFECT_TIMING')
            elif trend_1min == 'BULLISH':
                score = 10
                signals.append('1MIN_GOOD_TIMING')
            elif 45 <= rsi_1min <= 65:
                score = 8
                signals.append('1MIN_RSI_TIMING')
            else:
                score = 3
                signals.append('1MIN_NEUTRAL')
        
        elif option_type == 'PE':
            if trend_1min == 'BEARISH' and 35 <= rsi_1min <= 55:
                score = 15
                signals.append('1MIN_PERFECT_TIMING')
            elif trend_1min == 'BEARISH':
                score = 10
                signals.append('1MIN_GOOD_TIMING')
            elif 35 <= rsi_1min <= 55:
                score = 8
                signals.append('1MIN_RSI_TIMING')
            else:
                score = 3
                signals.append('1MIN_NEUTRAL')
        
        return score, signals
    
    def get_technical_signals(self, option_type):
        """Legacy function - now calls multi-timeframe analysis"""
        return self.get_multi_timeframe_signals(option_type)
    
    def calculate_high_accuracy_score(self, option_data, market_analysis):
        """
        Calculate high accuracy score (0-100)
        Routes to appropriate scoring based on strategy_mode
        """
        
        if self.strategy_mode == 'SIMPLIFIED':
            return self.calculate_simplified_score(option_data, market_analysis)
        else:
            return self.calculate_current_score(option_data, market_analysis)
    
    def calculate_current_score(self, option_data, market_analysis):
        """Calculate CURRENT strategy score (complex - 260 points capped at 100)"""
        
        score = 0
        reasons = []
        
        # 1. Liquidity Score (25 points max)
        oi_score = min(25, (option_data['oi'] / 1000000) * 25)  # Max at 10L OI
        volume_score = min(10, (option_data['volume'] / 5000) * 10)  # Max at 5000 volume
        spread_score = max(0, 10 - option_data['bid_ask_spread'])  # Penalize wide spreads
        
        liquidity_score = oi_score + volume_score + spread_score
        score += liquidity_score
        
        if option_data['oi'] >= self.min_oi:
            reasons.append(f"Good OI: {option_data['oi']:,}")
        
        # PRIORITY 2: OI Change Analysis (0-15 points)
        oi_change_score = 0
        if self.priority_features:
            oi_analysis = self.priority_features.analyze_oi_changes(
                option_data,
                option_data['symbol']
            )
            
            # Add OI change score
            oi_change_score = oi_analysis['strength'] * 0.15
            score += oi_change_score
            
            if oi_analysis['strength'] > 50:
                reasons.append(f"OI: {oi_analysis['reason']}")
        
        # 2. Premium Quality Score (20 points max) - ADAPTIVE FILTER
        ltp = option_data['ltp']
        
        # 🚨 ADAPTIVE PREMIUM FILTER: Adjust based on market condition
        # Strong trends allow higher premiums, choppy markets need cheap options
        
        # Get market trend strength from analysis
        trend = market_analysis.get('trend', 'NEUTRAL')
        strength = market_analysis.get('strength', 0)
        
        # Determine premium limit based on market condition
        if trend in ['STRONG_BULLISH', 'STRONG_BEARISH'] and strength >= 0.7:
            # STRONG TREND: Allow expensive options (they work in trending markets)
            max_premium = 150
            premium_category = "Strong Trend"
        elif trend in ['BULLISH', 'BEARISH'] and strength >= 0.5:
            # MODERATE TREND: Allow moderate premiums
            max_premium = 100
            premium_category = "Moderate Trend"
        else:
            # CHOPPY/RANGE: Strict limit (your Nov 14 scenario)
            max_premium = 70
            premium_category = "Choppy/Range"
        
        # REJECT if premium exceeds market-condition limit
        if ltp > max_premium:
            return {
                'score': 0,
                'reasons': [f"❌ REJECTED: Premium ₹{ltp:.2f} too high for {premium_category} market (limit: ₹{max_premium})"],
                'penalties': [f"Premium exceeds {premium_category} limit of ₹{max_premium}"],
                'patterns': [],
                'breakdown': {}
            }
        
        # Score based on YOUR ACTUAL 5-DAY PERFORMANCE DATA
        if 25 <= ltp <= 40:  # BEST RANGE: 77.8% win rate, +₹9,475
            premium_score = 20
            reasons.append(f"✅ OPTIMAL premium: ₹{ltp:.2f} (77.8% win rate)")
        elif 15 <= ltp <= 25:  # GOOD RANGE: 60% win rate, +₹9,683
            premium_score = 18
            reasons.append(f"✅ Good premium: ₹{ltp:.2f} (60% win rate)")
        elif 40 < ltp <= 50:  # ACCEPTABLE
            premium_score = 15
            reasons.append(f"Good premium: ₹{ltp:.2f}")
        elif 50 < ltp <= 70:  # MODERATE (allowed in trends)
            premium_score = 12
            reasons.append(f"Moderate premium: ₹{ltp:.2f}")
        elif 70 < ltp <= 100:  # EXPENSIVE (only in strong trends)
            premium_score = 10
            reasons.append(f"⚠️ Expensive: ₹{ltp:.2f} ({premium_category})")
        elif 100 < ltp <= 150:  # VERY EXPENSIVE (only in very strong trends)
            premium_score = 8
            reasons.append(f"⚠️ Very expensive: ₹{ltp:.2f} ({premium_category})")
        elif ltp < 15:
            premium_score = 5  # Too cheap
            reasons.append(f"⚠️ Low premium: ₹{ltp:.2f}")
        else:
            premium_score = 0
        
        score += premium_score
        
        # 3. Trend Alignment Score (25 points max)
        trend = market_analysis['trend']
        strength = market_analysis['strength']
        
        if trend in ['STRONG_BULLISH', 'STRONG_BEARISH']:
            if ((trend == 'STRONG_BULLISH' and option_data['option_type'] == 'CE') or
                (trend == 'STRONG_BEARISH' and option_data['option_type'] == 'PE')):
                trend_score = 25
                reasons.append(f"Perfect trend alignment: {trend}")
            else:
                trend_score = 5  # Against trend
        elif trend in ['BULLISH', 'BEARISH']:
            if ((trend == 'BULLISH' and option_data['option_type'] == 'CE') or
                (trend == 'BEARISH' and option_data['option_type'] == 'PE')):
                trend_score = 15
                reasons.append(f"Good trend alignment: {trend}")
            else:
                trend_score = 8
        else:
            trend_score = 10  # Neutral/sideways
        
        score += trend_score
        
        # 4. Strike Selection Score (15 points max) - DATA-DRIVEN DISTANCE FILTER
        distance = abs(option_data['strike'] - self.last_nifty_price)
        
        # 🚨 CRITICAL: Premium-based distance limits (based on your 5-day data)
        # ₹15-40 premiums (66.7% win rate) can be far OTM - your winners!
        # ₹50-70 premiums must be ATM - risky otherwise
        
        if ltp <= 40:
            # OPTIMAL RANGE (₹15-40): Allow up to 400 points
            # Your winning trades: 25550 PE @ ₹20-26 (300+ pts away)
            max_distance = 400
            category = "Optimal"
        elif ltp <= 50:
            # ACCEPTABLE RANGE (₹40-50): Allow up to 200 points
            max_distance = 200
            category = "Acceptable"
        elif ltp <= 70:
            # RISKY RANGE (₹50-70): Must be within 100 points
            max_distance = 100
            category = "Risky"
        else:
            # REJECTED RANGE (>₹70): Already rejected above
            max_distance = 50
            category = "Rejected"
        
        # Reject if strike too far for this premium level
        if distance > max_distance:
            return {
                'score': 0,
                'reasons': [f"❌ REJECTED: {category} premium ₹{ltp:.2f} | Strike {distance:.0f} pts away (max: {max_distance})"],
                'penalties': [f"Strike distance {distance:.0f} exceeds limit {max_distance} for premium ₹{ltp:.2f}"],
                'patterns': [],
                'breakdown': {}
            }
        
        # Score based on distance (prefer closer strikes for better delta)
        if distance <= 50:  # ATM zone (best delta)
            strike_score = 15
            reasons.append(f"✅ ATM ({distance:.0f} pts)")
        elif distance <= 150:  # Near-ATM (good delta)
            strike_score = 13
            reasons.append(f"Near-ATM ({distance:.0f} pts)")
        elif distance <= 300:  # OTM (acceptable for cheap premiums)
            strike_score = 11
            reasons.append(f"OTM ({distance:.0f} pts)")
        else:  # Far OTM (only for very cheap premiums)
            strike_score = 9
            reasons.append(f"Far OTM ({distance:.0f} pts)")
        
        score += strike_score
        
        # 5. Market Structure Score (10 points max - reduced to make room for candlesticks)
        structure = market_analysis['structure']
        confidence = market_analysis['confidence']
        
        if structure in ['UPTREND', 'DOWNTREND'] and confidence >= 80:
            structure_score = 10
            reasons.append(f"Clear {structure.lower()}")
        elif structure == 'RANGE' and confidence >= 70:
            structure_score = 7
            reasons.append("Range-bound market")
        else:
            structure_score = 3
        
        score += structure_score
        
        # 6. Technical Indicators Score (85 points max - NEW!)
        technical_score, technical_signals = self.get_technical_signals(option_data['option_type'])
        score += technical_score
        
        if technical_signals:
            reasons.append(f"Technical: {', '.join(technical_signals[:2])}")
        
        # PRIORITY 3: Stochastic Oscillator (0-10 points)
        stoch_score = 0
        if self.priority_features and len(self.nifty_ohlc_5min) >= 17:
            stoch = self.priority_features.calculate_stochastic(self.nifty_ohlc_5min)
            
            # Add stochastic score
            stoch_score = stoch['score'] * 0.10
            score += stoch_score
            
            if stoch['crossover'] != 'NONE':
                reasons.append(f"Stoch: {stoch['crossover']} crossover")
            elif stoch['signal'] in ['OVERSOLD', 'OVERBOUGHT']:
                reasons.append(f"Stoch: {stoch['signal']}")
        
        # 7. Candlestick Pattern Score (15 points max - reduced to make room for technical)
        candlestick_score, pattern_names = self.get_candlestick_score(option_data['option_type'])
        candlestick_score = min(15, candlestick_score)  # Reduced from 25 to 15
        score += candlestick_score
        
        if pattern_names:
            reasons.append(f"Candlestick: {', '.join(pattern_names[:2])}")
        
        # 8. ATR Volatility Score (5 points max) - NEW!
        atr_score = 0
        atr_value = 0
        volatility_level = 'UNKNOWN'
        
        if self.current_indicators and 'atr' in self.current_indicators:
            atr_value = self.current_indicators['atr']
            
            # Score based on optimal volatility for options trading
            if 30 <= atr_value <= 60:  # Optimal volatility range
                atr_score = 5
                volatility_level = 'OPTIMAL'
                reasons.append(f"✅ Optimal volatility (ATR: {atr_value:.1f})")
            elif 20 <= atr_value < 30 or 60 < atr_value <= 80:  # Good volatility
                atr_score = 3
                volatility_level = 'GOOD'
                reasons.append(f"Good volatility (ATR: {atr_value:.1f})")
            elif atr_value < 20:  # Too low (choppy)
                atr_score = 1
                volatility_level = 'LOW'
            else:  # Too high (risky)
                atr_score = 2
                volatility_level = 'HIGH'
        
        score += atr_score
        
        # 9. Volume Profile Score (5 points max) - NEW!
        volume_profile = self.calculate_volume_profile(option_data)
        volume_score = volume_profile['score']
        score += volume_score
        
        if volume_profile['strength'] in ['HIGH', 'VERY_HIGH']:
            reasons.append(f"✅ {volume_profile['strength']} volume ({volume_profile['volume']:,})")
        
        # PRIORITY 4: Greeks Analysis (0-10 points)
        greeks_score = 0
        if self.priority_features:
            # Calculate days to expiry
            try:
                # Extract expiry from symbol (e.g., NIFTY25NOV25P25850)
                symbol = option_data.get('symbol', '')
                if 'NOV25' in symbol:
                    expiry_str = symbol.split('NOV25')[0][-2:] + 'NOV25'
                    expiry_date = datetime.strptime(expiry_str, '%d%b%y')
                    days_to_expiry = max(0, (expiry_date - datetime.now()).days)
                elif 'DEC25' in symbol:
                    expiry_str = symbol.split('DEC25')[0][-2:] + 'DEC25'
                    expiry_date = datetime.strptime(expiry_str, '%d%b%y')
                    days_to_expiry = max(0, (expiry_date - datetime.now()).days)
                else:
                    days_to_expiry = 7  # Default to 1 week
                
                greeks = self.priority_features.calculate_greeks(
                    option_data,
                    self.last_nifty_price,
                    days_to_expiry,
                    implied_volatility=0.20
                )
                
                # Add Greeks score
                greeks_score = greeks['score'] * 0.10
                score += greeks_score
                
                # Add delta to reasons
                reasons.append(f"Δ:{abs(greeks['delta']):.2f}")
                
                # Warn about high theta decay
                if days_to_expiry <= 3 and abs(greeks['theta']) > 50:
                    reasons.append(f"⚠️ High θ decay")
                
            except Exception as e:
                pass  # Skip Greeks if calculation fails
        
        # Update scoring breakdown
        scoring_breakdown = {
            'liquidity': liquidity_score,
            'premium': premium_score,
            'trend': trend_score,
            'strike': strike_score,
            'structure': structure_score,
            'technical': technical_score,
            'candlestick': candlestick_score,
            'atr': atr_score,
            'volume_profile': volume_score,
            'oi_change': oi_change_score,
            'stochastic': stoch_score,
            'greeks': greeks_score
        }
        
        # Penalty factors
        penalties = []
        
        # Penalty for low volume
        if option_data['volume'] < self.min_volume:
            score -= 10
            penalties.append("Low volume")
        
        # Penalty for wide bid-ask spread
        if option_data['bid_ask_spread'] > 5:
            score -= 5
            penalties.append("Wide spread")
        
        # Penalty for extreme moves (might be news-based)
        if abs(option_data['change_pct']) > 20:
            score -= 5
            penalties.append("Extreme move")
        
        # Penalty for expensive options (time decay risk)
        if option_data['ltp'] > 150:
            score -= 15
            penalties.append("Expensive premium")
        
        # Penalty for ATM options (maximum time decay)
        distance = abs(option_data['strike'] - self.last_nifty_price)
        if distance <= 25:
            score -= 10
            penalties.append("ATM time decay risk")
        
        final_score = max(0, min(100, score))
        
        return {
            'score': final_score,
            'reasons': reasons,
            'penalties': penalties,
            'patterns': pattern_names,
            'breakdown': scoring_breakdown
        }
    
    def calculate_simplified_score(self, option_data, market_analysis):
        """
        Calculate SIMPLIFIED strategy score (100 points max)
        
        Breakdown:
        1. Price Action Trend (25 pts) - Last 20 bars analysis
        2. Candlestick Patterns (25 pts) - Visual confirmation
        3. EMA Trend (15 pts) - EMA 9 & 21
        4. RSI Momentum (10 pts) - Overbought/Oversold
        5. Premium Quality (15 pts) - Smart selection by distance
        6. Liquidity (10 pts) - OI & Volume
        """
        
        score = 0
        reasons = []
        patterns = []
        
        # 1. PRICE ACTION TREND (25 points)
        if len(self.price_history) >= 20:
            recent_prices = [p['nifty'] for p in self.price_history[-20:]]
            up_moves = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] > recent_prices[i-1])
            down_moves = sum(1 for i in range(1, len(recent_prices)) if recent_prices[i] < recent_prices[i-1])
            total_moves = up_moves + down_moves
            
            if total_moves > 0:
                if option_data['option_type'] == 'CE':
                    up_pct = up_moves / total_moves
                    if up_pct >= 0.70:
                        score += 25
                        reasons.append(f"🟢 Strong Bullish PA ({up_pct:.0%})")
                    elif up_pct >= 0.60:
                        score += 20
                        reasons.append(f"🟢 Bullish PA ({up_pct:.0%})")
                    elif up_pct >= 0.55:
                        score += 15
                        reasons.append(f"🟢 Moderate Bullish PA")
                else:  # PE
                    down_pct = down_moves / total_moves
                    if down_pct >= 0.70:
                        score += 25
                        reasons.append(f"🔴 Strong Bearish PA ({down_pct:.0%})")
                    elif down_pct >= 0.60:
                        score += 20
                        reasons.append(f"🔴 Bearish PA ({down_pct:.0%})")
                    elif down_pct >= 0.55:
                        score += 15
                        reasons.append(f"🔴 Moderate Bearish PA")
        
        # 2. CANDLESTICK PATTERNS (25 points)
        if self.current_patterns:
            candle_score = 0
            for pattern in self.current_patterns:
                if option_data['option_type'] == 'CE' and pattern['signal'] == 'BULLISH':
                    candle_score += 12
                    patterns.append(pattern['name'])
                elif option_data['option_type'] == 'PE' and pattern['signal'] == 'BEARISH':
                    candle_score += 12
                    patterns.append(pattern['name'])
            
            candle_score = min(25, candle_score)
            score += candle_score
            if patterns:
                reasons.append(f"🕯️ {', '.join(patterns[:2])}")
        
        # 3. EMA TREND (15 points)
        if len(self.nifty_ohlc_5min) >= 21:
            closes = [c['close'] for c in self.nifty_ohlc_5min]
            current_price = closes[-1]
            ema_9 = self.calculate_ema(closes, 9)
            ema_21 = self.calculate_ema(closes, 21)
            
            if option_data['option_type'] == 'CE':
                if current_price > ema_9 > ema_21:
                    score += 15
                    reasons.append("📈 EMA: Strong Uptrend")
                elif current_price > ema_9:
                    score += 10
                    reasons.append("📈 EMA: Uptrend")
            else:  # PE
                if current_price < ema_9 < ema_21:
                    score += 15
                    reasons.append("📉 EMA: Strong Downtrend")
                elif current_price < ema_9:
                    score += 10
                    reasons.append("📉 EMA: Downtrend")
        
        # 4. RSI MOMENTUM (10 points)
        if len(self.nifty_ohlc_5min) >= 14:
            closes = [c['close'] for c in self.nifty_ohlc_5min]
            rsi = self.calculate_rsi(closes, 14)
            
            if option_data['option_type'] == 'CE':
                if rsi <= 30:
                    score += 10
                    reasons.append(f"📊 RSI: Oversold ({rsi:.0f})")
                elif rsi <= 40:
                    score += 7
                    reasons.append(f"📊 RSI: Near Oversold ({rsi:.0f})")
                elif rsi <= 60:
                    score += 5
            else:  # PE
                if rsi >= 70:
                    score += 10
                    reasons.append(f"📊 RSI: Overbought ({rsi:.0f})")
                elif rsi >= 60:
                    score += 7
                    reasons.append(f"📊 RSI: Near Overbought ({rsi:.0f})")
                elif rsi >= 40:
                    score += 5
        
        # 5. PREMIUM QUALITY - SMART SELECTION (15 points)
        ltp = option_data['ltp']
        distance = abs(option_data['strike'] - self.last_nifty_price)
        
        if distance <= 50:  # ATM
            optimal_min, optimal_max = 40, 80
            category = "ATM"
        elif distance <= 150:  # Near-ATM
            optimal_min, optimal_max = 20, 40
            category = "Near-ATM"
        elif distance <= 300:  # OTM
            optimal_min, optimal_max = 10, 20
            category = "OTM"
        else:
            optimal_min, optimal_max = 0, 0
        
        if optimal_min <= ltp <= optimal_max:
            score += 15
            reasons.append(f"💰 Optimal {category}: ₹{ltp:.0f}")
        elif optimal_min * 0.8 <= ltp <= optimal_max * 1.2:
            score += 10
            reasons.append(f"💰 Good {category}: ₹{ltp:.0f}")
        elif optimal_min * 0.6 <= ltp <= optimal_max * 1.4:
            score += 5
        
        # 6. LIQUIDITY (10 points)
        oi = option_data['oi']
        volume = option_data['volume']
        
        if oi >= 100000 and volume >= 500:
            if oi >= 500000:
                score += 7
            elif oi >= 200000:
                score += 5
            else:
                score += 3
            
            if volume >= 5000:
                score += 3
            elif volume >= 1000:
                score += 2
            else:
                score += 1
            
            reasons.append(f"📊 OI: {oi/100000:.1f}L")
        
        return {
            'score': score,
            'reasons': reasons,
            'penalties': [],
            'patterns': patterns,
            'breakdown': {
                'price_action': 25,
                'candlestick': 25,
                'ema': 15,
                'rsi': 10,
                'premium': 15,
                'liquidity': 10
            }
        }
    
    def find_high_accuracy_opportunities(self):
        """Find only high accuracy trading opportunities"""
        
        # 🚨 FILTER 1: MAX TRADES PER DAY (8 trades max - STRICT!)
        entry_trades_today = sum(1 for t in self.trade_history if t.get('action') == 'ENTRY')
        if entry_trades_today >= 8:
            print(f"🚫 MAX TRADES REACHED: {entry_trades_today}/8 trades today")
            print(f"   Reason: Prevent overtrading - Quality over quantity")
            print(f"   💤 Sitting out for rest of day")
            return []
        
        # 🚨 TIME-BASED FILTER: No trading after 2:30 PM (risky end-of-day volatility)
        current_time = datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        # Block trading after 2:30 PM (14:30)
        if current_hour > 14 or (current_hour == 14 and current_minute >= 30):
            print(f"⏰ No trading after 2:30 PM (Current: {current_hour}:{current_minute:02d})")
            print(f"   Reason: High reversal risk in final hour")
            return []
        
        # Also avoid first 15 minutes (9:15-9:30) - high volatility
        if current_hour == 9 and current_minute < 30:
            print(f"⏰ No trading before 9:30 AM (Current: {current_hour}:{current_minute:02d})")
            print(f"   Reason: Market opening volatility")
            return []
        
        market_analysis = self.analyze_market_structure()
        
        if market_analysis['confidence'] < 70:
            print(f"⚠️ Market analysis confidence too low: {market_analysis['confidence']:.1f}%")
            return []
        
        # 🚨 FILTER 2: MARKET CONDITION - Sit out if choppy (STRENGTHENED!)
        market_condition = None
        if self.priority_features:
            market_condition = self.priority_features.detect_market_condition(
                self.price_history,
                self.indicators_5min,
                self.indicators_15min
            )
            
            # Block trading in CHOPPY markets (STRICT!)
            if market_condition['condition'] == 'CHOPPY':
                print(f"🚫 MARKET CONDITION: {market_condition['condition']}")
                print(f"   Reason: {market_condition['reason']}")
                print(f"   💤 Sitting out - No trades in choppy market")
                return []
            
            # Block RANGING markets with low score (NEW!)
            if market_condition['condition'] == 'RANGE_BOUND' and market_condition['score'] < 65:
                print(f"🚫 MARKET CONDITION: {market_condition['condition']} (Low score: {market_condition['score']:.0f})")
                print(f"   Reason: {market_condition['reason']}")
                print(f"   💤 Sitting out - Ranging market not suitable")
                return []
            
            # Also check if market is too volatile (high risk)
            if market_condition['condition'] == 'VOLATILE' and market_condition['score'] < 50:
                print(f"⚠️ MARKET CONDITION: {market_condition['condition']} (Score: {market_condition['score']:.0f})")
                print(f"   Reason: {market_condition['reason']}")
                print(f"   💤 Sitting out - Too risky")
                return []
            
            print(f"✅ MARKET CONDITION: {market_condition['condition']} (Score: {market_condition['score']:.0f}/100)")
            print(f"   {market_condition['reason']}")
        
        # 🎯 ADAPTIVE ENGINE: Analyze market and get parameters
        adaptive_params = None
        if self.adaptive_engine:
            adaptive_params = self.adaptive_engine.analyze_and_adapt(
                self.price_history,
                self.indicators_5min,
                self.indicators_15min,
                self.current_capital
            )
            
            print(f"🎯 ADAPTIVE MODE: {adaptive_params['mode']} (Confidence: {adaptive_params['confidence']:.0f}%)")
            print(f"   Strategy: {adaptive_params['strategy']}")
            print(f"   {adaptive_params['reason']}")
            print(f"   Max Trades: {adaptive_params['max_trades']} | Position Size: {adaptive_params['position_size']} lots")
            print(f"   Trading: {'✅ ALLOWED' if adaptive_params['allow_trading'] else '🚫 SITTING OUT'}")
            
            # If not allowed to trade, return empty
            if not adaptive_params['allow_trading']:
                print(f"💤 Sitting out - Market conditions unfavorable")
                return []
            
            # Check trade limit
            if not self.adaptive_engine.can_take_more_trades(adaptive_params['max_trades']):
                print(f"⚠️ Trade limit reached ({adaptive_params['max_trades']} trades)")
                return []
        
        opportunities = []
        
        print(f"🔍 Market Analysis:")
        print(f"   Trend: {market_analysis['trend']} (Strength: {market_analysis['strength']:.2f})")
        print(f"   Structure: {market_analysis['structure']}")
        print(f"   NIFTY: {self.last_nifty_price:.0f}")
        
        for symbol, data in self.market_data.items():
            # Pre-filter with strict criteria
            if (data['ltp'] < self.min_premium or 
                data['ltp'] > self.max_premium or
                data['oi'] < self.min_oi or
                data['volume'] < self.min_volume):
                continue
            
            # 🚨 FIX 1: MANDATORY Trend Direction Filter (NO EXCEPTIONS!)
            if not self.priority_features:
                print(f"❌ CRITICAL: Priority features not available - Cannot trade safely!")
                return []
            
            trend_check = self.priority_features.check_trend_direction_alignment(
                data['option_type'],
                self.price_history,
                self.indicators_5min,
                self.indicators_15min
            )
            
            if not trend_check['allowed']:
                # 🆕 DEBUG: Print why trade was blocked
                print(f"   ⏭️ Skipping {data['symbol']} - {trend_check['reason']}")
                continue  # Skip this option - MANDATORY FILTER
            
            # 🚨 FILTER 3: Strike Diversity - Max 2 trades per strike per day (STRICT!)
            strike = data['strike']
            option_type = data['option_type']
            
            # Count trades for THIS SPECIFIC strike AND option type
            strike_trade_count = sum(1 for t in self.trade_history 
                                    if t.get('strike') == strike 
                                    and t.get('option_type') == option_type
                                    and t.get('action') == 'ENTRY')
            
            if strike_trade_count >= 2:
                # Skip this strike - already traded twice today
                print(f"   ⏭️ Skipping {strike} {option_type} - Already traded {strike_trade_count} times today (MAX 2)")
                continue
            
            # Calculate accuracy score
            score_data = self.calculate_high_accuracy_score(data, market_analysis)
            
            # Only consider high accuracy opportunities
            if score_data['score'] >= self.min_accuracy_score:
                # Determine strategy BEFORE adding to opportunities
                strategy = self.determine_strategy(data, market_analysis, market_condition)
                
                # 🚨 FILTER 4: Strategy-Market Fit - Block CONTRARIAN in ranging markets
                if strategy == 'CONTRARIAN' and market_condition:
                    # CONTRARIAN only works in TRENDING markets
                    if market_condition['condition'] in ['RANGING', 'CHOPPY']:
                        print(f"   ⏭️ Skipping CONTRARIAN trade - Market is {market_condition['condition']}")
                        print(f"      Reason: CONTRARIAN needs TRENDING market, not {market_condition['condition']}")
                        continue
                
                opportunities.append({
                    'data': data,
                    'score_data': score_data,
                    'market_analysis': market_analysis,
                    'strategy': strategy
                })
        
        # 🚨 FIX 3: Better Strike Selection - Multi-factor ranking
        # Sort by multiple factors, not just score
        opportunities.sort(key=lambda x: (
            x['score_data']['score'],  # Primary: Accuracy score
            x['data']['oi'],  # Secondary: Higher OI
            -abs(x['data']['strike'] - self.last_nifty_price),  # Tertiary: Closer to ATM
            x['data']['volume']  # Quaternary: Higher volume
        ), reverse=True)
        
        # Remove duplicate strikes (keep only best opportunity per strike)
        seen_strikes = set()
        unique_opportunities = []
        
        for opp in opportunities:
            strike = opp['data']['strike']
            if strike not in seen_strikes:
                unique_opportunities.append(opp)
                seen_strikes.add(strike)
        
        opportunities = unique_opportunities
        
        if opportunities:
            print(f"🎯 Found {len(opportunities)} high accuracy opportunities (after filters):")
            for i, opp in enumerate(opportunities[:3], 1):
                data = opp['data']
                score = opp['score_data']['score']
                distance = abs(data['strike'] - self.last_nifty_price)
                print(f"   {i}. {data['symbol']} @ ₹{data['ltp']:.2f}")
                print(f"      Score: {score:.0f}/100 | OI: {data['oi']:,} | Distance: {distance:.0f}pts")
        
        return opportunities[:1]  # Return ONLY 1 best opportunity (not 3)
    
    def determine_strategy(self, option_data, market_analysis, market_condition=None):
        """Determine the best strategy for the opportunity - OPTIMIZED FOR PROFITABILITY"""
        
        # 🎯 NEW WINNING STRATEGIES (Based on pattern analysis)
        # ✅ CONTRARIAN: +₹21,947 (57.9% WR) - PRIMARY (ONLY IN TRENDING MARKETS!)
        # ✅ SCALPER: +₹13,826 (100% WR) - NEW
        # ✅ TREND_RIDER: +₹44,403 (100% WR) - NEW
        # ✅ SUPPORT_RESISTANCE_BOUNCE: +₹6,255 (100% WR) - NEW
        # ✅ MOMENTUM_BREAKOUT: +₹7,477 (100% WR) - NEW (disabled for now)
        
        # Get market condition if not provided
        if market_condition is None and self.priority_features:
            market_condition = self.priority_features.detect_market_condition(
                self.price_history,
                self.indicators_5min,
                self.indicators_15min
            )
        
        trend = market_analysis['trend']
        structure = market_analysis['structure']
        strength = market_analysis['strength']
        option_type = option_data['option_type']
        ltp = option_data['ltp']
        
        # Get current time for time-based strategies
        current_time = datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        # 1. SCALPER STRATEGY - 🔴 DISABLED (31% WR, ₹-23,201 loss across 100 trades)
        # SCALPER has been proven to lose money consistently
        # Disabled on Nov 26, 2025 based on data analysis
        # if (15 <= ltp <= 40 and 
        #     10 <= current_hour < 14 and  # 10:00 AM - 2:00 PM
        #     option_data['bid_ask_spread'] < 0.5):
        #     
        #     # 🚨 CRITICAL: Block SCALPER in choppy markets
        #     if market_condition and not market_condition['allow_scalper']:
        #         print(f"⚠️ SCALPER blocked: {market_condition['reason']}")
        #         return 'CONTRARIAN'  # Fallback to contrarian
        #     
        #     return 'SCALPER'
        
        # 2. TREND RIDER STRATEGY (15% allocation)
        # Ride strong trends with cheap premiums for 60-120 minutes
        if (20 <= ltp <= 40 and 
            strength >= 0.7 and
            trend in ['STRONG_BULLISH', 'STRONG_BEARISH', 'BULLISH', 'BEARISH']):
            # Check trend alignment
            if ((trend in ['STRONG_BULLISH', 'BULLISH'] and option_type == 'CE') or
                (trend in ['STRONG_BEARISH', 'BEARISH'] and option_type == 'PE')):
                
                # Block TREND_RIDER in choppy markets
                if market_condition and not market_condition['allow_trend_rider']:
                    print(f"⚠️ TREND_RIDER blocked: {market_condition['reason']}")
                    return 'CONTRARIAN'
                
                return 'TREND_RIDER'
        
        # 3. SUPPORT/RESISTANCE BOUNCE STRATEGY (5% allocation)
        # Trade bounces at key round numbers
        round_numbers = [25500, 25600, 25700, 25800, 25900, 26000]
        nifty_level = self.last_nifty_price
        
        # Check if NIFTY is near a key level (within 20 points)
        for level in round_numbers:
            if abs(nifty_level - level) <= 20 and 15 <= ltp <= 50:
                # At support, buy CE (bounce up)
                # At resistance, buy PE (bounce down)
                if nifty_level <= level and option_type == 'CE':
                    return 'SUPPORT_BOUNCE'
                elif nifty_level >= level and option_type == 'PE':
                    return 'RESISTANCE_BOUNCE'
        
        # 4. MOMENTUM BREAKOUT STRATEGY (disabled for now - needs more testing)
        # Catch explosive moves with RSI extremes + MACD crossover
        # if self.current_indicators:
        #     rsi = self.current_indicators.get('rsi', 50)
        #     macd = self.current_indicators.get('macd', 0)
        #     macd_signal = self.current_indicators.get('macd_signal', 0)
        #     
        #     if option_type == 'CE' and rsi > 70 and macd > macd_signal:
        #         return 'MOMENTUM_BREAKOUT'
        #     elif option_type == 'PE' and rsi < 30 and macd < macd_signal:
        #         return 'MOMENTUM_BREAKOUT'
        
        # 5. CONTRARIAN STRATEGY (PRIMARY - 100% allocation now that SCALPER is disabled)
        # 🚨 CRITICAL: CONTRARIAN only works in TRENDING markets!
        # Block CONTRARIAN in RANGING/CHOPPY markets
        if market_condition:
            if market_condition['condition'] in ['RANGING', 'CHOPPY']:
                # Don't trade in ranging/choppy markets
                # Return None to skip this trade
                return None  # Will be filtered out
        
        # Default to CONTRARIAN for trending markets
        return 'CONTRARIAN'
    
    def calculate_optimal_position_size(self, option_price, accuracy_score):
        """Calculate position size based on accuracy and available capital - ADAPTIVE"""
        
        # 🎯 ADAPTIVE: Use engine's position size if available
        if self.adaptive_engine and hasattr(self.adaptive_engine, 'current_mode'):
            adaptive_params = self.adaptive_engine.analyze_and_adapt(
                self.price_history,
                self.indicators_5min,
                self.indicators_15min,
                self.current_capital
            )
            
            # Use adaptive position size directly
            base_quantity = adaptive_params['position_size']
            
            # Adjust slightly based on accuracy score
            if accuracy_score >= 100:
                final_quantity = base_quantity
            elif accuracy_score >= 95:
                final_quantity = int(base_quantity * 0.9)  # 90%
            else:
                final_quantity = int(base_quantity * 0.75)  # 75%
            
            # Ensure minimum 75 lots
            final_quantity = max(75, final_quantity)
            
            return final_quantity
        
        # Fallback to original logic if adaptive not available
        if accuracy_score >= 120:
            risk_pct = 0.25  # 25% for very high accuracy
        elif accuracy_score >= 100:
            risk_pct = 0.20  # 20% for high accuracy
        elif accuracy_score >= 90:
            risk_pct = 0.15  # 15% for good accuracy
        else:
            risk_pct = 0.10  # 10% for minimum accuracy
        
        # Calculate risk amount
        risk_amount = self.current_capital * risk_pct
        
        # Calculate quantity based on stop loss
        stop_loss_amount = option_price * self.stop_loss_pct
        
        if stop_loss_amount > 0:
            calculated_quantity = int(risk_amount / stop_loss_amount)
        else:
            calculated_quantity = int(risk_amount / option_price)
        
        # Standard lot sizes used in real trading (15, 30, 45, 60, 75, 90, etc.)
        standard_lots = [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300]
        
        # Find the closest standard lot size
        if calculated_quantity <= 15:
            final_quantity = 15  # Minimum standard lot
        else:
            # Find the largest standard lot that doesn't exceed calculated quantity
            final_quantity = 15  # Default
            for lot_size in standard_lots:
                if lot_size <= calculated_quantity:
                    final_quantity = lot_size
                else:
                    break
        
        # Ensure we don't exceed available capital
        trade_value = final_quantity * option_price + self.broker_charges
        if trade_value > self.current_capital:
            # Find smaller lot size that fits
            for lot_size in reversed(standard_lots):
                test_value = lot_size * option_price + self.broker_charges
                if test_value <= self.current_capital:
                    final_quantity = lot_size
                    break
            else:
                final_quantity = 15  # Minimum if nothing fits
        
        return final_quantity
    
    def place_high_accuracy_trade(self, opportunity):
        """Place a high accuracy trade with strict validation"""
        
        data = opportunity['data']
        score_data = opportunity['score_data']
        strategy = opportunity['strategy']
        
        # Final validation
        if len(self.positions) >= self.max_positions:
            print(f"⚠️ Maximum positions ({self.max_positions}) reached")
            return False
        
        # Calculate position size
        quantity = self.calculate_optimal_position_size(data['ltp'], score_data['score'])
        trade_value = data['ltp'] * quantity
        total_cost = trade_value + self.broker_charges
        
        # Capital validation - ensure we have enough capital
        if total_cost > self.current_capital:
            print(f"⚠️ Insufficient capital: ₹{total_cost:.2f} needed, ₹{self.current_capital:.2f} available")
            return False
        
        # Create trade
        trade_id = f"HA{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Calculate capital invested (premium value + entry charges)
        capital_invested = trade_value + self.broker_charges
        
        # 🎯 DYNAMIC STOP LOSS BASED ON ATR (NEW!)
        atr_value = self.current_indicators.get('atr', 50) if self.current_indicators else 50
        dynamic_sl = self.get_dynamic_stop_loss(atr_value, strategy)
        
        stop_loss_pct = dynamic_sl['stop_loss_pct']
        volatility = dynamic_sl['volatility']
        
        # Strategy-specific targets
        if strategy == 'SCALPER':
            target_pct = 0.20  # 20% target
        elif strategy == 'TREND_RIDER':
            target_pct = 0.60  # 60% target
        elif strategy in ['SUPPORT_BOUNCE', 'RESISTANCE_BOUNCE']:
            target_pct = 0.45  # 45% target
        else:
            target_pct = self.target_profit_pct  # Default 50%
        
        position = {
            'trade_id': trade_id,
            'symbol': data['symbol'],
            'strike': data['strike'],
            'option_type': data['option_type'],
            'entry_price': data['ltp'],
            'quantity': quantity,
            'capital_invested': capital_invested,  # NEW: Track capital used
            'entry_time': datetime.now(),
            'strategy': strategy,
            'accuracy_score': score_data['score'],
            'reasons': score_data['reasons'],
            'patterns': score_data.get('patterns', []),
            'stop_loss': data['ltp'] * (1 - stop_loss_pct),  # ATR-adjusted!
            'stop_loss_pct': stop_loss_pct,  # Store for display
            'target': data['ltp'] * (1 + target_pct),  # Strategy-specific!
            'target_pct': target_pct,  # Store for display
            'token': data['token'],
            'nifty_at_entry': self.last_nifty_price,
            'oi': data['oi'],
            'volume': data['volume'],
            'broker_charges': self.broker_charges,
            'atr': atr_value,  # Store ATR value
            'volatility': volatility  # Store volatility level
        }
        
        self.positions.append(position)
        # PROPERLY DEDUCT CAPITAL
        self.current_capital -= total_cost
        
        print(f"💰 Capital after trade: ₹{self.current_capital:.2f} (Deducted: ₹{total_cost:.2f})")
        
        # Log trade
        self.log_high_accuracy_trade(position, 'ENTRY')
        self.update_json_file()
        
        # 💾 SAVE POSITION STATE IMMEDIATELY AFTER ENTRY
        self._save_position_state()
        
        # Calculate risk percentage used
        risk_pct = (total_cost / self.current_capital) * 100
        
        print(f"\n{'='*80}")
        print(f"🟢 HIGH ACCURACY ENTRY")
        print(f"{'='*80}")
        print(f"   Symbol: {data['symbol']} @ ₹{data['ltp']:.2f} x {quantity} lots")
        print(f"   Score: {score_data['score']:.0f}/185 (Technical: +{score_data['breakdown']['technical']:.0f}, Candlestick: +{score_data['breakdown']['candlestick']:.0f})")
        print(f"   ─────────────────────────────────────────────────────────────────")
        print(f"   Capital Invested:       ₹{capital_invested:>12,.2f} ({risk_pct:.1f}% of capital)")
        print(f"   Premium Value:          ₹{trade_value:>12,.2f}")
        print(f"   Entry Charges:          ₹{self.broker_charges:>12.2f}")
        print(f"   ─────────────────────────────────────────────────────────────────")
        
        # Display ATR-adjusted stop loss
        sl_pct = position.get('stop_loss_pct', self.stop_loss_pct) * 100
        tgt_pct = position.get('target_pct', self.target_profit_pct) * 100
        volatility = position.get('volatility', 'MEDIUM')
        atr = position.get('atr', 0)
        
        print(f"   Stop Loss:              ₹{position['stop_loss']:>12.2f} (-{sl_pct:.0f}%) [{volatility} VOL]")
        print(f"   Target:                 ₹{position['target']:>12.2f} (+{tgt_pct:.0f}%)")
        if atr > 0:
            print(f"   ATR:                    {atr:>12.1f} (Volatility: {volatility})")
        print(f"   ─────────────────────────────────────────────────────────────────")
        print(f"   Reasons: {', '.join(score_data['reasons'][:4])}")
        if score_data.get('patterns'):
            print(f"   🕯️ Patterns: {', '.join(score_data['patterns'])}")
        print(f"{'='*80}\n")
        
        # Send Telegram notification
        if self.telegram:
            try:
                self.telegram.send_entry_signal({
                    'symbol': data['symbol'],
                    'strike': data['strike'],
                    'option_type': data['option_type'],
                    'entry_price': data['ltp'],
                    'quantity': quantity,
                    'strategy': strategy,
                    'reason': ', '.join(score_data['reasons'][:2])
                })
            except Exception as e:
                print(f"⚠️ Telegram notification failed: {e}")
        
        return True   
 
    def check_high_accuracy_exits(self):
        """Check exit conditions with STRATEGY-SPECIFIC logic"""
        
        exits = []
        
        for position in self.positions:
            try:
                quotes = self.api.get_quotes(exchange="NFO", token=position['token'])
                
                if quotes and quotes.get('stat') == 'Ok':
                    current_price = float(quotes.get('lp', 0))
                    
                    if current_price <= 0:
                        continue
                    
                    # Handle both datetime objects and string timestamps
                    entry_time = position['entry_time']
                    if isinstance(entry_time, str):
                        try:
                            entry_time = datetime.fromisoformat(entry_time)
                            position['entry_time'] = entry_time  # Update to datetime
                        except:
                            entry_time = datetime.now()
                            position['entry_time'] = entry_time
                    
                    holding_time = datetime.now() - entry_time
                    holding_minutes = holding_time.total_seconds() / 60
                    profit_pct = (current_price - position['entry_price']) / position['entry_price']
                    
                    strategy = position.get('strategy', 'CONTRARIAN')
                    
                    # 🎯 STRATEGY-SPECIFIC EXIT LOGIC
                    
                    # 1. SCALPER STRATEGY - Quick 5-15 min trades
                    if strategy == 'SCALPER':
                        # Tight stop loss (10%)
                        if current_price <= position['entry_price'] * 0.90:
                            exits.append((position, current_price, 'SCALPER_STOP_LOSS'))
                        # Quick target (20%)
                        elif profit_pct >= 0.20:
                            exits.append((position, current_price, 'SCALPER_TARGET'))
                        # Time exit (15 min max)
                        elif holding_minutes >= 15:
                            exits.append((position, current_price, 'SCALPER_TIME_EXIT'))
                        # Book any profit after 5 min
                        elif holding_minutes >= 5 and profit_pct >= 0.10:
                            exits.append((position, current_price, 'SCALPER_PROFIT_BOOK'))
                    
                    # 2. TREND RIDER STRATEGY - Ride trends 60-120 min
                    elif strategy == 'TREND_RIDER':
                        # 🎯 SMART TRAILING STOP for TREND_RIDER (wide trails)
                        if self.trailing_stop_manager and profit_pct > 0.10:
                            trail_result = self.trailing_stop_manager.calculate_trailing_stop(
                                position,
                                current_price,
                                'TRENDING'  # Always use trending mode for trend rider
                            )
                            
                            if trail_result['should_exit']:
                                exits.append((position, current_price, f"TREND_RIDER_{trail_result['reason']}"))
                                continue
                        
                        # Wider stop loss (25%)
                        if current_price <= position['stop_loss']:
                            exits.append((position, current_price, 'TREND_RIDER_STOP_LOSS'))
                        # Big target (60%)
                        elif profit_pct >= 0.60:
                            exits.append((position, current_price, 'TREND_RIDER_TARGET'))
                        # Time exit (120 min max)
                        elif holding_minutes >= 120:
                            exits.append((position, current_price, 'TREND_RIDER_TIME_EXIT'))
                    
                    # 3. SUPPORT/RESISTANCE BOUNCE - 30-60 min holds
                    elif strategy in ['SUPPORT_BOUNCE', 'RESISTANCE_BOUNCE']:
                        # Tight stop loss (20%)
                        if current_price <= position['entry_price'] * 0.80:
                            exits.append((position, current_price, 'BOUNCE_STOP_LOSS'))
                        # Target (45%)
                        elif profit_pct >= 0.45:
                            exits.append((position, current_price, 'BOUNCE_TARGET'))
                        # Time exit (60 min max)
                        elif holding_minutes >= 60:
                            exits.append((position, current_price, 'BOUNCE_TIME_EXIT'))
                        # Book profit after 30 min if 25%+
                        elif holding_minutes >= 30 and profit_pct >= 0.25:
                            exits.append((position, current_price, 'BOUNCE_PROFIT_BOOK'))
                    
                    # 4. CONTRARIAN STRATEGY (Default) - Original logic
                    else:
                        # 🎯 SMART TRAILING STOP (if available)
                        if self.trailing_stop_manager and profit_pct > 0.05:
                            # Get current market mode
                            market_mode = self.adaptive_engine.current_mode if self.adaptive_engine else 'RANGING'
                            
                            # Calculate smart trailing stop
                            trail_result = self.trailing_stop_manager.calculate_trailing_stop(
                                position,
                                current_price,
                                market_mode
                            )
                            
                            if trail_result['should_exit']:
                                exits.append((position, current_price, trail_result['reason']))
                                continue
                        
                        # Check stop loss
                        if current_price <= position['stop_loss']:
                            exits.append((position, current_price, 'STOP_LOSS'))
                        
                        # Check target
                        elif current_price >= position['target']:
                            exits.append((position, current_price, 'TARGET_HIT'))
                        
                        # Check maximum holding time (now 2 hours)
                        elif holding_minutes > (self.max_holding_time * 60):
                            exits.append((position, current_price, 'TIME_EXIT'))
                        
                        # Emergency exit if loss > 40% (prevent total loss)
                        elif current_price <= position['entry_price'] * 0.60:
                            exits.append((position, current_price, 'EMERGENCY_EXIT'))
                        
                        # Check trailing stop (if in profit and held for >15 minutes)
                        elif holding_minutes > 15:
                            # Aggressive trailing stops for profit protection
                            if profit_pct > 0.15:  # If 15%+ profit, use tight trailing stop
                                trailing_stop = position['entry_price'] * 1.05  # Move to 5% profit minimum
                                if current_price <= trailing_stop:
                                    exits.append((position, current_price, 'TRAILING_STOP_TIGHT'))
                            elif profit_pct > 0.05:  # If 5%+ profit, use breakeven stop
                                trailing_stop = position['entry_price'] * 1.02  # Move to 2% profit minimum
                                if current_price <= trailing_stop:
                                    exits.append((position, current_price, 'BREAKEVEN_STOP'))
                        
                        # Quick profit booking (if 10%+ profit after 15 minutes)
                        elif holding_minutes > 15:
                            if profit_pct > 0.10:  # Book 10%+ profits quickly
                                exits.append((position, current_price, 'QUICK_PROFIT_BOOK'))
                        
                        # Immediate profit booking (if 15%+ profit after 5 minutes)
                        elif holding_minutes > 5:
                            if profit_pct > 0.15:  # Book 15%+ profits immediately
                                exits.append((position, current_price, 'IMMEDIATE_PROFIT_BOOK'))
            
            except Exception as e:
                continue
        
        # Execute exits
        for position, exit_price, reason in exits:
            self.exit_high_accuracy_position(position, exit_price, reason)
    
    def exit_high_accuracy_position(self, position, exit_price, reason):
        """Exit position with detailed tracking and REALISTIC CHARGES"""
        
        # 💰 CALCULATE REALISTIC CHARGES using BrokerageCalculator
        charges = self.brokerage_calc.calculate_charges(
            buy_price=position['entry_price'],
            sell_price=exit_price,
            quantity=position['quantity'],
            lot_size=1  # Already in lots
        )
        
        # Extract all charge components
        gross_pnl = charges['gross_pnl']
        total_charges = charges['total_charges']
        net_pnl = charges['net_pnl']
        
        pnl_pct = ((exit_price - position['entry_price']) / position['entry_price']) * 100
        
        # Update capital (add back the sell value, charges already deducted in net_pnl)
        trade_value = exit_price * position['quantity']
        self.current_capital += trade_value  # Add sell proceeds
        self.current_capital -= total_charges  # Deduct all charges
        
        # Update daily P&L tracking
        self.daily_gross_pnl += gross_pnl
        self.daily_charges += total_charges
        self.daily_net_pnl += net_pnl
        
        # Calculate holding time
        entry_time = position['entry_time']
        if isinstance(entry_time, str):
            try:
                entry_time = datetime.fromisoformat(entry_time)
            except:
                entry_time = datetime.now()
        
        holding_time = datetime.now() - entry_time
        holding_minutes = holding_time.total_seconds() / 60
        
        # Create exit record with ALL charge details
        exit_record = position.copy()
        exit_record.update({
            'exit_price': exit_price,
            'exit_time': datetime.now(),
            'gross_pnl': gross_pnl,
            'brokerage': charges['brokerage']['total'],
            'exchange_charges': charges['exchange_charges'],
            'stt': charges['stt'],
            'gst': charges['gst'],
            'stamp_duty': charges['stamp_duty'],
            'sebi_charges': charges['sebi_charges'],
            'total_charges': total_charges,
            'net_pnl': net_pnl,
            'charges_percentage': charges['charges_percentage'],
            'pnl_pct': pnl_pct,
            'exit_reason': reason,
            'holding_minutes': holding_minutes,
            'success': net_pnl > 0,
            'running_daily_pnl': self.daily_net_pnl
        })
        
        # Add to trade history
        self.trade_history.append(exit_record)
        
        # Remove from positions
        self.positions.remove(position)
        
        # Log trade
        self.log_high_accuracy_trade(exit_record, 'EXIT')
        self.update_json_file()
        
        # 💾 SAVE POSITION STATE AFTER EXIT (or clear if no positions left)
        if len(self.positions) == 0:
            self.persistence.clear_state()
            print(f"🗑️ All positions closed - state cleared")
        else:
            self._save_position_state()
        
        print(f"\n{'='*80}")
        print(f"🔴 HIGH ACCURACY EXIT")
        print(f"{'='*80}")
        print(f"   Symbol: {position['symbol']} @ ₹{exit_price:.2f}")
        print(f"   Entry: ₹{position['entry_price']:.2f} | Exit: ₹{exit_price:.2f} | Qty: {position['quantity']}")
        print(f"   ─────────────────────────────────────────────────────────────────")
        print(f"   Gross P&L:              ₹{gross_pnl:>12,.2f} ({pnl_pct:+.1f}%)")
        print(f"   ─────────────────────────────────────────────────────────────────")
        print(f"   Charges Breakdown:")
        print(f"     • Brokerage:          ₹{charges['brokerage']['total']:>12.2f}")
        print(f"     • Exchange:           ₹{charges['exchange_charges']:>12.2f}")
        print(f"     • STT:                ₹{charges['stt']:>12.2f}")
        print(f"     • GST:                ₹{charges['gst']:>12.2f}")
        print(f"     • Stamp Duty:         ₹{charges['stamp_duty']:>12.2f}")
        print(f"     • SEBI:               ₹{charges['sebi_charges']:>12.2f}")
        print(f"   ─────────────────────────────────────────────────────────────────")
        print(f"   Total Charges:          ₹{total_charges:>12,.2f} ({charges['charges_percentage']:.2f}%)")
        print(f"   ─────────────────────────────────────────────────────────────────")
        if net_pnl > 0:
            print(f"   Net Profit (After All Charges): ₹{net_pnl:>12,.2f} ✅")
        else:
            print(f"   Net Loss (After All Charges):   ₹{net_pnl:>12,.2f} ❌")
        print(f"   ─────────────────────────────────────────────────────────────────")
        print(f"   Reason: {reason} | Held: {holding_minutes:.0f} min")
        print(f"   Capital: ₹{self.current_capital:,.2f}")
        print(f"{'='*80}")
        print(f"\n📊 TODAY'S RUNNING P&L:")
        print(f"   Gross P&L:              ₹{self.daily_gross_pnl:>12,.2f}")
        print(f"   Total Charges:          ₹{self.daily_charges:>12,.2f}")
        print(f"   ─────────────────────────────────────────────────────────────────")
        if self.daily_net_pnl > 0:
            print(f"   Net Profit (After Charges): ₹{self.daily_net_pnl:>12,.2f} 🎯")
        else:
            print(f"   Net Loss (After Charges):   ₹{self.daily_net_pnl:>12,.2f}")
        print(f"{'='*80}\n")
        
        # Send Telegram notification
        if self.telegram:
            try:
                self.telegram.send_exit_signal({
                    'symbol': position.get('symbol', 'UNKNOWN'),
                    'strike': position.get('strike', 0),
                    'option_type': position.get('option_type', 'UNKNOWN'),
                    'entry_price': position.get('entry_price', 0),
                    'exit_price': exit_price,
                    'quantity': position.get('quantity', 0),
                    'net_pnl': net_pnl,
                    'exit_reason': reason,
                    'holding_time_minutes': holding_minutes
                })
            except Exception as e:
                print(f"⚠️ Telegram notification failed: {e}")
        
        # Save capital persistence after each trade
        self.save_capital_persistence()
    
    def exit_all_positions_eod(self):
        """Exit all positions at end of day (3:00 PM)"""
        
        if not self.positions:
            print("✅ No positions to exit")
            return
        
        print(f"🚨 END OF DAY - EXITING ALL {len(self.positions)} POSITIONS")
        
        positions_to_exit = self.positions.copy()  # Copy to avoid modification during iteration
        
        for position in positions_to_exit:
            try:
                quotes = self.api.get_quotes(exchange="NFO", token=position['token'])
                
                if quotes and quotes.get('stat') == 'Ok':
                    current_price = float(quotes.get('lp', 0))
                    
                    if current_price > 0:
                        self.exit_high_accuracy_position(position, current_price, 'END_OF_DAY')
                    else:
                        # If no price available, exit at entry price
                        self.exit_high_accuracy_position(position, position['entry_price'], 'END_OF_DAY_NO_PRICE')
                else:
                    # If API fails, exit at entry price
                    self.exit_high_accuracy_position(position, position['entry_price'], 'END_OF_DAY_API_FAIL')
            
            except Exception as e:
                # Emergency exit at entry price
                self.exit_high_accuracy_position(position, position['entry_price'], 'END_OF_DAY_ERROR')
        
        print(f"✅ All positions closed for end of day")
        
        # Clear position state at end of day
        self.persistence.clear_state()
        print(f"🗑️ Position state cleared for end of day")
        
        # Save capital persistence at end of day
        self.save_capital_persistence()
    
    def log_high_accuracy_trade(self, trade_data, action):
        """Log trade with enhanced data including REALISTIC CHARGES"""
        
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            if action == 'ENTRY':
                row = [
                    trade_data['entry_time'].strftime('%Y-%m-%d %H:%M:%S'),
                    trade_data['trade_id'],
                    'ENTRY',
                    trade_data['symbol'],
                    trade_data['strike'],
                    trade_data['option_type'],
                    trade_data['entry_price'],
                    '',  # exit_price
                    trade_data['quantity'],
                    trade_data.get('capital_invested', ''),  # Capital invested
                    '',  # gross_pnl
                    '',  # total_charges
                    '',  # net_pnl_after_charges
                    self.current_capital,
                    ', '.join(trade_data['reasons'][:2]),
                    trade_data['accuracy_score'],
                    '',  # trend_strength
                    trade_data['nifty_at_entry'],
                    '',  # iv_rank
                    trade_data['oi'],
                    trade_data['volume'],
                    trade_data['strategy'],
                    '',  # holding_time_minutes
                    ', '.join(trade_data.get('patterns', [])),  # candlestick_patterns
                    ''   # running_daily_pnl
                ]
            else:  # EXIT
                row = [
                    trade_data['exit_time'].strftime('%Y-%m-%d %H:%M:%S'),
                    trade_data.get('trade_id', 'UNKNOWN'),
                    'EXIT',
                    trade_data.get('symbol', 'UNKNOWN'),
                    trade_data.get('strike', 0),  # Default to 0 if missing
                    trade_data.get('option_type', 'UNKNOWN'),  # Default if missing
                    trade_data.get('entry_price', 0),
                    trade_data.get('exit_price', 0),
                    trade_data.get('quantity', 0),
                    trade_data.get('capital_invested', ''),  # Capital invested
                    trade_data.get('gross_pnl', 0),
                    trade_data.get('total_charges', 0),
                    trade_data.get('net_pnl', 0),
                    self.current_capital,
                    trade_data.get('exit_reason', 'UNKNOWN'),
                    trade_data.get('accuracy_score', 0),
                    '',  # trend_strength
                    trade_data.get('nifty_at_entry', 0),
                    '',  # iv_rank
                    trade_data.get('oi', 0),
                    trade_data.get('volume', 0),
                    trade_data.get('strategy', 'UNKNOWN'),
                    trade_data.get('holding_minutes', 0),
                    ', '.join(trade_data.get('patterns', [])),  # candlestick_patterns
                    trade_data.get('running_daily_pnl', self.daily_net_pnl)
                ]
            
            writer.writerow(row)
    
    def update_json_file(self):
        """Update JSON with high accuracy metrics"""
        
        # Load existing data to preserve start_time and session_count
        existing_start_time = datetime.now().isoformat()
        session_count = 1
        
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as file:
                    existing_data = json.load(file)
                    existing_start_time = existing_data.get('start_time', existing_start_time)
                    session_count = existing_data.get('session_count', 1)
        except:
            pass
        
        # Calculate performance metrics
        total_trades = len(self.trade_history)
        winning_trades = len([t for t in self.trade_history if t.get('net_pnl', 0) > 0])
        losing_trades = total_trades - winning_trades
        
        total_gross_pnl = sum([t.get('gross_pnl', 0) for t in self.trade_history])
        total_charges = sum([t.get('total_charges', 0) for t in self.trade_history])
        total_net_pnl = sum([t.get('net_pnl', 0) for t in self.trade_history])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        avg_accuracy_score = sum([t.get('accuracy_score', 0) for t in self.trade_history]) / total_trades if total_trades > 0 else 0
        avg_holding_time = sum([t.get('holding_minutes', 0) for t in self.trade_history]) / total_trades if total_trades > 0 else 0
        
        data = {
            'start_time': existing_start_time,  # Preserve original start time
            'last_update': datetime.now().isoformat(),
            'session_count': session_count,
            'initial_capital': self.initial_capital,
            'current_capital': self.current_capital,
            'broker_charges_per_trade': self.broker_charges,
            'min_accuracy_score': self.min_accuracy_score,
            'target_trades_per_day': '1-10',
            'focus': 'High Accuracy Quality Trades',
            'total_gross_pnl': total_gross_pnl,
            'total_charges': total_charges,
            'total_net_pnl': total_net_pnl,
            'open_positions': len(self.positions),
            'positions': [
                {
                    'trade_id': p.get('trade_id', 'UNKNOWN'),
                    'symbol': p.get('symbol', 'UNKNOWN'),
                    'entry_price': p.get('entry_price', 0),
                    'quantity': p.get('quantity', 0),
                    'accuracy_score': p.get('accuracy_score', 0),
                    'strategy': p.get('strategy', 'UNKNOWN'),
                    'entry_time': p['entry_time'].isoformat() if isinstance(p.get('entry_time'), datetime) else p.get('entry_time', '')
                } for p in self.positions
            ],
            'trades': [
                {
                    'trade_id': t['trade_id'],
                    'symbol': t['symbol'],
                    'strike': t.get('strike', 0),
                    'option_type': t.get('option_type', ''),
                    'entry_price': t.get('entry_price', 0),
                    'exit_price': t.get('exit_price', 0),
                    'quantity': t.get('quantity', 0),
                    'gross_pnl': t.get('gross_pnl', 0),
                    'net_pnl': t.get('net_pnl', 0),
                    'charges': t.get('total_charges', 0),
                    'accuracy_score': t.get('accuracy_score', 0),
                    'strategy': t.get('strategy', ''),
                    'exit_reason': t.get('exit_reason', ''),
                    'holding_minutes': t.get('holding_minutes', 0),
                    'entry_time': t.get('entry_time', datetime.now()).isoformat() if isinstance(t.get('entry_time'), datetime) else t.get('entry_time', ''),
                    'exit_time': t.get('exit_time', datetime.now()).isoformat() if isinstance(t.get('exit_time'), datetime) else t.get('exit_time', '')
                } for t in self.trade_history  # ALL trades, not just last 5
            ],
            'performance': {
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': losing_trades,
                'total_gross_pnl': total_gross_pnl,
                'total_charges': total_charges,
                'total_net_pnl': total_net_pnl,
                'win_rate': win_rate,
                'avg_accuracy_score': avg_accuracy_score,
                'avg_holding_time_minutes': avg_holding_time,
                'current_nifty': self.last_nifty_price,
                'profit_factor': abs(total_gross_pnl / total_charges) if total_charges > 0 else 0
            }
        }
        
        with open(self.json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    
    def display_live_option_chain(self):
        """Display live option chain data in console"""
        
        # Clear screen for better display
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"📊 LIVE OPTION CHAIN - HIGH ACCURACY TRADING - {datetime.now().strftime('%H:%M:%S')}")
        print(f"🎯 NIFTY Estimated Level: {self.last_nifty_price:.0f}")
        
        # 🆕 Show Market Condition and Trend Direction
        if self.priority_features and len(self.price_history) >= 20:
            # Get market condition
            market_condition = self.priority_features.detect_market_condition(
                self.price_history,
                self.indicators_5min,
                self.indicators_15min
            )
            
            # Get trend direction
            trend_check_ce = self.priority_features.check_trend_direction_alignment(
                'CE',
                self.price_history,
                self.indicators_5min,
                self.indicators_15min
            )
            
            # Market condition emoji
            condition_emoji = {
                'TRENDING': '📈',
                'CHOPPY': '⚠️',
                'VOLATILE': '🌪️',
                'RANGE_BOUND': '↔️',
                'MODERATE': '📊',
                'INSUFFICIENT_DATA': '⏳'
            }.get(market_condition['condition'], '❓')
            
            # Trend direction emoji
            trend_emoji = {
                'BULLISH': '🟢⬆️',
                'BEARISH': '🔴⬇️',
                'NEUTRAL': '🟡➡️'
            }.get(trend_check_ce['trend_direction'], '❓')
            
            # Trading status
            if market_condition['condition'] == 'CHOPPY':
                trading_status = '🚫 SITTING OUT'
            elif trend_check_ce['trend_direction'] == 'NEUTRAL':
                trading_status = '🚫 NO CLEAR TREND'
            else:
                trading_status = '✅ TRADING ALLOWED'
            
            print(f"📊 Market: {condition_emoji} {market_condition['condition']} (Score: {market_condition['score']}/100) | Trend: {trend_emoji} {trend_check_ce['trend_direction']} (Conf: {trend_check_ce['confidence']}%) | {trading_status}")
            print(f"   {market_condition['reason']}")
        
        # Show multi-timeframe technical indicators
        if self.indicators_5min:
            # 15-minute trend
            trend_15min = self.indicators_15min.get('trend', 'CALCULATING') if self.indicators_15min else 'CALCULATING'
            trend_15min_emoji = "🟢" if trend_15min == 'BULLISH' else "🔴" if trend_15min == 'BEARISH' else "🟡"
            
            # 5-minute analysis (main)
            rsi_5min = self.indicators_5min['rsi']
            macd_5min = self.indicators_5min['macd']
            bb_pos_5min = self.indicators_5min['bb_position']
            trend_5min = self.indicators_5min['trend']
            trend_5min_emoji = "🟢" if trend_5min == 'BULLISH' else "🔴" if trend_5min == 'BEARISH' else "🟡"
            
            # 1-minute timing
            trend_1min = self.indicators_1min.get('trend', 'CALCULATING') if self.indicators_1min else 'CALCULATING'
            trend_1min_emoji = "🟢" if trend_1min == 'BULLISH' else "🔴" if trend_1min == 'BEARISH' else "🟡"
            
            print(f"📊 Multi-Timeframe: 15m{trend_15min_emoji} | 5m{trend_5min_emoji}(RSI:{rsi_5min:.0f},MACD:{macd_5min:.1f},BB:{bb_pos_5min}) | 1m{trend_1min_emoji}")
        else:
            print(f"📊 Multi-Timeframe: Calculating indicators...")
        
        # Show current candlestick patterns
        if self.current_patterns:
            pattern_summary = []
            for pattern in self.current_patterns[-2:]:  # Show last 2 patterns
                signal_emoji = "🟢" if pattern['signal'] == 'BULLISH' else "🔴" if pattern['signal'] == 'BEARISH' else "🟡"
                pattern_summary.append(f"{signal_emoji}{pattern['name']}")
            print(f"🕯️ Candlestick: {' | '.join(pattern_summary)}")
        else:
            print(f"🕯️ Candlestick: Analyzing...")
        
        print("=" * 150)
        
        # Header
        header = f"{'CALL OPTIONS':<55} {'STRIKE':<8} {'PUT OPTIONS':<55} {'ACCURACY':<20}"
        print(header)
        print("-" * 150)
        
        subheader = f"{'LTP':<7} {'Vol':<8} {'OI':<10} {'Chg%':<7} {'Bid':<6} {'Ask':<6} {'Sprd':<5} {'Strike':<8} {'LTP':<7} {'Vol':<8} {'OI':<10} {'Chg%':<7} {'Bid':<6} {'Ask':<6} {'Sprd':<5} {'Score':<20}"
        print(subheader)
        print("-" * 150)
        
        # Display option data for each strike - Extended to 27000
        strikes = [25200, 25250, 25300, 25350, 25400, 25450, 25500, 25550, 25600, 
                   25650, 25700, 25750, 25800, 25850, 25900, 25950, 26000, 26050,
                   26100, 26150, 26200, 26250, 26300, 26350, 26400, 26450, 26500,
                   26550, 26600, 26650, 26700, 26750, 26800, 26850, 26900, 26950, 27000]
        
        # Get market analysis once
        market_analysis = self.analyze_market_structure()
        
        print(f"🔍 Displaying {len(strikes)} strikes...")
        
        for i, strike in enumerate(strikes, 1):
            ce_data = None
            pe_data = None
            
            # Find CE and PE data for this strike
            for symbol, data in self.market_data.items():
                if data['strike'] == strike:
                    if data['option_type'] == 'CE':
                        ce_data = data
                    elif data['option_type'] == 'PE':
                        pe_data = data
            
            # Format CE data
            if ce_data:
                ce_ltp = f"{ce_data['ltp']:.2f}"
                ce_vol = f"{ce_data['volume']:,}"
                ce_oi = f"{ce_data['oi']:,}"
                ce_chg = f"{ce_data.get('change_pct', 0):+.1f}%"
                ce_bid = f"{ce_data['bid']:.2f}"
                ce_ask = f"{ce_data['ask']:.2f}"
                ce_spread = f"{ce_data['bid_ask_spread']:.1f}"
            else:
                ce_ltp = ce_vol = ce_oi = ce_chg = ce_bid = ce_ask = ce_spread = "N/A"
            
            # Format PE data
            if pe_data:
                pe_ltp = f"{pe_data['ltp']:.2f}"
                pe_vol = f"{pe_data['volume']:,}"
                pe_oi = f"{pe_data['oi']:,}"
                pe_chg = f"{pe_data.get('change_pct', 0):+.1f}%"
                pe_bid = f"{pe_data['bid']:.2f}"
                pe_ask = f"{pe_data['ask']:.2f}"
                pe_spread = f"{pe_data['bid_ask_spread']:.1f}"
            else:
                pe_ltp = pe_vol = pe_oi = pe_chg = pe_bid = pe_ask = pe_spread = "N/A"
            
            # Calculate accuracy scores
            ce_score = ""
            pe_score = ""
            
            if ce_data:
                try:
                    ce_score_data = self.calculate_high_accuracy_score(ce_data, market_analysis)
                    ce_score = f"CE:{ce_score_data['score']:.0f}"
                except:
                    ce_score = "CE:--"
            
            if pe_data:
                try:
                    pe_score_data = self.calculate_high_accuracy_score(pe_data, market_analysis)
                    pe_score = f"PE:{pe_score_data['score']:.0f}"
                except:
                    pe_score = "PE:--"
            
            accuracy_display = f"{ce_score} {pe_score}".strip()
            if not accuracy_display:
                accuracy_display = "No Data"
            
            # Determine strike status
            distance = abs(strike - self.last_nifty_price) if self.last_nifty_price > 0 else 999
            if distance <= 25:
                strike_marker = "🎯"  # ATM
            elif distance <= 50:
                strike_marker = "⭐"  # Near ATM
            else:
                strike_marker = "  "  # OTM
            
            # Print row - ALWAYS print all strikes
            row = f"{ce_ltp:<7} {ce_vol:<8} {ce_oi:<10} {ce_chg:<7} {ce_bid:<6} {ce_ask:<6} {ce_spread:<5} {strike:<8} {pe_ltp:<7} {pe_vol:<8} {pe_oi:<10} {pe_chg:<7} {pe_bid:<6} {pe_ask:<6} {pe_spread:<5} {accuracy_display:<20}"
            print(f"{strike_marker} {row}")
            
            # Add a small delay to prevent display issues
            if i % 5 == 0:  # Every 5 strikes, add tiny delay
                time.sleep(0.1)
        
        print("-" * 150)
        
        # Display data summary
        total_strikes = len(strikes)
        strikes_with_data = len(set([data['strike'] for data in self.market_data.values()]))
        print(f"📊 DATA SUMMARY: {strikes_with_data}/{total_strikes} strikes have live data | Total options: {len(self.market_data)}")
        
        # Verify all strikes were displayed
        print(f"✅ Displayed strikes: {', '.join([str(s) for s in strikes])}")
        
        # Display trading status
        self.display_trading_status_compact()
    
    def display_trading_status_compact(self):
        """Display compact trading status below option chain"""
        
        net_pnl = self.current_capital - self.initial_capital
        total_charges = len(self.trade_history) * self.broker_charges * 2
        
        print(f"💰 CAPITAL: ₹{self.current_capital:,.0f} | P&L: ₹{net_pnl:+,.0f} ({(net_pnl / self.initial_capital * 100):+.1f}%) | CHARGES: ₹{total_charges:.0f}")
        print(f"🎯 POSITIONS: {len(self.positions)}/{self.max_positions} | TRADES: {len(self.trade_history)}", end="")
        
        if self.trade_history:
            winning_trades = len([t for t in self.trade_history if t.get('net_pnl', 0) > 0])
            win_rate = (winning_trades / len(self.trade_history)) * 100
            avg_score = sum([t.get('accuracy_score', 0) for t in self.trade_history]) / len(self.trade_history)
            print(f" | WIN RATE: {win_rate:.0f}% | AVG SCORE: {avg_score:.0f}/100")
        else:
            print("")
        
        # Show open positions
        if self.positions:
            print(f"🔄 OPEN POSITIONS:")
            for pos in self.positions:
                # Handle both datetime objects and string timestamps
                entry_time = pos['entry_time']
                if isinstance(entry_time, str):
                    try:
                        entry_time = datetime.fromisoformat(entry_time)
                    except:
                        entry_time = datetime.now()  # Fallback
                
                holding_time = datetime.now() - entry_time
                holding_minutes = holding_time.total_seconds() / 60
                print(f"   {pos['symbol']} @ ₹{pos['entry_price']:.2f} x {pos['quantity']} | Score: {pos['accuracy_score']:.0f}/100 | Held: {holding_minutes:.0f}min")
        
        # Show recent trades
        if self.trade_history:
            print(f"📈 RECENT TRADES:")
            for trade in self.trade_history[-2:]:  # Last 2 trades
                net_pnl = trade.get('net_pnl', 0)
                score = trade.get('accuracy_score', 0)
                reason = trade.get('exit_reason', '')
                print(f"   {trade['symbol']}: ₹{net_pnl:+.0f} | Score: {score:.0f}/100 | {reason}")
        
        print(f"⏰ LAST UPDATE: {datetime.now().strftime('%H:%M:%S')} | Next check in 2 minutes")

    def display_simple_option_list(self):
        """Display simple list of all strikes with data"""
        
        # Same strike range as get_comprehensive_market_data() - Extended to 27000
        strikes = [25200, 25250, 25300, 25350, 25400, 25450, 25500, 25550, 25600, 
                   25650, 25700, 25750, 25800, 25850, 25900, 25950, 26000, 26050,
                   26100, 26150, 26200, 26250, 26300, 26350, 26400, 26450, 26500,
                   26550, 26600, 26650, 26700, 26750, 26800, 26850, 26900, 26950, 27000]
        
        print(f"\n📋 ALL STRIKES STATUS:")
        print("=" * 80)
        
        for strike in strikes:
            ce_data = None
            pe_data = None
            
            # Find data for this strike
            for symbol, data in self.market_data.items():
                if data['strike'] == strike:
                    if data['option_type'] == 'CE':
                        ce_data = data
                    elif data['option_type'] == 'PE':
                        pe_data = data
            
            # Status for this strike
            ce_status = f"CE: ₹{ce_data['ltp']:.2f}" if ce_data else "CE: No Data"
            pe_status = f"PE: ₹{pe_data['ltp']:.2f}" if pe_data else "PE: No Data"
            
            distance = abs(strike - self.last_nifty_price) if self.last_nifty_price > 0 else 999
            marker = "🎯" if distance <= 25 else "⭐" if distance <= 50 else "  "
            
            print(f"{marker} {strike}: {ce_status:<15} | {pe_status:<15}")
        
        print("=" * 80)
    
    def display_high_accuracy_status(self):
        """Display enhanced status for high accuracy trading"""
        
        # Use the new live option chain display
        self.display_live_option_chain()
        
        # Also show simple list for verification
        self.display_simple_option_list()
    
    def is_trading_hours(self):
        """Check if current time is within trading hours (9:15 AM to 3:30 PM)"""
        now = datetime.now()
        market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
        market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
        
        return market_open <= now <= market_close
    
    def run_high_accuracy_session(self, duration_minutes=None):
        """Run high accuracy trading session with automatic trading hours"""
        
        print(f"🎯 HIGH ACCURACY OPTIONS TRADING ALGORITHM")
        print(f"{'='*60}")
        print(f"💰 Capital: ₹{self.initial_capital:,}")
        print(f"⏰ Trading Hours: 9:15 AM to 3:30 PM (Auto)")
        print(f"🎯 Target: 1-10 high accuracy trades")
        print(f"📊 Min Score: {self.min_accuracy_score}/100")
        print(f"💸 Broker Charges: ₹{self.broker_charges} per trade")
        print(f"🛡️ Lot Sizes: 15, 30, 45, 60, 75, 90... (Standard)")
        
        if not self.login():
            return
        
        # Send session start notification
        if self.telegram:
            try:
                self.telegram.send_session_start(self.current_capital)
                print("📱 Telegram session start notification sent")
            except Exception as e:
                print(f"⚠️ Telegram notification failed: {e}")
        
        # Test API connection
        print("🔍 Testing API connection...")
        test_result = self.api.searchscrip(exchange="NFO", searchtext="25800")
        if test_result and test_result.get('stat') == 'Ok':
            print("✅ API connection working")
        else:
            print("❌ API connection issue")
            print(f"Response: {test_result}")
            return
        
        # Set trading hours automatically
        now = datetime.now()
        market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
        market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
        
        # If before market open, wait
        if now < market_open:
            wait_minutes = (market_open - now).total_seconds() / 60
            print(f"⏰ Market opens in {wait_minutes:.0f} minutes. Waiting...")
            time.sleep((market_open - now).total_seconds())
        
        # If after market close, exit
        if now > market_close:
            print(f"⏰ Market closed. No trading after 3:30 PM")
            return
        
        start_time = datetime.now()
        end_time = market_close  # Always end at 3:15 PM
        
        cycle_count = 0
        last_opportunity_time = datetime.now() - timedelta(minutes=30)  # Allow immediate first check
        
        try:
            while datetime.now() < end_time:
                # Check if still in trading hours
                if not self.is_trading_hours():
                    print(f"⏰ Outside trading hours. Exiting all positions...")
                    self.exit_all_positions_eod()
                    break
                
                cycle_count += 1
                print(f"\n🔄 Cycle {cycle_count} - {datetime.now().strftime('%H:%M:%S')}")
                
                # Get comprehensive market data
                market_data = self.get_comprehensive_market_data()
                
                if not market_data:
                    print("❌ No market data available")
                    time.sleep(60)  # Wait longer if no data
                    continue
                
                # Check exit conditions MORE FREQUENTLY
                self.check_high_accuracy_exits()
                
                # Additional exit check after 30 seconds (catch quick profits)
                time.sleep(30)
                self.check_high_accuracy_exits()
                
                # Exit all positions 15 minutes before market close
                now = datetime.now()
                market_close = now.replace(hour=15, minute=15, second=0, microsecond=0)  # 3:15 PM
                if now >= market_close:
                    print(f"⏰ 3:15 PM - Exiting all positions before market close")
                    self.exit_all_positions_eod()
                    break
                
                # Look for opportunities (but not too frequently)
                time_since_last_check = datetime.now() - last_opportunity_time
                
                if time_since_last_check.total_seconds() >= 300:  # Check every 5 minutes (more frequent)
                    opportunities = self.find_high_accuracy_opportunities()
                    last_opportunity_time = datetime.now()
                    
                    if opportunities and len(self.positions) < self.max_positions:
                        best_opportunity = opportunities[0]
                        
                        # Only take trades with very high scores
                        if best_opportunity['score_data']['score'] >= self.min_accuracy_score:
                            print(f"\n🚨 HIGH ACCURACY OPPORTUNITY FOUND!")
                            self.place_high_accuracy_trade(best_opportunity)
                        else:
                            print(f"⚠️ Best opportunity score too low: {best_opportunity['score_data']['score']:.0f}/100")
                    else:
                        print("🔍 No high accuracy opportunities found")
                
                # Display status
                self.display_high_accuracy_status()
                
                # Wait before next cycle with continuous position monitoring
                print(f"\n⏳ Waiting 2 minutes for next cycle...")
                
                # Monitor positions every 30 seconds during wait time
                for i in range(4):  # 4 × 30 seconds = 2 minutes
                    time.sleep(30)
                    if self.positions:  # Only if we have positions
                        self.check_high_accuracy_exits()
                        print(f"🔍 Position check {i+1}/4 - {len(self.positions)} positions monitored")
                        
                        # 💾 PERIODIC STATE SAVE (every 2 minutes during monitoring)
                        if i == 3:  # Last check in the cycle
                            self._save_position_state()
        
        except KeyboardInterrupt:
            print(f"\n🛑 High accuracy session stopped by user")
        
        # Final results
        print(f"\n🏁 HIGH ACCURACY SESSION COMPLETED")
        self.display_final_high_accuracy_results()
    
    def display_final_high_accuracy_results(self):
        """Display final results with detailed analysis"""
        
        net_pnl = self.current_capital - self.initial_capital
        net_pnl_pct = (net_pnl / self.initial_capital) * 100
        
        print(f"\n{'='*90}")
        print(f"🏆 HIGH ACCURACY TRADING RESULTS")
        print(f"{'='*90}")
        print(f"💰 Starting Capital: ₹{self.initial_capital:,}")
        print(f"💰 Ending Capital: ₹{self.current_capital:,.2f}")
        print(f"📊 Net P&L: ₹{net_pnl:+,.2f} ({net_pnl_pct:+.2f}%)")
        print(f"📋 Total Trades: {len(self.trade_history)}")
        
        if self.trade_history:
            # Detailed statistics
            winning_trades = len([t for t in self.trade_history if t.get('net_pnl', 0) > 0])
            losing_trades = len(self.trade_history) - winning_trades
            win_rate = (winning_trades / len(self.trade_history)) * 100
            
            total_gross_pnl = sum([t.get('gross_pnl', 0) for t in self.trade_history])
            total_charges = sum([t.get('total_charges', 0) for t in self.trade_history])
            
            avg_score = sum([t.get('accuracy_score', 0) for t in self.trade_history]) / len(self.trade_history)
            avg_holding = sum([t.get('holding_minutes', 0) for t in self.trade_history]) / len(self.trade_history)
            
            print(f"\n📈 PERFORMANCE METRICS:")
            print(f"🎯 Win Rate: {win_rate:.1f}% ({winning_trades}W / {losing_trades}L)")
            print(f"📊 Average Accuracy Score: {avg_score:.0f}/100")
            print(f"⏱️ Average Holding Time: {avg_holding:.0f} minutes")
            print(f"💰 Gross P&L: ₹{total_gross_pnl:+,.2f}")
            print(f"💸 Total Charges: ₹{total_charges:.2f}")
            print(f"🎯 Profit Factor: {abs(total_gross_pnl / total_charges):.2f}" if total_charges > 0 else "N/A")
            
            if winning_trades > 0:
                avg_win = sum([t.get('net_pnl', 0) for t in self.trade_history if t.get('net_pnl', 0) > 0]) / winning_trades
                print(f"📈 Average Win: ₹{avg_win:.2f}")
            
            if losing_trades > 0:
                avg_loss = sum([t.get('net_pnl', 0) for t in self.trade_history if t.get('net_pnl', 0) < 0]) / losing_trades
                print(f"📉 Average Loss: ₹{avg_loss:.2f}")
            
            # Trade quality analysis
            high_score_trades = len([t for t in self.trade_history if t.get('accuracy_score', 0) >= 90])
            print(f"\n🏆 QUALITY ANALYSIS:")
            print(f"⭐ High Score Trades (90+): {high_score_trades}/{len(self.trade_history)}")
            
            successful_high_score = len([t for t in self.trade_history 
                                       if t.get('accuracy_score', 0) >= 90 and t.get('net_pnl', 0) > 0])
            if high_score_trades > 0:
                high_score_success_rate = (successful_high_score / high_score_trades) * 100
                print(f"🎯 High Score Success Rate: {high_score_success_rate:.1f}%")
        
        print(f"\n📁 FILES GENERATED:")
        print(f"   📊 CSV Journal: {self.csv_file}")
        print(f"   📋 JSON Updates: {self.json_file}")
        
        print(f"\n💡 ALGORITHM VALIDATION:")
        if len(self.trade_history) == 0:
            print("✅ No trades taken - algorithm waited for high accuracy setups")
            print("💡 This shows excellent risk management and patience")
        elif len(self.trade_history) <= 10 and win_rate >= 70:
            print("✅ Quality over quantity achieved!")
        elif len(self.trade_history) > 10:
            print("⚠️ Too many trades - consider raising minimum score")
        elif win_rate < 60:
            print("⚠️ Win rate below target - review entry criteria")
        else:
            print("✅ Performance within acceptable range")
        
        # Send daily summary to Telegram
        if self.telegram and self.trade_history:
            try:
                winning_trades = len([t for t in self.trade_history if t.get('net_pnl', 0) > 0])
                losing_trades = len(self.trade_history) - winning_trades
                win_rate = (winning_trades / len(self.trade_history)) * 100
                
                self.telegram.send_daily_summary({
                    'starting_capital': self.initial_capital,
                    'ending_capital': self.current_capital,
                    'net_pnl': net_pnl,
                    'net_pnl_pct': net_pnl_pct,
                    'total_trades': len(self.trade_history),
                    'win_rate': win_rate,
                    'wins': winning_trades,
                    'losses': losing_trades
                })
                print("📱 Telegram daily summary sent")
            except Exception as e:
                print(f"⚠️ Telegram summary failed: {e}")

def main():
    """Main function for high accuracy trading"""
    
    print("🎯 HIGH ACCURACY OPTIONS TRADING ALGORITHM")
    print("=" * 60)
    print("Quality over Quantity - Designed for 1-10 trades per day")
    print("Focus: High probability setups with strict entry criteria")
    print()
    
    # Default settings
    capital = 100000  # Fixed ₹1,00,000 capital
    
    # 🆕 STRATEGY SELECTOR
    print("=" * 80)
    print("🎯 SELECT STRATEGY MODE")
    print("=" * 80)
    print()
    print("1. CURRENT Strategy Only (Complex - 12 indicators, min score 90)")
    print("2. SIMPLIFIED Strategy Only (Price Action - 6 components, min score 70)")
    print("3. BOTH Strategies Simultaneously (Compare side-by-side)")
    print()
    
    # Auto-select option 3 (both strategies) - no user input needed
    choice = "3"
    print("✅ Auto-selected: Option 3 - Running BOTH strategies simultaneously")
    print()
    
    if choice == "3":
        # RUN BOTH STRATEGIES SIMULTANEOUSLY
        print("\n✅ Running BOTH Strategies Simultaneously!")
        print("=" * 80)
        print()
        print("📊 STRATEGY 1: CURRENT (Complex)")
        print("   - File: current_trades_YYYYMMDD.csv")
        print("   - Scoring: 12 components, min score 90")
        print()
        print("📊 STRATEGY 2: SIMPLIFIED (Price Action)")
        print("   - File: simplified_trades_YYYYMMDD.csv")
        print("   - Scoring: 6 components, min score 70")
        print()
        print(f"💰 Capital per strategy: ₹{capital:,}")
        print(f"⏰ Trading hours: 9:15 AM to 3:30 PM")
        print("=" * 80)
        print()
        
        import threading
        import time
        
        def run_strategy(strategy_mode, capital):
            """Run a strategy in its own thread"""
            algo = HighAccuracyAlgo(initial_capital=capital, strategy_mode=strategy_mode)
            
            # Override CSV/JSON filenames
            algo.csv_file = f"{strategy_mode.lower()}_trades_{datetime.now().strftime('%Y%m%d')}.csv"
            algo.json_file = f"{strategy_mode.lower()}_updates_{datetime.now().strftime('%Y%m%d')}.json"
            algo.initialize_files()
            
            print(f"✅ {strategy_mode} Strategy started - {algo.csv_file}")
            algo.run_high_accuracy_session()
        
        # Create threads
        thread1 = threading.Thread(target=run_strategy, args=("CURRENT", capital), daemon=False)
        thread2 = threading.Thread(target=run_strategy, args=("SIMPLIFIED", capital), daemon=False)
        
        # Start both
        thread1.start()
        time.sleep(1)  # Small delay
        thread2.start()
        
        # Wait for completion
        thread1.join()
        thread2.join()
        
        print("\n" + "=" * 80)
        print("✅ Both strategies completed!")
        print("📊 Compare results:")
        print(f"   - current_trades_{datetime.now().strftime('%Y%m%d')}.csv")
        print(f"   - simplified_trades_{datetime.now().strftime('%Y%m%d')}.csv")
        print("=" * 80)
        
    elif choice == "2":
        strategy_mode = 'SIMPLIFIED'
        print("\n✅ Running SIMPLIFIED Strategy Only")
        print("   📊 Scoring: Price Action (50%) + Indicators (25%) + Options (25%)")
        print("   🎯 Min Score: 70/100")
        print(f"💰 Capital: ₹{capital:,}")
        print("=" * 80)
        print()
        
        algo = HighAccuracyAlgo(initial_capital=capital, strategy_mode=strategy_mode)
        algo.run_high_accuracy_session()
        
    else:
        strategy_mode = 'CURRENT'
        print("\n✅ Running CURRENT Strategy Only")
        print("   📊 Scoring: 12 components, 260 points capped at 100")
        print("   🎯 Min Score: 90/100")
        print(f"💰 Capital: ₹{capital:,}")
        print("=" * 80)
        print()
        
        algo = HighAccuracyAlgo(initial_capital=capital, strategy_mode=strategy_mode)
        algo.run_high_accuracy_session()

if __name__ == "__main__":
    main()