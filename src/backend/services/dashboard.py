"""
Flask server for serving the React dashboard.
"""
import os
import sys
import logging
from pathlib import Path
from flask import Flask, send_from_directory, redirect

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure Flask app
app = Flask(__name__)

# Path to the React build files
REACT_BUILD_DIR = Path(__file__).parent.parent.parent / "frontend" / "react-dashboard" / "dist"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    """Serve the React app or its static files."""
    logger.debug(f"Request received for path: {path}")
    
    # Check if a file exists in the React build directory
    if path and (REACT_BUILD_DIR / path).exists() and (REACT_BUILD_DIR / path).is_file():
        logger.debug(f"Serving static file: {path}")
        return send_from_directory(REACT_BUILD_DIR, path)
    
    # If no file matches or the path is empty, serve index.html for client-side routing
    logger.debug("Serving React app index.html")
    return send_from_directory(REACT_BUILD_DIR, 'index.html')

if __name__ == '__main__':
    # Check if the React build exists
    if not REACT_BUILD_DIR.exists() or not (REACT_BUILD_DIR / "index.html").exists():
        logger.error(f"React build not found at: {REACT_BUILD_DIR}")
        logger.error("Please build the React app first by running: npm run build")
        sys.exit(1)
    
    logger.info(f"Serving React dashboard from: {REACT_BUILD_DIR}")
    logger.info("Dashboard server starting on port 3000...")
    app.run(debug=True, port=3000) 