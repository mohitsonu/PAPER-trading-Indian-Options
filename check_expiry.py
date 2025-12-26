#!/usr/bin/env python3
"""
Check current expiry and verify market data availability
"""

from NorenRestApiPy.NorenApi import NorenApi
import pyotp
import os
import json
from dotenv import load_dotenv

load_dotenv()

def check_expiry():
    print("=" * 70)
    print("🔍 EXPIRY CHECKER")
    print("=" * 70)
    
    # Load config
    with open('expiry_config.json', 'r') as f:
        config = json.load(f)
    
    current_expiry = config.get('current_expiry')
    print(f"\n📅 Current expiry in config: {current_expiry}")
    
    # Login to API
    api = NorenApi(host='https://api.shoonya.com/NorenWClientTP/', 
                   websocket='wss://api.shoonya.com/NorenWSTP/')
    
    user_id = os.getenv('SHOONYA_USER_ID')
    password = os.getenv('SHOONYA_PASSWORD')
    totp_key = os.getenv('SHOONYA_TOTP_KEY')
    vendor_code = os.getenv('SHOONYA_VENDOR_CODE')
    api_secret = os.getenv('SHOONYA_API_SECRET')
    
    totp = pyotp.TOTP(totp_key).now()
    
    print("\n⏳ Logging in...")
    result = api.login(
        userid=user_id,
        password=password,
        twoFA=totp,
        vendor_code=vendor_code,
        api_secret=api_secret,
        imei='abc1234'
    )
    
    if not result or result.get('stat') != 'Ok':
        print(f"❌ Login failed: {result}")
        return
    
    print("✅ Login successful!")
    
    # Test search for a strike
    print("\n🔍 Testing market data availability...")
    print(f"   Searching for strike 26000...")
    
    search_result = api.searchscrip(exchange="NFO", searchtext="26000")
    
    if search_result and search_result.get('stat') == 'Ok':
        symbols = search_result.get('values', [])
        print(f"   Found {len(symbols)} results")
        
        # Filter for NIFTY options
        nifty_options = []
        for symbol in symbols:
            tsym = symbol.get('tsym', '')
            if tsym.startswith('NIFTY') and not tsym.startswith('NIFTYBANK'):
                nifty_options.append(tsym)
        
        print(f"\n📊 NIFTY options found:")
        for i, sym in enumerate(nifty_options[:10], 1):
            print(f"   {i}. {sym}")
        
        if nifty_options:
            # Check which expiries are available
            expiries = set()
            for sym in nifty_options:
                # Extract expiry from symbol (format: NIFTY09DEC2426000CE)
                if 'DEC' in sym:
                    # Find DEC and extract date
                    idx = sym.find('DEC')
                    if idx > 0:
                        expiry_part = sym[idx-2:idx+5]  # e.g., "09DEC24"
                        expiries.add(expiry_part)
            
            print(f"\n📅 Available expiries:")
            for exp in sorted(expiries):
                if exp == current_expiry:
                    print(f"   ✅ {exp} (CURRENT)")
                else:
                    print(f"   • {exp}")
            
            if current_expiry not in expiries:
                print(f"\n⚠️ WARNING: Current expiry '{current_expiry}' not found in market!")
                print(f"   Available expiries: {', '.join(sorted(expiries))}")
                print(f"\n💡 Update expiry_config.json with one of the available expiries")
        else:
            print("\n❌ No NIFTY options found!")
    else:
        print(f"❌ Search failed: {search_result}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    check_expiry()
