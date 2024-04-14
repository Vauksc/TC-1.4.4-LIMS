from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def create_pdf_report(file_name, sample_data, test_data):
    doc = SimpleDocTemplate(file_name, pagesize=A4)
    elements = []

    header_text = "Sample testing report"
    sample_text = "Sample information:"
    test_text = "Test information and result:"
    footer_text = f"Report generated on {str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}"

    styles = getSampleStyleSheet()
    header_style = styles["h1"]
    body_style = styles["Normal"]
    spacer = Spacer(1, 25)
    header = Paragraph(header_text, header_style)
    sample_body = Paragraph(sample_text, body_style)
    test_body = Paragraph(test_text, body_style)
    footer = Paragraph(footer_text, body_style)
    table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    sample_table = Table(sample_data)
    sample_table.setStyle(table_style)

    test_table = Table(test_data)
    test_table.setStyle(table_style)

    elements.append(header)
    elements.append(spacer)
    elements.append(sample_body)
    elements.append(spacer)
    elements.append(sample_table)
    elements.append(spacer)
    elements.append(test_body)
    elements.append(spacer)
    elements.append(test_table)
    elements.append(spacer)
    elements.append(spacer)
    elements.append(footer)

    doc.build(elements)
