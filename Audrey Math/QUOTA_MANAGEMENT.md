# 🔒 API Quota Management Guide

## 📊 **配額設定選項**

### **1. Google Cloud Console 設定**

#### **前往 Google Cloud Console：**
1. 前往：https://console.cloud.google.com/
2. 選擇專案 → **"APIs & Services"** → **"Quotas"**
3. 搜尋 **"Generative Language API"**

#### **建議配額設定：**

**🟢 保守設定（免費/低費用）：**
```
Daily Requests: 50
Hourly Requests: 10
Daily Characters: 25,000
Hourly Characters: 2,500
```

**🟡 中等設定（適度使用）：**
```
Daily Requests: 200
Hourly Requests: 30
Daily Characters: 100,000
Hourly Characters: 10,000
```

**🔴 高使用設定（大量使用）：**
```
Daily Requests: 1,000
Hourly Requests: 100
Daily Characters: 500,000
Hourly Characters: 50,000
```

### **2. 代碼層面配額控制**

#### **使用 APIQuotaManager：**
```python
from api_quota_manager import APIQuotaManager

# 初始化配額管理器
quota_manager = APIQuotaManager()

# 檢查是否可以發送請求
if quota_manager.check_request_quota():
    # 檢查字符配額
    if quota_manager.check_character_quota(1000):
        # 發送 API 請求
        response = send_api_request()
        # 記錄使用量
        quota_manager.record_request(1000)
    else:
        print("字符配額不足")
else:
    print("請求配額不足")
```

### **3. 環境變數設定**

#### **創建 .env 檔案：**
```bash
cp env.example .env
```

#### **編輯 .env 檔案：**
```env
# API 金鑰
GEMINI_API_KEY=your_actual_api_key_here

# 配額設定
API_DAILY_REQUESTS=50
API_HOURLY_REQUESTS=10
API_DAILY_CHARACTERS=25000
API_HOURLY_CHARACTERS=2500
API_MINUTE_DELAY=3
```

## 💰 **費用控制**

### **Google Gemini API 定價：**
- **免費配額**：每月 15 次請求
- **付費**：$0.0005 per 1K characters
- **建議**：設定每日 $1-5 的預算限制

### **設定預算警報：**
1. 前往 Google Cloud Console
2. **"Billing"** → **"Budgets & alerts"**
3. 創建預算警報：
   - 預算：$5/月
   - 警報：50%, 90%, 100%

## 🛡️ **安全最佳實踐**

### **1. 配額監控**
```python
# 定期檢查使用量
quota_manager.print_usage_stats()

# 每日重置配額
quota_manager.reset_daily_quotas()
```

### **2. 自動停止機制**
```python
# 達到配額時自動停止
if not quota_manager.check_request_quota():
    print("⚠️ 配額已用完，停止生成")
    exit(1)
```

### **3. 日誌記錄**
```python
# 記錄所有 API 使用
import logging
logging.basicConfig(filename='api_usage.log', level=logging.INFO)
logging.info(f"API request: {characters} characters used")
```

## 📈 **使用量監控**

### **查看使用統計：**
```bash
# 運行配額管理器
python api_quota_manager.py

# 查看使用量
cat api_quota.json
```

### **Google Cloud Console 監控：**
1. **"APIs & Services"** → **"Dashboard"**
2. 查看 **"Quotas"** 和 **"Usage"**
3. 設定 **"Alerts"** 當接近限制時通知

## ⚠️ **重要提醒**

1. **定期檢查**：每日檢查 API 使用量
2. **設定警報**：在 Google Cloud Console 設定預算警報
3. **測試環境**：先在測試環境測試配額設定
4. **備份設定**：保存配額設定檔案
5. **監控費用**：定期檢查 Google Cloud 帳單

## 🔧 **故障排除**

### **配額超限錯誤：**
```python
try:
    # API 請求
    response = make_api_request()
except QuotaExceededError:
    print("配額超限，等待重置...")
    time.sleep(3600)  # 等待 1 小時
```

### **檢查配額狀態：**
```python
# 檢查當前配額狀態
stats = quota_manager.get_usage_stats()
print(f"今日請求：{stats['daily_requests']}/{stats['daily_requests_limit']}")
```

---

**記住：安全第一，費用第二！** 🔒💰
