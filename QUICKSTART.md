# Quick Start Guide

Get the Foundation Dashboard running in 5 minutes!

## Prerequisites

- Python 3.10+ installed
- Git installed
- PowerShell (for Windows setup scripts)
- Microsoft Azure AD credentials (already configured in _scripts folder)

## Automated Setup (Recommended for Windows)

### One-Command Setup

Run this PowerShell script to set everything up automatically:

```powershell
.\setup-venv.ps1
```

This script will:
1. Create a virtual environment (`venv/`)
2. Install all dependencies from `requirements.txt`
3. Copy `.env.example` to `.env`
4. Run setup verification

Then configure your environment:

```powershell
.\set-local-env.ps1
```

This will populate `.env` with your Microsoft Azure AD credentials from the shared `_scripts` configuration.

### That's it! Now run:

```powershell
# Activate virtual environment (if not already active)
.\venv\Scripts\Activate.ps1

# Run the app
python app.py
```

Visit [http://localhost:5000](http://localhost:5000)

---

## Manual Setup (All Platforms)

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
venv\Scripts\activate.bat

# macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs Flask, gunicorn, and the foundation package from GitHub.

### Step 3: Configure Environment

**Option A: Use PowerShell script (Windows)**
```powershell
.\set-local-env.ps1
```
This automatically populates `.env` with credentials from `_scripts/set-config.ps1`.

**Option B: Manual configuration**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your favorite text editor
# Add your Microsoft Azure AD credentials
```

Your `.env` should look like:
```env
MS_CLIENT_ID=your-actual-client-id
MS_CLIENT_SECRET=your-actual-client-secret
MS_TENANT_ID=your-actual-tenant-id
REDIRECT_URI=http://localhost:5000/auth/callback
FLASK_SECRET_KEY=generate-a-random-key
FLASK_ENV=development
```

### Getting Azure AD Credentials

**If using shared credentials**: Your Microsoft credentials are already in `../_scripts/set-config.ps1`. Use the automated setup script or copy them from there.

**If setting up new credentials**:

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Create or select your application
4. Copy the **Application (client) ID** → This is your `MS_CLIENT_ID`
5. Copy the **Directory (tenant) ID** → This is your `MS_TENANT_ID`
6. Go to **Certificates & secrets** → **New client secret**
   - Description: "Local development"
   - Copy the secret value → This is your `MS_CLIENT_SECRET`
7. Add redirect URI: `http://localhost:5000/auth/callback`

### Generate Flask Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output to `FLASK_SECRET_KEY` in your `.env` file.

## Step 4: Verify Setup

```bash
python setup_check.py
```

This will check that all files and configurations are correct.

## Step 5: Run the Application

```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

## Step 6: Test in Browser

1. Open [http://localhost:5000](http://localhost:5000)
2. You'll be redirected to Microsoft login
3. Login with your Microsoft account
4. You should see the dashboard home page
5. Try navigating to **Pipeline** to see job status

## What You Should See

### Dashboard Home
- Welcome message
- Four system status cards (Pipeline, Reports, Receipts, Budgets)
- Quick statistics section
- Recent activity list

### Pipeline Page
- Overview cards showing job counts
- Table of scheduled jobs with status
- Recent job history
- System information

## PowerShell Scripts Reference

| Script | Purpose |
|--------|---------|
| `setup-venv.ps1` | Creates virtual environment and installs dependencies |
| `set-local-env.ps1` | Populates .env with shared credentials for local dev |
| `set-dashboard-config.ps1` | Sets Heroku config vars for deployment |

## Troubleshooting

### "Cannot import name 'MicrosoftAuth'"
**Problem**: Foundation package not installed correctly

**Solution**:
```bash
pip install --force-reinstall -r requirements.txt
```

### Redirect Loop on Login
**Problem**: Session not working correctly

**Solution**: Make sure `FLASK_SECRET_KEY` is set in `.env`

### "Invalid redirect_uri"
**Problem**: Azure AD redirect URI doesn't match

**Solution**:
1. Check that `REDIRECT_URI` in `.env` is `http://localhost:5000/auth/callback`
2. Verify this URI is added in Azure AD app registration

### Port Already in Use
**Problem**: Another app is using port 5000

**Solution**: Change port in `.env`:
```env
PORT=5001
```

Then update Azure AD redirect URI to `http://localhost:5001/auth/callback`

### PowerShell Script Execution Policy Error

If you get an error about script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Virtual Environment Notes

**Always activate the virtual environment before working:**
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

**To deactivate:**
```bash
deactivate
```

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents conflicts with system Python packages
- Makes deployment easier
- Allows different Python versions per project

## Deployment to Heroku

### Quick Deploy

```powershell
# Create Heroku app
heroku create your-app-name

# Configure with PowerShell script (uses shared credentials)
.\set-dashboard-config.ps1 -AppName your-app-name

# Deploy
git push heroku main

# Open app
heroku open
```

The `set-dashboard-config.ps1` script will:
- Set Microsoft Azure AD credentials (from _scripts)
- Configure Flask for production
- Generate secure secret key
- Set proper redirect URI for your Heroku app
- Optionally include Snowflake/QuickBooks credentials

**Don't forget**: Add the production redirect URI to your Azure AD app registration:
```
https://your-app-name.herokuapp.com/auth/callback
```

## Next Steps

### For Local Development
- Modify [app.py](app.py) to add new routes
- Create new templates in `templates/dashboard/`
- Install additional packages and add to `requirements.txt`
- Always work in the virtual environment

### For Production
- Use `set-dashboard-config.ps1` for Heroku deployment
- See [README.md](README.md) for detailed deployment instructions

## Common Commands

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start the app
python app.py

# Check setup
python setup_check.py

# Install/update dependencies
pip install -r requirements.txt

# Deactivate virtual environment
deactivate
```

## Getting Help

1. Check [README.md](README.md) for detailed documentation
2. Check [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture overview
3. Review error messages carefully - they usually tell you what's wrong
4. Check that all environment variables are set correctly
5. Make sure virtual environment is activated

## Success Indicators

You're all set when:
- ✓ Virtual environment created and activated
- ✓ `python setup_check.py` shows all checks passed
- ✓ `python app.py` starts without errors
- ✓ Browser shows Microsoft login page
- ✓ After login, you see the dashboard home page
- ✓ Navigation links work (Pipeline, Reports, etc.)

Happy coding!
