#!/usr/bin/env python3
"""
Launch the HDM Knowledge Graph Visualization in a web browser
"""

import http.server
import socketserver
import webbrowser
import os
import threading
import time

PORT = 8080
DIRECTORY = "visualization"

class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with less verbose logging"""
    def log_message(self, format, *args):
        # Only log errors, not every request
        if args[1] != '200':
            super().log_message(format, *args)

def start_server():
    """Start the HTTP server"""
    os.chdir(DIRECTORY)
    handler = QuietHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"🌐 Server running at http://localhost:{PORT}")
        print("📊 HDM Knowledge Graph Visualization is ready!")
        print("Press Ctrl+C to stop the server")
        httpd.serve_forever()

def open_browser():
    """Open the visualization in the default web browser"""
    time.sleep(1)  # Give the server time to start
    url = f"http://localhost:{PORT}"
    webbrowser.open(url)
    print(f"🚀 Opening visualization in browser: {url}")

if __name__ == "__main__":
    print("=" * 60)
    print("HDM Knowledge Graph Visualization Launcher")
    print("=" * 60)
    
    # Check if visualization directory exists
    if not os.path.exists(DIRECTORY):
        print(f"❌ Error: '{DIRECTORY}' directory not found!")
        print("Please run this script from the HDM project root directory")
        exit(1)
    
    # Check if data files exist
    data_files = ["graph_data.json", "themes.json", "index.json"]
    data_dir = os.path.join(DIRECTORY, "data")
    
    for file in data_files:
        path = os.path.join(data_dir, file)
        if not os.path.exists(path):
            print(f"❌ Error: Required data file '{file}' not found!")
            print("Please run 'python scripts/graph_generation/process_hdm_data.py' first")
            exit(1)
    
    print("✅ All required files found")
    print(f"📁 Serving files from: {os.path.abspath(DIRECTORY)}")
    print()
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
        print("Thank you for using HDM Knowledge Graph Visualization!")