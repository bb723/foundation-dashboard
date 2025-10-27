# Foundation Dashboard - Project Structure

## Quick Overview

This is a Flask web application that provides a property management dashboard. It uses a shared `foundation` package for common functionality.

## File Structure

```
foundation-dashboard/
│
├── app.py                          # Main Flask application
│   ├── Routes: /, /pipeline, /reports, /receipts, /budgets
│   ├── Authentication via foundation.auth
│   └── Error handlers (404, 500)
│
├── requirements.txt                # Python dependencies
│   └── foundation package from GitHub v0.1.0
│
├── Procfile                        # Heroku deployment config
│   └── web: gunicorn app:app
│
├── runtime.txt                     # Python version: 3.10.12
│
├── .env.example                    # Environment variables template
│   ├── MS_CLIENT_ID
│   ├── MS_CLIENT_SECRET
│   ├── MS_TENANT_ID
│   ├── REDIRECT_URI
│   └── FLASK_SECRET_KEY
│
├── .gitignore                      # Git ignore patterns
│   └── Standard Python/Flask patterns
│
├── README.md                       # Complete documentation
│   ├── Setup instructions
│   ├── Deployment guide
│   ├── Troubleshooting
│   └── API documentation
│
├── setup_check.py                  # Setup verification script
│   └── Validates configuration before running
│
└── templates/
    └── dashboard/
        ├── home.html               # Dashboard home page
        │   ├── System status cards
        │   ├── Quick statistics
        │   └── Recent activity
        │
        ├── pipeline.html           # Pipeline status page
        │   ├── Job schedule table
        │   ├── Status overview
        │   └── Recent history
        │
        ├── placeholder.html        # Generic coming soon page
        │   └── Used by /reports, /receipts, /budgets
        │
        └── error.html              # Error page template
            └── Used by 404, 500 handlers
```

## Key Components

### 1. Application (app.py)
- **Purpose**: Main Flask application with routes and authentication
- **Dependencies**: foundation package, Flask, python-dotenv
- **Key Features**:
  - Microsoft Azure AD authentication via foundation.auth
  - Login required decorator for protected routes
  - Error handling with friendly pages

### 2. Templates (templates/dashboard/)
- **Purpose**: HTML pages that extend foundation's base.html
- **Styling**: Uses Bootstrap 5 and foundation's CSS
- **Templates**:
  - `home.html`: Dashboard landing page with status overview
  - `pipeline.html`: Scheduled jobs and ETL monitoring
  - `placeholder.html`: Generic page for upcoming features
  - `error.html`: User-friendly error pages

### 3. Configuration Files
- **requirements.txt**: Python package dependencies
- **Procfile**: Tells Heroku how to run the app
- **runtime.txt**: Specifies Python version for Heroku
- **.env.example**: Template for environment variables

### 4. Documentation
- **README.md**: Comprehensive setup and deployment guide
- **PROJECT_STRUCTURE.md**: This file - quick reference

## Data Flow

```
User Request
    ↓
Foundation Auth Middleware (if protected route)
    ↓
Flask Route Handler (app.py)
    ↓
Render Template (extends foundation's base.html)
    ↓
HTML Response
```

## Authentication Flow

```
1. User visits protected route (e.g., /)
2. @login_required decorator checks session
3. If not authenticated → redirect to /auth/login
4. Foundation redirects to Microsoft Azure AD
5. User logs in with Microsoft credentials
6. Azure redirects to /auth/callback
7. Foundation validates token and creates session
8. User redirected to original route
```

## Template Inheritance

```
foundation/templates/base.html          # From foundation package
    ├── Navigation sidebar
    ├── Header with user info
    ├── Bootstrap CSS/JS
    └── {% block content %}

templates/dashboard/home.html           # This app
    └── {% extends "base.html" %}
        └── {% block content %}
            └── Dashboard-specific content
```

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `MS_CLIENT_ID` | Azure AD app ID | `abc123-...` |
| `MS_CLIENT_SECRET` | Azure AD secret | `secret123` |
| `MS_TENANT_ID` | Azure AD tenant | `tenant123` |
| `REDIRECT_URI` | OAuth callback | `http://localhost:5000/auth/callback` |
| `FLASK_SECRET_KEY` | Session encryption | Random 32-byte hex |
| `FLASK_ENV` | Environment mode | `development` or `production` |
| `PORT` | Server port | `5000` |

## Routes

| Route | Method | Auth Required | Purpose |
|-------|--------|---------------|---------|
| `/` | GET | Yes | Dashboard home |
| `/pipeline` | GET | Yes | Pipeline status |
| `/reports` | GET | Yes | Reports (placeholder) |
| `/receipts` | GET | Yes | Receipts (placeholder) |
| `/budgets` | GET | Yes | Budgets (placeholder) |
| `/auth/login` | GET | No | Microsoft login |
| `/auth/callback` | GET | No | OAuth callback |
| `/auth/logout` | GET | No | Logout |

## Quick Start Commands

```bash
# Setup
cp .env.example .env
# Edit .env with your credentials
pip install -r requirements.txt

# Verify setup
python setup_check.py

# Run locally
python app.py

# Deploy to Heroku
heroku create your-app-name
heroku config:set MS_CLIENT_ID=xxx MS_CLIENT_SECRET=xxx ...
git push heroku main
```

## Integration with Foundation Package

The `foundation` package (separate repository) provides:
- **foundation.auth**: MicrosoftAuth class, login_required decorator
- **foundation.clients**: Database connection clients (not used yet)
- **foundation/templates/base.html**: Base template with navigation
- **foundation/static/**: CSS, JavaScript, images

This separation allows multiple apps to share common infrastructure.

## Future Enhancements

1. **Pipeline Page**: Connect to real job scheduler (Azure Functions, etc.)
2. **Reports Page**: Implement financial and operational reports
3. **Receipts Page**: Build receipt upload and processing system
4. **Budgets Page**: Create budget tracking and forecasting tools
5. **API Endpoints**: Add REST API for external integrations
6. **User Management**: Role-based access control
7. **Audit Logging**: Track user actions and system events

## Testing Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy .env.example to .env
- [ ] Fill in Microsoft Azure AD credentials
- [ ] Run setup check: `python setup_check.py`
- [ ] Start app: `python app.py`
- [ ] Visit http://localhost:5000
- [ ] Verify Microsoft login redirect
- [ ] Login with valid credentials
- [ ] See dashboard home page
- [ ] Navigate to Pipeline page
- [ ] Test other navigation links
- [ ] Verify logout functionality

## Support

- **Application Issues**: Check README.md troubleshooting section
- **Foundation Package**: See foundation repository documentation
- **Azure AD Setup**: Microsoft Azure documentation
