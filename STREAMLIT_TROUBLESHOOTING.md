# 🔧 Streamlit Deployment Troubleshooting

## Common Errors & Solutions

---

### ❌ Error 1: "Deployment takes too long / Times out"

**Cause:** Installing all packages takes >10 minutes

**Solutions:**

#### Option A: Use Lighter Requirements (Recommended)
Already done! Your `requirements.txt` is optimized.

#### Option B: Check Deployment Logs
1. Go to your app on Streamlit Cloud
2. Click "Manage app" (bottom right)
3. View "Logs" tab
4. Look for specific error

---

### ❌ Error 2: "ModuleNotFoundError: No module named 'spacy'"

**Cause:** spaCy installation failed

**Solution 1 - Wait Longer:**
```
spaCy installation can take 5-7 minutes on Streamlit Cloud.
Let it finish - don't cancel!
```

**Solution 2 - Alternative spaCy install:**
Replace in `requirements.txt`:
```txt
# Instead of wheel URL, use:
spacy==3.7.2
```

Then add a file `setup.sh`:
```bash
#!/bin/bash
python -m spacy download en_core_web_sm
```

---

### ❌ Error 3: "Model 'en_core_web_sm' not found"

**Cause:** spaCy model didn't download

**Solution:**
The wheel URL in requirements.txt should handle this.
If it doesn't work, create `setup.sh`:

```bash
#!/bin/bash
python -m spacy download en_core_web_sm
```

---

### ❌ Error 4: "ANTHROPIC_API_KEY not found"

**Cause:** Secrets not configured

**Solution:**
1. Go to app Settings (⚙️)
2. Click "Secrets"
3. Add:
```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
LLM_PROVIDER = "anthropic"
```
4. Save and wait for restart

---

### ❌ Error 5: "FileNotFoundError: uploads/ directory"

**Cause:** Directory creation failed

**Solution:**
Already fixed in `config.py` with `.mkdir(exist_ok=True)`

If still an issue, add to `app.py` at the top:
```python
import os
from pathlib import Path

# Ensure directories exist
Path("uploads").mkdir(exist_ok=True)
Path("outputs").mkdir(exist_ok=True)
Path("audit_logs").mkdir(exist_ok=True)
```

---

### ❌ Error 6: "PDF processing fails"

**Cause:** Missing system dependencies

**Solution:**
Create `packages.txt` file (already done!):
```txt
poppler-utils
```

---

### ❌ Error 7: "App crashes after deployment"

**Cause:** Import error or missing dependency

**Solution:**
1. Check Streamlit logs
2. Look for "ImportError" or "ModuleNotFoundError"
3. Verify that module is in requirements.txt
4. Redeploy

---

## 🚀 Optimal Deployment Process

### Step-by-Step (Avoiding Issues)

#### 1. Before Deploying:

```bash
# Test locally first
cd LegalAI_ContractAnalyzer
pip install -r requirements.txt
streamlit run app.py

# If local works, deployment should work!
```

#### 2. Push to GitHub:

```bash
# Make sure requirements.txt is committed
git add requirements.txt packages.txt
git commit -m "Optimize for Streamlit deployment"
git push origin main
```

#### 3. Deploy to Streamlit:

- **Wait patiently** - Initial deployment takes 7-10 minutes
- **Don't refresh** - This can interrupt deployment
- **Watch logs** - See what's being installed

#### 4. After Deployment:

- Add secrets immediately
- Test the app
- If errors, check logs

---

## ⚡ Fast Deployment Alternative

If standard deployment keeps failing, try this minimal approach:

### Create `requirements-minimal.txt`:
```txt
streamlit==1.29.0
python-dotenv==1.0.0
anthropic==0.18.1
spacy==3.7.2
PyPDF2==3.0.1
python-docx==1.1.0
pandas==2.1.4
```

### Rename in Streamlit:
1. In Streamlit Cloud app settings
2. Advanced settings
3. Change requirements file to `requirements-minimal.txt`

This installs faster but you'll need to:
- Download spaCy model manually (add `setup.sh`)
- May lose some features temporarily

---

## 🔍 How to Read Streamlit Logs

### Key Log Sections:

**1. Package Installation:**
```
Collecting streamlit==1.29.0...
Successfully installed streamlit-1.29.0
```
✅ Good - packages installing

**2. spaCy Model:**
```
Collecting en_core_web_sm...
Successfully installed en-core-web-sm-3.7.0
```
✅ Good - model installed

**3. App Start:**
```
You can now view your Streamlit app in your browser.
```
✅ Good - app is running!

**4. Errors:**
```
ModuleNotFoundError: No module named 'xyz'
```
❌ Bad - missing package

---

## 🆘 Still Not Working?

### Quick Fixes:

#### Fix 1: Simplify requirements.txt
Remove optional packages temporarily:
```txt
# Comment out these if needed:
# openai==1.12.0
# pdfplumber==0.10.3
# reportlab==4.0.8
```

#### Fix 2: Use Hugging Face Spaces Instead
If Streamlit keeps failing:
1. Go to https://huggingface.co/spaces
2. Create new Space
3. Choose Streamlit SDK
4. Upload your files
5. Easier deployment sometimes!

#### Fix 3: Railway.app Alternative
1. Go to https://railway.app
2. Deploy from GitHub
3. Add environment variables
4. Usually faster deployment

---

## ✅ Deployment Success Checklist

After successful deployment:

- [ ] App loads without errors
- [ ] All tabs visible
- [ ] Can upload file
- [ ] Analysis works (may take 60s)
- [ ] Results display
- [ ] No error messages in logs

---

## 📊 Expected Deployment Times

| Step | Duration |
|------|----------|
| Push to GitHub | 1 min |
| Queue in Streamlit | 0-2 min |
| Install packages | 5-7 min |
| Install spaCy model | 2-3 min |
| Start app | 1 min |
| **Total** | **9-14 min** |

**Don't panic if it takes 10+ minutes on first deploy!**

---

## 🎯 If All Else Fails

### Minimal Working Version:

Create a new `app_minimal.py`:
```python
import streamlit as st

st.title("LegalAI ContractAnalyzer")
st.write("Basic version - testing deployment")

uploaded_file = st.file_uploader("Upload contract")
if uploaded_file:
    st.success("File uploaded!")
    st.write(f"File: {uploaded_file.name}")
```

Deploy this first to verify Streamlit works, then add features back gradually.

---

## 📝 Error Log Template

When reporting issues, include:

**1. Error message:**
```
[Copy exact error from logs]
```

**2. Deployment time:**
```
Started: [time]
Failed at: [time]
Total: [duration]
```

**3. What you've tried:**
```
- [ ] Waited 15+ minutes
- [ ] Checked secrets are set
- [ ] Verified requirements.txt
- [ ] Tested locally
```

---

## ✅ Most Common Solution

**90% of deployment issues are solved by:**

1. **Waiting longer** - First deploy takes 10-15 minutes
2. **Checking secrets** - ANTHROPIC_API_KEY must be set
3. **Reviewing logs** - Look for specific error message

**Be patient with first deployment!** ⏱️

---

**Need more help? Let me know the specific error message from Streamlit logs!**
