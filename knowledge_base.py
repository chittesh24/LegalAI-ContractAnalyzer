"""
Knowledge Base for common SME contract issues
Stores learnings and patterns from contract analyses
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from config import OUTPUT_DIR


class KnowledgeBase:
    """
    Build and maintain knowledge base of common contract issues faced by Indian SMEs
    """
    
    def __init__(self):
        self.kb_file = OUTPUT_DIR / "knowledge_base.json"
        self.kb = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> Dict:
        """Load existing knowledge base or create new"""
        if self.kb_file.exists():
            with open(self.kb_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self) -> Dict:
        """Initialize knowledge base with common SME contract issues"""
        return {
            "common_issues": {
                "vendor_contracts": [
                    {
                        "issue": "Unilateral Termination Rights",
                        "description": "Client can terminate without cause, vendor needs 180 days notice",
                        "frequency": "Very Common",
                        "severity": "High",
                        "impact": "Vendor loses revenue suddenly, no recourse",
                        "recommendation": "Negotiate mutual termination rights with equal notice periods (60-90 days)",
                        "sample_clause": "Either party may terminate this Agreement with 60 days written notice without cause."
                    },
                    {
                        "issue": "Unlimited Indemnity",
                        "description": "Vendor must indemnify client for unlimited amounts",
                        "frequency": "Common",
                        "severity": "High",
                        "impact": "Exposes vendor to potentially bankrupting liability",
                        "recommendation": "Cap indemnity at 6-12 months of contract value",
                        "sample_clause": "Total liability under this indemnification shall not exceed the total fees paid under this Agreement in the preceding 12 months."
                    },
                    {
                        "issue": "Auto-Renewal Without Consent",
                        "description": "Contract automatically renews unless vendor opts out",
                        "frequency": "Common",
                        "severity": "Medium",
                        "impact": "Vendor locked into unfavorable terms unintentionally",
                        "recommendation": "Require explicit opt-in for renewal by both parties",
                        "sample_clause": "This Agreement may be renewed for additional terms only by mutual written consent of both parties 30 days before expiry."
                    },
                    {
                        "issue": "Full IP Transfer",
                        "description": "All IP including vendor's tools and methods transfer to client",
                        "frequency": "Very Common",
                        "severity": "High",
                        "impact": "Vendor loses reusable assets, can't use own tools",
                        "recommendation": "Client gets project-specific IP, vendor retains general tools",
                        "sample_clause": "Client owns IP created specifically for this project. Vendor retains rights to pre-existing tools, frameworks, and general methodologies."
                    },
                    {
                        "issue": "Payment Terms Beyond 60 Days",
                        "description": "Client pays after 90-120 days",
                        "frequency": "Common",
                        "severity": "Medium",
                        "impact": "Cash flow problems for small vendors",
                        "recommendation": "Negotiate 30-45 day payment terms",
                        "sample_clause": "Payment due within 30 days of invoice date."
                    }
                ],
                "employment_agreements": [
                    {
                        "issue": "One-Sided Termination",
                        "description": "Employer can terminate immediately, employee needs 3 months notice",
                        "frequency": "Very Common",
                        "severity": "High",
                        "impact": "Employee has no job security, employer has full flexibility",
                        "recommendation": "Mutual notice period based on seniority (1-3 months)",
                        "sample_clause": "Either party may terminate with [X] months written notice."
                    },
                    {
                        "issue": "Excessive Non-Compete",
                        "description": "2-3 years, pan-India, entire industry",
                        "frequency": "Common",
                        "severity": "High",
                        "impact": "Employee cannot work in their field after leaving",
                        "recommendation": "Limit to 6-12 months, specific geography, direct competitors only",
                        "sample_clause": "For 6 months post-termination, Employee shall not work for direct competitors operating in [City/State] in the same product category."
                    },
                    {
                        "issue": "Personal Guarantee for Business Outcomes",
                        "description": "Employee personally liable for project failures or client losses",
                        "frequency": "Occasional",
                        "severity": "Critical",
                        "impact": "Personal assets at risk for business decisions",
                        "recommendation": "Remove personal guarantee clauses entirely",
                        "sample_clause": "[Delete this clause] Employer may pursue professional liability insurance instead."
                    },
                    {
                        "issue": "Unpaid Overtime Expectation",
                        "description": "45+ hours required without overtime as 'managerial position'",
                        "frequency": "Common",
                        "severity": "Medium",
                        "impact": "Work-life balance issues, unpaid labor",
                        "recommendation": "Clear working hours or overtime compensation policy",
                        "sample_clause": "Standard working hours are 40 hours per week. Overtime may be required occasionally and will be compensated [as per policy]."
                    },
                    {
                        "issue": "Perpetual Confidentiality",
                        "description": "Confidentiality obligation lasts forever",
                        "frequency": "Common",
                        "severity": "Low",
                        "impact": "Unclear what remains confidential over time",
                        "recommendation": "Limit to 3-5 years for non-trade secrets",
                        "sample_clause": "Confidentiality obligations survive for 3 years post-termination, except for trade secrets which remain confidential indefinitely."
                    }
                ],
                "service_contracts": [
                    {
                        "issue": "Scope Creep Without Additional Payment",
                        "description": "Client can add unlimited scope changes",
                        "frequency": "Very Common",
                        "severity": "Medium",
                        "impact": "Provider does more work than agreed without compensation",
                        "recommendation": "Clear change order process with pricing",
                        "sample_clause": "Any changes to scope require written change order with adjusted timeline and pricing."
                    },
                    {
                        "issue": "Unlimited Revisions",
                        "description": "Client entitled to unlimited revisions",
                        "frequency": "Common",
                        "severity": "Medium",
                        "impact": "Project never ends, provider keeps working",
                        "recommendation": "Specify number of revision rounds included",
                        "sample_clause": "Fee includes 2 rounds of revisions. Additional revisions billed at [rate]."
                    }
                ],
                "ndas": [
                    {
                        "issue": "One-Sided NDA",
                        "description": "Only one party bound to confidentiality",
                        "frequency": "Common",
                        "severity": "Medium",
                        "impact": "Unequal protection of information",
                        "recommendation": "Use mutual NDA",
                        "sample_clause": "This is a mutual NDA. Both parties agree to maintain confidentiality of information received."
                    }
                ]
            },
            "best_practices": {
                "general": [
                    "Read entire contract before signing",
                    "Negotiate unfavorable terms - everything is negotiable",
                    "Get legal review for contracts >10 lakhs or multi-year commitments",
                    "Document all verbal agreements in writing",
                    "Keep copies of all signed contracts"
                ],
                "red_flags": [
                    "Personal guarantees",
                    "Unlimited liability",
                    "Perpetual obligations",
                    "One-sided termination rights",
                    "Very broad non-compete clauses",
                    "Auto-renewal without opt-in",
                    "Payment terms >60 days",
                    "Full IP transfer including your tools"
                ],
                "negotiation_tips": [
                    "Propose mutual terms instead of one-sided",
                    "Add caps and limits (liability cap, time limits)",
                    "Request cure periods before termination",
                    "Clarify scope to prevent scope creep",
                    "Ask for shorter contract terms (easier to renegotiate)",
                    "Get payment terms in writing",
                    "Ensure you can showcase your work (portfolio rights)"
                ]
            },
            "indian_law_specifics": {
                "contract_act_1872": [
                    "Contracts must have lawful consideration",
                    "Agreements not enforceable by law are void",
                    "Capacity to contract required (age, mental soundness)",
                    "Free consent required (no coercion, fraud, misrepresentation)"
                ],
                "common_provisions": [
                    "Governing law should specify Indian law",
                    "Jurisdiction clause specifying Indian courts",
                    "Arbitration clause as per Arbitration and Conciliation Act, 1996",
                    "Stamp duty requirements vary by state",
                    "Electronic contracts valid under IT Act, 2000"
                ],
                "employment_specific": [
                    "Shops and Establishments Act applies",
                    "PF and ESI registration required for eligible employees",
                    "Gratuity Act applies after 5 years",
                    "Notice period must be mutual or reasonable",
                    "Non-compete enforceability limited by courts"
                ]
            },
            "statistics": {
                "total_analyses": 0,
                "issues_identified": {},
                "average_risk_score": 0,
                "most_common_risks": []
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def add_analysis_learnings(self, analysis_result: Dict):
        """Add learnings from new analysis to knowledge base"""
        # Update statistics
        self.kb["statistics"]["total_analyses"] += 1
        
        # Track issues identified
        risk_analysis = analysis_result.get("risk_analysis", {})
        for category, count in risk_analysis.get("risk_categories", {}).items():
            if count > 0:
                if category not in self.kb["statistics"]["issues_identified"]:
                    self.kb["statistics"]["issues_identified"][category] = 0
                self.kb["statistics"]["issues_identified"][category] += count
        
        # Update average risk score
        current_avg = self.kb["statistics"]["average_risk_score"]
        total = self.kb["statistics"]["total_analyses"]
        new_score = risk_analysis.get("composite_risk_score", 0)
        
        self.kb["statistics"]["average_risk_score"] = (
            (current_avg * (total - 1) + new_score) / total
        )
        
        # Update most common risks (top 5)
        sorted_issues = sorted(
            self.kb["statistics"]["issues_identified"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        self.kb["statistics"]["most_common_risks"] = [
            issue[0] for issue in sorted_issues[:5]
        ]
        
        self.kb["last_updated"] = datetime.now().isoformat()
        self._save_knowledge_base()
    
    def get_issue_info(self, issue_type: str, contract_type: str = None) -> Dict:
        """Get detailed information about a specific issue"""
        if contract_type:
            issues = self.kb["common_issues"].get(contract_type, [])
            for issue in issues:
                if issue_type.lower() in issue["issue"].lower():
                    return issue
        
        # Search all contract types
        for ct, issues in self.kb["common_issues"].items():
            for issue in issues:
                if issue_type.lower() in issue["issue"].lower():
                    return issue
        
        return {}
    
    def get_best_practices(self, category: str = "general") -> List[str]:
        """Get best practices for contracts"""
        return self.kb["best_practices"].get(category, [])
    
    def get_statistics(self) -> Dict:
        """Get knowledge base statistics"""
        return self.kb["statistics"]
    
    def get_indian_law_info(self, category: str = None) -> Dict:
        """Get Indian law specific information"""
        if category:
            return {category: self.kb["indian_law_specifics"].get(category, [])}
        return self.kb["indian_law_specifics"]
    
    def search_knowledge_base(self, query: str) -> List[Dict]:
        """Search knowledge base for relevant information"""
        results = []
        query_lower = query.lower()
        
        # Search common issues
        for contract_type, issues in self.kb["common_issues"].items():
            for issue in issues:
                if (query_lower in issue["issue"].lower() or 
                    query_lower in issue["description"].lower()):
                    results.append({
                        "type": "issue",
                        "contract_type": contract_type,
                        "data": issue
                    })
        
        # Search best practices
        for category, practices in self.kb["best_practices"].items():
            for practice in practices:
                if query_lower in practice.lower():
                    results.append({
                        "type": "best_practice",
                        "category": category,
                        "data": practice
                    })
        
        return results
    
    def _save_knowledge_base(self):
        """Save knowledge base to file"""
        with open(self.kb_file, 'w', encoding='utf-8') as f:
            json.dump(self.kb, f, indent=2, ensure_ascii=False)
    
    def export_knowledge_base(self, output_path: Path = None) -> Path:
        """Export knowledge base as readable document"""
        if not output_path:
            output_path = OUTPUT_DIR / "sme_contract_knowledge_base.txt"
        
        content = """
