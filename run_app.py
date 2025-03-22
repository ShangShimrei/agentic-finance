"""
Run the YRS Agentic Finance Application.
This script starts the unified server, which serves both the landing page and the React dashboard.
"""
import sys
import os
import subprocess
import webbrowser

def main():
    """Run the application."""
    print("=== YRS Agentic Finance Application ===")
    print("Starting unified server...")
    
    # Path to the unified server script
    unified_server_path = os.path.join("src", "backend", "unified_server.py")
    
    # Check if the file exists
    if not os.path.exists(unified_server_path):
        print(f"Error: Unified server script not found at {unified_server_path}")
        sys.exit(1)
    
    print("Opening application in your browser...")
    print("Dashboard will be available at: http://localhost:8000/dashboard")
    print("Press CTRL+C to stop the server.")
    
    # Run the unified server script
    subprocess.run([sys.executable, unified_server_path])

if __name__ == "__main__":
    main() 