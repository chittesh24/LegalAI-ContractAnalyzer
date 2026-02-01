"""
Streamlit UI for Contract Analysis Bot
"""
import streamlit as st
from pathlib import Path
import json
from datetime import datetime
import sys

from contract_analyzer import ContractAnalyzer
from report_generator import ReportGenerator
from audit_logger import AuditLogger
from template_generator import TemplateGenerator
from knowledge_base import KnowledgeBase
from app_enhanced import show_template_section, show_knowledge_base_section
from config import UPLOAD_DIR, OUTPUT_DIR, CONTRACT_TYPES, RISK_LEVELS, MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Page configuration
st.set_page_config(
    page_title="Contract Analysis Bot",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f3c88;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-high {
        color: #dc3545;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .risk-medium {
        color: #ffc107;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .risk-low {
        color: #28a745;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .clause-box {
        border: 1px solid #ddd;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        background-color: #f8f9fa;
    }
    .recommendation-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = ContractAnalyzer()
if 'report_generator' not in st.session_state:
    st.session_state.report_generator = ReportGenerator()
if 'audit_logger' not in st.session_state:
    st.session_state.audit_logger = AuditLogger()
if 'template_generator' not in st.session_state:
    st.session_state.template_generator = TemplateGenerator()
if 'knowledge_base' not in st.session_state:
    st.session_state.knowledge_base = KnowledgeBase()


def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">📄 Contract Analysis & Risk Assessment Bot</h1>', 
                unsafe_allow_html=True)
    st.markdown("### AI-Powered Legal Assistant for SME Business Owners")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        use_llm = st.checkbox("Enable AI Analysis", value=True, 
                             help="Use Claude/GPT-4 for advanced legal reasoning")
        
        st.markdown("---")
        st.header("📚 About")
        st.info("""
        This tool helps you:
        - Understand complex contracts
        - Identify potential risks
        - Get plain-language explanations
        - Receive negotiation suggestions
        - Check Indian law compliance
        """)
        
        st.markdown("---")
        st.header("📊 Supported Files")
        st.write("• PDF (text-based)")
        st.write("• DOCX/DOC")
        st.write("• TXT")
        st.write(f"• Max size: {MAX_FILE_SIZE_MB}MB")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📤 Upload & Analyze", 
        "📊 Analysis Results", 
        "🔍 Clause Explorer", 
        "📝 Contract Templates",
        "📚 Knowledge Base",
        "📥 Export"
    ])
    
    with tab1:
        show_upload_section(use_llm)
    
    with tab2:
        show_results_section()
    
    with tab3:
        show_clause_explorer()
    
    with tab4:
        show_template_section()
    
    with tab5:
        show_knowledge_base_section()
    
    with tab6:
        show_export_section()


def show_upload_section(use_llm: bool):
    """File upload and analysis section"""
    st.header("Upload Contract for Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a contract file",
            type=['pdf', 'docx', 'doc', 'txt'],
            help=f"Upload contracts in PDF, DOCX, or TXT format (max {MAX_FILE_SIZE_MB}MB)"
        )
    
    with col2:
        st.markdown("#### Quick Tips")
        st.markdown("""
        - Upload clear, text-based documents
        - Hindi contracts are supported
        - Analysis takes 30-60 seconds
        """)
    
    if uploaded_file is not None:
        # Check file size
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        if file_size_mb > MAX_FILE_SIZE_MB:
            st.error(f"File too large! Maximum size is {MAX_FILE_SIZE_MB}MB")
            return
        
        # Display file info
        st.success(f"✅ File uploaded: {uploaded_file.name} ({file_size_mb:.2f}MB)")
        
        # Save uploaded file
        file_path = UPLOAD_DIR / uploaded_file.name
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Analyze button
        if st.button("🚀 Analyze Contract", type="primary", use_container_width=True):
            with st.spinner("🔍 Analyzing contract... This may take a minute..."):
                try:
                    # Perform analysis
                    result = st.session_state.analyzer.analyze_contract(file_path, use_llm=use_llm)
                    
                    if result["success"]:
                        st.session_state.analysis_result = result
                        
                        # Log analysis
                        st.session_state.audit_logger.log_analysis(result)
                        
                        # Save results
                        output_file = OUTPUT_DIR / f"{uploaded_file.name}_analysis.json"
                        st.session_state.analyzer.save_analysis(result, output_file)
                        
                        st.success("✅ Analysis complete! Check the 'Analysis Results' tab.")
                        st.balloons()
                    else:
                        st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")


