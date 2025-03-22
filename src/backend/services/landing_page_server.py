"""
Flask server for serving the landing page.
"""
import os
from pathlib import Path
from flask import Flask, send_from_directory, redirect

app = Flask(__name__)

# Path to the landing page assets
LANDING_PAGE_PATH = Path(__file__).parent.parent.parent / "frontend" / "assets"

@app.route('/')
def index():
    """Serve the landing page."""
    return send_from_directory(LANDING_PAGE_PATH, 'landing_page.html')

@app.route('/dashboard')
def redirect_to_dashboard():
    """Redirect to the dashboard."""
    return redirect('/dashboard/')

if __name__ == '__main__':
    app.run(debug=True, port=8000) 