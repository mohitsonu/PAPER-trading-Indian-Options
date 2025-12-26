#!/usr/bin/env python3
"""
Test with exact NorenApi library format
"""

import requests
import json
import pyotp
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

def test_library_format():
    """Test with exact format used by NorenApi library"""
    print("🔧 TESTING EXACT LIBRARY FORMAT")
    print("=" * 50)
    
    user_id = os.getenv('SHOONYA_USER_ID')
    password = os.getenv('SHOONYA_PASSWORD')
    totp_key = os.getenv('SHOONYA_TOTP_KEY')
    vendor_code = os.getenv('SHOONYA_VENDOR_CODE')
    api_secret = os.getenv('SHOONYA_API_SECRET')
    
    totp = pyotp.TOTP(totp_key).now()
    
    # Use exact format from NorenApi library
    # Convert to SHA 256 for password and app key
    pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
    u_app_key = f'{user_id}|{api_secret}'
    app_key = hashlib.sha256(u_app_key.encode('utf-8')).hexdigest()
    
    # Prepare the data exactly like the library
    values = {"source": "API", "apkversion": "1.0.0"}
    values["uid"] = user_id
    values["pwd"] = pwd
    values["factor2"] = totp
    values["vc"] = vendor_code
    values["appkey"] = app_key
    values["imei"] = 'abc1234'
    
    payload = 'jData=' + json.dumps(values)
    
    print(f"📤 Using exact library format")
    print(f"📋 Original password: {password}")
    print(f"📋 SHA256 password: {pwd}")
    print(f"📋 App key string: {u_app_key}")
    print(f"📋 SHA256 app key: {app_key}")
    print(f"📋 TOTP: {totp}")
    print(f"📋 Payload: {payload}")
    
    try:
        response = requests.post(
            'https://api.shoonya.com/NorenWClientTP/QuickAuth',
            data=payload,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Text: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"📥 Parsed JSON: {json.dumps(result, indent=2)}")
                
                if result.get('stat') == 'Ok':
                    print("✅ Login successful with library format!")
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
    test_library_format()