import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. Generate and Save the Visual Chart
categories = ['Ring', 'Key Chain', 'Bangles', 'Hair Clip', 'Lipstick', 'Ribbon']
quantities = [128, 63, 43, 18, 13, 9]
revenues = [1865, 2255, 3910, 332, 460, 90]

fig, ax1 = plt.subplots(figsize=(7, 3.2))

color = '#1A365D'
ax1.set_xlabel('Product Name', fontweight='bold', fontsize=9)
ax1.set_ylabel('Quantity Sold (Units)', color=color, fontweight='bold', fontsize=9)
bars = ax1.bar(categories, quantities, color=color, alpha=0.8, width=0.45)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  
color = '#C53030'
ax2.set_ylabel('Total Revenue (₹)', color=color, fontweight='bold', fontsize=9)
lines = ax2.plot(categories, revenues, color=color, marker='o', linewidth=2, markersize=6)
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Product Performance: Units Sold vs. Revenue Generated', fontsize=11, pad=10, fontweight='bold')
fig.tight_layout()
chart_path = "sales_chart.png"
plt.savefig(chart_path, dpi=300)
plt.close()

# 2. Build PDF Layout
pdf_filename = "Accessories_Stall_Report.pdf"
doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    rightMargin=36,
    leftMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#1A365D'))
h2_style = ParagraphStyle('Heading2Custom', parent=styles['Heading2'], fontSize=11, leading=15, textColor=colors.HexColor('#2B6CB0'), spaceBefore=8, spaceAfter=4)
body_style = ParagraphStyle('BodyCustom', parent=styles['Normal'], fontSize=8.5, leading=12, textColor=colors.HexColor('#2D3748'))

story = []

# Title Header
story.append(Paragraph("Accessories Stall Performance & Consumer Behavior Analysis", title_style))
story.append(Spacer(1, 4))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1A365D'), spaceAfter=8))

# Executive Summary
story.append(Paragraph("Executive Summary", h2_style))
story.append(Paragraph("This report analyzes sales performance, peak operational hours, gender-based product preferences, and consumer purchasing psychology based on transaction records from the <b>Fashion Blast</b> accessories stall.", body_style))
story.append(Spacer(1, 6))

# Table
story.append(Paragraph("1. Product Performance & Popularity", h2_style))
data = [
    ["Item Name", "Quantity Sold", "Total Value (₹)", "Demographic & Preference Level"],
    ["Ring", "128", "1,865.00", "High Preference (Girls / Mixed)"],
    ["Key Chain", "63", "2,255.00", "High Preference (Boys / Unisex)"],
    ["Bangles", "43", "3,910.00", "High Value & Volume (Girls)"],
    ["Hair Clip", "18", "332.00", "Moderate Preference (Girls)"],
    ["Lipstick", "13", "460.00", "Moderate Preference (Girls)"],
    ["Ribbon", "9", "90.00", "Low Preference (Girls)"],
    ["Other Items", "16", "6,856.00", "Targeted / Specialized"]
]

t = Table(data, colWidths=[80, 85, 85, 270])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')]),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t)
story.append(Spacer(1, 8))

# Embedded Graph
story.append(Image(chart_path, width=520, height=225))
story.append(Spacer(1, 6))

# Key Insights
story.append(Paragraph("2. Peak Hours & Consumer Psychology Highlights", h2_style))
story.append(Paragraph("• <b>Peak Time:</b> 11:13 AM – 11:40 AM saw over 20 transactions within short 1–2 minute intervals.", body_style))
story.append(Paragraph("• <b>Impulse Buying:</b> High volume in low-priced items (Rings: 128 units) demonstrates quick, instant-gratification purchasing.", body_style))
story.append(Paragraph("• <b>Gender Preferences:</b> Male buyers favored practical items (Key Chains), while female buyers selected aesthetic products (Rings, Bangles, Clips).", body_style))

# Build PDF
doc.build(story)
print("Successfully generated 'Accessories_Stall_Report.pdf'")