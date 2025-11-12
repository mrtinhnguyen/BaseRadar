# Railway Deployment Guide

Hướng dẫn deploy BaseRadar lên Railway và xử lý các vấn đề thường gặp.

## Cấu hình Railway

### 1. File cấu hình

Dự án đã bao gồm các file cấu hình sau:

- **`Procfile`**: Định nghĩa command để chạy ứng dụng
- **`railway.json`**: Cấu hình Railway deployment (optional)
- **`requirements.txt`**: Python dependencies (Railway tự detect từ file này)

**Lưu ý**: Railway tự động detect Python project từ `requirements.txt`, không cần `nixpacks.toml`.

### 2. Environment Variables

Thiết lập các biến môi trường trong Railway Dashboard:

**Bắt buộc:**
- `CONFIG_PATH`: Đường dẫn đến file config (mặc định: `config/config.yaml`)
- `FREQUENCY_WORDS_PATH`: Đường dẫn đến file frequency words

**Tùy chọn (nếu không dùng config file):**
- `TELEGRAM_BOT_TOKEN`: Token của Telegram bot
- `TELEGRAM_CHAT_ID`: Chat ID để nhận thông báo
- `EMAIL_FROM`: Email người gửi
- `EMAIL_PASSWORD`: Mật khẩu hoặc app password
- `EMAIL_TO`: Email người nhận (có thể nhiều, phân cách bằng dấu phẩy)
- `EMAIL_SMTP_SERVER`: SMTP server (tùy chọn, tự động phát hiện)
- `EMAIL_SMTP_PORT`: SMTP port (tùy chọn, tự động phát hiện)

### 3. Deploy

#### Cách 1: Deploy từ GitHub

1. Kết nối repository GitHub với Railway
2. Railway sẽ tự động detect và build
3. Thiết lập environment variables
4. Deploy

#### Cách 2: Deploy từ CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to existing project (optional)
railway link

# Deploy
railway up
```

### 4. Cấu hình Files

Railway cần các file config được commit vào repository:

- `config/config.yaml` - File cấu hình chính
- `config/frequency_words.txt` - Danh sách từ khóa

Đảm bảo các file này được commit vào git.

## Vấn đề Email trên Railway

### Vấn đề: Network is unreachable

Railway có thể chặn kết nối SMTP trực tiếp ra ngoài. Lỗi thường gặp:

```
OSError: [Errno 101] Network is unreachable
```

### Giải pháp

#### Giải pháp 1: Sử dụng Email API Service (Khuyến nghị)

Thay vì SMTP trực tiếp, sử dụng email API service:

**SendGrid:**
- Free tier: 100 emails/day
- Dễ tích hợp
- Không bị chặn bởi firewall

**Mailgun:**
- Free tier: 5,000 emails/month
- API đơn giản

**AWS SES:**
- Rất rẻ ($0.10 per 1,000 emails)
- Cần AWS account

#### Giải pháp 2: Kiểm tra Railway Network Settings

1. Vào Railway Dashboard
2. Chọn project → Settings
3. Kiểm tra Network/Firewall settings
4. Đảm bảo outbound connections được cho phép

#### Giải pháp 3: Sử dụng Railway Private Networking

Nếu có service khác trên Railway, có thể sử dụng private networking.

### Retry Logic

Code đã được cải thiện với retry logic:

- Tự động retry 3 lần khi gặp lỗi network
- Exponential backoff (2s, 4s, 6s)
- Thông báo lỗi chi tiết với gợi ý giải pháp

## Monitoring và Logs

### Xem Logs

```bash
# Via CLI
railway logs

# Via Dashboard
# Project → Deployments → Select deployment → View logs
```

### Health Checks

Ứng dụng sẽ tự động log các thông tin:
- Configuration loading
- Crawler execution
- Email sending status
- Error messages với traceback

## Tối ưu hóa

### 1. Build Time

- Railway tự động detect Python từ `requirements.txt`
- Sử dụng Nixpacks để build tự động
- Dependencies được cache giữa các lần build
- Không cần file `nixpacks.toml` - Railway tự detect

### 2. Runtime

- Python version được tự động detect (thường là Python 3.10+)
- `PYTHONUNBUFFERED=1` được set tự động để log real-time
- Command chạy từ `Procfile`: `python main.py`

### 3. Resource Usage

- Railway free tier: 512MB RAM, 1GB storage
- Đủ cho ứng dụng crawler này
- Nếu cần nhiều hơn, upgrade plan

## Troubleshooting

### Build fails

**Lỗi:** `undefined variable 'pip'` hoặc `undefined variable '$NIXPACKS_PATH'`
- **Nguyên nhân:** File `nixpacks.toml` có cấu hình sai hoặc không cần thiết
- **Giải pháp:** 
  - Xóa file `nixpacks.toml` (Railway tự detect Python từ `requirements.txt`)
  - Railway sẽ tự động detect và build Python project
  - Chỉ cần `Procfile` và `requirements.txt`

**Lỗi:** `ModuleNotFoundError`
- **Giải pháp:** Kiểm tra `requirements.txt` có đầy đủ dependencies

**Lỗi:** `FileNotFoundError: config/config.yaml`
- **Giải pháp:** Đảm bảo file config được commit vào git

**Lỗi:** Build timeout hoặc chậm
- **Giải pháp:** 
  - Kiểm tra `requirements.txt` không có dependencies quá lớn
  - Railway cache dependencies giữa các lần build
  - Có thể set env var `NIXPACKS_NO_CACHE=1` để clear cache nếu cần

### Runtime errors

**Lỗi:** `Network is unreachable` (Email)
- **Giải pháp:** Xem phần "Vấn đề Email trên Railway" ở trên

**Lỗi:** `ImportError`
- **Giải pháp:** Kiểm tra Python version (cần 3.10+)

### Performance

**Crawler chạy chậm:**
- Kiểm tra `REQUEST_INTERVAL` trong config
- Railway có thể có network latency

**Memory issues:**
- Giảm số lượng platforms trong config
- Tối ưu HTML generation

## Best Practices

1. **Environment Variables**: Luôn dùng env vars cho secrets, không hardcode
2. **Error Handling**: Code đã có error handling tốt, monitor logs thường xuyên
3. **Backup Config**: Giữ backup của config files
4. **Testing**: Test locally trước khi deploy
5. **Monitoring**: Check logs định kỳ để phát hiện vấn đề sớm

## Setup Cron Job

Railway không có tính năng cron job built-in. Xem hướng dẫn chi tiết trong file **`RAILWAY_CRON_SETUP.md`**.

**Tóm tắt nhanh:**

1. **Sử dụng External Cron Service** (Khuyến nghị):
   - **cron-job.org** (miễn phí, không giới hạn)
   - Tạo cron job với URL: `https://your-project.up.railway.app/api`
   - Schedule: `0 * * * *` (mỗi giờ) hoặc tùy chỉnh

2. **GitHub Actions** (nếu dùng GitHub):
   - Workflow đã có sẵn trong `.github/workflows/crawler.yml`
   - Enable Actions và cấu hình secrets

3. **Kiểm tra:**
   - Test URL thủ công trước
   - Monitor logs trong Railway Dashboard
   - Đảm bảo service không bị sleep (free tier)

Xem chi tiết: [RAILWAY_CRON_SETUP.md](./RAILWAY_CRON_SETUP.md)

## Support

Nếu gặp vấn đề:
1. Check Railway logs
2. Check error messages trong code (đã được cải thiện)
3. Xem troubleshooting section ở trên
4. Xem RAILWAY_CRON_SETUP.md cho cron job issues
5. Open GitHub issue với error details

