# Hướng Dẫn Cấu Hình Cron Job Bên Ngoài cho BaseRadar

## Tổng Quan

Vercel Hobby plan chỉ cho phép cron job chạy **1 lần mỗi ngày**. Để chạy crawler thường xuyên hơn (mỗi giờ, mỗi 6 giờ, v.v.), bạn cần sử dụng dịch vụ cron bên ngoài.

## Dịch Vụ Cron Bên Ngoài

### 1. cron-job.org (Khuyến Nghị) ⭐

**Ưu điểm:**
- ✅ Miễn phí
- ✅ Không giới hạn số lượng jobs
- ✅ Hỗ trợ nhiều schedule options
- ✅ Email notifications
- ✅ Logs và statistics

**Cách thiết lập:**

1. **Đăng ký tài khoản**
   - Truy cập: https://cron-job.org
   - Đăng ký miễn phí

2. **Tạo Cron Job mới**
   - Click "Create cronjob"
   - Điền thông tin:
     ```
     Title: BaseRadar Crawler
     Address (URL): https://your-project.vercel.app/api
     Schedule: 0 * * * *  (mỗi giờ)
     Request Method: GET
     Request Timeout: 300 (5 phút)
     ```

3. **Các Schedule phổ biến:**
   ```
   Mỗi giờ:        0 * * * *
   Mỗi 6 giờ:      0 */6 * * *
   Mỗi 12 giờ:      0 */12 * * *
   Mỗi ngày 9h:     0 9 * * *
   9h và 21h:       0 9,21 * * *
   ```

4. **Test và kích hoạt**
   - Click "Test" để kiểm tra
   - Nếu thành công, click "Save"
   - Job sẽ tự động chạy theo lịch

**Giá**: Miễn phí (có premium options)

---

### 2. EasyCron

**Ưu điểm:**
- ✅ Dễ sử dụng
- ✅ Giao diện đẹp
- ⚠️ Free tier: 1 job/giờ

**Cách thiết lập:**

1. Đăng ký tại: https://www.easycron.com
2. Tạo cron job:
   - **URL**: `https://your-project.vercel.app/api`
   - **Schedule**: Chọn từ dropdown hoặc custom
   - **HTTP Method**: GET
3. Lưu và kích hoạt

**Giá**: 
- Free: 1 job/giờ
- Paid: $2.99/tháng (unlimited)

---

### 3. UptimeRobot

**Ưu điểm:**
- ✅ Miễn phí
- ✅ 50 monitors
- ✅ Email/SMS alerts
- ⚠️ Minimum interval: 5 phút

**Cách thiết lập:**

1. Đăng ký tại: https://uptimerobot.com
2. Thêm Monitor:
   - **Monitor Type**: HTTP(s)
   - **URL**: `https://your-project.vercel.app/api`
   - **Monitoring Interval**: 60 phút (hoặc tùy chỉnh)
3. Lưu và kích hoạt

**Giá**: Miễn phí (có premium)

---

### 4. GitHub Actions (Nếu dùng GitHub)

**Ưu điểm:**
- ✅ Miễn phí
- ✅ Tích hợp với GitHub
- ✅ 2000 phút/tháng (free)
- ✅ Logs chi tiết

**Cách thiết lập:**

1. **Workflow đã có sẵn** trong `.github/workflows/crawler.yml`

2. **Enable GitHub Actions:**
   - Vào repository Settings
   - Actions > General
   - Enable "Allow all actions and reusable workflows"

3. **Cấu hình Secrets:**
   - Settings > Secrets and variables > Actions
   - Thêm các secrets:
     - `TELEGRAM_BOT_TOKEN`
     - `TELEGRAM_CHAT_ID`
     - `EMAIL_FROM`
     - `EMAIL_PASSWORD`
     - `EMAIL_TO`

4. **Chỉnh sửa Schedule** (nếu cần):
   ```yaml
   on:
     schedule:
       - cron: '0 * * * *'  # Mỗi giờ
       # - cron: '0 */6 * * *'  # Mỗi 6 giờ
   ```

5. **Manual Trigger:**
   - Vào tab Actions
   - Chọn workflow "Crawler"
   - Click "Run workflow"

**Giá**: Miễn phí (2000 phút/tháng)

---

### 5. PythonAnywhere (Nếu có tài khoản)

**Ưu điểm:**
- ✅ Free tier có sẵn
- ✅ Scheduled tasks
- ⚠️ Free tier: 1 task/ngày

**Cách thiết lập:**

1. Đăng nhập PythonAnywhere
2. Vào "Tasks" tab
3. Tạo scheduled task:
   ```bash
   curl https://your-project.vercel.app/api
   ```
4. Set schedule

**Giá**: Free (1 task/ngày), $5/tháng (unlimited)

---

## So Sánh Các Dịch Vụ

| Dịch vụ | Miễn phí | Giới hạn | Dễ sử dụng | Khuyến nghị |
|---------|----------|----------|------------|-------------|
| **cron-job.org** | ✅ | Không | ⭐⭐⭐⭐⭐ | ⭐ Tốt nhất |
| **EasyCron** | ⚠️ | 1 job/giờ | ⭐⭐⭐⭐ | Tốt |
| **UptimeRobot** | ✅ | 50 monitors | ⭐⭐⭐⭐ | Tốt |
| **GitHub Actions** | ✅ | 2000 phút/tháng | ⭐⭐⭐ | Tốt nếu dùng GitHub |
| **PythonAnywhere** | ⚠️ | 1 task/ngày | ⭐⭐⭐ | Hạn chế |

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
curl https://your-project.vercel.app/api

# Hoặc dùng browser
# Mở: https://your-project.vercel.app/api
```

### 2. Kiểm Tra Logs

**Vercel:**
- Dashboard > Functions > Logs
- Xem execution logs

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
4. Service có đang hoạt động không?

**Giải pháp:**
- Test URL thủ công trước
- Kiểm tra logs trong cron service
- Xem logs trong Vercel Dashboard

### Timeout Errors

**Nguyên nhân:**
- Crawler chạy quá lâu
- Vercel timeout (10s free, 60s pro)

**Giải pháp:**
- Tối ưu crawler
- Giảm số lượng platforms
- Tăng request interval

### 429 Too Many Requests

**Nguyên nhân:**
- Cron job chạy quá thường xuyên
- Vercel rate limiting

**Giải pháp:**
- Tăng interval giữa các lần chạy
- Giảm tần suất cron job

## Best Practices

1. **Bắt đầu với interval lớn**: Bắt đầu với mỗi 6-12 giờ, sau đó điều chỉnh
2. **Monitor logs**: Thường xuyên kiểm tra logs để đảm bảo hoạt động bình thường
3. **Test trước**: Test thủ công trước khi setup cron
4. **Backup config**: Lưu lại cấu hình cron job
5. **Notifications**: Bật email notifications để biết khi có lỗi

## Khuyến Nghị

**Cho người mới:**
- Sử dụng **cron-job.org** (dễ nhất, miễn phí)

**Cho người dùng GitHub:**
- Sử dụng **GitHub Actions** (tích hợp tốt)

**Cho production:**
- **cron-job.org** hoặc **EasyCron** (paid) cho reliability cao

## Tài Liệu Tham Khảo

- [cron-job.org Documentation](https://cron-job.org/en/help/)
- [Cron Expression Generator](https://crontab.guru/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

