# Get Started - Foundation Dashboard

## 🚀 Quick Setup (30 seconds)

### Option 1: One Script Does Everything (Recommended)

```powershell
.\START-HERE.ps1
```

That's it! This will:
1. ✅ Create virtual environment
2. ✅ Install all dependencies
3. ✅ Configure .env with your credentials
4. ✅ Verify everything works

Then run:
```powershell
python app.py
```

Visit: **http://localhost:5000**

---

## Option 2: Step by Step

If you prefer to see each step:

```powershell
# 1. Setup virtual environment
.\setup-venv.ps1

# 2. Configure credentials
.\set-local-env.ps1

# 3. Run!
python app.py
```

---

## Option 3: Manual Commands

```powershell
# Create and activate venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies (note the -r flag!)
pip install -r requirements.txt

# Create .env
.\set-local-env.ps1

# Run
python app.py
```

---

## ⚠️ Common Issues

### "ModuleNotFoundError: No module named 'foundation'"

You forgot to install dependencies or venv isn't activated:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "pip install requirements.txt" error

You're missing the `-r` flag:
```powershell
pip install -r requirements.txt  # ✅ Correct
pip install requirements.txt     # ❌ Wrong
```

### Need help?

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

---

## 📁 Important Files

| File | What It Does |
|------|--------------|
| **START-HERE.ps1** | Complete automated setup (run this first!) |
| **app.py** | Main Flask application |
| **.env** | Your local credentials (created by scripts) |
| **TROUBLESHOOTING.md** | Solutions to common issues |
| **QUICKSTART.md** | Detailed setup guide |
| **README.md** | Complete documentation |

---

## ✅ Verify Setup

```powershell
python setup_check.py
```

Should show: "✓ All checks passed!"

---

## 🎯 Next Steps

Once running:
1. Login with Microsoft account
2. Explore the dashboard
3. Check Pipeline status page
4. Start building features!

## 📚 Full Documentation

- [QUICKSTART.md](QUICKSTART.md) - Detailed setup guide
- [README.md](README.md) - Complete documentation
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problem solutions
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Architecture

---

**Having issues?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or run `python setup_check.py` to diagnose problems.
