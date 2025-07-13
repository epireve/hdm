#!/usr/bin/env python3
"""
Test script to verify server setup and file access.
"""

import os
import requests
import time
import subprocess
import sys

def test_server():
    """Test if the server is working correctly."""
    BASE_URL = "http://localhost:8000"
    
    print("Testing server setup...")
    
    # Test 1: Check if basic visualization loads
    try:
        response = requests.get(f"{BASE_URL}/visualization/pkg_research_explorer/index.html", timeout=5)
        print(f"✓ Visualization page: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Visualization page failed: {e}")
    
    # Test 2: Check if markdown papers directory is accessible
    try:
        response = requests.get(f"{BASE_URL}/markdown_papers/ain_2024/paper.md", timeout=5)
        print(f"✓ Paper file access: {response.status_code}")
        if response.status_code == 200:
            print(f"  Paper content length: {len(response.text)} characters")
    except requests.exceptions.RequestException as e:
        print(f"✗ Paper file access failed: {e}")
    
    # Test 3: Check if images are accessible
    try:
        response = requests.get(f"{BASE_URL}/markdown_papers/ain_2024/_page_0_Picture_0.jpeg", timeout=5)
        print(f"✓ Image file access: {response.status_code}")
        if response.status_code == 200:
            print(f"  Image content length: {len(response.content)} bytes")
    except requests.exceptions.RequestException as e:
        print(f"✗ Image file access failed: {e}")
    
    # Test 4: Check file system
    print("\nFile system check:")
    print(f"Current directory: {os.getcwd()}")
    print(f"markdown_papers exists: {os.path.exists('markdown_papers')}")
    if os.path.exists('markdown_papers/ain_2024'):
        files = os.listdir('markdown_papers/ain_2024')
        print(f"ain_2024 paper files: {files}")
    

if __name__ == "__main__":
    test_server()