═══════════════════════════════════════════════════════════
SME CONTRACT KNOWLEDGE BASE
Common Issues & Best Practices for Indian Businesses
═══════════════════════════════════════════════════════════

"""
        
        # Add common issues by contract type
        for contract_type, issues in self.kb["common_issues"].items():
            content += f"\n{'='*60}\n"
            content += f"{contract_type.upper().replace('_', ' ')}\n"
            content += f"{'='*60}\n\n"
            
            for idx, issue in enumerate(issues, 1):
                content += f"{idx}. {issue['issue']}\n"
                content += f"   Description: {issue['description']}\n"
                content += f"   Frequency: {issue['frequency']} | Severity: {issue['severity']}\n"
                content += f"   Impact: {issue['impact']}\n"
                content += f"   ✓ Recommendation: {issue['recommendation']}\n"
                content += f"   Sample Clause: {issue['sample_clause']}\n\n"
        
        # Add best practices
        content += f"\n{'='*60}\n"
        content += "BEST PRACTICES FOR SME CONTRACTS\n"
        content += f"{'='*60}\n\n"
        
        for category, practices in self.kb["best_practices"].items():
            content += f"\n{category.upper().replace('_', ' ')}:\n"
            for practice in practices:
                content += f"  • {practice}\n"
        
        # Add Indian law info
        content += f"\n{'='*60}\n"
        content += "INDIAN LAW CONSIDERATIONS\n"
        content += f"{'='*60}\n\n"
        
        for category, points in self.kb["indian_law_specifics"].items():
            if isinstance(points, list):
                content += f"\n{category.upper().replace('_', ' ')}:\n"
                for point in points:
                    content += f"  • {point}\n"
        
        # Add statistics
        stats = self.kb["statistics"]
        content += f"\n{'='*60}\n"
        content += "KNOWLEDGE BASE STATISTICS\n"
        content += f"{'='*60}\n\n"
        content += f"Total Analyses Performed: {stats['total_analyses']}\n"
        content += f"Average Risk Score: {stats['average_risk_score']:.1f}/100\n"
        if stats['most_common_risks']:
            content += f"\nMost Common Risks:\n"
            for risk in stats['most_common_risks']:
                count = stats['issues_identified'].get(risk, 0)
                content += f"  • {risk.replace('_', ' ').title()}: {count} occurrences\n"
        
        content += f"\nLast Updated: {self.kb['last_updated']}\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path
