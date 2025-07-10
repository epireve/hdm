#!/usr/bin/env python3
"""
Simple HTTP server to serve the visualization locally.
This avoids CORS issues when loading JSON files.
"""

import http.server
import socketserver
import os
import webbrowser
from threading import Timer

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def open_browser():
    """Open the visualization in the default browser."""
    webbrowser.open(f'http://localhost:{PORT}/visualization/pkg_research_explorer/index.html')

# Change to the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(project_root)

print(f"Starting server on http://localhost:{PORT}")
print(f"Opening PKG Research Explorer in your browser...")
print("Press Ctrl+C to stop the server")

# Open browser after a short delay
timer = Timer(1, open_browser)
timer.start()

# Start the server
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        timer.cancel()