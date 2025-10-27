"""
foundation-dashboard - Property Management Dashboard
Main Flask application using the foundation package for auth, clients, and UI templates.
"""

import os
from flask import Flask, render_template, redirect, url_for, session, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import authentication from foundation package
from foundation.auth import MicrosoftAuth, MSALConfig, login_required

# Initialize Flask application
app = Flask(__name__)

# Configure Flask app with secret key from environment
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure template and static folders to use foundation's assets
# Foundation package provides base.html, CSS, and JavaScript
app.template_folder = 'templates'
app.static_folder = 'static'

# Initialize Microsoft authentication
# MSALConfig reads credentials from environment variables automatically
auth = MicrosoftAuth()

# Get redirect URI from environment
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/auth/callback')


# Authentication Routes
# These routes handle Microsoft OAuth login flow

@app.route('/login')
def login():
    """Redirect to Microsoft login page"""
    auth_url = auth.get_auth_url(REDIRECT_URI)
    return redirect(auth_url)


@app.route('/auth/callback')
def auth_callback():
    """Handle OAuth callback from Microsoft"""
    # Check for errors in callback
    if 'error' in request.args:
        return f"Error: {request.args.get('error')} - {request.args.get('error_description')}", 400

    # Verify state to prevent CSRF
    if request.args.get('state') != session.get('state'):
        return "Error: State mismatch. Possible CSRF attack.", 400

    # Get authorization code
    code = request.args.get('code')
    if not code:
        return "Error: No authorization code received", 400

    # Exchange code for tokens
    result = auth.get_token_from_code(code, REDIRECT_URI)

    if 'error' in result:
        return f"Error: {result.get('error')} - {result.get('error_description')}", 400

    # Store user info in session
    session['user'] = result.get('id_token_claims')
    session['access_token'] = result.get('access_token')

    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    """Log out and clear session"""
    session.clear()
    logout_url = auth.get_logout_url(url_for('login', _external=True))
    return redirect(logout_url)


# Dashboard Routes
# All routes require authentication using the @login_required decorator

@app.route('/')
@login_required
def home():
    """
    Dashboard home page - main landing page after login.
    Shows system overview, quick stats, and recent activity.
    """
    return render_template('dashboard/home.html')


@app.route('/pipeline')
@login_required
def pipeline():
    """
    Redirect to Pipeline application.
    The pipeline app is a separate application with its own UI.

    For local development: http://localhost:5001
    For production: https://pipeline-app-name.herokuapp.com
    """
    # Configure pipeline app URL based on environment
    pipeline_url = os.getenv('PIPELINE_APP_URL', 'http://localhost:5001')

    # For now, show a link page
    # Later, can redirect directly: return redirect(pipeline_url)
    return render_template('dashboard/pipeline_link.html', pipeline_url=pipeline_url)


@app.route('/reports')
@login_required
def reports():
    """
    Reports page - placeholder for future reporting features.
    Will display financial reports, occupancy reports, etc.
    """
    return render_template('dashboard/placeholder.html',
                         page_title='Reports',
                         page_description='Financial and operational reports coming soon.')


@app.route('/receipts')
@login_required
def receipts():
    """
    Receipts page - placeholder for receipt management.
    Will handle receipt uploads, processing, and storage.
    """
    return render_template('dashboard/placeholder.html',
                         page_title='Receipts',
                         page_description='Receipt management system coming soon.')


@app.route('/budgets')
@login_required
def budgets():
    """
    Budgets page - placeholder for budget management.
    Will track property budgets, expenses, and forecasts.
    """
    return render_template('dashboard/placeholder.html',
                         page_title='Budgets',
                         page_description='Budget management system coming soon.')


# Error handlers

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with a friendly page."""
    return render_template('dashboard/error.html',
                         error_code=404,
                         error_message='Page not found'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with a friendly page."""
    return render_template('dashboard/error.html',
                         error_code=500,
                         error_message='Internal server error'), 500


if __name__ == '__main__':
    # Run Flask development server
    # For production, use gunicorn instead (see Procfile)
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'

    app.run(host='0.0.0.0', port=port, debug=debug)
