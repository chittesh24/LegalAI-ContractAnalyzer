"""
LLM interface for advanced legal reasoning and analysis
Supports both Anthropic Claude and OpenAI GPT-4
"""
import os
import streamlit as st
from typing import Dict, List, Optional
from config import LLM_PROVIDER, ANTHROPIC_API_KEY, OPENAI_API_KEY, LLM_MODEL, MAX_TOKENS, TEMPERATURE


class LLMInterface:
    def __init__(self):
        self.provider = LLM_PROVIDER
        self.model = LLM_MODEL

        # Load API keys safely
        anthropic_key = ANTHROPIC_API_KEY or st.secrets.get("ANTHROPIC_API_KEY")
        openai_key = OPENAI_API_KEY or st.secrets.get("OPENAI_API_KEY")

        if self.provider == "anthropic":
            try:
                import anthropic

                if not anthropic_key:
                    print("WARNING: Anthropic API key missing. LLM disabled.")
                    self.client = None
                else:
                    self.client = anthropic.Anthropic(api_key=str(anthropic_key))


            except ImportError:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")

        elif self.provider == "openai":
            try:
                import openai

                if not openai_key:
                    print("WARNING: OpenAI API key missing. LLM disabled.")
                    self.client = None
                else:
                    self.client = openai.OpenAI(api_key=str(openai_key))

            except ImportError:
                raise ImportError("openai package not installed. Run: pip install openai")

        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def classify_contract_type(self, text: str) -> Dict[str, any]:
        """
        Classify the type of contract using LLM
        
        Returns:
            Dictionary with contract type and confidence
        """
        prompt = f"""Analyze the following contract text and classify it into one of these categories:
- Employment Agreement
- Vendor Contract
- Lease Agreement
- Partnership Deed
- Service Contract
- Non-Disclosure Agreement (NDA)
- Consultant Agreement
- Purchase Agreement
- Licensing Agreement
- Other

Contract text (first 2000 chars):
{text[:2000]}

Respond in JSON format:
{{
    "contract_type": "the category",
    "confidence": "high/medium/low",
    "reasoning": "brief explanation"
}}"""

        response = self._call_llm(prompt)
        return self._parse_json_response(response)
    
    def explain_clause(self, clause_text: str, context: str = "") -> str:
        """
        Provide plain-language explanation of a contract clause
        
        Args:
            clause_text: The clause to explain
            context: Optional contract context
            
        Returns:
            Plain language explanation
        """
        prompt = f"""You are a legal assistant helping SME business owners understand contracts.
Explain the following contract clause in simple, plain business language that a non-lawyer can understand.

Clause:
{clause_text}

{f"Contract context: {context[:500]}" if context else ""}

Provide:
1. What it means in simple terms
2. Why it matters to a business owner
3. Any important implications

Keep the explanation concise and practical."""

        return self._call_llm(prompt)
    
    def suggest_alternatives(self, clause_text: str, risk_type: str) -> List[str]:
        """
        Suggest alternative clauses that are more favorable
        
        Args:
            clause_text: Original clause
            risk_type: Type of risk identified
            
        Returns:
            List of alternative clause suggestions
        """
        prompt = f"""You are helping SME business owners negotiate better contract terms.

Original clause (identified as {risk_type}):
{clause_text}

Suggest 2-3 alternative clauses that would be more favorable to the business owner while still being reasonable for both parties.
Format each alternative clearly and explain briefly why it's better.

Provide alternatives that:
1. Reduce risk exposure
2. Add balance and fairness
3. Include reasonable protections

Format as numbered alternatives."""

        response = self._call_llm(prompt)
        # Parse numbered alternatives
        alternatives = []
        for line in response.split('\n'):
            if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-')):
                alternatives.append(line.strip())
        
        return alternatives if alternatives else [response]
    
    def generate_contract_summary(self, text: str, entities: Dict, risk_analysis: Dict) -> Dict[str, any]:
        """
        Generate comprehensive contract summary
        
        Args:
            text: Full contract text
            entities: Extracted entities
            risk_analysis: Risk analysis results
            
        Returns:
            Dictionary with structured summary
        """
        prompt = f"""You are analyzing a contract for an SME business owner. Provide a comprehensive summary.

Contract text (first 3000 chars):
{text[:3000]}

Key entities found:
- Parties: {', '.join(entities.get('parties', [])[:3])}
- Dates: {', '.join(entities.get('dates', [])[:3])}
- Amounts: {', '.join(entities.get('amounts', [])[:3])}

Risk level: {risk_analysis.get('overall_risk_level', 'Unknown')}

Provide a summary in JSON format:
{{
    "contract_purpose": "what this contract is for",
    "key_parties": ["party 1", "party 2"],
    "main_obligations": ["obligation 1", "obligation 2", "obligation 3"],
    "key_dates_and_terms": "important dates and duration",
    "payment_terms": "payment details if any",
    "termination_conditions": "how can it be terminated",
    "notable_clauses": ["any special terms worth highlighting"],
    "overall_assessment": "brief assessment for business owner"
}}

Be specific and practical."""

        response = self._call_llm(prompt)
        return self._parse_json_response(response)
    
    def check_legal_compliance(self, text: str, contract_type: str) -> Dict[str, any]:
        """
        Check for potential legal compliance issues (Indian law context)
        
        Returns:
            Dictionary with compliance analysis
        """
        prompt = f"""Analyze this {contract_type} for compliance with Indian business law standards.

Contract excerpt:
{text[:2500]}

Check for:
1. Proper jurisdiction and governing law clauses (should reference Indian law)
2. Compliance with Indian Contract Act principles
3. Proper party identification
4. Clear consideration (payment/exchange)
5. Legal capacity indicators
6. Any potentially illegal or unenforceable clauses

Respond in JSON format:
{{
    "has_jurisdiction_clause": true/false,
    "jurisdiction_location": "location mentioned",
    "has_governing_law": true/false,
    "governing_law": "law mentioned",
    "compliance_issues": ["issue 1", "issue 2"],
    "missing_elements": ["element 1", "element 2"],
    "recommendations": ["recommendation 1", "recommendation 2"]
}}"""

        response = self._call_llm(prompt)
        return self._parse_json_response(response)
    
    def identify_obligations(self, clauses: List[Dict]) -> Dict[str, List[str]]:
        """
        Identify and categorize obligations from clauses
        
        Returns:
            Dictionary categorizing obligations by party
        """
        clauses_text = "\n\n".join([f"Clause {c['id']}: {c['text'][:300]}" for c in clauses[:10]])
        
        prompt = f"""Analyze these contract clauses and identify the obligations for each party.

Clauses:
{clauses_text}

Categorize obligations as:
{{
    "party_a_obligations": ["obligation 1", "obligation 2"],
    "party_b_obligations": ["obligation 1", "obligation 2"],
    "mutual_obligations": ["obligation 1", "obligation 2"]
}}

Use generic "Party A" and "Party B" or actual party names if clear."""

        response = self._call_llm(prompt)
        return self._parse_json_response(response)
    
    def translate_hindi_to_english(self, text: str) -> str:
        """
        Translate Hindi text to English for analysis
        
        Args:
            text: Hindi text (Devanagari script)
            
        Returns:
            English translation
        """
        prompt = f"""Translate the following Hindi contract text to English. Maintain legal terminology and formal structure.

Hindi text:
{text[:2000]}

Provide accurate English translation:"""

        return self._call_llm(prompt)
    
    def _call_llm(self, prompt: str, max_tokens: int = MAX_TOKENS) -> str:
        """
        Call the configured LLM provider
        
        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens in response
            
        Returns:
            LLM response text
        """
        try:
            if self.provider == "anthropic":
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=TEMPERATURE,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return message.content[0].text
            
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a legal assistant helping SME business owners understand contracts."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=TEMPERATURE
                )
                return response.choices[0].message.content
        
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON from LLM response"""
        import json
        import re
        
        # Try to extract JSON from response
        try:
            # First try direct parsing
            return json.loads(response)
        except:
            # Try to find JSON in response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass
        
        # Return error dict if parsing fails
        return {"error": "Failed to parse response", "raw_response": response}
