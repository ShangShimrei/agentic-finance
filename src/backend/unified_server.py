"""
Unified server for serving both the landing page and React dashboard.
This eliminates the need to run multiple servers.
"""
import os
import logging
import threading
import subprocess
import time
import http.server
import socketserver
import signal
import webbrowser
import sys
import re
from pathlib import Path

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Constants
PORT = 8000
HOST = 'localhost'
REACT_BUILD_DIR = Path(__file__).parent.parent / "frontend" / "react-dashboard" / "dist"

class UnifiedServerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for serving both landing page and dashboard."""
    
    def do_GET(self):
        """Handle GET requests."""
        logger.info(f"Handling request for path: {self.path}")
        
        # Landing page route
        if self.path == "/" or self.path == "":
            self._serve_landing_page()
            
        # Dashboard route - index.html
        elif self.path == "/dashboard" or self.path == "/dashboard/":
            self._serve_dashboard_index()
            
        # Dashboard assets with normal path
        elif self.path.startswith("/assets/"):
            asset_path = self.path.replace("/", "", 1)  # Remove leading slash
            self._serve_dashboard_asset(asset_path)
            
        # Dashboard assets with dashboard prefix
        elif self.path.startswith("/dashboard/assets/"):
            asset_path = self.path.replace("/dashboard/", "", 1)
            self._serve_dashboard_asset(asset_path)
        
        # Assets directly in dist directory
        elif self.path.startswith("/dashboard/") and "." in self.path:
            asset_path = self.path.replace("/dashboard/", "", 1)
            self._serve_dashboard_asset(asset_path)
            
        # Fallback to handle deep links in the dashboard SPA
        elif self.path.startswith("/dashboard/"):
            self._serve_dashboard_index()
            
        # Serve other static files
        else:
            super().do_GET()
    
    def _serve_landing_page(self):
        """Serve the landing page."""
        try:
            # Get the path to the landing page HTML file
            landing_page_path = Path(__file__).parent.parent / "frontend" / "assets" / "landing_page.html"
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open(landing_page_path, 'rb') as file:
                self.wfile.write(file.read())
                
            logger.info("Served landing page")
        except Exception as e:
            logger.error(f"Error serving landing page: {e}")
            self.send_error(500, str(e))
    
    def _serve_dashboard_index(self):
        """Serve the dashboard React app index.html."""
        try:
            # Get the path to the React app's index.html
            dashboard_index_path = REACT_BUILD_DIR / "index.html"
            
            # If the React build doesn't exist, show an error
            if not dashboard_index_path.exists():
                logger.error(f"React build not found at: {dashboard_index_path}")
                self.send_error(500, "Dashboard not built. Please run 'npm run build' in the react-dashboard directory.")
                return
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open(dashboard_index_path, 'rb') as file:
                content = file.read()
                self.wfile.write(content)
                
            logger.info("Served dashboard index")
        except Exception as e:
            logger.error(f"Error serving dashboard index: {e}")
            self.send_error(500, str(e))
    
    def _serve_dashboard_asset(self, asset_path):
        """Serve static assets for the dashboard."""
        try:
            # Calculate the file path relative to the React build directory
            file_path = REACT_BUILD_DIR / asset_path
            
            logger.info(f"Looking for asset: {asset_path} at {file_path}")
            
            if not file_path.exists():
                logger.error(f"Asset not found: {file_path}")
                self.send_error(404, f"Asset not found: {asset_path}")
                return
                
            # Determine content type based on file extension
            _, ext = os.path.splitext(file_path)
            content_type = self._get_content_type(ext)
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            
            with open(file_path, 'rb') as file:
                self.wfile.write(file.read())
                
            logger.info(f"Served asset: {asset_path}")
        except Exception as e:
            logger.error(f"Error serving asset: {e}")
            self.send_error(500, str(e))
    
    def _get_content_type(self, ext):
        """Get content type based on file extension."""
        content_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon'
        }
        return content_types.get(ext.lower(), 'application/octet-stream')

def update_landing_page_link():
    """Update the landing page to point to /dashboard instead of external URL."""
    try:
        landing_page_path = Path(__file__).parent.parent / "frontend" / "assets" / "landing_page.html"
        
        with open(landing_page_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Update the link to use /dashboard instead of dashboard
        updated_content = content.replace('href="dashboard"', 'href="/dashboard"')
        
        with open(landing_page_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
            
        logger.info("Updated landing page link to /dashboard")
    except Exception as e:
        logger.error(f"Error updating landing page link: {e}")

def run_server():
    """Run the unified server."""
    # Update the landing page link
    update_landing_page_link()
    
    # Check if the React build exists
    react_build_dir = Path(__file__).parent.parent / "frontend" / "react-dashboard" / "dist"
    if not react_build_dir.exists() or not (react_build_dir / "index.html").exists():
        logger.warning("React dashboard build not found. The /dashboard route may not work.")
        logger.info("To build the React dashboard, run: cd frontend/react-dashboard && npm run build")
    else:
        logger.info(f"Found React dashboard build at {react_build_dir}")
        
        # List assets to verify they're where we expect them
        assets_dir = react_build_dir / "assets"
        if assets_dir.exists():
            logger.info(f"Found assets directory at {assets_dir}")
            logger.info(f"Assets: {[f.name for f in assets_dir.iterdir() if f.is_file()]}")
    
    # Set up the HTTP server for the landing page and dashboard
    handler = UnifiedServerHandler
    handler.extensions_map.update({
        '': 'application/octet-stream',
    })
    
    try:
        with socketserver.TCPServer((HOST, PORT), handler) as httpd:
            server_url = f"http://{HOST}:{PORT}"
            logger.info(f"Unified server started at {server_url}")
            logger.info(f"Landing page available at {server_url}")
            logger.info(f"Dashboard available at {server_url}/dashboard")
            
            # Open the browser
            webbrowser.open(server_url)
            
            # Handle shutdown gracefully
            def signal_handler(sig, frame):
                logger.info("Shutting down server...")
                httpd.shutdown()
                sys.exit(0)
            
            signal.signal(signal.SIGINT, signal_handler)
            
            # Start the server
            httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")

if __name__ == "__main__":
    run_server() 