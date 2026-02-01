"""
Enhanced sections for Streamlit UI - Templates and Knowledge Base
"""
import streamlit as st
from pathlib import Path


def show_template_section():
    """Display contract template generation section"""
    st.header("📝 SME-Friendly Contract Templates")
    st.write("Generate standardized, balanced contract templates that protect your interests.")
    
    template_gen = st.session_state.template_generator
    
    # Template selection
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Select Template Type")
        template_types = template_gen.list_available_templates()
        selected_template = st.selectbox(
            "Choose template:",
            template_types,
            help="Select the type of contract you need"
        )
    
    with col2:
        st.subheader("Template Guidelines")
        guidelines = template_gen.get_template_guidelines(selected_template)
        
        if guidelines.get("fair_terms"):
            st.success("**✓ Fair Terms to Include:**")
            for term in guidelines["fair_terms"]:
                st.write(f"• {term}")
        
        if guidelines.get("avoid"):
            st.error("**⚠️ Terms to Avoid:**")
            for term in guidelines["avoid"]:
                st.write(f"• {term}")
    
    st.markdown("---")
    
    # Template generation form
    st.subheader("Generate Custom Template")
    
    if selected_template == "Service Agreement":
        with st.form("service_agreement_form"):
            st.write("**Party Information:**")
            col1, col2 = st.columns(2)
            
            with col1:
                client_name = st.text_input("Client Name")
                client_address = st.text_input("Client Address")
            
            with col2:
                provider_name = st.text_input("Service Provider Name")
                provider_address = st.text_input("Service Provider Address")
            
            st.write("**Contract Terms:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                duration = st.text_input("Duration", value="12 months")
                payment = st.text_input("Payment Amount", value="Rs. 50,000")
            
            with col2:
                payment_days = st.number_input("Payment Terms (days)", value=30, min_value=15, max_value=90)
                termination_notice = st.number_input("Termination Notice (days)", value=60, min_value=30, max_value=90)
            
            with col3:
                jurisdiction = st.text_input("Jurisdiction (City)", value="Mumbai")
                start_date = st.date_input("Start Date")
            
            scope = st.text_area("Scope of Services", height=100)
            
            submit = st.form_submit_button("Generate Template", type="primary", use_container_width=True)
            
            if submit:
                parties = {
                    "client": client_name,
                    "client_address": client_address,
                    "provider": provider_name,
                    "provider_address": provider_address
                }
                
                terms = {
                    "date": start_date.strftime("%B %d, %Y"),
                    "start_date": start_date.strftime("%B %d, %Y"),
                    "duration": duration,
                    "payment": payment,
                    "payment_days": str(payment_days),
                    "termination_notice": str(termination_notice),
                    "jurisdiction": jurisdiction,
                    "scope": scope if scope else "[DESCRIBE SERVICES IN DETAIL]"
                }
                
                template = template_gen.generate_service_agreement(parties, terms)
                
                st.success("✅ Template Generated!")
                st.download_button(
                    label="📥 Download Service Agreement",
                    data=template,
                    file_name=f"service_agreement_{client_name.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
                with st.expander("📄 Preview Template"):
                    st.text(template)
    
    elif selected_template == "NDA (Non-Disclosure Agreement)":
        with st.form("nda_form"):
            st.write("**Party Information:**")
            col1, col2 = st.columns(2)
            
            with col1:
                party1_name = st.text_input("Party 1 Name")
                party1_address = st.text_input("Party 1 Address")
            
            with col2:
                party2_name = st.text_input("Party 2 Name")
                party2_address = st.text_input("Party 2 Address")
            
            st.write("**NDA Terms:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                duration = st.text_input("Agreement Duration", value="2 years")
            
            with col2:
                confidentiality_period = st.text_input("Confidentiality Period", value="3 years")
            
            with col3:
                jurisdiction = st.text_input("Jurisdiction", value="Mumbai")
            
            purpose = st.text_area("Purpose of NDA", height=100)
            sign_date = st.date_input("Signing Date")
            
            submit = st.form_submit_button("Generate NDA", type="primary", use_container_width=True)
            
            if submit:
                parties = {
                    "party1": party1_name,
                    "party1_address": party1_address,
                    "party2": party2_name,
                    "party2_address": party2_address
                }
                
                terms = {
                    "date": sign_date.strftime("%B %d, %Y"),
                    "duration": duration,
                    "confidentiality_period": confidentiality_period,
                    "jurisdiction": jurisdiction,
                    "purpose": purpose if purpose else "[STATE PURPOSE]"
                }
                
                template = template_gen.generate_nda(parties, terms)
                
                st.success("✅ NDA Generated!")
                st.download_button(
                    label="📥 Download NDA",
                    data=template,
                    file_name=f"nda_{party1_name.replace(' ', '_')}_{party2_name.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
                with st.expander("📄 Preview NDA"):
                    st.text(template)
    
    elif selected_template == "Freelancer Agreement":
        with st.form("freelancer_form"):
            st.write("**Party Information:**")
            col1, col2 = st.columns(2)
            
            with col1:
                client_name = st.text_input("Client Name")
                client_address = st.text_input("Client Address")
            
            with col2:
                freelancer_name = st.text_input("Freelancer Name")
                freelancer_address = st.text_input("Freelancer Address")
            
            st.write("**Contract Terms:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                rate = st.text_input("Rate", value="Rs. 2,000")
                rate_basis = st.selectbox("Rate Basis", ["per hour", "per day", "per project"])
            
            with col2:
                payment_terms = st.text_input("Payment Terms", value="Net 30 days")
                completion_date = st.date_input("Expected Completion")
            
            with col3:
                notice_period = st.number_input("Notice Period (days)", value=15, min_value=7, max_value=30)
                jurisdiction = st.text_input("Jurisdiction", value="Mumbai")
            
            services = st.text_area("Services Description", height=100)
            sign_date = st.date_input("Contract Date")
            
            submit = st.form_submit_button("Generate Agreement", type="primary", use_container_width=True)
            
            if submit:
                parties = {
                    "client": client_name,
                    "client_address": client_address,
                    "freelancer": freelancer_name,
                    "freelancer_address": freelancer_address
                }
                
                terms = {
                    "date": sign_date.strftime("%B %d, %Y"),
                    "rate": rate,
                    "rate_basis": rate_basis,
                    "payment_terms": payment_terms,
                    "completion_date": completion_date.strftime("%B %d, %Y"),
                    "notice_period": str(notice_period),
                    "jurisdiction": jurisdiction,
                    "services": services if services else "[DESCRIBE SERVICES]"
                }
                
                template = template_gen.generate_freelancer_agreement(parties, terms)
                
                st.success("✅ Freelancer Agreement Generated!")
                st.download_button(
                    label="📥 Download Agreement",
                    data=template,
                    file_name=f"freelancer_agreement_{freelancer_name.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
                with st.expander("📄 Preview Agreement"):
                    st.text(template)
    
    else:
        st.info(f"Template generation form for '{selected_template}' coming soon! Use the available templates above for now.")


def show_knowledge_base_section():
    """Display knowledge base of common SME contract issues"""
    st.header("📚 SME Contract Knowledge Base")
    st.write("Learn about common contract issues faced by Indian SMEs and how to avoid them.")
    
    kb = st.session_state.knowledge_base
    
    # Knowledge base statistics
    stats = kb.get_statistics()
    
    if stats["total_analyses"] > 0:
        st.subheader("📊 Knowledge Base Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Analyses", stats["total_analyses"])
        
        with col2:
            st.metric("Avg Risk Score", f"{stats['average_risk_score']:.1f}/100")
        
        with col3:
            st.metric("Issues Tracked", len(stats["issues_identified"]))
        
        with col4:
            st.metric("Top Risks", len(stats["most_common_risks"]))
        
        if stats["most_common_risks"]:
            st.write("**Most Common Risks Detected:**")
            for idx, risk in enumerate(stats["most_common_risks"], 1):
                count = stats["issues_identified"].get(risk, 0)
                st.write(f"{idx}. {risk.replace('_', ' ').title()}: **{count}** occurrences")
        
        st.markdown("---")
    
    # Common issues by contract type
    st.subheader("🔍 Common Contract Issues")
    
    contract_type_filter = st.selectbox(
        "Select Contract Type:",
        ["All", "Vendor Contracts", "Employment Agreements", "Service Contracts", "NDAs"]
    )
    
    kb_data = kb.kb
    
    if contract_type_filter == "All":
        for contract_type, issues in kb_data["common_issues"].items():
            with st.expander(f"📄 {contract_type.replace('_', ' ').title()} ({len(issues)} issues)"):
                for idx, issue in enumerate(issues, 1):
                    st.markdown(f"### {idx}. {issue['issue']}")
                    st.write(f"**Description:** {issue['description']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        freq_color = "🔴" if issue['frequency'] == "Very Common" else "🟡" if issue['frequency'] == "Common" else "🟢"
                        st.write(f"{freq_color} **Frequency:** {issue['frequency']}")
                    with col2:
                        sev_color = "🔴" if issue['severity'] in ["High", "Critical"] else "🟡" if issue['severity'] == "Medium" else "🟢"
                        st.write(f"{sev_color} **Severity:** {issue['severity']}")
                    
                    st.info(f"**Impact:** {issue['impact']}")
                    st.success(f"**✓ Recommendation:** {issue['recommendation']}")
                    
                    st.markdown("**Sample Clause**")
                    st.code(issue['sample_clause'], language=None)

                    st.markdown("---")
    else:
        # Show specific contract type
        contract_key = contract_type_filter.lower().replace(" ", "_")
        issues = kb_data["common_issues"].get(contract_key, [])
        
        if issues:
            for idx, issue in enumerate(issues, 1):
                st.markdown(f"### {idx}. {issue['issue']}")
                st.write(f"**Description:** {issue['description']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    freq_color = "🔴" if issue['frequency'] == "Very Common" else "🟡" if issue['frequency'] == "Common" else "🟢"
                    st.write(f"{freq_color} **Frequency:** {issue['frequency']}")
                with col2:
                    sev_color = "🔴" if issue['severity'] in ["High", "Critical"] else "🟡" if issue['severity'] == "Medium" else "🟢"
                    st.write(f"{sev_color} **Severity:** {issue['severity']}")
                
                st.info(f"**Impact:** {issue['impact']}")
                st.success(f"**✓ Recommendation:** {issue['recommendation']}")
                
                st.markdown("**Sample Clause**")
                st.code(issue['sample_clause'], language=None)
   
                st.markdown("---")
        else:
            st.warning("No issues found for this contract type.")
    
    st.markdown("---")
    
    # Best Practices
    st.subheader("💡 Best Practices for SME Contracts")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ✅ General Tips")
        for tip in kb.get_best_practices("general"):
            st.write(f"• {tip}")
    
    with col2:
        st.markdown("### 🚩 Red Flags")
        for flag in kb.get_best_practices("red_flags"):
            st.write(f"• {flag}")
    
    with col3:
        st.markdown("### 🤝 Negotiation Tips")
        for tip in kb.get_best_practices("negotiation_tips"):
            st.write(f"• {tip}")
    
    st.markdown("---")
    
    # Indian Law Information
    st.subheader("⚖️ Indian Law Considerations")
    
    law_info = kb.get_indian_law_info()
    
    tabs = st.tabs(["Contract Act 1872", "Common Provisions", "Employment Specific"])
    
    with tabs[0]:
        st.write("**Indian Contract Act, 1872 - Key Points:**")
        for point in law_info.get("contract_act_1872", []):
            st.write(f"• {point}")
    
    with tabs[1]:
        st.write("**Common Contract Provisions:**")
        for point in law_info.get("common_provisions", []):
            st.write(f"• {point}")
    
    with tabs[2]:
        st.write("**Employment-Specific Regulations:**")
        for point in law_info.get("employment_specific", []):
            st.write(f"• {point}")
    
    st.markdown("---")
    
    # Search functionality
    st.subheader("🔎 Search Knowledge Base")
    search_query = st.text_input("Search for contract issues, best practices, or legal info:")
    
    if search_query:
        results = kb.search_knowledge_base(search_query)
        
        if results:
            st.success(f"Found {len(results)} result(s):")
            for result in results:
                if result["type"] == "issue":
                    issue = result["data"]
                    with st.expander(f"📄 {issue['issue']} ({result['contract_type']})"):
                        st.write(f"**Description:** {issue['description']}")
                        st.success(f"**Recommendation:** {issue['recommendation']}")
                elif result["type"] == "best_practice":
                    st.info(f"💡 {result['data']}")
        else:
            st.warning("No results found. Try different keywords.")
    
    st.markdown("---")
    
    # Export knowledge base
    if st.button("📥 Export Knowledge Base as Document", type="secondary"):
        output_path = kb.export_knowledge_base()
        
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        st.download_button(
            label="📥 Download Knowledge Base",
            data=content,
            file_name="sme_contract_knowledge_base.txt",
            mime="text/plain"
        )
        st.success("✅ Knowledge base exported!")
