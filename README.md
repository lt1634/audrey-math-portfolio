# Audrey Math 安蕎的數學 - Educational Platform

A modern, bilingual educational platform for mathematics learning with interactive features and a beautiful user interface.

## 🌟 Features

- **Bilingual Support**: English and Traditional Chinese (繁體中文)
- **Dark/Light Mode**: Toggle between themes with smooth transitions
- **Responsive Design**: Works perfectly on all devices
- **Modern UI**: Clean, professional design with organic shapes
- **Interactive Elements**: Smooth animations and hover effects
- **6-Stage Learning System**: Comprehensive math learning progression
- **API Quota Management**: Built-in usage limits and cost control
- **STEM Integration**: Science, Technology, Engineering, Arts, and Mathematics
- **Play-Based Learning**: Interactive games and hands-on activities
- **Global Resources**: Curated international educational content

## 🔒 API Quota Management

### **配額設定**
- **每日請求限制**: 50 次
- **每小時請求限制**: 10 次  
- **每日字符限制**: 25,000 字符
- **每小時字符限制**: 2,500 字符
- **請求間隔**: 3 秒

### **監控使用量**
```bash
# 檢查配額狀態
python3 quota_checker.py

# 重置每日配額
python3 quota_checker.py reset
```

### **費用控制**
- **預估月費用**: $0.38
- **預估年費用**: $4.56
- **自動配額管理**: 防止超限使用

## 🚀 Live Demo

