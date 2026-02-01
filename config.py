"""
Configuration module for Contract Analysis Bot
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
AUDIT_LOG_DIR = BASE_DIR / "audit_logs"
TEMPLATES_DIR = BASE_DIR / "templates"

# Create directories if they don't exist
for directory in [UPLOAD_DIR, OUTPUT_DIR, AUDIT_LOG_DIR, TEMPLATES_DIR]:
    directory.mkdir(exist_ok=True)

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")  # 'anthropic' or 'openai'
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "claude-3-sonnet-20240229")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

# Feature Flags
ENABLE_HINDI = os.getenv("ENABLE_HINDI", "true").lower() == "true"
ENABLE_AUDIT_LOGS = os.getenv("ENABLE_AUDIT_LOGS", "true").lower() == "true"
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# Contract Types
CONTRACT_TYPES = [
    "Employment Agreement",
    "Vendor Contract",
    "Lease Agreement",
    "Partnership Deed",
    "Service Contract",
    "Non-Disclosure Agreement (NDA)",
    "Consultant Agreement",
    "Purchase Agreement",
    "Licensing Agreement",
    "Other"
]

# Risk Levels
RISK_LEVELS = {
    "LOW": {"score": 1, "color": "#28a745", "label": "Low Risk"},
    "MEDIUM": {"score": 2, "color": "#ffc107", "label": "Medium Risk"},
    "HIGH": {"score": 3, "color": "#dc3545", "label": "High Risk"}
}

# Risk Indicators - Patterns to detect high-risk clauses
RISK_INDICATORS = {
    "penalty": ["penalty", "liquidated damages", "fine", "forfeit"],
    "indemnity": ["indemnify", "indemnification", "hold harmless"],
    "unilateral_termination": ["terminate at will", "without cause", "sole discretion"],
    "arbitration": ["arbitration", "dispute resolution", "mediation"],
    "auto_renewal": ["auto-renew", "automatically renew", "automatic renewal"],
    "lock_in": ["lock-in", "minimum term", "fixed period"],
    "non_compete": ["non-compete", "non-competition", "shall not compete"],
    "ip_transfer": ["intellectual property", "IP rights", "transfer of rights", "assignment of rights"]
}

# Indian Law Compliance Keywords
INDIAN_LAW_KEYWORDS = [
    "Indian Contract Act",
    "Companies Act",
    "Labour Laws",
    "GST",
    "jurisdiction",
    "governing law",
    "Indian courts"
]

# Supported Languages
SUPPORTED_LANGUAGES = ["en", "hi"]  # English, Hindi

# File Upload Settings
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".doc", ".txt"]
