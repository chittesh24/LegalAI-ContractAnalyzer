"""
Report generation module for creating PDF exports
"""
from pathlib import Path
from datetime import datetime
from typing import Dict
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


class ReportGenerator:
    """Generate PDF reports from contract analysis"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1f3c88'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskHigh',
            parent=self.styles['Normal'],
            textColor=colors.red,
            fontSize=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskMedium',
            parent=self.styles['Normal'],
            textColor=colors.orange,
            fontSize=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskLow',
            parent=self.styles['Normal'],
            textColor=colors.green,
            fontSize=12,
            fontName='Helvetica-Bold'
        ))
    
    def generate_pdf_report(self, analysis: Dict, output_path: Path):
        """Generate comprehensive PDF report"""
        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        story = []
        
        # Title
        story.append(Paragraph("Contract Analysis Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.extend(self._create_executive_summary(analysis))
        story.append(PageBreak())
        
        # Risk Analysis
        story.extend(self._create_risk_section(analysis))
        story.append(PageBreak())
        
        # Detailed Findings
        story.extend(self._create_findings_section(analysis))
        
        # Build PDF
        doc.build(story)
    
    def _create_executive_summary(self, analysis: Dict) -> list:
        """Create executive summary section"""
        elements = []
        metadata = analysis.get('metadata', {})
        risk = analysis.get('risk_analysis', {})
        
        elements.append(Paragraph("Executive Summary", self.styles['Heading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Basic info
        data = [
            ['Contract File:', metadata.get('file_name', 'N/A')],
            ['Analysis Date:', datetime.now().strftime('%Y-%m-%d %H:%M')],
            ['Contract Type:', analysis.get('llm_analysis', {}).get('contract_type', {}).get('contract_type', 'Unknown')],
            ['Risk Level:', risk.get('overall_risk_level', 'Unknown')],
            ['Risk Score:', f"{risk.get('composite_risk_score', 0)}/100"]
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_risk_section(self, analysis: Dict) -> list:
        """Create risk analysis section"""
        elements = []
        risk = analysis.get('risk_analysis', {})
        
        elements.append(Paragraph("Risk Analysis", self.styles['Heading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Risk distribution
        dist = risk.get('risk_distribution', {})
        elements.append(Paragraph(f"High Risk Clauses: {dist.get('high', 0)}", self.styles['RiskHigh']))
        elements.append(Paragraph(f"Medium Risk Clauses: {dist.get('medium', 0)}", self.styles['RiskMedium']))
        elements.append(Paragraph(f"Low Risk Clauses: {dist.get('low', 0)}", self.styles['RiskLow']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Critical clauses
        elements.append(Paragraph("Critical Issues:", self.styles['Heading2']))
        for critical in risk.get('critical_clauses', [])[:5]:
            for rec in critical.get('recommendations', []):
                elements.append(Paragraph(f"• {rec}", self.styles['Normal']))
        
        return elements
    
    def _create_findings_section(self, analysis: Dict) -> list:
        """Create detailed findings section"""
        elements = []
        
        elements.append(Paragraph("Detailed Findings", self.styles['Heading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Unfavorable terms
        unfavorable = analysis.get('unfavorable_terms', [])
        if unfavorable:
            elements.append(Paragraph("Unfavorable Terms:", self.styles['Heading2']))
            for term in unfavorable[:5]:
                elements.append(Paragraph(f"<b>{term.get('term_type')}:</b> {term.get('explanation')}", 
                                        self.styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        
        return elements
