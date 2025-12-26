#!/usr/bin/env python3
"""
Test correct Shoonya API format
"""

import requests
import json
import pyotp
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

def test_correct_login_format():
    """Test with correct jData format"""
    print("🔧 TESTING CORRECT API FORMAT")
    print("=" * 50)
    
    user_id = os.getenv('SHOONYA_USER_ID')
    password = os.getenv('SHOONYA_PASSWORD')
    totp_key = os.getenv('SHOONYA_TOTP_KEY')
    vendor_code = os.getenv('SHOONYA_VENDOR_CODE')
    api_secret = os.getenv('SHOONYA_API_SECRET')
    
    totp = pyotp.TOTP(totp_key).now()
    
    # Create the correct format with jData
    login_data = {
        'userid': user_id,
        'password': password,
        'twoFA': totp,
        'vendor_code': vendor_code,
        'api_secret': api_secret,
        'imei': 'abc1234'
    }
    
    # Convert to JSON string for jData parameter
    jdata = json.dumps(login_data)
    
    # Send with jData parameter
    payload = {'jData': jdata}
    
    print(f"📤 Sending with jData format")
    print(f"📋 jData: {jdata}")
    
    try:
        response = requests.post(
            'https://api.shoonya.com/NorenWClientTP/QuickAuth',
            data=payload,
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Text: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"📥 Parsed JSON: {json.dumps(result, indent=2)}")
                
                if result.get('stat') == 'Ok':
                    print("✅ Login successful with correct format!")
                    return True
                else:
                    print(f"❌ Login failed: {result.get('emsg', 'Unknown error')}")
                    return False
            except json.JSONDecodeError:
                print("❌ Response is not valid JSON")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_correct_login_format()