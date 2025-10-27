# Troubleshooting Guide

## Common Setup Issues

### "ModuleNotFoundError: No module named 'foundation'"

**Problem**: Dependencies not installed in virtual environment

**Solution**:
```powershell
# Make sure venv is activated (you should see (venv) in prompt)
.\venv\Scripts\Activate.ps1

# Install dependencies with -r flag
pip install -r requirements.txt
```

**Why this happens**: The `-r` flag tells pip to read from a requirements file. Without it, pip tries to install a package literally named "requirements.txt".

---

### ".env file not found"

**Problem**: Environment configuration file doesn't exist

**Solution** (Automated):
```powershell
.\set-local-env.ps1
```

**Solution** (Manual):
```powershell
cp .env.example .env
# Then edit .env with your credentials
```

The automated script populates it with credentials from `../_scripts/set-config.ps1`.

---

### "pip install requirements.txt" Error

**Problem**: Missing `-r` flag

**Wrong**:
```powershell
pip install requirements.txt  # ❌ Wrong!
```

**Correct**:
```powershell
pip install -r requirements.txt  # ✅ Correct!
```

---

### Virtual Environment Not Activated

**Problem**: Installing packages globally instead of in venv

**Check**: Your prompt should show `(venv)`:
```
(venv) PS C:\...\foundation-dashboard>  # ✅ Good!
PS C:\...\foundation-dashboard>         # ❌ Not activated
```

**Solution**:
```powershell
.\venv\Scripts\Activate.ps1
```

---

## Complete Fresh Setup

If you're having multiple issues, start fresh:

```powershell
# 1. Remove virtual environment if it exists
Remove-Item -Recurse -Force venv

# 2. Remove .env if it exists
Remove-Item .env

# 3. Run automated setup
.\setup-venv.ps1

# 4. Configure environment
.\set-local-env.ps1

# 5. Verify (optional but recommended)
python setup_check.py

# 6. Run the app
python app.py
```

---

## Step-by-Step Manual Setup

If scripts aren't working:

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\Activate.ps1

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies (note the -r!)
pip install -r requirements.txt

# 5. Create .env file
.\set-local-env.ps1
# OR manually copy and edit:
# cp .env.example .env

# 6. Verify setup
python setup_check.py

# 7. Run app
python app.py
```

---

## Quick Checklist

Before running `python app.py`, verify:

- [ ] Virtual environment exists: `venv/` folder present
- [ ] Virtual environment activated: `(venv)` in prompt
- [ ] Dependencies installed: `pip list | grep foundation` shows foundation
- [ ] Environment configured: `.env` file exists
- [ ] Setup verified: `python setup_check.py` passes

---

## Verification Commands

```powershell
# Check if venv is activated
Get-Command python | Select-Object Source
# Should show: ...\venv\Scripts\python.exe

# Check if foundation is installed
pip show foundation
# Should show: Name: foundation, Version: 0.1.0

# Check if .env exists
Test-Path .env
# Should show: True

# List all installed packages
pip list

# Run full setup check
python setup_check.py
```

---

## Installation Issues

### "git checkout -q v0.2.0 did not run successfully"

**Fixed!** The requirements.txt now uses `v0.1.0` which exists.

If you still see this:
```powershell
pip install -r requirements.txt --force-reinstall
```

### "Cannot install foundation package"

**Problem**: Git not accessible or GitHub connection issue

**Solution**:
1. Check Git is installed: `git --version`
2. Test GitHub access: `git ls-remote https://github.com/bb723/foundation.git`
3. Try with --no-cache: `pip install -r requirements.txt --no-cache-dir`

---

## Running the App

### Port Already in Use

If port 5000 is taken:

1. Edit `.env`:
   ```
   PORT=5001
   ```

2. Update Azure AD redirect URI to `http://localhost:5001/auth/callback`

### "Address already in use"

Find and kill the process:
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill it (replace PID with actual number)
taskkill /PID <PID> /F
```

---

## Authentication Issues

### Redirect Loop

**Problem**: Flask session not working

**Solution**: Check `.env` has `FLASK_SECRET_KEY` set:
```powershell
cat .env | Select-String "FLASK_SECRET_KEY"
```

Should show a long random string, not "your-secret-key-here".

### "Invalid redirect_uri"

**Problem**: Azure AD doesn't have your redirect URI

**Solution**: Add to Azure AD app registration:
- Local: `http://localhost:5000/auth/callback`
- Production: `https://your-app.herokuapp.com/auth/callback`

---

## PowerShell Script Issues

### "Cannot be loaded because running scripts is disabled"

**Problem**: PowerShell execution policy

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try the script again.

---

## Still Having Issues?

### Get Detailed Information

```powershell
# Python version
python --version

# Pip version
pip --version

# Virtual environment status
Get-Command python | Select-Object Source

# Installed packages
pip list

# Environment variables
cat .env
```

### Common Command Reference

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env
.\set-local-env.ps1

# Verify setup
python setup_check.py

# Run app
python app.py

# Deactivate venv
deactivate
```

---

## Getting Help

1. Run `python setup_check.py` and note which checks fail
2. Review error messages carefully
3. Check this troubleshooting guide for your specific error
4. Verify all checklist items above
5. Try the "Complete Fresh Setup" section

## Success Indicators

You're ready when:
- ✅ `(venv)` appears in your prompt
- ✅ `pip show foundation` shows version 0.1.0
- ✅ `.env` file exists and has real values
- ✅ `python setup_check.py` shows "All checks passed!"
- ✅ `python app.py` starts without errors
- ✅ Browser redirects to Microsoft login
