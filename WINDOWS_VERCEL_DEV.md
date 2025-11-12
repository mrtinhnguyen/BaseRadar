# Running Vercel Dev on Windows

## Problem

When running `vercel dev` on Windows, you may encounter:

```
AttributeError: module 'socket' has no attribute 'AF_UNIX'
```

This happens because:
- `AF_UNIX` sockets are Unix/Linux-only
- Vercel's local dev server uses Unix sockets internally
- Windows doesn't support Unix domain sockets

## Solutions

### Option 1: Use WSL (Windows Subsystem for Linux) - Recommended

**Install WSL:**
```powershell
# In PowerShell as Administrator
wsl --install
```

**Use WSL:**
```bash
# In WSL terminal
cd /mnt/d/2025/Blockchain/basechain/BaseRadar
vercel dev
```

**Benefits:**
- Full Linux environment
- All Vercel features work
- Best compatibility

### Option 2: Deploy to Vercel (Skip Local Dev)

Since production works fine, you can:

```powershell
# Deploy to preview
vercel

# Or deploy to production
vercel --prod
```

Then test on the deployed URL. This works because Vercel production runs on Linux.

**Benefits:**
- No local setup needed
- Tests actual production environment
- Fast iteration

### Option 3: Test API Directly with Python

Instead of `vercel dev`, run your API directly:

```powershell
# Install dependencies
pip install -r requirements.txt

# Run a simple test server
python -c "from api.index import handler; print('API loaded successfully')"
```

Or create a simple test script:

```python
# test_api.py
from api.index import handler

# Simulate a request
class MockRequest:
    def __init__(self):
        self.path = "/api"
        self.method = "GET"

result = handler(MockRequest())
print(result)
```

### Option 4: Use Docker (If Available)

```bash
# Run in Linux container
docker run -it -v ${PWD}:/app -w /app python:3.10 bash

# Inside container
pip install -r requirements.txt
vercel dev
```

## Recommendation

**For Windows users:**
1. **Best**: Use WSL for local development
2. **Alternative**: Deploy to Vercel and test production
3. **Quick test**: Test API code directly with Python

## Note

This is a **Vercel CLI limitation**, not an issue with your code. Your production deployments will work perfectly fine on Vercel's Linux servers.

