# Fix Vercel UV Lock File Issue

## Problem

Vercel is trying to use `uv.lock` file when it detects `pyproject.toml`, but the lock file doesn't exist or causes errors.

**Note**: `.vercelignore` only works for production deployments, NOT for `vercel dev` local testing.

## Solution

### For Local Development (`vercel dev`)

**Option A: Use PowerShell Scripts (Recommended)**

1. **Before running `vercel dev`**, run:
   ```powershell
   .\vercel-dev-setup.ps1
   ```

2. **Run `vercel dev`**:
   ```powershell
   vercel dev
   ```

3. **After testing**, restore `pyproject.toml`:
   ```powershell
   .\vercel-dev-restore.ps1
   ```

**Option B: Manual Rename**

1. **Rename `pyproject.toml`**:
   ```powershell
   Rename-Item pyproject.toml pyproject.toml.hidden
   ```

2. **Run `vercel dev`**

3. **Restore after testing**:
   ```powershell
   Rename-Item pyproject.toml.hidden pyproject.toml
   ```

### For Production Deployment

**`.vercelignore` is automatically applied:**

- ✅ `pyproject.toml` is ignored in production builds
- ✅ `uv.lock` is ignored
- ✅ Vercel will use `requirements.txt` automatically

**No action needed for production!**

## Current Configuration

- ✅ `requirements.txt` exists with all dependencies
- ✅ `pyproject.toml` added to `.vercelignore` (production only)
- ✅ `uv.lock` added to `.vercelignore`
- ✅ Helper scripts created for local dev

## Testing

### Local (`vercel dev`):
1. Run `.\vercel-dev-setup.ps1`
2. Run `vercel dev`
3. Should see: "Installing required dependencies from requirements.txt"
4. After testing, run `.\vercel-dev-restore.ps1`

### Production:
- Check Vercel build logs
- Should see: "Installing required dependencies from requirements.txt"
- Should NOT see: "Installing required dependencies from uv.lock"

## Why This Happens

- **`.vercelignore`** only applies to production deployments
- **`vercel dev`** runs locally and reads all files in project
- **Solution**: Temporarily hide `pyproject.toml` for local testing

## Important: Do NOT Create uv.lock

**Do not run `uv lock`** - This will create a `uv.lock` file that Vercel will try to use, causing errors.

If you accidentally created `uv.lock`:
1. **Delete it**: `Remove-Item uv.lock`
2. **Add to `.gitignore`**: `uv.lock` (already added)
3. **Vercel will use `requirements.txt` instead**

## If Still Having Issues

1. **For local dev**: Use the setup script to hide `pyproject.toml`
2. **For production**: Check that `.vercelignore` includes `pyproject.toml`
3. **Verify** `requirements.txt` is in repository root
4. **Check build logs** in Vercel dashboard
5. **Ensure** `uv.lock` does NOT exist (delete if found)

