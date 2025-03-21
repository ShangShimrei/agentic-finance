"""
Simple script to run the unified server.
"""
import os
import sys
from pathlib import Path

# Make sure we can import the unified_server module
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import and run the unified server
from unified_server import run_server

if __name__ == "__main__":
    print("Starting the unified server for YRS Agentic Finance...")
    
    # Change to the frontend directory to ensure correct relative paths
    os.chdir(current_dir)
    
    # Run the server
    run_server() 