Visit the live website: [Audrey Math Platform](https://your-username.github.io/audrey-math-portfolio)

## 🛠️ Technologies Used

- **HTML5**: Semantic markup and structure
- **CSS3**: Modern styling with CSS variables and animations
- **JavaScript**: Interactive functionality and language switching
- **Font Awesome**: Icons and visual elements
- **Google Fonts**: Typography (Inter + Noto Sans TC)

## 📁 Project Structure

```
audrey-math-portfolio/
├── index.html          # Main HTML file
├── styles.css          # CSS styles and animations
├── script.js           # JavaScript functionality
├── audrey-math-logo.svg # Logo SVG file
├── Audrey-Math-profile.jpg # Profile image
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## 🎨 Design Features

- **Modern Color Palette**: Clean grays with gradient accents
- **Organic Shapes**: Floating background elements
- **Typography**: Professional font pairing
- **Animations**: Smooth transitions and micro-interactions
- **Accessibility**: Proper contrast and focus states

## 🌐 Language Support

- **English**: Complete interface translation
- **Traditional Chinese**: 繁體中文完整翻譯
- **Language Toggle**: Seamless switching between languages
- **Font Support**: Proper Chinese character rendering

## 📱 Responsive Design

- **Mobile First**: Optimized for mobile devices
- **Tablet Support**: Perfect layout for tablets
- **Desktop**: Enhanced experience on larger screens
- **Cross-Browser**: Compatible with all modern browsers

## 🚀 Deployment

### Vercel (Recommended) ⭐

**🌍 Live Demo**: [audrey-math-portfolio-usn6.vercel.app](https://audrey-math-portfolio-usn6-26g879u9x-lt1634s-projects.vercel.app/)

1. **Import** your GitHub repository to Vercel
2. **Framework Preset**: Other (Static Site)
3. **Build Command**: (leave empty)
4. **Output Directory**: (leave empty)
5. **Deploy** automatically on every push

**Advantages**:
- ⚡ Global CDN for faster loading
- 🔄 Automatic deployments from GitHub
- 📊 Built-in analytics and monitoring
- 🆓 Generous free tier

### GitHub Pages (Deprecated)

~~GitHub Pages deployment has been disabled in favor of Vercel for better performance.~~

### Netlify (Alternative)

1. **Connect** your GitHub repository to Netlify
2. **Build Settings**:
   - Build command: (leave empty)
   - Publish directory: `/` (root)
3. **Deploy** automatically on every push

## 🔧 Local Development

1. **Clone** the repository:
   ```bash
   git clone https://github.com/your-username/audrey-math-portfolio.git
   cd audrey-math-portfolio
   ```

2. **Open** `index.html` in your browser or use a local server:
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   ```

3. **Visit** `http://localhost:8000` in your browser

## 📝 Customization

### Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --bg-primary: #f8fafc;
    --text-primary: #1e293b;
    --text-accent: #3b82f6;
    /* ... more variables */
}
```

### Content
- **Text**: Edit content in `index.html`
- **Images**: Replace `Audrey-Math-profile.jpg` with your image
- **Logo**: Modify `audrey-math-logo.svg`

### Languages
- **Add Translations**: Use `data-en` and `data-zh` attributes
- **New Languages**: Extend the JavaScript language system

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Commit** changes: `git commit -m 'Add feature'`
4. **Push** to branch: `git push origin feature-name`
5. **Submit** a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📚 Educational Resources

### 🧮 Math Learning Tools

#### **Mighty Mind Basic 卓越思考拼圖**
- **適用年齡**: 3-6歲
- **學習目標**: 幾何圖形認知、空間概念建立、數學邏輯思維
- **特色**: 32片不同大小的彩色塑膠方塊，涵蓋6種基本幾何圖形
- **教育理論**: 基於皮亞傑認知發展理論，通過具體操作建立抽象概念

#### **Swift 不插電程式遊戲 - 迷宮**
- **適用年齡**: 4歲以上
- **學習目標**: 邏輯思考、問題解決、最佳路徑概念
- **遊戲方式**: 使用指令卡引導角色從起點到終點
- **指令類型**: moveForward(), turnLeft(), turnRight(), end()

#### **復活節彩蛋 - 最佳路徑遊戲**
- **適用年齡**: 4-6歲
- **學習目標**: 最佳路徑 (Optimal Path)、數數、簡易加法
- **核心概念**: 從起點到終點，用最少步數獲得最多彩蛋
- **生活應用**: 路線規劃、時間管理、成本效益分析

### 🌍 Global STEM Resources

#### **美國兒童科學網站 (11個推薦)**
1. **Frontiers for Young Minds** - 8-15歲科學教育
2. **USGS Earthquakes for Kids** - 地球科學與地理學
3. **Chemicool** - 化學元素學習
4. **NASA Galileo Legacy Site** - 天文學探索
5. **Smithsonian Air & Space Museum** - 太空與航空
6. **NASA Climate Kids** - 氣候變遷教育
7. **The Lorax Project** - 生態保育
8. **My First Garden** - 園藝與植物學
9. **Farmer's Almanac for Kids** - 天文觀測
10. **Building Big** - 土木工程與建築
11. **Discovery Kids** - 多元科學領域

#### **國際教育研究**
- **澳洲蒙納許大學 STEM 研究**: 320萬澳幣基金支持的概念樂園實驗室
- **小班制對女孩 STEM 學習的影響**: 康乃爾大學研究顯示小班制提升女性參與度
- **108課綱素養教育**: STEAM 繪遊書系列，整合知識、態度、技能

### 🎯 Learning Methodology

#### **Play-Based Learning (以玩為基礎的學習)**
- **核心理念**: 透過遊戲和想像力刺激腦神經發育
- **五大步驟**: 發問 → 觀察/思考 → 假設/設計 → 行動/創造 → 評估和改良
- **適用年齡**: 0-3歲大腦發展關鍵期，持續至學齡期

#### **STEAM 整合教育**
- **Science (科學)**: 自然現象觀察與實驗
- **Technology (科技)**: 工具使用與創新思維
- **Engineering (工程)**: 問題解決與設計思維
- **Arts (藝術)**: 創意表達與美感培養
- **Mathematics (數學)**: 邏輯推理與數量概念

### 📖 Recommended Reading

#### **《跟大師學創造力》系列**
- **全美科學教師協會推薦**
- **近200個STEAM實驗**
- **涵蓋大師**: 伽利略、牛頓、達爾文、達文西、貝多芬、愛因斯坦、梵谷等
- **適合年齡**: 小學中高年級以上

#### **《孩子的第一套STEAM繪遊書》**
- **台灣原創科普書**
- **真實事件改編**
- **問題導向學習**
- **素養教育核心精神**

## 📞 Contact

- **Website**: [Audrey Math Platform](https://your-username.github.io/audrey-math-portfolio)
- **Email**: your-email@example.com

---

Made with ❤️ for mathematics education