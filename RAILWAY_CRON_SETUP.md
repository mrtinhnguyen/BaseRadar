# Hướng Dẫn Setup Cron Job trên Railway

Railway không có tính năng cron job built-in, nhưng có nhiều cách để chạy scheduled tasks. Hướng dẫn này sẽ giúp bạn setup cron job cho BaseRadar trên Railway.

## Phương Pháp 1: External Cron Service (Khuyến Nghị) ⭐

Sử dụng dịch vụ cron bên ngoài để gọi HTTP endpoint của Railway service.

### Bước 1: Tạo HTTP Endpoint (Đã có sẵn)

Dự án đã có sẵn endpoint tại `api/index.py`. Nếu chưa có, bạn cần tạo một endpoint để trigger crawler.

**Endpoint hiện tại:**
- File: `api/index.py`
- Route: `/api` hoặc `/api/index`
- Method: GET hoặc POST

### Bước 2: Deploy lên Railway và Lấy URL

1. Deploy service lên Railway
2. Lấy public URL từ Railway Dashboard
3. URL sẽ có dạng: `https://your-project.up.railway.app`

### Bước 3: Setup External Cron Service

#### Option A: cron-job.org (Miễn phí, Khuyến nghị)

1. **Đăng ký tài khoản**
   - Truy cập: https://cron-job.org
   - Đăng ký miễn phí

2. **Tạo Cron Job mới**
   - Click "Create cronjob"
   - Điền thông tin:
     ```
     Title: BaseRadar Crawler
     Address (URL): https://your-project.up.railway.app/api
     Schedule: 0 * * * *  (mỗi giờ)
     Request Method: GET
     Request Timeout: 300 (5 phút)
     ```

3. **Các Schedule phổ biến:**
   ```
   Mỗi giờ:        0 * * * *
   Mỗi 6 giờ:      0 */6 * * *
   Mỗi 12 giờ:     0 */12 * * *
   Mỗi ngày 9h:    0 9 * * *
   9h và 21h:      0 9,21 * * *
   Mỗi 30 phút:    */30 * * * *
   ```

4. **Test và kích hoạt**
   - Click "Test" để kiểm tra
   - Nếu thành công, click "Save"
   - Job sẽ tự động chạy theo lịch

**Ưu điểm:**
- ✅ Miễn phí
- ✅ Không giới hạn số lượng jobs
- ✅ Email notifications khi có lỗi
- ✅ Logs và statistics

#### Option B: EasyCron

1. Đăng ký tại: https://www.easycron.com
2. Tạo cron job:
   - **URL**: `https://your-project.up.railway.app/api`
   - **Schedule**: Chọn từ dropdown hoặc custom
   - **HTTP Method**: GET
3. Lưu và kích hoạt

**Giá**: 
- Free: 1 job/giờ
- Paid: $2.99/tháng (unlimited)

#### Option C: UptimeRobot

1. Đăng ký tại: https://uptimerobot.com
2. Thêm Monitor:
   - **Monitor Type**: HTTP(s)
   - **URL**: `https://your-project.up.railway.app/api`
   - **Monitoring Interval**: 60 phút (hoặc tùy chỉnh)
3. Lưu và kích hoạt

**Giá**: Miễn phí (50 monitors)

#### Option D: GitHub Actions (Nếu dùng GitHub)

1. **Workflow đã có sẵn** trong `.github/workflows/crawler.yml`

2. **Enable GitHub Actions:**
   - Vào repository Settings
   - Actions > General
   - Enable "Allow all actions and reusable workflows"

3. **Cấu hình Secrets:**
   - Settings > Secrets and variables > Actions
   - Thêm các secrets cần thiết

4. **Chỉnh sửa Schedule** (nếu cần):
   ```yaml
   on:
     schedule:
       - cron: '0 * * * *'  # Mỗi giờ
   ```

**Giá**: Miễn phí (2000 phút/tháng)

## Phương Pháp 2: Railway Scheduler (Nếu có)

Railway đang phát triển tính năng Scheduler. Nếu có sẵn:

1. Vào Railway Dashboard
2. Chọn project → Scheduler
3. Tạo scheduled task:
   - **Command**: `python main.py`
   - **Schedule**: Cron expression (ví dụ: `0 * * * *`)
4. Lưu và kích hoạt

**Lưu ý**: Tính năng này có thể chưa có sẵn trên tất cả plans.

## Phương Pháp 3: Tạo HTTP Endpoint Đơn Giản

Nếu bạn muốn tạo một endpoint đơn giản chỉ để trigger crawler:

### Tạo file `api/trigger.py`:

```python
"""
Simple HTTP endpoint to trigger crawler
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def handler(request):
    """
    Simple handler to trigger crawler
    """
    try:
        # Set Vercel/Railway environment flag
        os.environ["RAILWAY"] = "1"
        
        # Import and run
        from main import NewsAnalyzer
        
        print("Starting crawler from HTTP trigger...", file=sys.stderr)
        analyzer = NewsAnalyzer()
        analyzer.run()
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": '{"status":"success","message":"Crawler executed successfully"}'
        }
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error: {e}", file=sys.stderr)
        print(error_trace, file=sys.stderr)
        
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": f'{{"status":"error","message":"{str(e)}"}}'
        }
```

