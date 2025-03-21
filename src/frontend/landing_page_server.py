"""
Server module for serving the landing page.
"""
import logging
import os
import http.server
import socketserver
import webbrowser
import threading
from pathlib import Path

logger = logging.getLogger(__name__)

class LandingPageHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for serving the landing page."""
    
    def do_GET(self):
        """Handle GET requests."""
        # Landing page route
        if self.path == "/" or self.path == "":
            self._serve_landing_page()
        # Dashboard route - redirect to the dashboard server
        elif self.path == "/dashboard":
            self.send_response(302)
            self.send_header('Location', 'http://localhost:3000')
            self.end_headers()
        # Serve other static files
        else:
            super().do_GET()
    
    def _serve_landing_page(self):
        """Serve the landing page."""
        try:
            # Get the path to the landing page HTML file
            landing_page_path = Path(__file__).parent / "landing_page.html"
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open(landing_page_path, 'rb') as file:
                self.wfile.write(file.read())
        except Exception as e:
            logger.error(f"Error serving landing page: {e}")
            self.send_error(500, str(e))

class LandingPageServer:
    """Server for the landing page."""
    
    def __init__(self, host='localhost', port=8000):
        """
        Initialize the landing page server.
        
        Args:
            host: Host address to bind the server
            port: Port to use for the server
        """
        self.host = host
        self.port = port
        self.server = None
        self.server_thread = None
        
        logger.info(f"Initializing Landing Page Server on {host}:{port}")
    
    def start(self):
        """Start the landing page server."""
        try:
            # Change to the directory with frontend files
            frontend_dir = Path(__file__).parent
            os.chdir(frontend_dir)
            
            # Create a server and bind to specified host and port
            self.server = socketserver.TCPServer((self.host, self.port), LandingPageHandler)
            
            # Start the server in a separate thread
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            logger.info(f"Landing Page Server started at http://{self.host}:{self.port}")
            logger.info(f"Open a browser and navigate to http://{self.host}:{self.port} to view the landing page")
            
            # Open the landing page in the default web browser
            webbrowser.open(f"http://{self.host}:{self.port}")
            
        except Exception as e:
            logger.error(f"Error starting landing page server: {e}")
            raise
    
    def stop(self):
        """Stop the landing page server."""
        if self.server:
            self.server.shutdown()
            self.server = None
            logger.info("Landing Page Server stopped")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Start the landing page server
    server = LandingPageServer()
    server.start()
    
    try:
        # Keep the main thread running
        while True:
            pass
    except KeyboardInterrupt:
        # Stop the server on keyboard interrupt
        server.stop()
        logger.info("Exiting...") 