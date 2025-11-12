# Deployment Guide

This guide covers different deployment options for BaseRadar, including both the main crawler application and the MCP Server.

## Table of Contents

- [Vercel Deployment](#vercel-deployment)
  - [Main Application](#main-application-deployment)
  - [MCP Server](#mcp-server-deployment)
- [Docker Deployment](#docker-deployment)
- [GitHub Actions](#github-actions)
- [Local Server](#local-server)

## Vercel Deployment

### Prerequisites

- Vercel account (free tier available)
- Vercel CLI installed: `npm i -g vercel`
- GitHub repository (optional, for automatic deployments)

### Main Application Deployment

#### 1. Prepare Project Structure

Ensure you have:
- `vercel.json` in project root
- `api/index.py` for serverless function
- `requirements.txt` with all dependencies

#### 2. Install Vercel CLI

```bash
npm install -g vercel
```

#### 3. Login to Vercel

```bash
vercel login
```

#### 4. Configure Environment Variables

Set environment variables in Vercel dashboard or via CLI:

```bash
# Via CLI
vercel env add TELEGRAM_BOT_TOKEN
vercel env add TELEGRAM_CHAT_ID
vercel env add EMAIL_FROM
vercel env add EMAIL_PASSWORD
vercel env add EMAIL_TO

# Or set in Vercel Dashboard:
# Project Settings > Environment Variables
```

Required variables:
- `TELEGRAM_BOT_TOKEN` (if using Telegram)
- `TELEGRAM_CHAT_ID` (if using Telegram)
- `EMAIL_FROM` (if using Email)
- `EMAIL_PASSWORD` (if using Email)
- `EMAIL_TO` (if using Email)

#### 5. Deploy

```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

#### 6. Setup Cron Job

Vercel Pro plan includes cron jobs. For free tier, use external cron service.

**Option A: Vercel Cron (Pro plan)**

The `vercel.json` already includes cron configuration:
```json
{
  "crons": [{
    "path": "/api",
    "schedule": "0 * * * *"
  }]
}
```

This runs every hour at minute 0.

**Option B: External Cron Service (Free tier)**

Use services like:
- [cron-job.org](https://cron-job.org)
- [EasyCron](https://www.easycron.com)
- [UptimeRobot](https://uptimerobot.com)

Set URL: `https://your-project.vercel.app/api`
Set schedule: Every hour (or as needed)

#### 7. Verify Deployment

1. Check Vercel dashboard for deployment status
2. Test the endpoint: `https://your-project.vercel.app/api`
3. Check function logs in Vercel dashboard
4. Verify notifications are received

### MCP Server Deployment

**Important Note**: MCP Server deployment on Vercel has limitations:

1. **STDIO Mode**: Not supported on Vercel (requires persistent process)
2. **HTTP Mode**: Partially supported, but with limitations:
   - Vercel serverless functions are stateless
   - FastMCP HTTP mode expects a persistent server
   - Full MCP protocol support requires a dedicated HTTP server

#### Option 1: Deploy MCP Server Endpoint (Basic)

The project includes `api/mcp.py` which provides a basic HTTP endpoint for MCP Server:

```bash
# The endpoint will be available at:
https://your-project.vercel.app/api/mcp
```

**Limitations:**
- This is a simplified adapter
- Full MCP protocol features may not work
- Best for health checks and basic connectivity

#### Option 2: Deploy as Standalone HTTP Service (Recommended)

For production MCP Server deployment, consider:

1. **Railway** (Recommended):
   ```bash
   # Install Railway CLI
   npm i -g @railway/cli
   
   # Login
   railway login
   
   # Deploy
   railway init
   railway up
   ```

2. **Render**:
   - Create a Web Service
   - Build command: `pip install -r requirements.txt`
   - Start command: `python -m mcp_server.server --transport http --port $PORT`

3. **Fly.io**:
   ```bash
   # Install flyctl
   curl -L https://fly.io/install.sh | sh
   
   # Launch
   fly launch
   ```

4. **Self-hosted VPS**:
   ```bash
   # Run MCP Server as HTTP service
   python -m mcp_server.server --transport http --port 3333
   
   # Or use systemd service (see Local Server section)
   ```

#### MCP Server HTTP Mode Configuration

For standalone deployment, use HTTP transport:

```bash
# Run MCP Server in HTTP mode
python -m mcp_server.server --transport http --port 3333

# Or with custom host
python -m mcp_server.server --transport http --host 0.0.0.0 --port 3333
```

**MCP Client Configuration (HTTP Mode):**

For MCP clients that support HTTP transport:

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

**Note**: Most MCP clients (Claude Desktop, Cline) use STDIO mode. For HTTP mode, you may need:
- Custom MCP client that supports HTTP
- Or use STDIO mode locally and deploy data/API endpoints separately

### Troubleshooting Vercel

**Issue: Function timeout**
- Vercel free tier has 10s timeout for Hobby, 60s for Pro
- Optimize crawler to complete faster
- Consider using background jobs

**Issue: Import errors**
- Ensure all dependencies are in `requirements.txt`
- Check Python version (3.10+)
- Review Vercel build logs

**Issue: File not found**
- Ensure `api/index.py` exists
- Check `vercel.json` routes configuration
- Verify project structure

**Issue: MCP Server not working on Vercel**
- MCP Server requires persistent connection (not ideal for serverless)
- Consider deploying MCP Server separately (Railway, Render, Fly.io)
- Use Vercel endpoint only for health checks

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t baseradar -f docker/Dockerfile .

# Run container
docker run -d \
  --name baseradar \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/output:/app/output \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e TELEGRAM_CHAT_ID=your_chat_id \
  baseradar
```

### Using Docker Compose

```bash
cd docker
docker-compose up -d
```

### Docker Configuration

Edit `docker/docker-compose.yml`:

```yaml
version: '3.8'

services:
  baseradar:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    volumes:
      - ../config:/app/config
      - ../output:/app/output
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}
    restart: unless-stopped
```

## GitHub Actions

### Setup

1. **Add Secrets** to GitHub repository:
   - Go to: Settings > Secrets and variables > Actions
   - Add required secrets:
     - `TELEGRAM_BOT_TOKEN`
     - `TELEGRAM_CHAT_ID`
     - `EMAIL_FROM`
     - `EMAIL_PASSWORD`
     - `EMAIL_TO`

2. **Workflow File**

The workflow is already configured in `.github/workflows/crawler.yml`.

3. **Enable Actions**

- Go to repository Settings > Actions > General
- Enable "Allow all actions and reusable workflows"

### Schedule Configuration

Edit `.github/workflows/crawler.yml` to change schedule:

```yaml
on:
  schedule:
    - cron: '0 * * * *'  # Every hour
    # - cron: '0 */6 * * *'  # Every 6 hours
    # - cron: '0 9,18 * * *'  # 9 AM and 6 PM daily
```

### Manual Trigger

You can also trigger manually:
- Go to Actions tab
- Select "Crawler" workflow
- Click "Run workflow"

## Local Server

### Run as Service

**Linux (systemd):**

Create `/etc/systemd/system/baseradar.service`:

```ini
[Unit]
Description=BaseRadar News Crawler
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/BaseRadar
ExecStart=/usr/bin/python3 /path/to/BaseRadar/main.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable baseradar
sudo systemctl start baseradar
```

**Windows (Task Scheduler):**

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily/hourly)
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\BaseRadar\main.py`
7. Start in: `C:\path\to\BaseRadar`

### Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add line (runs every hour)
0 * * * * cd /path/to/BaseRadar && /usr/bin/python3 main.py >> /var/log/baseradar.log 2>&1
```

## Comparison of Deployment Options

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **Vercel** | Free tier, easy setup, automatic HTTPS | 10s timeout (free), serverless limitations | Quick deployment, low traffic |
| **Docker** | Full control, no timeout, portable | Requires server management | Self-hosted, high reliability |
| **GitHub Actions** | Free, integrated with repo | Limited execution time, rate limits | Automated, scheduled runs |
| **Local Server** | Full control, no external dependencies | Requires always-on server | Internal use, high frequency |

## Monitoring

### Check Logs

**Vercel:**
- Dashboard > Functions > View logs

**Docker:**
```bash
docker logs baseradar
docker logs -f baseradar  # Follow logs
```

**GitHub Actions:**
- Actions tab > Select workflow run > View logs

### Health Checks

Create a simple health check endpoint:

```python
# api/health.py
def handler(request):
    return {
        "statusCode": 200,
        "body": json.dumps({"status": "healthy"})
    }
```

Access: `https://your-project.vercel.app/api/health`

## Best Practices

1. **Environment Variables**: Never commit secrets to repository
2. **Error Handling**: Monitor logs regularly
3. **Rate Limiting**: Respect platform rate limits
4. **Backup**: Keep config files backed up
5. **Testing**: Test locally before deploying
6. **Monitoring**: Set up alerts for failures

## Support

For deployment issues:
- Check logs for specific errors
- Review configuration files
- Test locally first
- Open GitHub issue with error details

