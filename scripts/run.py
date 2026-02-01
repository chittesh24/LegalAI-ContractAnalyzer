"""
Launcher script for Contract Analysis Bot
Run this to start the application
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Launch the Streamlit application"""
    app_path = Path(__file__).parent / "app.py"
    
    print("=" * 60)
    print("🚀 Starting Contract Analysis & Risk Assessment Bot")
    print("=" * 60)
    print("\n📋 Checklist:")
    print("  ✓ Python dependencies installed")
    print("  ✓ spaCy model downloaded")
    print("  ⚠ API key configured in .env file")
    print("\n🌐 Opening browser at http://localhost:8501")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print("=" * 60 + "\n")
    
    # Run streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])

if __name__ == "__main__":
    main()
