"""
Risk analysis module for identifying and scoring contract risks
"""
import re
from typing import List, Dict, Tuple
from config import RISK_INDICATORS, RISK_LEVELS


class RiskAnalyzer:
    """Analyze contracts for potential risks and unfavorable terms"""
    
    def __init__(self):
        self.risk_indicators = RISK_INDICATORS
        self.risk_levels = RISK_LEVELS
    
    def analyze_clause_risk(self, clause: Dict[str, any]) -> Dict[str, any]:
        """
        Analyze a single clause for risk factors
        
        Args:
            clause: Dictionary containing clause text and metadata
            
        Returns:
            Dictionary with risk analysis results
        """
        text = clause.get("text", "").lower()
        risks_found = []
        risk_score = 0
        
        # Check for each risk indicator category
        for risk_type, keywords in self.risk_indicators.items():
            for keyword in keywords:
                if keyword in text:
                    risks_found.append({
                        "type": risk_type,
                        "keyword": keyword,
                        "severity": self._calculate_severity(risk_type, text)
                    })
                    risk_score += self._get_risk_weight(risk_type)
                    break  # Only count once per category
        
        # Determine overall risk level
        risk_level = self._determine_risk_level(risk_score)
        
        return {
            "clause_id": clause.get("id"),
            "risk_level": risk_level,
            "risk_score": risk_score,
            "risks_found": risks_found,
            "is_high_risk": risk_level == "HIGH",
            "recommendations": self._generate_recommendations(risks_found)
        }
    
    def analyze_contract_risk(self, clauses: List[Dict[str, any]]) -> Dict[str, any]:
        """
        Analyze entire contract and calculate composite risk score
        
        Args:
            clauses: List of clause dictionaries
            
        Returns:
            Dictionary with overall contract risk analysis
        """
        clause_risks = []
        total_risk_score = 0
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0
        
        risk_categories = {key: 0 for key in self.risk_indicators.keys()}
        
        for clause in clauses:
            risk_analysis = self.analyze_clause_risk(clause)
            clause_risks.append(risk_analysis)
            
            total_risk_score += risk_analysis["risk_score"]
            
            if risk_analysis["risk_level"] == "HIGH":
                high_risk_count += 1
            elif risk_analysis["risk_level"] == "MEDIUM":
                medium_risk_count += 1
            else:
                low_risk_count += 1
            
            # Count risk categories
            for risk in risk_analysis["risks_found"]:
                risk_categories[risk["type"]] += 1
        
        # Calculate composite risk score (0-100)
        avg_risk = total_risk_score / len(clauses) if clauses else 0
        composite_score = min(100, int(avg_risk * 20))  # Scale to 0-100
        
        # Determine overall risk level
        if composite_score >= 70:
            overall_risk = "HIGH"
        elif composite_score >= 40:
            overall_risk = "MEDIUM"
        else:
            overall_risk = "LOW"
        
        return {
            "composite_risk_score": composite_score,
            "overall_risk_level": overall_risk,
            "clause_risks": clause_risks,
            "risk_distribution": {
                "high": high_risk_count,
                "medium": medium_risk_count,
                "low": low_risk_count
            },
            "risk_categories": risk_categories,
            "total_clauses_analyzed": len(clauses),
            "critical_clauses": self._identify_critical_clauses(clause_risks)
        }
    
    def _calculate_severity(self, risk_type: str, clause_text: str) -> str:
        """Calculate severity based on risk type and context"""
        # High severity indicators
        high_severity_terms = ["unlimited", "sole discretion", "without notice", "forfeit", "immediate"]
        
        if any(term in clause_text for term in high_severity_terms):
            return "HIGH"
        
        # Risk types that are inherently high severity
        high_risk_types = ["penalty", "indemnity", "unilateral_termination", "ip_transfer"]
        if risk_type in high_risk_types:
            return "MEDIUM"
        
        return "LOW"
    
    def _get_risk_weight(self, risk_type: str) -> int:
        """Get numerical weight for risk type"""
        weights = {
            "penalty": 3,
            "indemnity": 3,
            "unilateral_termination": 3,
            "ip_transfer": 3,
            "non_compete": 2,
            "lock_in": 2,
            "auto_renewal": 2,
            "arbitration": 1
        }
        return weights.get(risk_type, 1)
    
    def _determine_risk_level(self, risk_score: int) -> str:
        """Determine risk level based on score"""
        if risk_score >= 5:
            return "HIGH"
        elif risk_score >= 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_recommendations(self, risks_found: List[Dict]) -> List[str]:
        """Generate recommendations for mitigating identified risks"""
        recommendations = []
        
        for risk in risks_found:
            risk_type = risk["type"]
            
            if risk_type == "penalty":
                recommendations.append("Consider negotiating a cap on penalties or liquidated damages")
            elif risk_type == "indemnity":
                recommendations.append("Request mutual indemnification or limit indemnity scope")
            elif risk_type == "unilateral_termination":
                recommendations.append("Negotiate for mutual termination rights or require notice period")
            elif risk_type == "ip_transfer":
                recommendations.append("Clarify IP ownership and consider licensing instead of full transfer")
            elif risk_type == "non_compete":
                recommendations.append("Limit non-compete scope, duration, and geographic area")
            elif risk_type == "lock_in":
                recommendations.append("Negotiate shorter lock-in period or early exit clauses")
            elif risk_type == "auto_renewal":
                recommendations.append("Request opt-in renewal instead of automatic renewal")
            elif risk_type == "arbitration":
                recommendations.append("Ensure arbitration venue is convenient and cost-effective")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _identify_critical_clauses(self, clause_risks: List[Dict]) -> List[Dict]:
        """Identify the most critical high-risk clauses"""
        high_risk_clauses = [
            clause for clause in clause_risks 
            if clause["risk_level"] == "HIGH"
        ]
        
        # Sort by risk score (descending)
        critical = sorted(high_risk_clauses, key=lambda x: x["risk_score"], reverse=True)
        
        return critical[:5]  # Return top 5 critical clauses
    
    def identify_unfavorable_terms(self, clauses: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Identify specifically unfavorable terms for SMEs
        
        Returns:
            List of unfavorable terms with explanations
        """
        unfavorable = []
        
        unfavorable_patterns = {
            "unlimited_liability": r"unlimited liability|without limit",
            "one_sided_termination": r"(?:may|can)\s+terminate.*without.*(?:cause|notice|reason)",
            "ip_assignment": r"assign.*all.*(?:intellectual property|IP|rights)",
            "exclusive_dealing": r"exclusive.*(?:right|dealing|arrangement)",
            "personal_guarantee": r"personal guarantee|personally liable",
            "waiver_of_rights": r"waive.*(?:all|any).*rights",
            "unilateral_changes": r"(?:may|can).*(?:modify|amend|change).*(?:unilaterally|at.*discretion)"
        }
        
        for clause in clauses:
            text = clause.get("text", "")
            
            for term_type, pattern in unfavorable_patterns.items():
                if re.search(pattern, text, re.IGNORECASE):
                    unfavorable.append({
                        "clause_id": clause.get("id"),
                        "clause_text": text[:200] + "..." if len(text) > 200 else text,
                        "term_type": term_type.replace("_", " ").title(),
                        "explanation": self._get_term_explanation(term_type),
                        "severity": "HIGH"
                    })
        
        return unfavorable
    
    def _get_term_explanation(self, term_type: str) -> str:
        """Get plain language explanation for unfavorable terms"""
        explanations = {
            "unlimited_liability": "This clause exposes you to potentially unlimited financial risk without a cap.",
            "one_sided_termination": "The other party can end the contract without reason while you may not have the same right.",
            "ip_assignment": "You would transfer all intellectual property rights, losing ownership of your creations.",
            "exclusive_dealing": "This restricts your ability to work with other clients or vendors.",
            "personal_guarantee": "You become personally liable, putting your personal assets at risk.",
            "waiver_of_rights": "You give up important legal protections and rights.",
            "unilateral_changes": "The other party can change terms without your agreement."
        }
        return explanations.get(term_type, "This term may put you at a disadvantage.")
