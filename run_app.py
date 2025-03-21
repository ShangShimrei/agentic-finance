"""
Launch the YRS Agentic Finance application from the root directory.
"""
import os
import sys
import subprocess
from pathlib import Path

if __name__ == "__main__":
    # Get the path to the frontend directory
    frontend_dir = Path(__file__).parent / "src" / "frontend"
    
    if not frontend_dir.exists():
        print(f"Error: Frontend directory not found at {frontend_dir}")
        sys.exit(1)
    
    # Change to the frontend directory
    os.chdir(frontend_dir)
    
    # Import and run the unified server
    try:
        sys.path.append(str(frontend_dir))
        from unified_server import run_server
        
        print("=" * 50)
        print("  YRS Agentic Finance Application")
        print("  Starting unified server...")
        print("=" * 50)
        print("  The application will open in your default browser.")
        print("  Press Ctrl+C to stop the server.")
        print("=" * 50)
        
        # Run the server
        run_server()
    except ImportError as e:
        print(f"Error importing unified_server: {e}")
        print("Running the server script directly...")
        
        # If import fails, try to run the script directly using subprocess
        run_script_path = frontend_dir / "run_app.py"
        try:
            subprocess.run([sys.executable, str(run_script_path)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}") 