import markdown
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

# Read the Markdown file
with open('SYNOPSIS.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert Markdown to HTML
html_content = markdown.markdown(md_content)

# Create a PDF using reportlab
doc = SimpleDocTemplate("SYNOPSIS.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add the HTML content as paragraphs
for line in html_content.split('\n'):
    if line.strip():
        p = Paragraph(line, styles["Normal"])
        story.append(p)
        story.append(Spacer(1, 12))

# Build the PDF
doc.build(story)

print("PDF has been generated as SYNOPSIS.pdf") 