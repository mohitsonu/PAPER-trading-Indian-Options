#!/usr/bin/env python3
"""
Test Shoonya login to isolate the issue
"""

from NorenRestApiPy.NorenApi import NorenApi
import pyotp
import os
from dotenv import load_dotenv

load_dotenv()

def test_login():
    """Test login with detailed debugging"""
    
    # Initialize API
    api = NorenApi(host='https://api.shoonya.com/NorenWClientTP/', 
                   websocket='wss://api.shoonya.com/NorenWSTP/')
    
    # Get credentials
    user_id = os.getenv('SHOONYA_USER_ID')
    password = os.getenv('SHOONYA_PASSWORD')
    totp_key = os.getenv('SHOONYA_TOTP_KEY')
    vendor_code = os.getenv('SHOONYA_VENDOR_CODE')
    api_secret = os.getenv('SHOONYA_API_SECRET')
    
    print("🔐 TESTING SHOONYA LOGIN")
    print("=" * 50)
    print(f"User ID: {user_id}")
    print(f"Vendor Code: {vendor_code}")
    print(f"API Secret: {api_secret[:10]}...")
    print(f"TOTP Key: {totp_key}")
    
    # Generate TOTP
    totp = pyotp.TOTP(totp_key).now()
    print(f"Current TOTP: {totp}")
    
    try:
        print("\n🔄 Attempting login...")
        
        result = api.login(
            userid=user_id,
            password=password,
            twoFA=totp,
            vendor_code=vendor_code,
            api_secret=api_secret,
            imei='abc1234'
        )
        
        print(f"\n📋 Raw Result: {result}")
        print(f"📋 Result Type: {type(result)}")
        
        if result is None:
            print("❌ Result is None - API call failed")
            return False
        
        if isinstance(result, dict):
            print(f"📋 Status: {result.get('stat', 'Not found')}")
            print(f"📋 Message: {result.get('emsg', 'No message')}")
            
            if result.get('stat') == 'Ok':
                print("✅ Login successful!")
                return True
            else:
                print("❌ Login failed!")
                return False
        else:
            print(f"❌ Unexpected result type: {type(result)}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during login: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_login()
    print(f"\n🎯 Final Result: {'SUCCESS' if success else 'FAILED'}")