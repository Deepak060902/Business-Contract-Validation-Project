import re
from typing import List, Dict
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



def classify_text(text: str) -> Dict[str, str]:
    patterns = {
        "Introduction": r"(BUSINESS CONTRACT|WHEREAS|NOW, THEREFORE)",
        "Definitions": r"(Definitions)",
        "Scope of Services": r"(Scope of Services)",
        "Delivery of Products": r"(Delivery of Products)",
        "Payment Terms": r"(Payment Terms)",
        "Term and Termination": r"(Term and Termination)",
        "Confidentiality": r"(Confidentiality|Non-Disclosure)",
        "Intellectual Property": r"(Intellectual Property)",
        "Warranties and Representations": r"(Warranties and Representations)",
        "Indemnification": r"(Indemnification)",
        "Limitation of Liability": r"(Limitation of Liability)",
        "Dispute Resolution": r"(Dispute Resolution)",
        "Miscellaneous": r"(Miscellaneous|Governing Law)",
    }
    
    clauses = {}
    current_clause = "General"
    clause_text = []
    
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        for clause, pattern in patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                if current_clause not in clauses:
                    clauses[current_clause] = ""
                clauses[current_clause] += "\n".join(clause_text).strip()
                current_clause = clause
                clause_text = []
                break
        clause_text.append(line)
    
    if current_clause not in clauses:
        clauses[current_clause] = ""
    clauses[current_clause] += "\n".join(clause_text).strip()
    
    return clauses
