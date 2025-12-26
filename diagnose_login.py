#!/usr/bin/env python3
"""
Detailed Shoonya Login Diagnostics
"""

import requests
import json
import pyotp
import os
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

def test_network_connectivity():
    """Test basic network connectivity"""
    print("🌐 TESTING NETWORK CONNECTIVITY")
    print("=" * 50)
    
    try:
        # Test general internet
        response = requests.get('https://google.com', timeout=5)
        print(f"✅ Internet: OK ({response.status_code})")
    except Exception as e:
        print(f"❌ Internet: FAILED - {e}")
        return False
    
    try:
        # Test Shoonya main site
        response = requests.get('https://shoonya.com', timeout=10)
        print(f"✅ Shoonya Website: OK ({response.status_code})")
    except Exception as e:
        print(f"❌ Shoonya Website: FAILED - {e}")
    
    try:
        # Test Shoonya API base
        response = requests.get('https://api.shoonya.com', timeout=10)
        print(f"✅ Shoonya API Base: OK ({response.status_code})")
    except Exception as e:
        print(f"❌ Shoonya API Base: FAILED - {e}")
    
    return True

def test_credentials():
    """Test credential format and TOTP generation"""
    print("\n🔑 TESTING CREDENTIALS")
    print("=" * 50)
    
    user_id = os.getenv('SHOONYA_USER_ID')
    password = os.getenv('SHOONYA_PASSWORD')
    totp_key = os.getenv('SHOONYA_TOTP_KEY')
    vendor_code = os.getenv('SHOONYA_VENDOR_CODE')
    api_secret = os.getenv('SHOONYA_API_SECRET')
    
    # Check if all credentials exist
    missing = []
    if not user_id: missing.append('SHOONYA_USER_ID')
    if not password: missing.append('SHOONYA_PASSWORD')
    if not totp_key: missing.append('SHOONYA_TOTP_KEY')
    if not vendor_code: missing.append('SHOONYA_VENDOR_CODE')
    if not api_secret: missing.append('SHOONYA_API_SECRET')
    
    if missing:
        print(f"❌ Missing credentials: {', '.join(missing)}")
        return False
    
    print(f"✅ User ID: {user_id}")
    print(f"✅ Password: {'*' * len(password)} (length: {len(password)})")
    print(f"✅ Vendor Code: {vendor_code}")
    print(f"✅ API Secret: {api_secret[:10]}... (length: {len(api_secret)})")
    print(f"✅ TOTP Key: {totp_key}")
    
    # Test TOTP generation
    try:
        totp = pyotp.TOTP(totp_key)
        current_otp = totp.now()
        print(f"✅ Current TOTP: {current_otp}")
        
        # Generate next few TOTPs to check consistency
        print("📊 TOTP sequence:")
        for i in range(3):
            otp = totp.now()
            print(f"   {datetime.now().strftime('%H:%M:%S')}: {otp}")
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ TOTP Generation Failed: {e}")
        return False
    
    return True

def test_raw_api_call():
    """Test raw API call to Shoonya login endpoint"""
    print("\n🔧 TESTING RAW API CALL")
    print("=" * 50)
    
    user_id = os.getenv('SHOONYA_USER_ID')
    password = os.getenv('SHOONYA_PASSWORD')
    totp_key = os.getenv('SHOONYA_TOTP_KEY')
    vendor_code = os.getenv('SHOONYA_VENDOR_CODE')
    api_secret = os.getenv('SHOONYA_API_SECRET')
    
    totp = pyotp.TOTP(totp_key).now()
    
    # Prepare login data
    login_data = {
        'userid': user_id,
        'password': password,
        'twoFA': totp,
        'vendor_code': vendor_code,
        'api_secret': api_secret,
        'imei': 'abc1234'
    }
    
    print(f"📤 Sending login request to: https://api.shoonya.com/NorenWClientTP/QuickAuth")
    print(f"📋 Data: {json.dumps({k: v if k != 'password' else '*' * len(v) for k, v in login_data.items()}, indent=2)}")
    
    try:
        response = requests.post(
            'https://api.shoonya.com/NorenWClientTP/QuickAuth',
            data=login_data,
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Headers: {dict(response.headers)}")
        print(f"📥 Response Text: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"📥 Parsed JSON: {json.dumps(result, indent=2)}")
                
                if result.get('stat') == 'Ok':
                    print("✅ Raw API call successful!")
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
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (30 seconds)")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_noren_api_library():
    """Test the NorenApi library specifically"""
    print("\n📚 TESTING NOREN API LIBRARY")
    print("=" * 50)
    
    try:
        from NorenRestApiPy.NorenApi import NorenApi
        print("✅ NorenApi library imported successfully")
        
        # Check library version
        import pkg_resources
        version = pkg_resources.get_distribution("NorenRestApiPy").version
        print(f"✅ Library version: {version}")
        
        # Initialize API
        api = NorenApi(
            host='https://api.shoonya.com/NorenWClientTP/', 
            websocket='wss://api.shoonya.com/NorenWSTP/'
        )
        print("✅ NorenApi initialized")
        
        # Test login
        user_id = os.getenv('SHOONYA_USER_ID')
        password = os.getenv('SHOONYA_PASSWORD')
        totp_key = os.getenv('SHOONYA_TOTP_KEY')
        vendor_code = os.getenv('SHOONYA_VENDOR_CODE')
        api_secret = os.getenv('SHOONYA_API_SECRET')
        
        totp = pyotp.TOTP(totp_key).now()
        
        print("🔄 Calling api.login()...")
        result = api.login(
            userid=user_id,
            password=password,
            twoFA=totp,
            vendor_code=vendor_code,
            api_secret=api_secret,
            imei='abc1234'
        )
        
        print(f"📥 Library result: {result}")
        print(f"📥 Result type: {type(result)}")
        
        if result is None:
            print("❌ Library returned None - This is the problem!")
            return False
        elif isinstance(result, dict) and result.get('stat') == 'Ok':
            print("✅ Library login successful!")
            return True
        else:
            print(f"❌ Library login failed: {result}")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import NorenApi: {e}")
        return False
    except Exception as e:
        print(f"❌ Library test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all diagnostic tests"""
    print("🔍 SHOONYA LOGIN DIAGNOSTIC TOOL")
    print("=" * 60)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Network connectivity
    results['network'] = test_network_connectivity()
    
    # Test 2: Credentials
    results['credentials'] = test_credentials()
    
    # Test 3: Raw API call
    results['raw_api'] = test_raw_api_call()
    
    # Test 4: NorenApi library
    results['library'] = test_noren_api_library()
    
    # Summary
    print("\n📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test.upper()}: {status}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("=" * 50)
    
    if not results['network']:
        print("🔧 Fix network connectivity issues first")
    elif not results['credentials']:
        print("🔧 Check your .env file for missing/incorrect credentials")
    elif results['raw_api'] and not results['library']:
        print("🔧 NorenApi library issue - try reinstalling: pip install --upgrade NorenRestApiPy")
    elif not results['raw_api']:
        print("🔧 Shoonya API issue - check account status or contact support")
    else:
        print("🎉 All tests passed - login should work!")

if __name__ == "__main__":
    main()