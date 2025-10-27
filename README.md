# Foundation Dashboard

A property management dashboard web application built with Flask, utilizing the [foundation](https://github.com/bb723/foundation) package for authentication, database clients, and UI templates.

## Overview

The Foundation Dashboard provides a web interface for managing property operations, including:
- Pipeline job monitoring (ETL processes, mailers, reports)
- Financial reports and analytics
- Receipt processing and management
- Budget tracking and forecasting

This application serves as the web layer, while the `foundation` package provides shared infrastructure components including Microsoft Azure AD authentication, database clients, and base UI templates.

## Architecture

```
foundation-dashboard/          # Web application (this repo)
├── app.py                     # Flask routes and application logic
├── templates/dashboard/       # Dashboard-specific templates
└── requirements.txt           # Includes foundation package from GitHub

foundation/                    # Shared package (separate repo)
├── auth/                      # Microsoft authentication
├── clients/                   # Database and API clients
├── templates/                 # Base HTML templates
└── static/                    # CSS, JavaScript, assets
```

## Features

- **Microsoft Azure AD Authentication**: Secure SSO login using the foundation package
- **Dashboard Home**: Overview of system status and quick stats
- **Pipeline Status**: Monitor scheduled ETL jobs, mailers, and automated tasks
- **Responsive UI**: Bootstrap-based interface with foundation's styling
- **Heroku-Ready**: Configured for easy deployment to Heroku

## Prerequisites

- Python 3.10.12 or compatible version
- Git (for installing foundation package from GitHub)
- Microsoft Azure AD application registration with OAuth credentials
- Heroku account (for production deployment)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd foundation-dashboard
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install Flask, gunicorn, and the foundation package from GitHub.

### 4. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your Microsoft Azure AD credentials:

```env
MS_CLIENT_ID=your-azure-client-id
MS_CLIENT_SECRET=your-azure-client-secret
MS_TENANT_ID=your-azure-tenant-id
REDIRECT_URI=http://localhost:5000/auth/callback
FLASK_SECRET_KEY=your-secure-secret-key
FLASK_ENV=development
```

**Getting Azure AD Credentials:**
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to Azure Active Directory > App registrations
3. Create or select your application
4. Copy Client ID and Tenant ID from the Overview page
5. Generate a Client Secret in Certificates & secrets
6. Add redirect URI: `http://localhost:5000/auth/callback`

**Generate a secure Flask secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Run the Application

```bash
python app.py
```

The application will start on [http://localhost:5000](http://localhost:5000)

### 6. Test the Application

1. Visit `http://localhost:5000` in your browser
2. You should be redirected to Microsoft login
3. After successful authentication, you'll see the dashboard home page
4. Navigate to Pipeline to see scheduled job status

## Application Structure

```
foundation-dashboard/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── Procfile                        # Heroku process configuration
├── runtime.txt                     # Python version specification
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore patterns
├── README.md                       # This file
└── templates/
    └── dashboard/
        ├── home.html               # Dashboard home page
        ├── pipeline.html           # Pipeline status page
        ├── placeholder.html        # Template for coming soon pages
        └── error.html              # Error page template
```

## Available Routes

| Route | Description | Authentication |
|-------|-------------|----------------|
| `/` | Dashboard home page | Required |
| `/pipeline` | Pipeline job status | Required |
| `/reports` | Financial reports (placeholder) | Required |
| `/receipts` | Receipt management (placeholder) | Required |
| `/budgets` | Budget tracking (placeholder) | Required |
| `/auth/login` | Microsoft login | Public |
| `/auth/callback` | OAuth callback | Public |
| `/auth/logout` | Logout | Public |

## Deployment to Heroku

### 1. Create Heroku Application

```bash
heroku create your-app-name
```

### 2. Set Environment Variables

```bash
heroku config:set MS_CLIENT_ID=your-client-id
heroku config:set MS_CLIENT_SECRET=your-client-secret
heroku config:set MS_TENANT_ID=your-tenant-id
heroku config:set REDIRECT_URI=https://your-app-name.herokuapp.com/auth/callback
heroku config:set FLASK_SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production
```

### 3. Update Azure AD Redirect URI

Add the production redirect URI to your Azure AD app registration:
```
https://your-app-name.herokuapp.com/auth/callback
```

### 4. Deploy Application

```bash
git push heroku main
```

### 5. Open Application

```bash
heroku open
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `MS_CLIENT_ID` | Azure AD application client ID | Yes | - |
| `MS_CLIENT_SECRET` | Azure AD application client secret | Yes | - |
| `MS_TENANT_ID` | Azure AD tenant ID | Yes | - |
| `REDIRECT_URI` | OAuth callback URL | Yes | `http://localhost:5000/auth/callback` |
| `FLASK_SECRET_KEY` | Flask session secret key | Yes | - |
| `FLASK_ENV` | Environment (development/production) | No | `development` |
| `PORT` | Application port | No | `5000` |

### Foundation Package

The application uses the `foundation` package (v0.1.0) which provides:
- **Authentication**: `MicrosoftAuth` class and `@login_required` decorator
- **Database Clients**: Connection managers for various databases
- **UI Templates**: `base.html` with navigation, styling, and common layouts
- **Static Assets**: CSS, JavaScript, and UI components

To update the foundation package version, modify `requirements.txt`:
```
# Use a specific version tag
git+https://github.com/bb723/foundation.git@v0.1.0

# Or use the latest development version from main branch
git+https://github.com/bb723/foundation.git@main
```

You can also use `requirements-dev.txt` for development with the latest main branch:
```bash
pip install -r requirements-dev.txt
```

## Development

### Adding New Routes

1. Add route handler in [app.py](app.py):
```python
@app.route('/new-feature')
@login_required
def new_feature():
    return render_template('dashboard/new_feature.html')
```

2. Create template in `templates/dashboard/new_feature.html`:
```html
{% extends "base.html" %}
{% block title %}New Feature{% endblock %}
{% block content %}
<!-- Your content here -->
{% endblock %}
```

3. Add navigation link (foundation's base.html handles sidebar navigation)

### Styling and CSS

The application uses foundation's base templates which include:
- Bootstrap 5 CSS framework
- Custom CSS from foundation package
- Bootstrap Icons

Use Bootstrap classes and foundation's custom classes in your templates:
```html
<div class="card">
    <div class="card-body">
        <button class="btn btn-primary">Action</button>
    </div>
</div>
```

### Testing Locally

```bash
# Run with debug mode
export FLASK_ENV=development  # or set in .env
python app.py

# Run with production settings
export FLASK_ENV=production
gunicorn app:app
```

## Troubleshooting

### Authentication Issues

**Problem**: Redirecting to login repeatedly
- **Solution**: Check that `FLASK_SECRET_KEY` is set and consistent
- **Solution**: Verify Azure AD redirect URI matches your configuration

**Problem**: "Invalid client secret" error
- **Solution**: Regenerate client secret in Azure AD and update `.env`

### Installation Issues

**Problem**: Can't install foundation package
- **Solution**: Ensure Git is installed and accessible in your PATH
- **Solution**: Verify you have access to the foundation repository

**Problem**: Module not found errors
- **Solution**: Activate virtual environment: `source venv/bin/activate`
- **Solution**: Reinstall dependencies: `pip install -r requirements.txt`

### Deployment Issues

**Problem**: Heroku build fails
- **Solution**: Check that `runtime.txt` matches a supported Python version
- **Solution**: Verify all dependencies in `requirements.txt` are valid

**Problem**: Application crashes on Heroku
- **Solution**: Check logs: `heroku logs --tail`
- **Solution**: Verify all environment variables are set: `heroku config`

## Contributing

1. Create a feature branch: `git checkout -b feature-name`
2. Make your changes
3. Test locally
4. Commit with clear messages
5. Push and create a pull request

## License

[Your license here]

## Support

For issues related to:
- **This dashboard**: Open an issue in this repository
- **Foundation package**: Open an issue in the [foundation repository](https://github.com/bb723/foundation)
- **Azure AD**: Consult [Microsoft Azure documentation](https://docs.microsoft.com/azure)

## Roadmap

- [ ] Implement real-time pipeline monitoring
- [ ] Add financial reports functionality
- [ ] Build receipt processing system
- [ ] Create budget tracking features
- [ ] Add user management and permissions
- [ ] Implement audit logging
- [ ] Add API endpoints for external integrations
