# ⚡ Quick Deploy Guide - 3 Commands

## 🚀 Deploy in 12 Minutes

### Step 1: Push to GitHub (2 min)

```bash
cd LegalAI_ContractAnalyzer

git init
git add .
git commit -m "Initial commit: LegalAI ContractAnalyzer"
git remote add origin https://github.com/YOUR_USERNAME/LegalAI-ContractAnalyzer.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your GitHub username!**

---

### Step 2: Deploy to Streamlit (10 min)

1. Go to: **https://streamlit.io/cloud**
2. Sign in with GitHub
3. Click **"New app"**
4. Fill in:
   - Repository: `YOUR_USERNAME/LegalAI-ContractAnalyzer`
   - Branch: `main`
   - Main file: `app.py`
5. Click **"Deploy"**
6. **Wait 10-15 minutes** ⏱️ (don't refresh!)

---

### Step 3: Add API Key (1 min)

After deployment completes:

1. Click ⚙️ **Settings** → **Secrets**
2. Add:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
LLM_PROVIDER = "anthropic"
```

3. Click **"Save"**
4. App restarts automatically ✅

---

## ✅ Done!

Your URLs:
- **GitHub:** `https://github.com/YOUR_USERNAME/LegalAI-ContractAnalyzer`
- **Live App:** `https://your-app.streamlit.app`

---

## 🐛 If Deployment Fails

See: **STREAMLIT_TROUBLESHOOTING.md** for solutions

**Most common fix:** Wait 15 minutes on first deploy!

---

## 🎯 Test Your App

1. Open live URL
2. Upload `templates/sample_vendor_contract.txt`
3. Click "Analyze Contract"
4. Wait ~60 seconds
5. See results: HIGH RISK (82/100) ✅

---

**Total Time: 12 minutes from code to live app!** 🚀