def show_results_section():
    """Display analysis results"""
    if st.session_state.analysis_result is None:
        st.info("👆 Upload and analyze a contract first to see results here.")
        return
    
    result = st.session_state.analysis_result
    risk_analysis = result.get('risk_analysis', {})
    llm_analysis = result.get('llm_analysis', {})
    
    # Executive Summary
    st.header("📋 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Contract Type", 
                 llm_analysis.get('contract_type', {}).get('contract_type', 'Unknown'))
    
    with col2:
        risk_level = risk_analysis.get('overall_risk_level', 'UNKNOWN')
        risk_color = RISK_LEVELS.get(risk_level, {}).get('color', '#666')
        st.markdown(f"**Risk Level**")
        st.markdown(f'<p class="risk-{risk_level.lower()}">{risk_level}</p>', 
                   unsafe_allow_html=True)
    
    with col3:
        st.metric("Risk Score", f"{risk_analysis.get('composite_risk_score', 0)}/100")
    
    with col4:
        st.metric("Total Clauses", risk_analysis.get('total_clauses_analyzed', 0))
    
    st.markdown("---")
    
    # Risk Distribution
    st.subheader("⚠️ Risk Distribution")
    dist = risk_analysis.get('risk_distribution', {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔴 High Risk", dist.get('high', 0))
    with col2:
        st.metric("🟡 Medium Risk", dist.get('medium', 0))
    with col3:
        st.metric("🟢 Low Risk", dist.get('low', 0))
    
    st.markdown("---")
    
    # Key Entities
    st.subheader("🏢 Key Information Extracted")
    entities = result.get('entities', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        if entities.get('parties'):
            st.write("**Parties:**")
            for party in entities['parties'][:5]:
                st.write(f"• {party}")
        
        if entities.get('amounts'):
            st.write("**Financial Amounts:**")
            for amount in entities['amounts'][:5]:
                st.write(f"• {amount}")
    
    with col2:
        if entities.get('dates'):
            st.write("**Important Dates:**")
            for date in entities['dates'][:5]:
                st.write(f"• {date}")
        
        if entities.get('locations'):
            st.write("**Locations/Jurisdiction:**")
            for loc in entities['locations'][:5]:
                st.write(f"• {loc}")
    
    st.markdown("---")
    
    # Critical Issues
    st.subheader("🚨 Critical Issues & Recommendations")
    
    critical_clauses = risk_analysis.get('critical_clauses', [])
    if critical_clauses:
        for idx, critical in enumerate(critical_clauses[:3], 1):
            with st.expander(f"Critical Issue #{idx} (Risk Score: {critical.get('risk_score', 0)})", expanded=True):
                st.write("**Risks Found:**")
                for risk in critical.get('risks_found', []):
                    st.warning(f"⚠️ {risk['type'].replace('_', ' ').title()}: {risk['keyword']}")
                
                st.write("**Recommendations:**")
                for rec in critical.get('recommendations', []):
                    st.markdown(f'<div class="recommendation-box">💡 {rec}</div>', 
                              unsafe_allow_html=True)
    else:
        st.success("✅ No critical issues identified!")
    
    st.markdown("---")
    
    # Unfavorable Terms
    unfavorable = result.get('unfavorable_terms', [])
    if unfavorable:
        st.subheader("⚡ Unfavorable Terms Detected")
        
        for term in unfavorable[:5]:
            with st.expander(f"⚠️ {term.get('term_type', 'Unknown')}"):
                st.write(f"**Explanation:** {term.get('explanation', 'N/A')}")
                st.code(term.get('clause_text', ''), language=None)
    
    st.markdown("---")
    
    # Compliance Check
    st.subheader("⚖️ Legal Compliance (Indian Law)")
    compliance = result.get('compliance', {})
    legal_compliance = llm_analysis.get('legal_compliance', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        if compliance.get('has_jurisdiction_clause'):
            st.success("✅ Jurisdiction clause present")
        else:
            st.warning("⚠️ No clear jurisdiction clause")
        
        if compliance.get('has_indian_reference'):
            st.success("✅ References Indian law/jurisdiction")
        else:
            st.warning("⚠️ No Indian law references")
    
    with col2:
        compliance_issues = legal_compliance.get('compliance_issues', [])
        if compliance_issues:
            st.write("**Compliance Issues:**")
            for issue in compliance_issues:
                st.error(f"❌ {issue}")


def show_clause_explorer():
    """Interactive clause exploration"""
    if st.session_state.analysis_result is None:
        st.info("👆 Analyze a contract first to explore clauses.")
        return
    
    st.header("🔍 Clause-by-Clause Explorer")
    
    result = st.session_state.analysis_result
    clauses = result.get('clauses', [])
    
    if not clauses:
        st.warning("No clauses extracted from the contract.")
        return
    
    # Filter options
    col1, col2 = st.columns([1, 3])
    
    with col1:
        filter_option = st.selectbox(
            "Filter by:",
            ["All Clauses", "High Risk Only", "Medium Risk Only", "Ambiguous Only"]
        )
    
    # Filter clauses
    clause_risks = result.get('risk_analysis', {}).get('clause_risks', [])
    risk_map = {cr['clause_id']: cr for cr in clause_risks}
    
    filtered_clauses = clauses
    if filter_option == "High Risk Only":
        filtered_clauses = [c for c in clauses if risk_map.get(c['id'], {}).get('risk_level') == 'HIGH']
    elif filter_option == "Medium Risk Only":
        filtered_clauses = [c for c in clauses if risk_map.get(c['id'], {}).get('risk_level') == 'MEDIUM']
    elif filter_option == "Ambiguous Only":
        ambiguous_ids = [ac['clause_id'] for ac in result.get('ambiguous_clauses', [])]
        filtered_clauses = [c for c in clauses if c['id'] in ambiguous_ids]
    
    st.write(f"**Showing {len(filtered_clauses)} clause(s)**")
    
    # Display clauses
    for clause in filtered_clauses[:20]:  # Limit to 20 for performance
        clause_id = clause['id']
        clause_risk = risk_map.get(clause_id, {})
        risk_level = clause_risk.get('risk_level', 'LOW')
        
        # Color code by risk
        if risk_level == 'HIGH':
            icon = "🔴"
        elif risk_level == 'MEDIUM':
            icon = "🟡"
        else:
            icon = "🟢"
        
        with st.expander(f"{icon} Clause {clause_id} - {clause['type'].title()} [{risk_level}]"):
            st.markdown(f'<div class="clause-box">{clause["text"]}</div>', 
                       unsafe_allow_html=True)
            
            # Show risk details
            if clause_risk.get('risks_found'):
                st.write("**Risks:**")
                for risk in clause_risk['risks_found']:
                    st.warning(f"⚠️ {risk['type'].replace('_', ' ').title()}")
            
            # Get detailed explanation button
            if st.button(f"Get AI Explanation", key=f"explain_{clause_id}"):
                with st.spinner("Getting detailed explanation..."):
                    try:
                        explanation = st.session_state.analyzer.explain_clause_detailed(
                            clause, 
                            result.get('metadata', {}).get('contract_type', '')
                        )
                        
                        st.success("**Plain Language Explanation:**")
                        st.write(explanation.get('explanation', 'No explanation available'))
                        
                        if explanation.get('alternatives'):
                            st.info("**Suggested Alternative Clauses:**")
                            for alt in explanation['alternatives']:
                                st.write(alt)
                    
                    except Exception as e:
                        st.error(f"Error getting explanation: {str(e)}")


def show_export_section():
    """Export and download section"""
    if st.session_state.analysis_result is None:
        st.info("👆 Analyze a contract first to export results.")
        return
    
    st.header("📥 Export Analysis Results")
    
    result = st.session_state.analysis_result
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Export as PDF Report")
        st.write("Generate a comprehensive PDF report for legal review.")
        
        if st.button("Generate PDF Report", type="primary"):
            with st.spinner("Generating PDF report..."):
                try:
                    output_path = OUTPUT_DIR / f"{result['file_name']}_report.pdf"
                    st.session_state.report_generator.generate_pdf_report(result, output_path)
                    
                    with open(output_path, 'rb') as f:
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=f,
                            file_name=f"{result['file_name']}_report.pdf",
                            mime="application/pdf"
                        )
                    
                    st.success("✅ PDF report generated!")
                
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
    
    with col2:
        st.subheader("📊 Export as JSON")
        st.write("Download complete analysis data in JSON format.")
        
        # Prepare JSON
        json_str = json.dumps(result, indent=2, ensure_ascii=False)
        
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"{result['file_name']}_analysis.json",
            mime="application/json"
        )
    
    st.markdown("---")
    
    # Analysis summary for copy-paste
    st.subheader("📋 Quick Summary (Copy & Paste)")
    
    risk_analysis = result.get('risk_analysis', {})
    summary_text = f"""
Contract Analysis Summary
========================
File: {result['file_name']}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Type: {result.get('llm_analysis', {}).get('contract_type', {}).get('contract_type', 'Unknown')}

RISK ASSESSMENT
--------------
Overall Risk Level: {risk_analysis.get('overall_risk_level', 'Unknown')}
Risk Score: {risk_analysis.get('composite_risk_score', 0)}/100

Risk Distribution:
- High Risk Clauses: {risk_analysis.get('risk_distribution', {}).get('high', 0)}
- Medium Risk Clauses: {risk_analysis.get('risk_distribution', {}).get('medium', 0)}
- Low Risk Clauses: {risk_analysis.get('risk_distribution', {}).get('low', 0)}

CRITICAL ISSUES: {len(risk_analysis.get('critical_clauses', []))}
UNFAVORABLE TERMS: {len(result.get('unfavorable_terms', []))}

Recommendation: Review highlighted issues before signing.
"""
    
    st.code(summary_text, language=None)


if __name__ == "__main__":
    main()
