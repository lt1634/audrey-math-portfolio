# 🚀 Vercel 部署指南

## 📋 **部署步驟**

### **方法 1: 通過 Vercel 網站 (推薦)**

1. **訪問 Vercel Dashboard**
   - 前往 [vercel.com/dashboard](https://vercel.com/dashboard)
   - 確保已登入並連接 GitHub 帳戶

2. **導入項目**
   - 點擊 "New Project" 按鈕
   - 選擇 "Import Git Repository"
   - 找到 `lt1634/audrey-math-portfolio` 項目
   - 點擊 "Import"

3. **配置項目設置**
   - **Project Name**: `audrey-math-portfolio`
   - **Framework Preset**: `Other` (靜態網站)
   - **Root Directory**: `./` (根目錄)
   - **Build Command**: 留空 (靜態文件)
   - **Output Directory**: `./` (根目錄)

4. **部署**
   - 點擊 "Deploy" 按鈕
   - 等待部署完成
   - 獲得部署 URL

### **方法 2: 通過 Vercel CLI**

```bash
# 安裝 Vercel CLI (如果尚未安裝)
npm install -g vercel

# 登入 Vercel
vercel login

# 部署項目
vercel

# 生產環境部署
vercel --prod
```

## ⚙️ **項目配置**

### **vercel.json 配置**
```json
{
  "version": 2,
  "name": "audrey-math-portfolio",
  "builds": [
    {
      "src": "**/*",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ],
  "headers": [
    {
      "source": "/(.*\\.(css|js|png|jpg|jpeg|gif|svg|ico|woff|woff2))",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

## 🌟 **Vercel 優勢**

### **🚀 性能優勢**
- ✅ **全球 CDN**: 自動分發到全球節點
- ✅ **自動優化**: 圖片和資源自動優化
- ✅ **HTTP/2**: 更快的網絡協議
- ✅ **邊緣計算**: 更低的延遲

### **🛠️ 開發優勢**
- ✅ **自動部署**: GitHub 推送自動觸發部署
- ✅ **預覽部署**: 每個 PR 都有預覽 URL
- ✅ **回滾功能**: 輕鬆回滾到之前版本
- ✅ **環境變量**: 安全的配置管理

### **📊 監控優勢**
- ✅ **實時分析**: 訪問統計和性能監控
- ✅ **錯誤追蹤**: 自動錯誤報告
- ✅ **速度測試**: 自動性能測試
- ✅ **SEO 優化**: 自動 SEO 優化

## 🔄 **自動部署**

### **GitHub 集成**
- ✅ **自動觸發**: 每次 `git push` 自動部署
- ✅ **分支部署**: 不同分支有不同 URL
- ✅ **預覽部署**: PR 自動生成預覽
- ✅ **生產部署**: main 分支自動部署到生產

### **部署 URL 格式**
```
生產環境: https://audrey-math-portfolio.vercel.app
預覽環境: https://audrey-math-portfolio-git-[branch].vercel.app
```

## 🎯 **部署後檢查**

### **✅ 功能檢查**
- [ ] 網站正常載入
- [ ] 語言切換功能正常
- [ ] 深色模式切換正常
- [ ] 響應式設計正常
- [ ] 所有圖片正常顯示
- [ ] 動畫效果流暢

### **✅ 性能檢查**
- [ ] 載入速度 < 3 秒
- [ ] Lighthouse 分數 > 90
- [ ] 移動端體驗良好
- [ ] SEO 優化正常

## 🆚 **Vercel vs GitHub Pages**

| 功能 | Vercel | GitHub Pages |
|------|--------|--------------|
| **部署速度** | ⚡ 極快 | 🐌 較慢 |
| **全球 CDN** | ✅ 自動 | ❌ 無 |
| **自動優化** | ✅ 是 | ❌ 否 |
| **預覽部署** | ✅ 是 | ❌ 否 |
| **回滾功能** | ✅ 是 | ❌ 否 |
| **分析工具** | ✅ 內建 | ❌ 無 |
| **免費額度** | 🆓 100GB | 🆓 1GB |

## 🎉 **完成部署**

部署完成後，你的 Audrey Math 網站將擁有：
- 🌍 **全球加速**: 通過 Vercel 的全球 CDN
- ⚡ **極速載入**: 優化的資源和緩存
- 🔄 **自動部署**: GitHub 推送自動更新
- 📊 **實時監控**: 訪問統計和性能分析

**享受更快的網站體驗！** 🚀✨
