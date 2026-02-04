# 🏆 LegalAI ContractAnalyzer

> **AI-Powered Legal Assistant for Indian SMEs**  
> Analyze contracts in 60 seconds • Identify 8 risk types • Plain English explanations • Hindi support

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GenAI Hackathon](https://img.shields.io/badge/GenAI-Hackathon%202024-orange.svg)](https://github.com/yourusername/LegalAI-ContractAnalyzer)

---

## 🎯 Problem Statement

**Problem #174: Contract Analysis & Risk Assessment Bot**

63 million SMEs in India lack resources for legal contract review, costing ₹10,000-50,000 per contract and taking 3-5 days. This leads to:
- Signing unfavorable agreements
- Missing hidden risky clauses
- Costly legal disputes
- Business growth constraints

**65% of SME legal disputes stem from poorly understood contract terms.**

---

## 💡 Solution

**LegalAI ContractAnalyzer** democratizes legal intelligence for Indian SMEs using AI-powered analysis:

✅ **Instant Analysis** - Under 60 seconds (vs 3-5 days)  
✅ **Risk Detection** - 8 categories, scored 0-100  
✅ **Plain English** - No legal jargon  
✅ **Smart Recommendations** - Alternative clauses for negotiation  
✅ **Indian Law Compliance** - Contract Act, jurisdiction checking  
✅ **Bilingual** - English + Hindi support  
✅ **Template Generator** - Create 10 fair contract types  
✅ **Knowledge Base** - 15+ common issues documented  

---

## ✨ Key Features

### Core Capabilities (All 50 Requirements Met ✅)

**Legal NLP Tasks:**
- Contract type classification (10 types)
- Clause & sub-clause extraction
- Named entity recognition (parties, dates, amounts, jurisdiction)
- Obligation vs. Right vs. Prohibition identification
- Ambiguity detection (30+ vague terms)
- Risk & compliance detection

**Risk Assessment:**
- Clause-level scores (Low/Medium/High)
- Contract-level composite score (0-100)
- 8 risk categories: Penalty, Indemnity, Unilateral Termination, Arbitration, Auto-Renewal, Lock-in, Non-compete, IP Transfer

**User Outputs:**
- Simplified contract summary
- Clause-by-clause explanations
- Unfavorable terms highlighted
- Alternative clause suggestions
- PDF export for legal review

### 🌟 Bonus Features

1. **Contract Template Generator** - 10 template types with interactive forms
2. **SME Knowledge Base** - 15+ documented issues with solutions
3. **Best Practices Library** - Tips, red flags, negotiation strategies
4. **Indian Law Guide** - Contract Act 1872, employment laws
5. **Search Functionality** - Query knowledge base
6. **Automated Testing** - 7 validation tests
7. **Comprehensive Docs** - 12 guides (95KB)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- API key for Claude (Anthropic) or GPT-4 (OpenAI)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/LegalAI-ContractAnalyzer.git
cd LegalAI-ContractAnalyzer

# 2. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 3. Configure API key
cp .env.example .env
# Edit .env and add your API key:
# ANTHROPIC_API_KEY=sk-ant-xxxxx  OR
# OPENAI_API_KEY=sk-xxxxx

# 4. Run application
streamlit run app.py
```

Browser opens at `http://localhost:8501`

### Run Tests

```bash
python scripts/test_contract_analyzer.py
```

---

## 🎬 Demo

### Live Application
**🌐 Deployed URL:** [Your Streamlit Cloud URL]

### Demo Video
**🎥 Watch Demo:** [Your YouTube URL]

### Try It Out
1. Upload `templates/sample_vendor_contract.txt`
2. Click "Analyze Contract"
3. View HIGH RISK (82/100) with 8 critical issues
4. Explore all 6 tabs:
   - Analysis Results
   - Clause Explorer
   - Contract Templates
   - Knowledge Base
   - Export

---

## 📊 Project Structure

```
LegalAI-ContractAnalyzer/
│
├── app.py                          # Main Streamlit UI
├── contract_analyzer.py            # Orchestrator
├── document_parser.py              # PDF/DOCX/TXT parsing
├── nlp_processor.py               # spaCy NLP analysis
├── risk_analyzer.py               # Risk detection engine
├── llm_interface.py               # Claude/GPT-4 integration
├── template_generator.py          # Contract templates
├── knowledge_base.py              # SME knowledge base
├── report_generator.py            # PDF export
├── audit_logger.py                # Activity logging
├── app_enhanced.py                # Template & KB UI
├── config.py                      # Configuration
│
├── requirements.txt                # Dependencies
├── .env.example                   # API key template
├── .gitignore                     # Git exclusions
│
├── templates/                      # Sample contracts
│   ├── sample_vendor_contract.txt
│   ├── sample_employment_agreement.txt
│   └── balanced_service_contract.txt
│
├── .streamlit/                    # Streamlit config
│   └── config.toml
│
├── scripts/                       # Helper scripts
│   ├── setup.sh
│   ├── setup.ps1
│   ├── run.py
│   └── test_contract_analyzer.py
│
└── docs/                          # Documentation (local reference)
    └── ... (submission guides, not in GitHub)
```

---

## 🛠️ Technology Stack

**AI/ML:**
- Claude 3 Sonnet / GPT-4 (legal reasoning)
- spaCy + NLTK (NLP processing)

**Backend:**
- Python 3.8+
- Document processing: PyPDF2, pdfplumber, python-docx
- PDF generation: ReportLab

**Frontend:**
- Streamlit (interactive UI)

**Storage:**
- JSON-based audit logs
- Local file system

---

## 🎯 Use Cases

### For SME Business Owners:
- Review vendor contracts before signing
- Understand employment agreements
- Negotiate service contracts
- Create fair freelancer agreements
- Learn contract best practices

### For Startups:
- Quick legal due diligence
- Template generation for standard contracts
- Risk assessment for partnerships
- Educational resource for founders

### For Consultants:
- Initial contract screening
- Client education tool
- Time-saving preliminary analysis
- Knowledge base reference

---

## 🏆 Unique Differentiators

1. ✅ **Only bilingual SME legal AI** (English + Hindi)
2. ✅ **Only template generator** (creates contracts, not just analyzes)
3. ✅ **Only knowledge base** (15+ issues with solutions)
4. ✅ **100% requirements met** (50/50 + 7 bonuses)
5. ✅ **Production-ready** (modular, tested, documented)
6. ✅ **Indian law focus** (Contract Act, jurisdiction)
7. ✅ **SME-centric** (built for business owners, not lawyers)

---

## 📈 Business Impact

**Target Market:** 63 million SMEs in India

**Value Proposition:**
| Before | After | Improvement |
|--------|-------|-------------|
| ₹10-50K cost | FREE | 100% savings |
| 3-5 days | 60 seconds | 99% faster |
| Legal jargon | Plain English | 100% accessible |
| Unknown risks | Highlighted | Risk prevention |

**Market Opportunity:** ₹6,300 crore (63M SMEs × ₹1,000/year)

---

## 🧪 Testing

Run comprehensive test suite:

```bash
python scripts/test_contract_analyzer.py
```

**Tests include:**
1. Document parsing (PDF, DOCX, TXT)
2. Clause extraction
3. Entity recognition
4. Risk analysis
5. Full analysis pipeline
6. Template generation
7. Knowledge base

**Expected:** 7/7 tests pass ✅

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

**Built for:** GenAI Hackathon 2024  
**Problem:** #174 - Contract Analysis & Risk Assessment Bot  
**Technologies:** Claude 3, spaCy, Streamlit, Python  

---

## 📞 Contact

**Project:** LegalAI ContractAnalyzer  
**GitHub:** https://github.com/chittesh24/ 
**Demo:** https://aicontractanalyzer-q45dyqcf69omb.streamlit.app/
**Created by:** Chittesh S  
**Email:** chittesh.work@gmail.com  


---

**⭐ If this project helps you, please star the repository!**

---

**Built with ❤️ for India's 63 million SMEs**
