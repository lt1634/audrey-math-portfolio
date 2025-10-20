# 🚀 Deployment Guide for Audrey Math Platform

This guide will help you deploy your Audrey Math educational platform to various hosting services.

## 📋 Pre-Deployment Checklist

- [ ] All files are ready (`index.html`, `styles.css`, `script.js`)
- [ ] Profile image is properly named (`Audrey-Math-profile.jpg`)
- [ ] Logo SVG is updated (`audrey-math-logo.svg`)
- [ ] `.gitignore` file is created
- [ ] README.md is updated
- [ ] Test the website locally

## 🌐 GitHub Pages (Recommended)

### Step 1: Create GitHub Repository
1. Go to [GitHub](https://github.com) and sign in
2. Click "New repository"
3. Name it: `audrey-math-portfolio` or `audrey-math-platform`
4. Make it **Public** (required for free GitHub Pages)
5. Don't initialize with README (you already have one)

### Step 2: Upload Files
```bash
# Navigate to your project folder
cd /Users/tim/Desktop/Learn

# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Audrey Math educational platform"

# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/audrey-math-portfolio.git

# Push to GitHub
git push -u origin main
```

### Step 3: Enable GitHub Pages
1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll down to **Pages** section
4. Under **Source**, select "Deploy from a branch"
5. Choose **main** branch
6. Select **/ (root)** folder
7. Click **Save**

### Step 4: Access Your Site
- Your site will be available at: `https://YOUR_USERNAME.github.io/audrey-math-portfolio`
- It may take 5-10 minutes to deploy initially

## ☁️ Netlify (Alternative)

### Method 1: Drag & Drop
1. Go to [Netlify](https://netlify.com)
2. Sign up/login with GitHub
3. Drag your project folder to the deploy area
4. Your site will be live instantly!

### Method 2: GitHub Integration
1. Connect your GitHub account to Netlify
2. Select your repository
3. Build settings:
   - Build command: (leave empty)
   - Publish directory: `/` (root)
4. Click "Deploy site"

## ⚡ Vercel (Alternative)

1. Go to [Vercel](https://vercel.com)
2. Sign up with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Framework Preset: **Other**
6. Build Command: (leave empty)
7. Output Directory: (leave empty)
8. Click "Deploy"

## 🔧 Custom Domain (Optional)

### GitHub Pages
1. Add a `CNAME` file to your repository root:
   ```
   your-domain.com
   ```
2. Configure DNS with your domain provider:
   - Type: CNAME
   - Name: www
   - Value: YOUR_USERNAME.github.io

### Netlify/Vercel
1. Go to Domain settings
2. Add your custom domain
3. Follow the DNS configuration instructions

## 📱 Testing Your Deployment

After deployment, test these features:
- [ ] Website loads correctly
- [ ] Language toggle works (English/Chinese)
- [ ] Dark/Light mode toggle works
- [ ] All sections are visible
- [ ] Profile image displays properly
- [ ] Responsive design works on mobile
- [ ] All animations and transitions work

## 🔄 Updating Your Site

To update your deployed site:

```bash
# Make your changes to files
# Then commit and push:

git add .
git commit -m "Update: describe your changes"
git push origin main
```

- **GitHub Pages**: Updates automatically (may take a few minutes)
- **Netlify/Vercel**: Updates automatically on every push

## 🐛 Troubleshooting

### Common Issues:

**Profile image not showing:**
- Check file name is exactly `Audrey-Math-profile.jpg`
- Ensure file is in the root directory
- Check file size (should be under 5MB)

**Language toggle not working:**
- Check browser console for JavaScript errors
- Ensure `script.js` is properly linked
- Test locally first

**Styling issues:**
- Check `styles.css` is properly linked
- Clear browser cache
- Test in different browsers

**GitHub Pages not updating:**
- Check repository is public
- Wait 10-15 minutes for deployment
- Check GitHub Actions tab for errors

## 📞 Support

If you encounter issues:
1. Check the browser console for errors
2. Test locally first
3. Check file names and paths
4. Ensure all files are committed to git

## 🎉 Success!

Once deployed, your Audrey Math educational platform will be live and accessible worldwide!

**Live URL**: `https://YOUR_USERNAME.github.io/audrey-math-portfolio`

---

Happy deploying! 🚀
