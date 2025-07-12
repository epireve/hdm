#!/usr/bin/env python3
"""
Test Kilocode API connection with SSL handling
"""

import sys
import json
import urllib.request
import urllib.error
import ssl
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import Kilocode configuration
from lib.kilocode_config_simple import load_config, ConfigurationError

def test_api():
    """Test the Kilocode API connection"""
    try:
        # Load configuration
        config = load_config()
        print(f"✓ Configuration loaded")
        print(f"  Token: {config.token[:10]}...")
        print(f"  API URL: {config.openrouter_url}")
        print(f"  Model: {config.default_model}")
        
        # Create SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Create request
        url = config.openrouter_url + "/chat/completions"
        
        data = {
            "model": config.default_model,
            "messages": [
                {"role": "user", "content": "Say 'Hello, HDM project!' in exactly 3 words."}
            ],
            "temperature": 0.1,
            "max_tokens": 10
        }
        
        headers = {
            "Authorization": f"Bearer {config.token}",
            "Content-Type": "application/json",
            "HTTP-Referer": config.http_referer,
            "X-Title": config.x_title
        }
        
        # Make request
        print(f"\n✓ Testing API connection...")
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, context=ssl_context) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        print(f"✓ API call successful!")
        print(f"  Response: {result['choices'][0]['message']['content']}")
        print(f"\n✅ Kilocode API is working correctly!")
        
        # Show usage if available
        if 'usage' in result:
            usage = result['usage']
            print(f"\n📊 Token usage:")
            print(f"  Prompt tokens: {usage.get('prompt_tokens', 'N/A')}")
            print(f"  Completion tokens: {usage.get('completion_tokens', 'N/A')}")
            print(f"  Total tokens: {usage.get('total_tokens', 'N/A')}")
        
    except ConfigurationError as e:
        print(f"❌ Configuration error: {e}")
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP error: {e.code} - {e.reason}")
        error_body = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_body)
            print(f"  Error details: {json.dumps(error_json, indent=2)}")
        except:
            print(f"  Response: {error_body}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_api()