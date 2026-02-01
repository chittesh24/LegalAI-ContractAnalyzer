"""
Template Generator for SME-friendly contracts
Creates standardized, balanced contract templates
"""
from typing import Dict, List
from pathlib import Path
from config import TEMPLATES_DIR


class TemplateGenerator:
    """Generate standardized SME-friendly contract templates"""
    
    def __init__(self):
        self.templates_dir = TEMPLATES_DIR
        self.template_types = [
            "Service Agreement",
            "Vendor Contract",
            "Employment Agreement",
            "Consultant Agreement",
            "NDA (Non-Disclosure Agreement)",
            "Partnership Deed",
            "Lease Agreement",
            "Purchase Order",
            "Software License",
            "Freelancer Agreement"
        ]
    
    def generate_service_agreement(self, parties: Dict, terms: Dict) -> str:
        """
        Generate a balanced service agreement template
        
        Args:
            parties: Dict with 'client' and 'provider' info
            terms: Dict with 'scope', 'duration', 'payment', etc.
        """
        template = f"""SERVICE AGREEMENT

This Service Agreement is entered into on {terms.get('date', '[DATE]')}

BETWEEN:
{parties.get('client', '[CLIENT NAME]')}, having office at {parties.get('client_address', '[CLIENT ADDRESS]')} (hereinafter referred to as "Client")

AND:
{parties.get('provider', '[PROVIDER NAME]')}, having office at {parties.get('provider_address', '[PROVIDER ADDRESS]')} (hereinafter referred to as "Service Provider")

WHEREAS both parties wish to enter into a mutually beneficial service arrangement.

1. SERVICES
The Service Provider shall provide the following services:
{terms.get('scope', '[DESCRIBE SERVICES IN DETAIL]')}

2. TERM
This Agreement shall be effective from {terms.get('start_date', '[START DATE]')} for an initial period of {terms.get('duration', '12 months')}.

2.1 Renewal: Either party may choose to renew by mutual written consent {terms.get('renewal_notice', '30 days')} before expiry.
2.2 No automatic renewal without explicit consent from both parties.

3. COMPENSATION
3.1 Service Fee: {terms.get('payment', 'Rs. [AMOUNT]')} per {terms.get('payment_frequency', 'month')} plus applicable GST
3.2 Payment Terms: Due within {terms.get('payment_days', '30 days')} of invoice date
3.3 Late Payment: {terms.get('late_fee', '1%')} per month interest after {terms.get('grace_period', '15 day')} grace period

4. TERMINATION
4.1 Either party may terminate with {terms.get('termination_notice', '60 days')} written notice
4.2 Termination for cause (material breach) requires {terms.get('cure_period', '15 days')} notice and opportunity to cure
4.3 Upon termination, Client shall pay for services rendered until termination date

5. INTELLECTUAL PROPERTY
5.1 Pre-existing IP of each party remains with that party
5.2 New IP created specifically for Client's project shall belong to Client
5.3 Service Provider retains right to use generic methodologies and frameworks
5.4 Service Provider may showcase work in portfolio with Client's prior written consent

6. CONFIDENTIALITY
6.1 Both parties shall maintain confidentiality of proprietary information
6.2 Confidentiality obligation survives for {terms.get('confidentiality_period', '3 years')} post-termination
6.3 Excludes: publicly available information, information required by law to be disclosed

7. LIABILITY AND INDEMNIFICATION
7.1 Each party shall indemnify the other for breaches of this Agreement
7.2 Total liability capped at {terms.get('liability_cap', '6 months of fees paid')}
7.3 Neither party liable for indirect, consequential, or punitive damages
7.4 Force majeure events exempt parties from liability

8. PERFORMANCE STANDARDS
Service Provider shall use commercially reasonable efforts to achieve agreed deliverables and quality standards outlined in Annexure A.

9. INDEPENDENT CONTRACTOR
Service Provider is an independent contractor, not an employee. Responsible for own taxes, insurance, and regulatory compliance.

10. AMENDMENTS
Any amendments must be in writing and signed by both parties. No unilateral changes permitted.

11. DISPUTE RESOLUTION
11.1 Disputes shall first be attempted to be resolved through good faith negotiations (30 days)
11.2 If unresolved, parties may pursue mediation
11.3 Arbitration under Arbitration and Conciliation Act, 1996
11.4 Venue: {terms.get('jurisdiction', '[CITY]')}
11.5 Each party bears own costs unless arbitrator decides otherwise

12. FORCE MAJEURE
Neither party liable for delays due to circumstances beyond reasonable control including natural disasters, strikes, pandemics, or government actions. Affected party must notify within 7 days.

13. GOVERNING LAW
This Agreement shall be governed by the laws of India. Courts in {terms.get('jurisdiction', '[CITY]')} shall have jurisdiction.

14. ENTIRE AGREEMENT
This Agreement constitutes the complete agreement between the parties and supersedes all prior discussions and understandings.

15. NOTICES
All notices shall be sent to the addresses mentioned above via email and registered post.

AGREED AND ACCEPTED:

For {parties.get('client', '[CLIENT]')}              For {parties.get('provider', '[PROVIDER]')}
_____________________                                _____________________
Name:                                                Name:
Designation:                                         Designation:
Date:                                                Date:

ANNEXURE A: Scope of Work and Deliverables
[To be attached]
"""
        return template
    
    def generate_nda(self, parties: Dict, terms: Dict) -> str:
        """Generate a balanced NDA template"""
        template = f"""NON-DISCLOSURE AGREEMENT (NDA)

This Agreement is made on {terms.get('date', '[DATE]')}

BETWEEN:
{parties.get('party1', '[PARTY 1 NAME]')}, having office at {parties.get('party1_address', '[ADDRESS]')} ("Disclosing Party")

AND:
{parties.get('party2', '[PARTY 2 NAME]')}, having office at {parties.get('party2_address', '[ADDRESS]')} ("Receiving Party")

WHEREAS the parties wish to explore a business relationship and need to share confidential information.

1. PURPOSE
The parties wish to share confidential information for the purpose of: {terms.get('purpose', '[STATE PURPOSE]')}

2. CONFIDENTIAL INFORMATION
"Confidential Information" means any information disclosed by one party to the other, whether orally or in writing, that is designated as confidential or that reasonably should be understood to be confidential.

2.1 Includes: Technical data, business plans, financial information, customer lists, trade secrets
2.2 Excludes:
    - Information that is publicly available
    - Information already known to receiving party
    - Information independently developed
    - Information required to be disclosed by law

3. OBLIGATIONS
3.1 Receiving Party shall:
    - Maintain confidentiality using reasonable care
    - Use information only for stated purpose
    - Not disclose to third parties without written consent
    - Return or destroy information upon request

3.2 This is a MUTUAL NDA - obligations apply to both parties

4. TERM
This Agreement shall remain in effect for {terms.get('duration', '2 years')} from the date of signing.
Confidentiality obligations survive for {terms.get('confidentiality_period', '3 years')} after termination.

5. NO LICENSE
This Agreement does not grant any license or rights to intellectual property.

6. REMEDIES
Breach of this Agreement may result in irreparable harm. Either party may seek injunctive relief and damages.

7. GOVERNING LAW
This Agreement is governed by Indian laws. Jurisdiction: {terms.get('jurisdiction', '[CITY]')}.

IN WITNESS WHEREOF, the parties have executed this Agreement.

For {parties.get('party1', '[PARTY 1]')}           For {parties.get('party2', '[PARTY 2]')}
_____________________                              _____________________
Authorized Signatory                               Authorized Signatory
Date:                                              Date:
"""
        return template
    
    def generate_freelancer_agreement(self, parties: Dict, terms: Dict) -> str:
        """Generate a fair freelancer/consultant agreement"""
        template = f"""FREELANCER AGREEMENT

This Agreement is made on {terms.get('date', '[DATE]')}

BETWEEN:
{parties.get('client', '[CLIENT NAME]')}, having office at {parties.get('client_address', '[ADDRESS]')} ("Client")

AND:
{parties.get('freelancer', '[FREELANCER NAME]')}, residing at {parties.get('freelancer_address', '[ADDRESS]')} ("Freelancer")

1. SERVICES
Freelancer shall provide the following services:
{terms.get('services', '[DESCRIBE SERVICES]')}

2. COMPENSATION
2.1 Rate: {terms.get('rate', 'Rs. [AMOUNT]')} per {terms.get('rate_basis', 'hour/day/project')}
2.2 Payment: {terms.get('payment_terms', 'Net 30 days')} from invoice
2.3 Expenses: {terms.get('expenses', 'Pre-approved expenses reimbursed with receipts')}

3. TERM
Project-based work expected to complete by {terms.get('completion_date', '[DATE]')}.
Either party may terminate with {terms.get('notice_period', '15 days')} notice.

4. INTELLECTUAL PROPERTY
4.1 Work Product: All deliverables created specifically for this project belong to Client
4.2 Freelancer Tools: Freelancer retains rights to general tools, templates, and methodologies
4.3 Attribution: Freelancer may showcase work in portfolio with Client consent

5. INDEPENDENT CONTRACTOR
Freelancer is an independent contractor. Responsible for own:
- Taxes and GST registration
- Insurance
- Equipment and software
- Work schedule and methods

6. CONFIDENTIALITY
Freelancer shall maintain confidentiality of Client information for {terms.get('confidentiality', '2 years')}.

7. NON-COMPETE (LIMITED)
During project term, Freelancer shall not work on directly competing projects for Client's direct competitors in the same niche.
Note: This does NOT restrict Freelancer from working in the same industry generally.

8. LIABILITY
8.1 Freelancer liable only for direct damages caused by gross negligence
8.2 Liability capped at total fees paid
8.3 No liability for consequential or indirect damages

9. DISPUTE RESOLUTION
Disputes to be resolved through mediation, then arbitration in {terms.get('jurisdiction', '[CITY]')}.

10. GOVERNING LAW
Governed by Indian laws. Jurisdiction: {terms.get('jurisdiction', '[CITY]')}.

AGREED:

Client: _____________________          Freelancer: _____________________
Date:                                  Date:
"""
        return template
    
    def list_available_templates(self) -> List[str]:
        """List all available template types"""
        return self.template_types
    
    def get_template_guidelines(self, template_type: str) -> Dict[str, any]:
        """Get guidelines for what makes a fair contract of each type"""
        guidelines = {
            "Service Agreement": {
                "fair_terms": [
                    "Mutual termination rights (60-90 days notice)",
                    "Liability cap at 6-12 months of fees",
                    "No automatic renewal",
                    "Clear scope and deliverables",
                    "Reasonable payment terms (30-45 days)"
                ],
                "avoid": [
                    "Unilateral termination by one party only",
                    "Unlimited liability",
                    "Excessive lock-in periods (>2 years)",
                    "Auto-renewal without consent",
                    "Personal guarantees"
                ]
            },
            "Employment Agreement": {
                "fair_terms": [
                    "Mutual notice period (1-3 months based on level)",
                    "Limited non-compete (6-12 months, specific geography)",
                    "Clear compensation and benefits",
                    "IP created during work hours belongs to company",
                    "Reasonable working hours"
                ],
                "avoid": [
                    "One-sided termination (employer can fire anytime, employee needs 3 months)",
                    "Excessive non-compete (2+ years, pan-India, all industries)",
                    "Personal guarantees for company losses",
                    "Unpaid overtime expectations",
                    "Perpetual confidentiality for non-trade secrets"
                ]
            },
            "NDA": {
                "fair_terms": [
                    "Mutual obligations (both parties bound)",
                    "Clear definition of confidential info",
                    "Reasonable term (2-3 years)",
                    "Exceptions for public info, prior knowledge",
                    "No restriction on independent development"
                ],
                "avoid": [
                    "One-sided NDA (only one party bound)",
                    "Perpetual confidentiality",
                    "Overly broad definition of confidential info",
                    "No exceptions",
                    "Excessive penalties"
                ]
            },
            "Freelancer Agreement": {
                "fair_terms": [
                    "Clear scope and deliverables",
                    "Reasonable payment terms (Net 15-30)",
                    "IP for specific work goes to client",
                    "Freelancer retains general tools/methods",
                    "Limited non-compete during project only"
                ],
                "avoid": [
                    "Full IP transfer including freelancer's tools",
                    "Broad non-compete (prevents working in industry)",
                    "Personal liability for business outcomes",
                    "Payment only after full project completion",
                    "Unlimited revisions"
                ]
            }
        }
        
        return guidelines.get(template_type, {
            "fair_terms": ["Mutual obligations", "Clear terms", "Reasonable duration"],
            "avoid": ["One-sided terms", "Unlimited liability", "Excessive restrictions"]
        })
    
    def save_template(self, template_name: str, content: str) -> Path:
        """Save generated template to file"""
        filename = f"{template_name.replace(' ', '_').lower()}_template.txt"
        filepath = self.templates_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
