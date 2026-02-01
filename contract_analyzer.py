"""
Main contract analyzer orchestrating all analysis components
"""
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
import json

from document_parser import DocumentParser
from nlp_processor import NLPProcessor
from risk_analyzer import RiskAnalyzer
from llm_interface import LLMInterface
from knowledge_base import KnowledgeBase


class ContractAnalyzer:
    """Main orchestrator for complete contract analysis"""
    
    def __init__(self):
        self.parser = DocumentParser()
        self.nlp = NLPProcessor()
        self.risk_analyzer = RiskAnalyzer()
        self.llm = LLMInterface()
        self.knowledge_base = KnowledgeBase()
    
    def analyze_contract(self, file_path: Path, use_llm: bool = True) -> Dict[str, any]:
        """
        Perform complete contract analysis
        
        Args:
            file_path: Path to contract file
            use_llm: Whether to use LLM for advanced analysis
            
        Returns:
            Comprehensive analysis results
        """
        analysis_start = datetime.now()
        
        # Step 1: Parse document
        parse_result = self.parser.parse_document(file_path)
        if not parse_result["success"]:
            return {
                "success": False,
                "error": parse_result["error"],
                "file_name": file_path.name
            }
        
        text = parse_result["text"]
        
        # Step 2: Detect language
        language = self.parser.detect_language(text)
        
        # Step 3: Translate if Hindi
        original_text = text
        if language in ['hi', 'mixed'] and use_llm:
            text = self.llm.translate_hindi_to_english(text)
        
        # Step 4: Extract clauses
        clauses = self.nlp.extract_clauses(text)
        
        # Step 5: Extract entities
        entities = self.nlp.extract_entities(text)
        
        # Step 6: Risk analysis
        risk_analysis = self.risk_analyzer.analyze_contract_risk(clauses)
        unfavorable_terms = self.risk_analyzer.identify_unfavorable_terms(clauses)
        
        # Step 7: Compliance check
        compliance = self.nlp.check_indian_law_compliance(text)
        
        # Step 8: LLM-powered analysis (if enabled)
        llm_analysis = {}
        if use_llm:
            try:
                # Contract classification
                contract_type_result = self.llm.classify_contract_type(text)
                llm_analysis["contract_type"] = contract_type_result
                
                # Generate summary
                summary = self.llm.generate_contract_summary(text, entities, risk_analysis)
                llm_analysis["summary"] = summary
                
                # Compliance check
                legal_compliance = self.llm.check_legal_compliance(
                    text, 
                    contract_type_result.get("contract_type", "Unknown")
                )
                llm_analysis["legal_compliance"] = legal_compliance
                
                # Identify obligations
                obligations = self.llm.identify_obligations(clauses[:15])  # Top 15 clauses
                llm_analysis["obligations"] = obligations
                
            except Exception as e:
                llm_analysis["error"] = f"LLM analysis failed: {str(e)}"
        
        # Step 9: Ambiguity detection
        ambiguous_clauses = []
        for clause in clauses:
            ambiguity = self.nlp.detect_ambiguity(clause["text"])
            if ambiguity["is_ambiguous"]:
                ambiguous_clauses.append({
                    "clause_id": clause["id"],
                    "clause_text": clause["text"][:200] + "...",
                    "ambiguity": ambiguity
                })
        
        analysis_end = datetime.now()
        processing_time = (analysis_end - analysis_start).total_seconds()
        
        # Add to knowledge base
        partial_result = {
            "risk_analysis": risk_analysis,
            "metadata": {"contract_type": llm_analysis.get("contract_type", {})}
        }
        self.knowledge_base.add_analysis_learnings(partial_result)
        
        # Compile results
        result = {
            "success": True,
            "file_name": file_path.name,
            "metadata": {
                "file_type": parse_result["file_type"],
                "char_count": parse_result["char_count"],
                "word_count": parse_result["word_count"],
                "language": language,
                "processing_time": processing_time,
                "analysis_timestamp": analysis_start.isoformat()
            },
            "clauses": clauses,
            "entities": entities,
            "risk_analysis": risk_analysis,
            "unfavorable_terms": unfavorable_terms,
            "compliance": compliance,
            "ambiguous_clauses": ambiguous_clauses,
            "llm_analysis": llm_analysis
        }
        
        return result
    
    def explain_clause_detailed(self, clause: Dict, context: str = "") -> Dict[str, any]:
        """
        Get detailed explanation for a specific clause
        
        Args:
            clause: Clause dictionary
            context: Contract context
            
        Returns:
            Detailed explanation with risks and alternatives
        """
        clause_text = clause.get("text", "")
        
        # Get risk analysis for this clause
        risk_analysis = self.risk_analyzer.analyze_clause_risk(clause)
        
        # Get ambiguity check
        ambiguity = self.nlp.detect_ambiguity(clause_text)
        
        # Get LLM explanation
        explanation = self.llm.explain_clause(clause_text, context)
        
        # Get alternatives if high risk
        alternatives = []
        if risk_analysis["is_high_risk"]:
            for risk in risk_analysis["risks_found"]:
                alts = self.llm.suggest_alternatives(clause_text, risk["type"])
                alternatives.extend(alts)
        
        return {
            "clause_id": clause.get("id"),
            "clause_text": clause_text,
            "explanation": explanation,
            "risk_analysis": risk_analysis,
            "ambiguity": ambiguity,
            "alternatives": alternatives[:3]  # Top 3 alternatives
        }
    
    def generate_report(self, analysis_result: Dict) -> Dict[str, any]:
        """
        Generate executive report from analysis
        
        Returns:
            Structured report for business owners
        """
        risk_analysis = analysis_result.get("risk_analysis", {})
        llm_analysis = analysis_result.get("llm_analysis", {})
        
        # Executive summary
        risk_level = risk_analysis.get("overall_risk_level", "UNKNOWN")
        risk_score = risk_analysis.get("composite_risk_score", 0)
        
        executive_summary = {
            "contract_name": analysis_result.get("file_name"),
            "analysis_date": analysis_result.get("metadata", {}).get("analysis_timestamp"),
            "contract_type": llm_analysis.get("contract_type", {}).get("contract_type", "Unknown"),
            "overall_risk": risk_level,
            "risk_score": risk_score,
            "recommendation": self._get_recommendation(risk_level, risk_score)
        }
        
        # Key findings
        key_findings = {
            "critical_issues": len(risk_analysis.get("critical_clauses", [])),
            "high_risk_clauses": risk_analysis.get("risk_distribution", {}).get("high", 0),
            "unfavorable_terms": len(analysis_result.get("unfavorable_terms", [])),
            "ambiguous_clauses": len(analysis_result.get("ambiguous_clauses", [])),
            "compliance_issues": len(llm_analysis.get("legal_compliance", {}).get("compliance_issues", []))
        }
        
        # Action items
        action_items = []
        
        # Add critical clause actions
        for critical in risk_analysis.get("critical_clauses", [])[:3]:
            action_items.extend(critical.get("recommendations", []))
        
        # Add compliance actions
        action_items.extend(
            llm_analysis.get("legal_compliance", {}).get("recommendations", [])
        )
        
        return {
            "executive_summary": executive_summary,
            "key_findings": key_findings,
            "action_items": list(set(action_items))[:10],  # Top 10 unique actions
            "detailed_analysis": {
                "entities": analysis_result.get("entities"),
                "risk_categories": risk_analysis.get("risk_categories"),
                "obligations": llm_analysis.get("obligations", {})
            }
        }
    
    def _get_recommendation(self, risk_level: str, risk_score: int) -> str:
        """Generate recommendation based on risk assessment"""
        if risk_level == "HIGH" or risk_score >= 70:
            return "⚠️ HIGH RISK: We strongly recommend legal review before signing. Several unfavorable terms identified."
        elif risk_level == "MEDIUM" or risk_score >= 40:
            return "⚡ MEDIUM RISK: Review highlighted clauses carefully. Consider negotiating key terms."
        else:
            return "✅ LOW RISK: Contract appears relatively balanced. Review standard terms and proceed with caution."
    
    def save_analysis(self, analysis_result: Dict, output_path: Path):
        """Save analysis results to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_result, f, indent=2, ensure_ascii=False)
