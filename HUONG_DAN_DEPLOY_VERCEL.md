# Hướng Dẫn Deploy BaseRadar lên Vercel

## Tổng Quan

BaseRadar có 2 thành phần chính:
1. **Main Application** (Crawler) - ✅ Có thể deploy lên Vercel
2. **MCP Server** - ⚠️ Có giới hạn trên Vercel

## 1. Deploy Main Application lên Vercel

### Bước 1: Cài đặt Vercel CLI

```bash
npm install -g vercel
```

### Bước 2: Đăng nhập Vercel

```bash
vercel login
```

### Bước 3: Cấu hình Environment Variables

Thiết lập các biến môi trường trong Vercel Dashboard hoặc qua CLI:

**Qua Vercel Dashboard:**
1. Vào Project Settings > Environment Variables
2. Thêm các biến sau:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
EMAIL_FROM=your_email@example.com
EMAIL_PASSWORD=your_email_password
EMAIL_TO=recipient@example.com
```

**Qua CLI:**
```bash
vercel env add TELEGRAM_BOT_TOKEN
vercel env add TELEGRAM_CHAT_ID
vercel env add EMAIL_FROM
vercel env add EMAIL_PASSWORD
vercel env add EMAIL_TO
```

### Bước 4: Deploy

```bash
# Deploy preview (test)
vercel

# Deploy production
vercel --prod
```

### Bước 5: Cấu hình Cron Job

**Vercel Pro Plan:**
- Cron job đã được cấu hình trong `vercel.json`
- Chạy mỗi giờ tại phút 0

**Vercel Free Plan:**
- Sử dụng dịch vụ cron bên ngoài:
  - [cron-job.org](https://cron-job.org)
  - [EasyCron](https://www.easycron.com)
  - [UptimeRobot](https://uptimerobot.com)
- URL: `https://your-project.vercel.app/api`
- Lịch: Mỗi giờ (hoặc tùy chỉnh)

### Kiểm tra Deployment

1. Vào Vercel Dashboard kiểm tra trạng thái
2. Test endpoint: `https://your-project.vercel.app/api`
3. Xem logs trong Vercel Dashboard
4. Kiểm tra nhận được notifications

## 2. Deploy MCP Server

### ⚠️ Lưu Ý Quan Trọng

**MCP Server KHÔNG thể deploy đầy đủ lên Vercel vì:**

1. **STDIO Mode**: Không hỗ trợ
   - Cần process chạy liên tục
   - Vercel serverless là stateless

2. **HTTP Mode**: Hỗ trợ hạn chế
   - FastMCP HTTP cần persistent server
   - Vercel functions chỉ là request-response

### Option 1: Endpoint Cơ Bản trên Vercel

Đã có sẵn endpoint tại:
```
https://your-project.vercel.app/api/mcp
```

**Chức năng:**
- Health check
- Kiểm tra kết nối
- Trả về trạng thái server

**Hạn chế:**
- Không hỗ trợ đầy đủ MCP protocol
- Không thể chạy tools qua HTTP
- Chỉ dùng để kiểm tra

### Option 2: Deploy MCP Server Riêng (Khuyến Nghị) ⭐

#### A. Railway (Khuyến Nghị)

```bash
# 1. Cài Railway CLI
npm i -g @railway/cli

# 2. Đăng nhập
railway login

# 3. Khởi tạo project
railway init

# 4. Deploy
railway up
```

**Tạo file `railway.json`:**
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

**Giá**: Free tier có sẵn, $5/tháng cho hobby

#### B. Render

