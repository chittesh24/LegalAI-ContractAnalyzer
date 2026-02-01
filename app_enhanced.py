"""
Enhanced sections for Streamlit UI - Templates and Knowledge Base
"""
import streamlit as st


# -------------------------------------------------
# TEMPLATE SECTION
# -------------------------------------------------
def show_template_section():
    st.header("📝 SME-Friendly Contract Templates")
    st.write(
        "Generate standardized, balanced contract templates that protect your interests."
    )

    template_gen = st.session_state.template_generator

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Select Template Type")
        template_types = template_gen.list_available_templates()
        selected_template = st.selectbox(
            "Choose template:", template_types
        )

    with col2:
        st.subheader("Template Guidelines")
        guidelines = template_gen.get_template_guidelines(selected_template)

        for term in guidelines.get("fair_terms", []):
            st.success(f"✓ {term}")

        for term in guidelines.get("avoid", []):
            st.error(f"⚠️ Avoid: {term}")

    st.markdown("---")
    st.subheader("Generate Custom Template")

    # ---------------- SERVICE AGREEMENT ----------------
    if selected_template == "Service Agreement":
        with st.form("service_agreement_form"):
            client_name = st.text_input("Client Name")
            provider_name = st.text_input("Service Provider Name")
            duration = st.text_input("Duration", "12 months")
            payment = st.text_input("Payment Amount", "Rs. 50,000")

            submit = st.form_submit_button("Generate Template")

        if submit:
            template = template_gen.generate_service_agreement({}, {})
            st.session_state.generated_template = template
            st.success("Template generated")

        if "generated_template" in st.session_state:
            st.download_button(
                "Download Template",
                st.session_state.generated_template,
                "service_agreement.txt",
            )

    # ---------------- NDA ----------------
    elif selected_template == "NDA (Non-Disclosure Agreement)":
        with st.form("nda_form"):
            party1 = st.text_input("Party 1")
            party2 = st.text_input("Party 2")
            submit = st.form_submit_button("Generate NDA")

        if submit:
            template = template_gen.generate_nda({}, {})
            st.session_state.generated_template = template
            st.success("NDA generated")

        if "generated_template" in st.session_state:
            st.download_button(
                "Download NDA",
                st.session_state.generated_template,
                "nda.txt",
            )

    # ---------------- FREELANCER ----------------
    elif selected_template == "Freelancer Agreement":
        with st.form("freelancer_form"):
            client = st.text_input("Client")
            freelancer = st.text_input("Freelancer")
            submit = st.form_submit_button("Generate Agreement")

        if submit:
            template = template_gen.generate_freelancer_agreement({}, {})
            st.session_state.generated_template = template
            st.success("Agreement generated")

        if "generated_template" in st.session_state:
            st.download_button(
                "Download Agreement",
                st.session_state.generated_template,
                "freelancer_agreement.txt",
            )


# -------------------------------------------------
# KNOWLEDGE BASE SECTION
# -------------------------------------------------
def show_knowledge_base_section():
    st.header("📚 SME Contract Knowledge Base")
    st.write("Common SME contract risks and guidance.")

    kb = st.session_state.knowledge_base

    stats = kb.get_statistics()

    st.metric("Total Analyses", stats.get("total_analyses", 0))

    st.markdown("---")

    st.subheader("Common Issues")

    for contract_type, issues in kb.kb.get("common_issues", {}).items():
        with st.expander(contract_type):
            for issue in issues:
                st.write(issue.get("issue"))
                st.info(issue.get("description"))

    st.markdown("---")

    st.subheader("Best Practices")

    for tip in kb.get_best_practices("general"):
        st.write("•", tip)
