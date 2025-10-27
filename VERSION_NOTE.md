# Foundation Package Version Information

## Current Setup

The project is now configured to use the **stable v0.1.0 tag** of the foundation package.

## Installation Files

### requirements.txt (Stable - Recommended)
Uses the tagged release `v0.1.0`:
```bash
pip install -r requirements.txt
```

This installs:
```
git+https://github.com/bb723/foundation.git@v0.1.0
```

### requirements-dev.txt (Development - Latest)
Uses the latest `main` branch:
```bash
pip install -r requirements-dev.txt
```

This installs:
```
git+https://github.com/bb723/foundation.git@main
```

## Which Should You Use?

### Use requirements.txt (v0.1.0) if:
- You want stability and reproducible builds
- You're deploying to production
- You want to avoid unexpected breaking changes
- This is your first time setting up the project

### Use requirements-dev.txt (main) if:
- You're actively developing new features
- You need the latest foundation package features
- You're contributing to the foundation package
- You're comfortable with potential breaking changes

## Version History

| Version | Status | Notes |
|---------|--------|-------|
| v0.1.0 | **Current** | Stable release, includes MicrosoftAuth |
| main | Latest | Development branch, may have breaking changes |

## Checking Your Installed Version

After installation, you can check which version you have:

```bash
pip show foundation
```

Look for the commit hash or tag in the version information.

## Updating Foundation Package

### To update to latest stable version:
```bash
pip install --force-reinstall -r requirements.txt
```

### To update to latest development version:
```bash
pip install --force-reinstall -r requirements-dev.txt
```

### To switch between versions:
```bash
# Switch to stable
pip uninstall foundation -y
pip install -r requirements.txt

# Switch to development
pip uninstall foundation -y
pip install -r requirements-dev.txt
```

## Troubleshooting

### Error: "pathspec 'v0.2.0' did not match any file(s)"
**Cause**: Trying to install a version tag that doesn't exist

**Solution**: The foundation repository currently only has v0.1.0. Use:
```bash
pip install -r requirements.txt  # for v0.1.0
```

### Error: "Cannot import name 'MicrosoftAuth'"
**Cause**: Foundation package not installed or incompatible version

**Solution**:
```bash
pip uninstall foundation -y
pip install -r requirements.txt
```

### Want to use a specific commit?
Edit requirements.txt and specify the commit hash:
```
git+https://github.com/bb723/foundation.git@abc1234567890
```

## Future Versions

When new versions are released (v0.2.0, v0.3.0, etc.), update requirements.txt:

```
# In requirements.txt
git+https://github.com/bb723/foundation.git@v0.2.0
```

Then reinstall:
```bash
pip install --force-reinstall -r requirements.txt
```

## Notes

- The foundation package is installed directly from GitHub
- Tags follow semantic versioning (v0.1.0, v0.2.0, etc.)
- The `main` branch always contains the latest development code
- Production deployments should always use tagged versions