1. Vào [render.com](https://render.com)
2. Tạo Web Service mới
3. Kết nối GitHub repository
4. Cấu hình:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m mcp_server.server --transport http --port $PORT`
   - **Environment**: Python 3
5. Deploy

**Giá**: Free tier (tự động tắt khi không dùng)

#### C. Fly.io

```bash
# 1. Cài flyctl
curl -L https://fly.io/install.sh | sh

# 2. Đăng nhập
fly auth login

# 3. Launch app
fly launch

# 4. Deploy
fly deploy
```

**Giá**: Free tier có sẵn

#### D. VPS Tự Host

```bash
# Chạy MCP Server
python -m mcp_server.server --transport http --port 3333
```

**Tự động khởi động với systemd:**

Tạo `/etc/systemd/system/baseradar-mcp.service`:

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

Kích hoạt:
```bash
sudo systemctl enable baseradar-mcp
sudo systemctl start baseradar-mcp
```

## 3. Cấu Hình MCP Client

### STDIO Mode (Local - Khuyến Nghị)

Hầu hết MCP clients dùng STDIO mode:

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

### HTTP Mode (Remote)

Nếu MCP client hỗ trợ HTTP:

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

**Lưu ý**: Hầu hết MCP clients chưa hỗ trợ HTTP mode. STDIO là chuẩn.

## 4. Kiểm Tra Deployment

### Main Application

```bash
# Test endpoint
curl https://your-project.vercel.app/api

# Xem logs
# Vào Vercel Dashboard > Functions > Logs
```

### MCP Server

```bash
# Health check
curl https://your-mcp-server.railway.app/mcp

# Expected response:
{
  "status": "online",
  "service": "BaseRadar MCP Server",
  "transport": "http"
}
```

## 5. So Sánh Các Platform

| Platform | Main App | MCP Server | Giá | Khuyến Nghị |
|----------|----------|------------|-----|-------------|
| **Vercel** | ✅ Tốt | ⚠️ Hạn chế | Free/Pro | Main app |
| **Railway** | ✅ Tốt | ✅ Tốt | Free/$5 | MCP Server ⭐ |
| **Render** | ✅ Tốt | ✅ Tốt | Free | MCP Server |
| **Fly.io** | ✅ Tốt | ✅ Tốt | Free | MCP Server |
| **VPS** | ✅ Tốt | ✅ Tốt | $5-20/tháng | Full control |

## 6. Giải Pháp Hybrid (Khuyến Nghị)

Deploy các thành phần riêng biệt:

1. **Main Crawler** → Vercel
   - Chạy crawler theo lịch
   - Gửi notifications
   - Tạo reports

2. **MCP Server** → Railway/Render/Fly.io
   - Cung cấp MCP tools
   - Truy cập dữ liệu đã crawl
   - Dùng bởi MCP clients

3. **Data Storage** → Shared
   - Cả 2 services truy cập cùng thư mục data
   - Dùng shared storage (S3, etc.) hoặc sync

## 7. Troubleshooting

### Main App không chạy trên Vercel

- Kiểm tra logs trong Vercel Dashboard
- Đảm bảo tất cả dependencies trong `requirements.txt`
- Kiểm tra Python version (3.10+)
- Xác minh environment variables đã được set

### MCP Server không hoạt động

- **Trên Vercel**: Bình thường, Vercel không hỗ trợ đầy đủ
- **Trên Railway/Render**: Kiểm tra logs, đảm bảo port được expose
- **Local**: Kiểm tra firewall, service đang chạy

### Timeout Errors

- Vercel free tier: 10s timeout
- Vercel Pro: 60s timeout
- Giải pháp: Tối ưu crawler hoặc dùng background jobs

## 8. Tóm Tắt Nhanh

### Deploy Main App (Vercel)

```bash
# 1. Cài Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Set env vars (trong Dashboard hoặc CLI)
vercel env add TELEGRAM_BOT_TOKEN
vercel env add TELEGRAM_CHAT_ID
# ... các biến khác

# 4. Deploy
vercel --prod
```

### Deploy MCP Server (Railway)

```bash
# 1. Cài Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Deploy
railway init
railway up
```

## Tài Liệu Tham Khảo

- [DEPLOYMENT.md](./DEPLOYMENT.md) - Hướng dẫn chi tiết
- [VERCEL_MCP_DEPLOYMENT.md](./VERCEL_MCP_DEPLOYMENT.md) - Hướng dẫn MCP Server
- [README-MCP.md](./README-MCP.md) - Cấu hình MCP Client

## Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra logs
2. Xem lại cấu hình
3. Test local trước
4. Mở GitHub issue với chi tiết lỗi

