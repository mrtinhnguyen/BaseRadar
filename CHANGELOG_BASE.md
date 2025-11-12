# BaseRadar - Changelog & Updates

## 🎯 Project Overview

BaseRadar is a specialized news aggregator focused on the Base blockchain ecosystem. It monitors 15+ crypto news platforms and filters content specifically related to Base chain, Coinbase L2, and Superchain.

## 📋 What's New

### Supported Platforms (15 Total)

#### General Crypto News (8 platforms)
1. **CoinDesk** - In-depth analysis on Bitcoin, Ethereum, DeFi, Web3
2. **Cointelegraph** - Fast updates (filtered for Base content)
3. **Decrypt** - Web3, blockchain, crypto content
4. **BeInCrypto** - Crypto and Web3 news
5. **CoinGape** - Fast news + analysis
6. **Cryptonews** - Diverse crypto news
7. **The Block** - Data-driven analysis
8. **Coinpedia** - News + guides

#### Base-Focused Platforms (7 platforms)
9. **Base Blog** - Official Base blog (base.org/blog)
10. **Mirror.xyz** - Base projects on Mirror
11. **Base Mirror** - Base's Mirror blog (base.mirror.xyz)
12. **DeFiLlama News** - DeFi data on Base
13. **Messari** - Research on Base, Optimism
14. **Airdrops.io** - Base airdrop updates
15. **CryptoSlate** - Filtered by Base blockchain

### Key Features

- ✅ **Custom Crawlers** - Dedicated crawlers for each platform
- ✅ **Base Filtering** - Smart filtering for Base-related content
- ✅ **RSS & Web Scraping** - Multiple data sources
- ✅ **Telegram & Email** - Notification support
- ✅ **Three Report Modes** - Daily, Current, Incremental
- ✅ **MCP Server** - AI-powered analysis

## 📁 New Files

### Documentation
- `README.md` - Main documentation (English)
- `DEPLOYMENT.md` - Deployment guide
- `LOCAL_SETUP.md` - Local development guide
- `QUICK_START.md` - Quick start guide
- `CHANGELOG_BASE.md` - This file

### Code
- `crawlers.py` - All platform crawlers
- `api/index.py` - Vercel serverless function
- `vercel.json` - Vercel configuration

## 🔧 Configuration Updates

### config.yaml Changes

**Removed:**
- Old Chinese news platforms (toutiao, baidu, weibo, etc.)
- Feishu, DingTalk, WeWork, ntfy webhooks

**Added:**
- 15 crypto/Base platforms
- Telegram and Email only

**Example:**
```yaml
platforms:
  - id: "base-blog"
    name: "Base Blog"
  - id: "cointelegraph"
    name: "Cointelegraph"
  # ... 13 more platforms
```

## 🚀 Deployment Options

### 1. Vercel (Recommended for Quick Deploy)

**Files:**
- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function

**Steps:**
1. Install Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel --prod`
4. Set environment variables in Vercel dashboard
5. Setup cron job (Vercel Pro) or external cron service

See [DEPLOYMENT.md](DEPLOYMENT.md) for details.

### 2. Docker

**Files:**
- `docker/Dockerfile` - Docker image
- `docker/docker-compose.yml` - Compose configuration

**Steps:**
```bash
cd docker
docker-compose up -d
```

### 3. GitHub Actions

**Files:**
- `.github/workflows/crawler.yml` - Workflow configuration

**Steps:**
1. Add secrets to GitHub repository
2. Enable GitHub Actions
3. Workflow runs automatically on schedule

### 4. Local Server

**Files:**
- `setup-windows.bat` - Windows setup
- `setup-mac.sh` - Mac/Linux setup

**Steps:**
```bash
# Windows
setup-windows.bat
python main.py

# Mac/Linux
./setup-mac.sh
python main.py
```

## 📝 Usage Examples

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Configure
# Edit config/config.yaml
# Edit config/frequency_words.txt

# Run
python main.py
```

### Test Individual Crawler

```python
from crawlers import crawl_platform

# Test Base Blog
result = crawl_platform("base-blog")
print(result)
```

### Configure Keywords

Edit `config/frequency_words.txt`:
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

## 🔍 How It Works

1. **Crawlers** (`crawlers.py`)
   - Each platform has a dedicated crawler class
   - Uses RSS feeds or web scraping
   - Filters for Base-related content

2. **Data Fetcher** (`main.py`)
   - Detects platform type
   - Routes to appropriate crawler
   - Formats data consistently

3. **Analysis** (`main.py`)
   - Filters by keywords
   - Generates HTML reports
   - Sends notifications

4. **MCP Server** (`mcp_server/`)
   - AI-powered analysis
   - Query historical data
   - Trend analysis

## 🛠️ Development

### Adding New Platform

1. **Create crawler** in `crawlers.py`:
```python
class NewPlatformCrawler(BaseCrawler):
    def crawl(self) -> List[Dict]:
        # Implementation
        return items
```

2. **Register** in `CRAWLERS` dict:
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

## 📚 Documentation Structure

- **README.md** - Main documentation (English)
- **readme.md** - Original documentation (Chinese)
- **DEPLOYMENT.md** - Deployment guides
- **LOCAL_SETUP.md** - Local development
- **QUICK_START.md** - Quick start
- **README-Cherry-Studio.md** - MCP server setup

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**
   - Solution: `pip install -r requirements.txt`

2. **Crawler failures**
   - Check internet connection
   - Verify platform URLs
   - Review logs

3. **Notification not working**
   - Verify credentials
   - Check `enable_notification: true`
   - Test manually

4. **Vercel deployment**
   - Check `vercel.json` configuration
   - Verify environment variables
   - Review function logs

## 📞 Support

- GitHub Issues
- Check documentation
- Review logs for errors

## 🎯 Next Steps

1. **Configure** - Edit `config/config.yaml`
2. **Test** - Run `python main.py`
3. **Deploy** - Choose deployment option
4. **Monitor** - Check notifications and reports

---

**BaseRadar** - Track Base ecosystem news automatically! 🚀

