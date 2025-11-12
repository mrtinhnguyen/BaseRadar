# MCP Server Deployment Guide for Vercel

## Overview

This guide explains how to deploy BaseRadar MCP Server, including limitations and recommended alternatives.

## Can MCP Server be Deployed on Vercel?

**Short Answer**: Partially, but with significant limitations.

### Why Vercel is Challenging for MCP Server

1. **STDIO Mode**: Not supported
   - MCP Server STDIO mode requires a persistent process
   - Vercel serverless functions are stateless and short-lived
   - STDIO communication needs continuous stdin/stdout streams

2. **HTTP Mode**: Partially supported
   - FastMCP HTTP mode expects a persistent HTTP server
   - Vercel functions are request-response based
   - Full MCP protocol requires WebSocket or long-polling (not available on Vercel)

## Current Implementation

The project includes `api/mcp.py` which provides a basic HTTP endpoint:

```
https://your-project.vercel.app/api/mcp
```

**What it does:**
- Health check endpoint
- Basic connectivity test
- Returns server status

**What it doesn't do:**
- Full MCP protocol support
- Tool execution via HTTP
- Real-time MCP communication

## Recommended Deployment Options

### Option 1: Railway (Recommended) ⭐

Railway is ideal for MCP Server deployment:

```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Set environment variables (if needed)
railway variables set PROJECT_ROOT=/app

# 5. Deploy
railway up
```

**Create `railway.json`**:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python -m mcp_server.server --transport http --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Pricing**: Free tier available, $5/month for hobby

### Option 2: Render

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m mcp_server.server --transport http --port $PORT`
   - **Environment**: Python 3
5. Deploy

**Pricing**: Free tier available (spins down after inactivity)

### Option 3: Fly.io

```bash
# 1. Install flyctl
curl -L https://fly.io/install.sh | sh

# 2. Login
fly auth login

# 3. Launch app
fly launch

# 4. Set secrets (if needed)
fly secrets set PROJECT_ROOT=/app

# 5. Deploy
fly deploy
```

**Create `fly.toml`**:
```toml
app = "baseradar-mcp"
primary_region = "iad"

[build]

[env]
  PORT = "8080"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

**Pricing**: Free tier available

### Option 4: Self-Hosted VPS

For full control and best performance:

```bash
# 1. SSH into your VPS
ssh user@your-server

# 2. Clone repository
git clone https://github.com/your-username/BaseRadar.git
cd BaseRadar

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run MCP Server
python -m mcp_server.server --transport http --port 3333
```

**Use systemd for auto-start**:

Create `/etc/systemd/system/baseradar-mcp.service`:

```ini
[Unit]
Description=BaseRadar MCP Server
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/BaseRadar
ExecStart=/usr/bin/python3 -m mcp_server.server --transport http --port 3333
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable baseradar-mcp
sudo systemctl start baseradar-mcp
```

## MCP Client Configuration

### For STDIO Mode (Local)

Most MCP clients use STDIO mode. Configure in your MCP client:

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "baseradar": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/BaseRadar",
        "run",
        "python",
        "mcp_server/server.py"
      ]
    }
  }
}
```

**Cline**:
```json
{
  "mcpServers": {
    "baseradar": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/BaseRadar"
    }
  }
}
```

### For HTTP Mode (Remote)

If your MCP client supports HTTP transport:

```json
{
  "mcpServers": {
    "baseradar": {
      "url": "http://your-server:3333/mcp",
      "transport": "http"
    }
  }
}
```

**Note**: Most MCP clients don't support HTTP transport yet. STDIO is the standard.

## Hybrid Approach (Recommended)

Deploy different components separately:

1. **Main Crawler**: Deploy on Vercel
   - Runs scheduled crawls
   - Sends notifications
   - Generates reports

2. **MCP Server**: Deploy on Railway/Render/Fly.io
   - Provides MCP tools
   - Accesses crawled data
   - Can be used by MCP clients

3. **Data Storage**: Shared
   - Both services access same data directory
   - Use shared storage (S3, etc.) or sync

## Testing MCP Server Deployment

### Health Check

```bash
# Test HTTP endpoint
curl https://your-mcp-server.railway.app/mcp

# Expected response:
{
  "status": "online",
  "service": "BaseRadar MCP Server",
  "transport": "http"
}
```

### Test MCP Tools

Use an MCP client or test directly:

```bash
# Example: Test get_latest_news tool
curl -X POST https://your-mcp-server.railway.app/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "get_latest_news",
      "arguments": {
        "limit": 10
      }
    }
  }'
```

## Troubleshooting

### Issue: MCP Server not starting

**Check logs**:
```bash
# Railway
railway logs

# Render
# Check logs in dashboard

# Fly.io
fly logs
```

### Issue: Connection refused

- Check firewall settings
- Verify port is exposed
- Check service is running

### Issue: Import errors

- Ensure all dependencies in `requirements.txt`
- Check Python version (3.10+)
- Verify project structure

## Summary

| Platform | STDIO Support | HTTP Support | Best For |
|----------|---------------|--------------|----------|
| **Vercel** | ❌ No | ⚠️ Limited | Main crawler only |
| **Railway** | ✅ Yes | ✅ Yes | MCP Server (recommended) |
| **Render** | ✅ Yes | ✅ Yes | MCP Server |
| **Fly.io** | ✅ Yes | ✅ Yes | MCP Server |
| **VPS** | ✅ Yes | ✅ Yes | Full control |

## Next Steps

1. **For Main App**: Deploy to Vercel (already configured)
2. **For MCP Server**: Choose Railway/Render/Fly.io
3. **Configure MCP Client**: Use STDIO mode with local/remote server
4. **Test**: Verify both services work correctly

For more details, see [README-MCP.md](./README-MCP.md)

