"""
NLP processing module using spaCy and NLTK for contract analysis
"""
import re
from typing import List, Dict, Tuple
import spacy
from spacy.matcher import Matcher
import nltk
# Ensure required NLTK data is available
def _download_nltk_data():
    required_packages = [
        "punkt",
        "punkt_tab",
        "stopwords",
        "wordnet",
        "omw-1.4"
    ]

    for pkg in required_packages:
        try:
            nltk.data.find(pkg)
        except LookupError:
            nltk.download(pkg, quiet=True)

_download_nltk_data()
from nltk.tokenize import sent_tokenize
from config import INDIAN_LAW_KEYWORDS

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)


class NLPProcessor:
    """NLP processing for contract text analysis"""
    
    def __init__(self):
        """Initialize NLP models safely for deployment"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError(
                "spaCy model 'en_core_web_sm' not installed. "
                "Ensure it is included in requirements.txt."
            )

        # Safe tokenizer fallback if punkt missing
        try:
            nltk.data.find('tokenizers/punkt')
            self.use_nltk = True
        except LookupError:
            self.use_nltk = False

        self.matcher = Matcher(self.nlp.vocab)
        self._setup_patterns()
    
    def _setup_patterns(self):
        """Setup spaCy patterns for clause detection"""
        # Pattern for detecting obligations (shall, must, will)
        obligation_pattern = [
            {"LOWER": {"IN": ["shall", "must", "will", "agrees", "undertakes"]}},
            {"OP": "*"},
            {"POS": "VERB"}
        ]
        
        # Pattern for rights (may, can, entitled)
        rights_pattern = [
            {"LOWER": {"IN": ["may", "can", "entitled", "right"]}},
            {"OP": "*"},
            {"POS": "VERB"}
        ]
        
        # Pattern for prohibitions (shall not, must not, cannot)
        prohibition_pattern = [
            {"LOWER": {"IN": ["shall", "must", "will", "cannot"]}},
            {"LOWER": "not"},
            {"OP": "*"},
            {"POS": "VERB"}
        ]
        
        self.matcher.add("OBLIGATION", [obligation_pattern])
        self.matcher.add("RIGHT", [rights_pattern])
        self.matcher.add("PROHIBITION", [prohibition_pattern])
    
    def extract_clauses(self, text: str) -> List[Dict[str, any]]:
        """
        Extract clauses from contract text
        
        Returns:
            List of clauses with metadata
        """
        clauses = []
        
        # Split by common clause patterns
        # Look for numbered clauses (1., 1.1, etc.) or lettered clauses (A., a., etc.)
        clause_pattern = r'(?:^|\n)(?:\d+\.|\d+\.\d+\.?|\([a-z]\)|\([0-9]+\)|[A-Z]\.|WHEREAS|THEREFORE)'
        
        splits = re.split(clause_pattern, text)
        
        # Also split by sentence if no clear structure
        if len(splits) <= 2:
            splits = sent_tokenize(text)
        
        for idx, clause_text in enumerate(splits):
            clause_text = clause_text.strip()
            if len(clause_text) > 20:  # Filter out very short fragments
                clause_type = self._classify_clause_type(clause_text)
                
                clauses.append({
                    "id": idx + 1,
                    "text": clause_text,
                    "type": clause_type,
                    "word_count": len(clause_text.split())
                })
        
        return clauses
    
    def _classify_clause_type(self, clause_text: str) -> str:
        """Classify clause as obligation, right, or prohibition"""
        doc = self.nlp(clause_text[:500])  # Process first 500 chars for efficiency
        matches = self.matcher(doc)
        
        if matches:
            match_id = matches[0][0]
            return self.nlp.vocab.strings[match_id].lower()
        
        return "general"
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from contract
        
        Returns:
            Dictionary of entity types and their values
        """
        doc = self.nlp(text[:10000])  # Process first 10k chars
        
        entities = {
            "parties": [],
            "dates": [],
            "amounts": [],
            "locations": [],
            "organizations": []
        }
        
        # Extract using spaCy NER
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG"]:
                if "party" in text[max(0, ent.start_char-50):ent.end_char+50].lower():
                    entities["parties"].append(ent.text)
                else:
                    entities["organizations"].append(ent.text)
            elif ent.label_ == "DATE":
                entities["dates"].append(ent.text)
            elif ent.label_ in ["MONEY", "CARDINAL"]:
                entities["amounts"].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                entities["locations"].append(ent.text)
        
        # Additional pattern-based extraction
        entities["amounts"].extend(self._extract_amounts(text))
        entities["dates"].extend(self._extract_dates(text))
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))[:10]  # Keep top 10
        
        return entities
    
    def _extract_amounts(self, text: str) -> List[str]:
        """Extract monetary amounts using regex"""
        patterns = [
            r'₹\s*[\d,]+(?:\.\d{2})?',  # Indian Rupees
            r'Rs\.?\s*[\d,]+(?:\.\d{2})?',  # Rupees
            r'\$\s*[\d,]+(?:\.\d{2})?',  # US Dollars
            r'INR\s*[\d,]+(?:\.\d{2})?'  # INR
        ]
        
        amounts = []
        for pattern in patterns:
            amounts.extend(re.findall(pattern, text))
        
        return amounts[:5]  # Return top 5
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates using regex patterns"""
        patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # DD/MM/YYYY or MM-DD-YYYY
            r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}',  # DD Month YYYY
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}'  # Month DD, YYYY
        ]
        
        dates = []
        for pattern in patterns:
            dates.extend(re.findall(pattern, text, re.IGNORECASE))
        
        return dates[:5]
    
    def detect_ambiguity(self, clause_text: str) -> Dict[str, any]:
        """
        Detect ambiguous language in clauses
        
        Returns:
            Dictionary with ambiguity score and indicators
        """
        ambiguous_terms = [
            "reasonable", "appropriate", "sufficient", "adequate",
            "may", "could", "should", "approximately", "about",
            "as soon as possible", "in due course", "promptly",
            "best efforts", "commercially reasonable"
        ]
        
        found_terms = []
        text_lower = clause_text.lower()
        
        for term in ambiguous_terms:
            if term in text_lower:
                found_terms.append(term)
        
        ambiguity_score = len(found_terms)
        is_ambiguous = ambiguity_score > 0
        
        return {
            "is_ambiguous": is_ambiguous,
            "score": ambiguity_score,
            "terms": found_terms
        }
    
    def check_indian_law_compliance(self, text: str) -> Dict[str, any]:
        """Check for Indian law references and compliance indicators"""
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in INDIAN_LAW_KEYWORDS:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
        
        has_jurisdiction = any(term in text_lower for term in ["jurisdiction", "governing law"])
        has_indian_reference = any(term in text_lower for term in ["india", "indian"])
        
        return {
            "has_compliance_indicators": len(found_keywords) > 0,
            "keywords_found": found_keywords,
            "has_jurisdiction_clause": has_jurisdiction,
            "has_indian_reference": has_indian_reference,
            "compliance_score": len(found_keywords)
        }
