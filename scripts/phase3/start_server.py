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

PORT = 8000


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()
    
    def log_message(self, format, *args):
        """Override to add more detailed logging."""
        print(f"[{self.log_date_time_string()}] {format % args}")
        
    def do_GET(self):
        """Override to add request logging and debug info."""
        print(f"GET request for: {self.path}")
        print(f"Current working directory: {os.getcwd()}")
        
        # Check if requesting a markdown paper file
        if self.path.startswith('/markdown_papers/'):
            full_path = os.path.join(os.getcwd(), self.path.lstrip('/'))
            print(f"Attempting to serve file: {full_path}")
            print(f"File exists: {os.path.exists(full_path)}")
            
            # Additional debugging
            dir_path = os.path.dirname(full_path)
            print(f"Directory exists: {os.path.exists(dir_path)}")
            if os.path.exists(dir_path):
                print(f"Directory contents: {os.listdir(dir_path)}")
            
        super().do_GET()


def open_browser():
    """Open the visualization in the default browser."""
    webbrowser.open(
        f"http://localhost:{PORT}/visualization/pkg_research_explorer/index.html"
    )


# Change to the project root directory
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
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
