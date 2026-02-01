"""
Audit logging module for tracking contract analyses
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict
from config import AUDIT_LOG_DIR, ENABLE_AUDIT_LOGS


class AuditLogger:
    """Log all contract analysis activities for audit trail"""
    
    def __init__(self):
        self.log_dir = AUDIT_LOG_DIR
        self.enabled = ENABLE_AUDIT_LOGS
    
    def log_analysis(self, analysis_data: Dict) -> Path:
        """
        Log a contract analysis event
        
        Args:
            analysis_data: Analysis results and metadata
            
        Returns:
            Path to log file
        """
        if not self.enabled:
            return None
        
        timestamp = datetime.now()
        log_entry = {
            "timestamp": timestamp.isoformat(),
            "event_type": "contract_analysis",
            "file_name": analysis_data.get("file_name"),
            "contract_type": analysis_data.get("llm_analysis", {}).get("contract_type", {}).get("contract_type"),
            "risk_level": analysis_data.get("risk_analysis", {}).get("overall_risk_level"),
            "risk_score": analysis_data.get("risk_analysis", {}).get("composite_risk_score"),
            "processing_time": analysis_data.get("metadata", {}).get("processing_time"),
            "language": analysis_data.get("metadata", {}).get("language")
        }
        
        # Save to daily log file
        log_file = self.log_dir / f"audit_log_{timestamp.strftime('%Y%m%d')}.json"
        
        # Append to existing log
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return log_file
