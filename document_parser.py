"""
Document parsing module for extracting text from various file formats
"""
import re
from pathlib import Path
from typing import Dict, Optional
import PyPDF2
import pdfplumber
from docx import Document


class DocumentParser:
    """Parse various document formats and extract text content"""
    
    @staticmethod
    def parse_pdf(file_path: Path) -> str:
        """Extract text from PDF files"""
        text = ""
        
        # Try pdfplumber first (better for complex PDFs)
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
        except Exception as e:
            print(f"pdfplumber failed: {e}, trying PyPDF2...")
        
        # Fallback to PyPDF2
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Failed to parse PDF: {e}")
        
        return text
    
    @staticmethod
    def parse_docx(file_path: Path) -> str:
        """Extract text from DOCX files"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Failed to parse DOCX: {e}")
    
    @staticmethod
    def parse_txt(file_path: Path) -> str:
        """Extract text from TXT files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
    
    @classmethod
    def parse_document(cls, file_path: Path) -> Dict[str, any]:
        """
        Parse document and return extracted text with metadata
        
        Args:
            file_path: Path to the document
            
        Returns:
            Dict containing text, metadata, and parsing status
        """
        suffix = file_path.suffix.lower()
        
        try:
            if suffix == '.pdf':
                text = cls.parse_pdf(file_path)
            elif suffix in ['.docx', '.doc']:
                text = cls.parse_docx(file_path)
            elif suffix == '.txt':
                text = cls.parse_txt(file_path)
            else:
                raise ValueError(f"Unsupported file format: {suffix}")
            
            # Basic preprocessing
            text = cls.preprocess_text(text)
            
            return {
                "success": True,
                "text": text,
                "char_count": len(text),
                "word_count": len(text.split()),
                "file_type": suffix,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "char_count": 0,
                "word_count": 0,
                "file_type": suffix,
                "error": str(e)
            }
    
    @staticmethod
    def preprocess_text(text: str) -> str:
        """Basic text preprocessing"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\-\(\)\[\]\"\'\₹\$\%\@]', '', text)
        return text.strip()
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect if text contains Hindi (Devanagari script)
        
        Returns:
            'hi' for Hindi, 'en' for English, 'mixed' for both
        """
        # Check for Devanagari Unicode range
        hindi_pattern = re.compile(r'[\u0900-\u097F]')
        
        has_hindi = bool(hindi_pattern.search(text))
        has_english = bool(re.search(r'[a-zA-Z]', text))
        
        if has_hindi and has_english:
            return 'mixed'
        elif has_hindi:
            return 'hi'
        else:
            return 'en'