**Lưu ý**: Railway không hỗ trợ serverless functions như Vercel. Bạn cần chạy ứng dụng như một web service.

## Phương Pháp 4: Sử dụng Docker với Supercronic (Cho Self-hosted)

Nếu bạn deploy bằng Docker trên Railway hoặc self-hosted:

1. **Sử dụng Dockerfile có sẵn** trong `docker/Dockerfile`
2. **Set environment variables:**
   ```
   RUN_MODE=cron
   CRON_SCHEDULE=0 * * * *  # Mỗi giờ
   IMMEDIATE_RUN=true  # Chạy ngay khi start
   ```

3. **Deploy với Docker:**
   ```bash
   railway up --dockerfile docker/Dockerfile
   ```

**Lưu ý**: Railway có thể không hỗ trợ long-running processes trên free tier.

## Cron Schedule Syntax

Cron expression format: `minute hour day month weekday`

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── weekday (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *
```

**Ví dụ:**

```bash
# Mỗi giờ tại phút 0
0 * * * *

# Mỗi 6 giờ
0 */6 * * *

# Mỗi 12 giờ (9h và 21h)
0 9,21 * * *

# Mỗi ngày lúc 9h sáng
0 9 * * *

# Mỗi ngày lúc 9h sáng và 6h chiều
0 9,18 * * *

# Mỗi 30 phút
*/30 * * * *

# Mỗi ngày từ thứ 2 đến thứ 6 lúc 9h
0 9 * * 1-5
```

## Kiểm Tra Cron Job

### 1. Test Thủ Công

```bash
# Test endpoint
curl https://your-project.up.railway.app/api

# Hoặc dùng browser
# Mở: https://your-project.up.railway.app/api
```

### 2. Kiểm Tra Logs

**Railway:**
```bash
# Via CLI
railway logs

# Via Dashboard
# Project → Deployments → Select deployment → View logs
```

**cron-job.org:**
- Dashboard > Cronjobs > View logs

**GitHub Actions:**
- Tab Actions > Select workflow run > View logs

### 3. Kiểm Tra Notifications

- Kiểm tra Telegram/Email có nhận được notifications không
- Nếu không nhận được, kiểm tra:
  - Environment variables đã được set chưa
  - Notification channels đã được cấu hình chưa
  - Logs có lỗi không

## Troubleshooting

### Cron job không chạy

**Kiểm tra:**
1. Cron job đã được kích hoạt chưa?
2. URL có đúng không?
3. Schedule có đúng format không?
4. Railway service có đang chạy không?

**Giải pháp:**
- Test URL thủ công trước
- Kiểm tra logs trong cron service
- Xem logs trong Railway Dashboard
- Đảm bảo Railway service không bị sleep (free tier có thể sleep sau khi không dùng)

### Railway Service Sleep

Railway free tier có thể sleep service sau một thời gian không hoạt động.

**Giải pháp:**
1. Sử dụng external cron service với retry logic
2. Upgrade lên paid plan để tránh sleep
3. Sử dụng uptime monitoring service để "đánh thức" service

### Timeout Errors

**Nguyên nhân:**
- Crawler chạy quá lâu
- Railway timeout

**Giải pháp:**
- Tối ưu crawler
- Giảm số lượng platforms
- Tăng request interval
- Kiểm tra Railway plan limits

### 429 Too Many Requests

**Nguyên nhân:**
- Cron job chạy quá thường xuyên
- Railway rate limiting

**Giải pháp:**
- Tăng interval giữa các lần chạy
- Giảm tần suất cron job
- Kiểm tra Railway plan limits

## Best Practices

1. **Bắt đầu với interval lớn**: Bắt đầu với mỗi 6-12 giờ, sau đó điều chỉnh
2. **Monitor logs**: Thường xuyên kiểm tra logs để đảm bảo hoạt động bình thường
3. **Test trước**: Test thủ công trước khi setup cron
4. **Backup config**: Lưu lại cấu hình cron job
5. **Notifications**: Bật email notifications để biết khi có lỗi
6. **Handle Railway Sleep**: Sử dụng external cron với retry để đảm bảo service được đánh thức

## Khuyến Nghị

**Cho người mới:**
- Sử dụng **cron-job.org** (dễ nhất, miễn phí)
- Setup với schedule mỗi 6-12 giờ để test

**Cho production:**
- Sử dụng **cron-job.org** hoặc **EasyCron** (paid) cho reliability cao
- Kết hợp với uptime monitoring để đảm bảo service không sleep

**Cho người dùng GitHub:**
- Sử dụng **GitHub Actions** (tích hợp tốt, miễn phí)

## Tài Liệu Tham Khảo

- [cron-job.org Documentation](https://cron-job.org/en/help/)
- [Cron Expression Generator](https://crontab.guru/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Railway Documentation](https://docs.railway.app/)

