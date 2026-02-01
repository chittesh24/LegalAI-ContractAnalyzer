# Setup script for Contract Analysis Bot (Windows PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Contract Analysis Bot - Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "✓ Checking Python version..." -ForegroundColor Green
python --version

# Create virtual environment
Write-Host "✓ Creating virtual environment..." -ForegroundColor Green
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "✓ Installing dependencies..." -ForegroundColor Green
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
Write-Host "✓ Downloading spaCy English model..." -ForegroundColor Green
python -m spacy download en_core_web_sm

# Create .env file if doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "✓ Creating .env file..." -ForegroundColor Green
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit .env file and add your API key!" -ForegroundColor Yellow
    Write-Host "   - For Claude: Get key from https://console.anthropic.com/" -ForegroundColor Yellow
    Write-Host "   - For GPT-4: Get key from https://platform.openai.com/" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Edit .env file and add your API key"
Write-Host "2. Run: .\venv\Scripts\Activate.ps1"
Write-Host "3. Run: python run.py"
Write-Host ""
