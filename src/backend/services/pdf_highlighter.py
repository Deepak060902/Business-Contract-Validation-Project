from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
import difflib
import re

def highlight_differences(text1, text2):
    differ = difflib.Differ()
    diff = list(differ.compare(text1.split(), text2.split()))
    highlighted_text = []
    for word in diff:
        if word.startswith('- '):
            highlighted_text.append(f'<font color="red">{word[2:]}</font>')
        elif word.startswith('  '):
            highlighted_text.append(word[2:])    
    return ' '.join(highlighted_text)

def generate_pdf(clauses, deviations):
    output_filename = 'highlighted_contract.pdf' 
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                            rightMargin=15, leftMargin=15,
                            topMargin=15, bottomMargin=15)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    story = []
    story.append(Paragraph("Contract with Highlighted Deviations", styles['Title']))
    story.append(Spacer(1, 12))

    for clause_name, clause_content in clauses.items():
    
        story.append(Paragraph(clause_name, styles['Heading2']))
        if clause_name in deviations.keys():
            if deviations[clause_name][1] == "Missing clause":
                p = Paragraph(f"<font color=red>This clause is missing from the actual contract. Template text: {template_text}</font>", styles['Normal'])
            else:
                highlighted_text = highlight_differences(clause_content, deviations[clause_name][1])
            
                p = Paragraph(highlighted_text, styles['Justify'])
            story.append(p)
        else:
            story.append(Paragraph(clause_content, styles['Justify']))
        story.append(Spacer(1,12))

    doc.build(story)
    return output_filename

