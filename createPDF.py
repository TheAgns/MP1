from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

def create_invitation_pdf(invitee_name, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []

  
    logo = Image("grøn.png", width=100, height=100)  # Replace with your company logo
    story.append(logo)

    report_title = Paragraph("Company Name Yearly Report", styles["Title"])
    story.append(report_title)

    story.append(Spacer(1, 20))

    invite_text = f"Her ses vores report"

    invite_paragraph = Paragraph(invite_text, styles["Normal"])
    story.append(invite_paragraph)


    doc.build(story)

invitee_name = "Kollega"
pdf_filename = "yearly_report.pdf"

create_invitation_pdf(invitee_name, pdf_filename)

