# Local Setup Guide

Complete guide for setting up BaseRadar on your local machine.

## Prerequisites

- **Python 3.10+** - Check version: `python --version`
- **pip** or **uv** package manager
- **Git** (for cloning repository)

## Quick Setup

### Windows

1. **Run setup script**
```bash
setup-windows.bat
```

2. **Configure**
   - Edit `config/config.yaml`
   - Edit `config/frequency_words.txt`

3. **Run**
```bash
python main.py
```

### Linux/Mac

1. **Run setup script**
```bash
chmod +x setup-mac.sh
./setup-mac.sh
```

2. **Configure**
   - Edit `config/config.yaml`
   - Edit `config/frequency_words.txt`

3. **Run**
```bash
python main.py
```

## Manual Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/BaseRadar.git
cd BaseRadar
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

**Using pip:**
```bash
pip install -r requirements.txt
```

**Using uv (faster):**
```bash
# Install uv first
pip install uv

# Install dependencies
uv sync
```

### Step 4: Configure

1. **Copy config file** (if example exists)
```bash
cp config/config.yaml.example config/config.yaml
```

2. **Edit `config/config.yaml`**

   - Set notification webhooks:
   ```yaml
   webhooks:
     telegram_bot_token: "your_bot_token"
     telegram_chat_id: "your_chat_id"
     email_from: "sender@example.com"
     email_password: "your_password"
     email_to: "recipient@example.com"
   ```

   - Configure platforms (already set for Base-focused platforms)
   - Set report mode:
   ```yaml
   report:
     mode: "daily"  # or "current" or "incremental"
   ```

3. **Edit `config/frequency_words.txt`**

   Add keywords to filter news:
   ```
   Base
   Base chain
   Coinbase L2
   Superchain
   +announcement
   
   DeFi
   Base DeFi
   +protocol
   
   airdrop
   +Base
   !scam
   ```

### Step 5: Test Run

```bash
# Single run
python main.py
```

Expected output:
```
正在加载配置...
TrendRadar v3.0.4 配置加载完成
监控平台数量: 15
开始爬取数据...
```

## Configuration Details

### config.yaml Structure

```yaml
app:
  version_check_url: "..."  # Version check URL
  show_version_update: true  # Show update notifications

crawler:
  request_interval: 1000  # Request interval in milliseconds
  enable_crawler: true  # Enable/disable crawler
  use_proxy: false  # Use proxy
  default_proxy: "http://127.0.0.1:10086"  # Proxy URL

report:
  mode: "daily"  # daily | current | incremental
  rank_threshold: 5  # Rank highlight threshold

notification:
  enable_notification: true  # Enable notifications
  message_batch_size: 4000  # Message batch size
  batch_send_interval: 3  # Batch send interval in seconds
  
  push_window:
    enabled: false  # Enable time window
    time_range:
      start: "20:00"  # Start time (Beijing time)
      end: "22:00"    # End time
    once_per_day: true  # Push once per day in window

  webhooks:
    telegram_bot_token: ""  # Telegram bot token
    telegram_chat_id: ""   # Telegram chat ID
    email_from: ""          # Email sender
    email_password: ""      # Email password
    email_to: ""           # Email recipient

weight:
  rank_weight: 0.6        # Rank weight
  frequency_weight: 0.3   # Frequency weight
  hotness_weight: 0.1     # Hotness weight

platforms:
  - id: "base-blog"
    name: "Base Blog"
  # ... more platforms
```

### frequency_words.txt Syntax

- **Normal words**: Match if any word appears
  ```
  Base
  DeFi
  ```

- **Required words** (`+word`): Must appear together
  ```
  Base
  +announcement
  ```
  Matches: "Base announces..." ✅
  Doesn't match: "Base ecosystem..." ❌

- **Excluded words** (`!word`): Exclude if appears
  ```
  Base
  !scam
  ```
  Matches: "Base launches..." ✅
  Doesn't match: "Base scam alert" ❌

- **Groups**: Separate with blank lines
  ```
  Base
  +announcement
  
  DeFi
  +protocol
  ```

## Running Options

### Single Run

```bash
python main.py
```

### Scheduled Runs

**Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (hourly/daily)
4. Action: Start program
5. Program: `python`
6. Arguments: `C:\path\to\BaseRadar\main.py`
7. Start in: `C:\path\to\BaseRadar`

**Linux Cron:**
```bash
# Edit crontab
crontab -e

# Add (runs every hour)
0 * * * * cd /path/to/BaseRadar && /usr/bin/python3 main.py
```

**Mac LaunchAgent:**
Create `~/Library/LaunchAgents/com.baseradar.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.baseradar</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/BaseRadar/main.py</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Load:
```bash
launchctl load ~/Library/LaunchAgents/com.baseradar.plist
```

## Testing

### Test Individual Crawler

```python
from crawlers import crawl_platform

# Test Base Blog crawler
result = crawl_platform("base-blog")
print(result)
```

### Test Notification

```python
from main import send_to_telegram, CONFIG

# Test Telegram
send_to_telegram(
    CONFIG["TELEGRAM_BOT_TOKEN"],
    CONFIG["TELEGRAM_CHAT_ID"],
    {"title": "Test", "content": "This is a test"},
    "test",
    None
)
```

## Troubleshooting

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.10+
```

### Crawler Failures

1. **Check internet connection**
2. **Verify platform URLs** are accessible
3. **Check logs** for specific errors
4. **Test individual crawler**:
   ```python
   from crawlers import get_crawler
   crawler = get_crawler("base-blog")
   items = crawler.crawl()
   print(items)
   ```

### Notification Not Working

1. **Verify credentials** in config.yaml
2. **Test manually**:
   ```python
   # Test Telegram
   import requests
   url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
   requests.post(url, json={"chat_id": CHAT_ID, "text": "Test"})
   ```

3. **Check notification settings**:
   ```yaml
   notification:
     enable_notification: true  # Must be true
   ```

### File Permission Issues

**Linux/Mac:**
```bash
chmod +x setup-mac.sh
chmod +x start-http.sh
```

**Windows:**
- Run as Administrator if needed
- Check file permissions in Properties

## Development

### Project Structure

```
BaseRadar/
├── api/              # Vercel serverless functions
├── config/           # Configuration files
│   ├── config.yaml   # Main config
│   └── frequency_words.txt  # Keywords
├── crawlers.py       # Platform crawlers
├── main.py           # Main entry point
├── mcp_server/       # MCP server
├── output/           # Generated reports
└── requirements.txt  # Dependencies
```

### Adding New Crawler

1. **Create crawler class** in `crawlers.py`:
```python
class NewPlatformCrawler(BaseCrawler):
    def crawl(self) -> List[Dict]:
        items = []
        # Your crawling logic
        return items
```

2. **Register in CRAWLERS**:
```python
CRAWLERS = {
    # ... existing
    "new-platform": NewPlatformCrawler,
}
```

3. **Add to config.yaml**:
```yaml
platforms:
  - id: "new-platform"
    name: "New Platform"
```

4. **Update main.py**:
```python
crypto_platforms = [
    # ... existing
    "new-platform"
]
```

## Next Steps

- [Deployment Guide](DEPLOYMENT.md) - Deploy to production
- [README](README.md) - Full documentation
- [MCP Setup](README-Cherry-Studio.md) - AI analysis setup

