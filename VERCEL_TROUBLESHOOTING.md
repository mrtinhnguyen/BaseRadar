# Vercel Deployment Troubleshooting

## Common Issues

### 1. Python Process Exited with Status 1

**Symptoms:**
- `[fatal] Python process exited with exit status: 1`
- Serverless Function has crashed

**Possible Causes:**

#### A. Missing Configuration File

**Check:**
- Ensure `config/config.yaml` exists in repository
- Verify file is not in `.gitignore` or `.vercelignore`
- Check Vercel build logs for file inclusion

**Solution:**
1. Verify `config/config.yaml` is committed to git:
   ```bash
   git ls-files config/config.yaml
   ```

2. Check `.vercelignore` (if exists):
   ```bash
   cat .vercelignore
   ```
   Should NOT include `config/`

3. Ensure file structure:
   ```
   project-root/
   ├── config/
   │   ├── config.yaml
   │   └── frequency_words.txt
   ├── api/
   │   └── index.py
   └── main.py
   ```

#### B. Missing Dependencies

**Check:**
- Verify `requirements.txt` includes all dependencies
- Check Vercel build logs for pip install errors

**Solution:**
1. Review `requirements.txt`:
   ```bash
   cat requirements.txt
   ```

2. Ensure all imports are covered:
   - `requests`
   - `pytz`
   - `PyYAML`
   - `beautifulsoup4`
   - `lxml`

#### C. Import Errors

**Check:**
- Missing `crawlers.py` (optional, but may cause warnings)
- Circular imports
- Module path issues

**Solution:**
1. `crawlers.py` is optional - warnings are suppressed in Vercel
2. Check import paths in `api/index.py`
3. Verify project structure

#### D. Path Issues

**Check:**
- Project root detection
- Config file path resolution

**Solution:**
The handler sets `project_root` correctly:
```python
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

### 2. Configuration File Not Found

**Error Message:**
```json
{
  "status": "error",
  "message": "Configuration file not found at: ...",
  "type": "FileNotFoundError"
}
```

**Solution:**
1. **Verify file exists in repository:**
   ```bash
   ls -la config/config.yaml
   ```

2. **Check if file is tracked by git:**
   ```bash
   git status config/config.yaml
   ```

3. **Ensure file is not ignored:**
   - Check `.gitignore`
   - Check `.vercelignore` (if exists)

4. **Verify deployment includes config:**
   - Check Vercel build logs
   - Look for "config" directory in build output

### 3. Import Errors

**Error Message:**
```json
{
  "status": "error",
  "message": "Failed to import main module: ...",
  "type": "ImportError"
}
```

**Solution:**
1. **Check dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify all imports:**
   - `main.py` imports should work
   - Optional imports (like `crawlers`) are handled gracefully

3. **Check Python version:**
   - Vercel uses Python 3.10 (as specified in `vercel.json`)
   - Ensure code is compatible

### 4. Missing Files in Deployment

**Check:**
1. **Files must be in git repository:**
   - Vercel only deploys files tracked by git
   - Untracked files won't be deployed

2. **Check `.vercelignore`:**
   ```bash
   cat .vercelignore 2>/dev/null || echo "No .vercelignore file"
   ```

3. **Verify file structure:**
   ```
   BaseRadar/
   ├── api/
   │   └── index.py
   ├── config/
   │   ├── config.yaml
   │   └── frequency_words.txt
   ├── main.py
   ├── crawlers.py (optional)
   ├── requirements.txt
   └── vercel.json
   ```

## Debugging Steps

### Step 1: Check Vercel Logs

1. Go to Vercel Dashboard
2. Select your project
3. Go to "Functions" tab
4. Click on the failed function
5. View "Logs" tab
6. Look for detailed error messages

### Step 2: Test Locally

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Test function locally:**
   ```bash
   vercel dev
   ```

3. **Check local logs:**
   - Should show same errors as production
   - Easier to debug locally

### Step 3: Verify File Structure

1. **Check repository structure:**
   ```bash
   tree -L 2 -a
   ```

2. **Verify config files:**
   ```bash
   ls -la config/
   ```

3. **Check if files are tracked:**
   ```bash
   git ls-files | grep config
   ```

### Step 4: Test Import

1. **Test Python imports:**
   ```bash
   python -c "from main import get_config; print('OK')"
   ```

2. **Test config loading:**
   ```bash
   python -c "from main import get_config; config = get_config(); print('Config loaded:', len(config))"
   ```

## Quick Fixes

### Fix 1: Ensure Config File is Committed

```bash
# Add config file if missing
git add config/config.yaml
git commit -m "Add config file"
git push
```

### Fix 2: Create .vercelignore (if needed)

If you want to exclude certain files but NOT config:

```bash
# Create .vercelignore
cat > .vercelignore << EOF
# Exclude these but NOT config/
*.log
*.pyc
__pycache__/
.env.local
EOF
```

### Fix 3: Verify vercel.json

Ensure `vercel.json` is correct:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.10"
  }
}
```

## Windows-Specific Issues

### Issue: `AttributeError: module 'socket' has no attribute 'AF_UNIX'`

**Error Message:**
```
AttributeError: module 'socket' has no attribute 'AF_UNIX'
```

**Cause:**
- `AF_UNIX` sockets are Unix/Linux-only and not available on Windows
- Vercel's local development server (`vercel dev`) uses Unix sockets internally
- This is a limitation of running `vercel dev` on Windows

**Solutions:**

**Option 1: Use WSL (Windows Subsystem for Linux) - Recommended**
```bash
# Install WSL if not already installed
wsl --install

# In WSL, navigate to your project
cd /mnt/d/2025/Blockchain/basechain/BaseRadar

# Run vercel dev in WSL
vercel dev
```

**Option 2: Deploy to Vercel and Test Production**
- Skip local `vercel dev` testing
- Deploy directly to Vercel: `vercel --prod`
- Test on production URL
- Vercel production runs on Linux, so this works fine

**Option 3: Use Docker (if available)**
```bash
# Run in a Linux container
docker run -it -v ${PWD}:/app -w /app python:3.10 bash
# Then run vercel dev inside container
```

**Option 4: Test API Endpoints Directly**
- Use `python api/index.py` with a local HTTP server
- Or use `uvicorn` or `gunicorn` to run the API locally
- Test endpoints with `curl` or Postman

**Note:** This is a Vercel CLI limitation on Windows, not an issue with your code. Production deployments work fine.

## Getting More Information

The updated `api/index.py` now provides detailed error information:

1. **File existence check** before import
2. **Detailed error messages** with hints
3. **Traceback information** for debugging
4. **Path information** to verify file locations

Check the error response from the endpoint to see:
- Exact file path being checked
- Files in project root
- Detailed traceback

## Still Having Issues?

1. **Check Vercel build logs:**
   - Dashboard > Project > Deployments > Latest > Build Logs

2. **Check function logs:**
   - Dashboard > Project > Functions > api/index > Logs

3. **Test endpoint directly:**
   ```bash
   curl https://your-project.vercel.app/api
   ```

4. **Review error response:**
   - The JSON response now includes detailed information
   - Check `hint`, `traceback`, and `message` fields

