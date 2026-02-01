#!/bin/bash
# Setup script for Contract Analysis Bot (Linux/Mac)

echo "=========================================="
echo "Contract Analysis Bot - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Create virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
echo "✓ Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Create .env file if doesn't exist
if [ ! -f .env ]; then
    echo "✓ Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your API key!"
    echo "   - For Claude: Get key from https://console.anthropic.com/"
    echo "   - For GPT-4: Get key from https://platform.openai.com/"
fi

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API key"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python run.py"
echo ""
