# Quick Start Guide

Get BaseRadar up and running in 5 minutes!

## 🚀 Fastest Setup (Windows)

1. **Run setup script**
   ```bash
   setup-windows.bat
   ```

2. **Configure notifications** in `config/config.yaml`:
   ```yaml
   webhooks:
     telegram_bot_token: "your_token"
     telegram_chat_id: "your_chat_id"
   ```

3. **Run**
   ```bash
   python main.py
   ```

Done! ✅

## 📦 Manual Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure

Edit `config/config.yaml`:
- Add Telegram/Email credentials
- Platforms are already configured for Base ecosystem

Edit `config/frequency_words.txt`:
```
Base
Base chain
Coinbase L2
Superchain
```

### 3. Run

```bash
python main.py
```

## 🔧 Setup Telegram Notifications

1. **Create bot**: Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot`
   - Follow instructions
   - Save the bot token

2. **Get chat ID**: Message [@userinfobot](https://t.me/userinfobot)
   - It will reply with your chat ID

3. **Add to config**:
   ```yaml
   webhooks:
     telegram_bot_token: "123456:ABC-DEF..."
     telegram_chat_id: "123456789"
   ```

## 📊 What You Get

- **15 crypto news platforms** monitored
- **Base-focused filtering** - Only relevant Base ecosystem news
- **Smart notifications** - Telegram or Email
- **HTML reports** - Generated in `output/` directory
- **Three modes**: Daily summary, Current ranking, Incremental

## 🎯 Next Steps

- [Full Documentation](README.md)
- [Local Setup Details](LOCAL_SETUP.md)
- [Deployment Guide](DEPLOYMENT.md)
- [MCP Server Setup](README-Cherry-Studio.md)

## ❓ Need Help?

- Check [Troubleshooting](LOCAL_SETUP.md#troubleshooting)
- Review configuration in `config/config.yaml`
- Test individual crawlers:
  ```python
  from crawlers import crawl_platform
  result = crawl_platform("base-blog")
  print(result)
  ```

---

**That's it!** You're ready to track Base ecosystem news. 🎉

