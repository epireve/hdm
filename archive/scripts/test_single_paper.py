#!/usr/bin/env python3
"""Test processing a single paper with minimal content"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from lib.kilocode_config_simple import load_config
import json
import urllib.request
import ssl

# Load config
config = load_config()

# SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Simple test prompt
prompt = """Format this into standard structure:

---
cite_key: test_2025
title: Test Paper
---

# Test Paper

This is a test abstract.

## Introduction
Test introduction.

Return a properly formatted paper with YAML frontmatter."""

# API call
url = config.openrouter_url + "/chat/completions"

data = {
    "model": config.default_model,
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.3,
    "max_tokens": 1000
}

headers = {
    "Authorization": f"Bearer {config.token}",
    "Content-Type": "application/json",
    "HTTP-Referer": config.http_referer,
    "X-Title": config.x_title
}

print("Calling API...")
req = urllib.request.Request(
    url,
    data=json.dumps(data).encode('utf-8'),
    headers=headers,
    method='POST'
)

try:
    with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        print("Success!")
        print("Response:")
        print(result['choices'][0]['message']['content'])
except Exception as e:
    print(f"Error: {e}")