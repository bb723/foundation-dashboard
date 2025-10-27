"""
foundation-dashboard - Property Management Dashboard
Main Flask application using the foundation package for auth, clients, and UI templates.
"""

import os
from flask import Flask, render_template, redirect, url_for, session, request, make_response
from dotenv import load_dotenv
import secrets

# Load environment variables from .env file
load_dotenv()

# Import authentication from foundation package
from foundation.auth import MicrosoftAuth, MSALConfig, login_required

# Initialize Flask application
app = Flask(__name__)

# Configure Flask app with secret key from environment
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Session configuration for OAuth flow
# These settings ensure session cookies work correctly with Microsoft OAuth redirects
app.config['SESSION_COOKIE_SECURE'] = True  # Required for HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Security best practice
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Allow cookies on redirects from Microsoft
app.config['SESSION_COOKIE_NAME'] = 'dashboard_session'  # Unique session cookie name
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour session lifetime

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
    # Generate state manually and store in both session and cookie
    state = secrets.token_hex(16)
    session['state'] = state
    session.permanent = True

    # Build auth URL manually with our state
    from msal import ConfidentialClientApplication
    msal_app = ConfidentialClientApplication(
        os.getenv('MS_CLIENT_ID'),
        authority=f"https://login.microsoftonline.com/{os.getenv('MS_TENANT_ID')}",
        client_credential=os.getenv('MS_CLIENT_SECRET')
    )

    auth_url = msal_app.get_authorization_request_url(
        scopes=['User.Read'],  # Don't include openid, profile, offline_access - MSAL adds them automatically
        redirect_uri=REDIRECT_URI,
        state=state
    )

    app.logger.debug(f"Login - Generated state: {state}")

    # Create response with redirect and set state cookie
    response = make_response(redirect(auth_url))
    response.set_cookie('oauth_state', state, secure=True, httponly=True, samesite='Lax', max_age=600)

    return response


@app.route('/auth/callback')
def auth_callback():
    """Handle OAuth callback from Microsoft"""
    # Check for errors in callback
    if 'error' in request.args:
        error_msg = f"Error: {request.args.get('error')} - {request.args.get('error_description')}"
        app.logger.error(f"OAuth callback error: {error_msg}")
        return error_msg, 400

    # Verify state to prevent CSRF - check both session and cookie
    request_state = request.args.get('state')
    session_state = session.get('state')
    cookie_state = request.cookies.get('oauth_state')

    app.logger.debug(f"Callback - Request state: {request_state}, Session state: {session_state}, Cookie state: {cookie_state}")

    # Verify against cookie if session doesn't have it
    expected_state = session_state or cookie_state

    if request_state != expected_state:
        error_msg = f"Error: State mismatch. Request: {request_state}, Expected: {expected_state}"
        app.logger.error(error_msg)
        return error_msg, 400

    # Get authorization code
    code = request.args.get('code')
    if not code:
        app.logger.error("No authorization code received in callback")
        return "Error: No authorization code received", 400

    # Exchange code for tokens
    app.logger.debug("Exchanging code for tokens")
    result = auth.get_token_from_code(code, REDIRECT_URI)

    if 'error' in result:
        error_msg = f"Error: {result.get('error')} - {result.get('error_description')}"
        app.logger.error(f"Token exchange error: {error_msg}")
        return error_msg, 400

    # Store user info in session
    session['user'] = result.get('id_token_claims')
    session['access_token'] = result.get('access_token')

    app.logger.info(f"User logged in: {session['user'].get('preferred_username')}")

    # Clear the state cookie and redirect to home
    response = make_response(redirect(url_for('home')))
    response.set_cookie('oauth_state', '', expires=0)  # Clear the cookie

    return response


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
    return redirect(pipeline_url)

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
