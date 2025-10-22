# Audrey Math 完整項目整合文件

## 項目概述
Audrey Math 是一個現代化的雙語數學教育平台，整合了 STEM 學習資源、互動遊戲和國際教育內容。

## 核心功能
- 雙語支援 (英文/繁體中文)
- 暗色/亮色主題切換
- 響應式設計
- 6階段學習系統
- 互動數學遊戲
- 全球 STEM 資源整合

## HTML 結構 (index.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audrey Math 安蕎的數學 - Educational Platform</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+TC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <!-- 導航欄 -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <img src="audrey-math-logo.svg" alt="Audrey Math Logo" class="logo-img">
            </div>
            <div class="nav-controls">
                <!-- 語言切換 -->
                <div class="language-toggle">
                    <input type="checkbox" id="language-toggle" class="language-toggle-checkbox">
                    <label for="language-toggle" class="language-toggle-label">
                        <span class="en-icon">🇺🇸</span>
                        <span class="zh-icon">🇹🇼</span>
                    </label>
                </div>
                <!-- 主題切換 -->
                <div class="theme-toggle">
                    <input type="checkbox" id="theme-toggle" class="theme-toggle-checkbox">
                    <label for="theme-toggle" class="theme-toggle-label">
                        <span class="sun-icon">☀️</span>
                        <span class="moon-icon">🌙</span>
                    </label>
                </div>
            </div>
            <ul class="nav-menu">
                <li class="nav-item"><a href="#home" class="nav-link" data-en="Home" data-zh="首頁">Home</a></li>
                <li class="nav-item"><a href="#about" class="nav-link" data-en="About" data-zh="關於">About</a></li>
                <li class="nav-item"><a href="#games" class="nav-link" data-en="Math Games" data-zh="數學遊戲">Math Games</a></li>
                <li class="nav-item"><a href="#projects" class="nav-link" data-en="Courses" data-zh="課程">Courses</a></li>
                <li class="nav-item"><a href="#contact" class="nav-link" data-en="Contact" data-zh="聯絡">Contact</a></li>
            </ul>
        </div>
    </nav>

    <!-- 主要內容區塊 -->
    <section id="home" class="hero">
        <!-- Hero 內容 -->
    </section>

    <section id="about" class="about">
        <!-- 關於我們 -->
    </section>

    <section id="games" class="games">
        <!-- 數學遊戲區 -->
    </section>

    <section id="projects" class="projects">
        <!-- 學習模組 -->
    </section>

    <section id="resources" class="resources">
        <!-- 全球資源 -->
    </section>

    <section id="contact" class="contact">
        <!-- 聯絡我們 -->
    </section>

    <script src="script.js"></script>
</body>
</html>
```

## CSS 樣式重點 (styles.css)

```css
/* 顏色主題 */
:root {
    --primary-color: #2563EB;
    --secondary-color: #059669;
    --accent-color: #DC2626;
    --bg-primary: #FFFFFF;
    --text-primary: #1E293B;
    --gradient-primary: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
}

/* 暗色主題 */
[data-theme="dark"] {
    --primary-color: #60A5FA;
    --bg-primary: #0F172A;
    --text-primary: #F1F5F9;
}

/* 響應式設計 */
@media (max-width: 768px) {
    .hero-content { grid-template-columns: 1fr; }
    .games-grid { grid-template-columns: 1fr; }
    .resources-grid { grid-template-columns: 1fr; }
}

/* 動畫效果 */
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}

.organic-shape {
    animation: float 6s ease-in-out infinite;
}
```

## JavaScript 功能 (script.js)

```javascript
// 語言切換功能
const languageToggle = document.getElementById('language-toggle');
const body = document.body;

languageToggle.addEventListener('change', function() {
    if (this.checked) {
        body.setAttribute('data-lang', 'zh');
        localStorage.setItem('language', 'zh');
        updateLanguageContent('zh');
    } else {
        body.setAttribute('data-lang', 'en');
        localStorage.setItem('language', 'en');
        updateLanguageContent('en');
    }
});

// 主題切換功能
const themeToggle = document.getElementById('theme-toggle');

themeToggle.addEventListener('change', function() {
    if (this.checked) {
        body.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    } else {
        body.setAttribute('data-theme', 'light');
        localStorage.setItem('theme', 'light');
    }
});

// 遊戲按鈕互動
function initGameButtons() {
    const gamePlayBtns = document.querySelectorAll('.game-play-btn');
    
    gamePlayBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const gameCard = btn.closest('.game-card');
            const gameTitle = gameCard.querySelector('h3').textContent;
            showNotification(`Starting ${gameTitle}... Coming soon!`, 'info');
        });
    });
}

// 通知系統
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    document.body.appendChild(notification);
}
```

## 新增功能詳情

### 1. 數學遊戲區
- **Mighty Mind Basic Puzzle** (3-6歲)
  - 幾何圖形認知
  - 32片拼圖，6種基本形狀
  - 空間邏輯訓練

- **Swift Maze Adventure** (4歲以上)
  - 不插電程式設計
  - Swift 指令學習
  - 路徑規劃概念

- **Easter Egg Hunt** (4-6歲)
  - 最佳路徑概念
  - 數數和簡單加法
  - 策略思維培養

### 2. 全球 STEM 資源
- **NASA 教育資源**
  - NASA Climate Kids
  - Galileo Legacy Site

- **史密森學會**
  - Air & Space Museum

- **科學教育**
  - Frontiers for Young Minds
  - Chemicool

- **教育研究**
  - Monash PlayWorld

### 3. 教育理論整合
- **Play-Based Learning**: 以玩為基礎的學習
- **STEAM 教育**: 科學、科技、工程、藝術、數學整合
- **年齡分層設計**: 3-6歲不同階段學習內容

## 技術特色

### 響應式設計
- 移動優先設計
- 平板和桌面適配
- 跨瀏覽器兼容

### 性能優化
- CSS 變數系統
- 漸進式增強
- 平滑動畫過渡

### 可訪問性
- 語義化 HTML
- 鍵盤導航支援
- 螢幕閱讀器友好

## 部署資訊
- **GitHub**: https://github.com/lt1634/audrey-math-portfolio
- **Vercel**: https://audrey-math-portfolio-tijk.vercel.app/
- **狀態**: 已成功部署並運行

## 改進建議方向

### 短期改進
1. **實際遊戲功能實現**
   - Mighty Mind 拼圖拖拽功能
   - Swift 迷宮指令系統
   - 復活節彩蛋路徑算法

2. **教育內容擴展**
   - 更多年齡層適配
   - 進度追蹤系統
   - 個性化學習路徑

### 中期發展
1. **互動功能增強**
   - 實時反饋系統
   - 成就徽章系統
   - 家長監控面板

2. **內容管理系統**
   - 動態內容更新
   - 多語言內容管理
   - 用戶生成內容

### 長期規劃
1. **AI 整合**
   - 智能學習推薦
   - 自動化評估
   - 個性化教學

2. **社群功能**
   - 學習者社群
   - 教師資源分享
   - 家長交流平台

---

*此文件整合了 Audrey Math 項目的所有核心內容，包含 HTML 結構、CSS 樣式、JavaScript 功能、新增特色和改進建議，方便進行全面的項目分析和優化。*
