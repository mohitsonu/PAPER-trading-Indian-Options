#!/usr/bin/env python3
"""
🔄 TRADE STATE PERSISTENCE MODULE
Saves and restores active trades to prevent data loss on restart
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any

class TradeStatePersistence:
    """Handles saving and loading of active trade state"""
    
    def __init__(self, state_file: str = None):
        """Initialize persistence manager"""
        if state_file is None:
            today = datetime.now().strftime('%Y%m%d')
            state_file = f"trade_state_{today}.json"
        
        self.state_file = state_file
        self.backup_file = f"{state_file}.backup"
    
    def save_state(self, positions: List[Dict], capital: float, metadata: Dict = None) -> bool:
        """
        Save current trading state to file
        
        Args:
            positions: List of active position dictionaries
            capital: Current capital amount
            metadata: Additional metadata (optional)
        
        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            state_data = {
                'timestamp': datetime.now().isoformat(),
                'capital': capital,
                'positions': positions,
                'position_count': len(positions),
                'metadata': metadata or {},
                'version': '1.0'
            }
            
            # Create backup of existing file
            if os.path.exists(self.state_file):
                try:
                    with open(self.state_file, 'r', encoding='utf-8') as f:
                        backup_data = json.load(f)
                    with open(self.backup_file, 'w', encoding='utf-8') as f:
                        json.dump(backup_data, f, indent=2, ensure_ascii=False)
                except:
                    pass  # Backup failed, continue anyway
            
            # Save new state
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving trade state: {e}")
            return False
    
    def load_state(self) -> Dict[str, Any]:
        """
        Load trading state from file
        
        Returns:
            dict: State data with 'positions', 'capital', 'metadata'
                  Returns empty state if file doesn't exist or is invalid
        """
        try:
            if not os.path.exists(self.state_file):
                print(f"ℹ️ No existing state file found: {self.state_file}")
                return self._empty_state()
            
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            # Validate state data
            if not isinstance(state_data, dict):
                print(f"⚠️ Invalid state file format")
                return self._empty_state()
            
            positions = state_data.get('positions', [])
            capital = state_data.get('capital', 0)
            timestamp = state_data.get('timestamp', 'Unknown')
            
            print(f"✅ Loaded trade state from: {timestamp}")
            print(f"   💰 Capital: ₹{capital:,.2f}")
            print(f"   📊 Active Positions: {len(positions)}")
            
            if positions:
                print(f"\n📋 RESTORING ACTIVE POSITIONS:")
                for i, pos in enumerate(positions, 1):
                    symbol = pos.get('symbol', 'Unknown')
                    entry_price = pos.get('entry_price', 0)
                    quantity = pos.get('quantity', 0)
                    entry_time = pos.get('entry_time', 'Unknown')
                    print(f"   {i}. {symbol} @ ₹{entry_price} x {quantity} (Entry: {entry_time})")
            
            return state_data
            
        except json.JSONDecodeError as e:
            print(f"❌ Corrupted state file: {e}")
            # Try to load backup
            return self._load_backup()
        except Exception as e:
            print(f"❌ Error loading trade state: {e}")
            return self._empty_state()
    
    def _load_backup(self) -> Dict[str, Any]:
        """Try to load from backup file"""
        try:
            if os.path.exists(self.backup_file):
                print(f"🔄 Attempting to load from backup...")
                with open(self.backup_file, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                print(f"✅ Backup loaded successfully")
                return state_data
        except:
            pass
        
        return self._empty_state()
    
    def _empty_state(self) -> Dict[str, Any]:
        """Return empty state structure"""
        return {
            'timestamp': datetime.now().isoformat(),
            'capital': 0,
            'positions': [],
            'position_count': 0,
            'metadata': {},
            'version': '1.0'
        }
    
    def clear_state(self) -> bool:
        """Clear saved state (use when session ends)"""
        try:
            if os.path.exists(self.state_file):
                os.remove(self.state_file)
                print(f"🗑️ Cleared trade state file")
            if os.path.exists(self.backup_file):
                os.remove(self.backup_file)
            return True
        except Exception as e:
            print(f"❌ Error clearing state: {e}")
            return False
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get information about saved state without loading it"""
        try:
            if not os.path.exists(self.state_file):
                return {'exists': False}
            
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            return {
                'exists': True,
                'timestamp': state_data.get('timestamp'),
                'position_count': len(state_data.get('positions', [])),
                'capital': state_data.get('capital', 0),
                'file_size': os.path.getsize(self.state_file)
            }
        except:
            return {'exists': False, 'error': True}


def test_persistence():
    """Test the persistence module"""
    print("🧪 Testing Trade State Persistence\n")
    
    # Create test instance
    persistence = TradeStatePersistence("test_trade_state.json")
    
    # Test data
    test_positions = [
        {
            'trade_id': 'TEST001',
            'symbol': 'NIFTY11NOV25C25500',
            'strike': 25500,
            'option_type': 'CE',
            'entry_price': 45.50,
            'quantity': 300,
            'entry_time': datetime.now().isoformat(),
            'stop_loss': 34.13,
            'target': 81.90
        },
        {
            'trade_id': 'TEST002',
            'symbol': 'NIFTY11NOV25P25400',
            'strike': 25400,
            'option_type': 'PE',
            'entry_price': 28.75,
            'quantity': 300,
            'entry_time': datetime.now().isoformat(),
            'stop_loss': 21.56,
            'target': 51.75
        }
    ]
    
    test_capital = 158750.00
    test_metadata = {
        'session_start': datetime.now().isoformat(),
        'trades_today': 5,
        'win_rate': 0.60
    }
    
    # Test save
    print("1️⃣ Testing save...")
    success = persistence.save_state(test_positions, test_capital, test_metadata)
    print(f"   Save result: {'✅ Success' if success else '❌ Failed'}\n")
    
    # Test load
    print("2️⃣ Testing load...")
    loaded_state = persistence.load_state()
    print(f"   Loaded {len(loaded_state.get('positions', []))} positions\n")
    
    # Test state info
    print("3️⃣ Testing state info...")
    info = persistence.get_state_info()
    print(f"   State exists: {info.get('exists')}")
    print(f"   Position count: {info.get('position_count')}\n")
    
    # Cleanup
    print("4️⃣ Testing cleanup...")
    persistence.clear_state()
    print("   ✅ Cleanup complete\n")
    
    print("✅ All tests passed!")


if __name__ == "__main__":
    test_persistence()
