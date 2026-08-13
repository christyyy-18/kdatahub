#!/usr/bin/env python3
"""
K-DATAHUB Documentation PDF Generator
Generates a comprehensive PDF document of all website pages and documentation
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime

# Create PDF
pdf_filename = "K-DATAHUB_Documentation.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4,
                        rightMargin=0.75*inch, leftMargin=0.75*inch,
                        topMargin=0.75*inch, bottomMargin=0.75*inch)

# Container for PDF elements
elements = []

# Define custom styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#667eea'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor('#667eea'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold',
    borderColor=colors.HexColor('#667eea'),
    borderWidth=0,
    borderPadding=5
)

section_style = ParagraphStyle(
    'SectionHeading',
    parent=styles['Heading3'],
    fontSize=12,
    textColor=colors.HexColor('#764ba2'),
    spaceAfter=8,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=12
)

# Title Page
elements.append(Spacer(1, 1.5*inch))
elements.append(Paragraph("🌐 K-DATAHUB", title_style))
elements.append(Spacer(1, 0.2*inch))
elements.append(Paragraph("Complete Website Documentation", ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=16, alignment=TA_CENTER, textColor=colors.HexColor('#764ba2'))))
elements.append(Spacer(1, 0.1*inch))
elements.append(Paragraph("Buy MTN, Airtel and Telecel plans instantly with the best prices, fast delivery, and support", ParagraphStyle('subtitle2', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER, textColor=colors.grey)))
elements.append(Spacer(1, 1*inch))
elements.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}", body_style))
elements.append(Paragraph(f"<b>Django Version:</b> 5.0.2", body_style))
elements.append(Paragraph(f"<b>Database:</b> SQLite3", body_style))
elements.append(PageBreak())

# Table of Contents
elements.append(Paragraph("Table of Contents", heading_style))
elements.append(Spacer(1, 0.2*inch))
toc_data = [
    ["1.", "Project Overview"],
    ["2.", "Pages & Routes"],
    ["3.", "Technical Stack"],
    ["4.", "Project Structure"],
    ["5.", "Security Features"],
    ["6.", "Payment Integration"],
    ["7.", "Database Models"],
    ["8.", "Getting Started"],
    ["9.", "Support & Contact"]
]
toc_table = Table(toc_data, colWidths=[0.5*inch, 5.5*inch])
toc_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f0f4ff')])
]))
elements.append(toc_table)
elements.append(PageBreak())

# Project Overview
elements.append(Paragraph("1. Project Overview", heading_style))
elements.append(Paragraph(
    "K-DATAHUB is a modern Django web application that enables users to purchase telecom data plans "
    "(MTN, Airtel, and Telecel) with competitive pricing and fast delivery. The platform provides seamless "
    "payment integration through Paystack, user authentication, and agent registration system with automated "
    "account upgrades upon successful payment.",
    body_style
))

# Pages Overview
elements.append(Paragraph("2. Pages & Routes", heading_style))

pages_data = [
    ("Homepage", "http://localhost:8000", "Landing page with navigation and hero section"),
    ("Login", "http://localhost:8000/accounts/login/", "User authentication page"),
    ("Sign Up", "http://localhost:8000/accounts/signup/", "New user registration page"),
    ("Become Agent", "http://localhost:8000/accounts/become-agent/", "Agent registration with ₵25 payment"),
    ("Support", "http://localhost:8000/support/", "Customer support and FAQ")
]

for page_name, url, desc in pages_data:
    elements.append(Paragraph(f"<b>{page_name}</b>", section_style))
    elements.append(Paragraph(f"<b>URL:</b> {url}", body_style))
    elements.append(Paragraph(f"<b>Description:</b> {desc}", body_style))
    elements.append(Spacer(1, 0.1*inch))

elements.append(PageBreak())

# Technical Stack
elements.append(Paragraph("3. Technical Stack", heading_style))

tech_data = [
    ["Component", "Technology"],
    ["Framework", "Django 5.0.2"],
    ["Language", "Python 3.8+"],
    ["Database", "SQLite3"],
    ["Frontend", "HTML5, CSS3, JavaScript"],
    ["Payment Gateway", "Paystack API"],
    ["SMS Service", "SMS notifications"],
    ["Deployment", "Vercel"],
    ["Server", "Django Development Server"]
]

tech_table = Table(tech_data, colWidths=[2.5*inch, 3.5*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
elements.append(tech_table)
elements.append(Spacer(1, 0.2*inch))

elements.append(PageBreak())

# Project Structure
elements.append(Paragraph("4. Project Structure", heading_style))
elements.append(Paragraph("The K-DATAHUB project is organized into several Django apps:", body_style))
elements.append(Spacer(1, 0.1*inch))

apps_data = [
    ["App", "Purpose"],
    ["accounts", "User authentication, profiles, agent requests"],
    ["orders", "Order management and tracking"],
    ["payments", "Payment processing with Paystack"],
    ["kdatahub", "Main project settings and configuration"],
    ["static", "CSS, JavaScript, images"],
    ["templates", "HTML templates for all pages"],
    ["media", "User uploads (profile pictures)"]
]

apps_table = Table(apps_data, colWidths=[2.5*inch, 3.5*inch])
apps_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
elements.append(apps_table)
elements.append(Spacer(1, 0.2*inch))

elements.append(PageBreak())

# Security Features
elements.append(Paragraph("5. Security Features", heading_style))
elements.append(Paragraph(
    "K-DATAHUB implements comprehensive security measures to protect user data and transactions:",
    body_style
))
elements.append(Spacer(1, 0.1*inch))

security_features = [
    "CSRF protection on all forms",
    "Secure password hashing using Django's PBKDF2",
    "Session-based user authentication",
    "PCI-DSS Level 1 compliant payment processing via Paystack",
    "SSL/TLS encryption for data in transit",
    "User data isolation and access controls",
    "Webhook verification for payment confirmations",
    "Admin-only access to sensitive information"
]

for i, feature in enumerate(security_features, 1):
    elements.append(Paragraph(f"<b>{i}.</b> {feature}", body_style))

elements.append(PageBreak())

# Payment Flow
elements.append(Paragraph("6. Payment Integration", heading_style))
elements.append(Paragraph(
    "Agent Registration Payment Flow:",
    section_style
))
elements.append(Spacer(1, 0.1*inch))

payment_steps = [
    ("1", "User navigates to /accounts/become-agent/"),
    ("2", "User completes registration form"),
    ("3", "User clicks 'Pay ₵25.00 & Register'"),
    ("4", "Order created with 'pending' status"),
    ("5", "User redirected to Paystack payment page"),
    ("6", "User enters payment details (on Paystack)"),
    ("7", "Payment processed securely"),
    ("8", "Paystack sends webhook notification"),
    ("9", "Order status updated to 'paid'"),
    ("10", "User status upgraded to agent"),
    ("11", "SMS notification sent to user"),
    ("12", "User redirected to tracking page")
]

for step, description in payment_steps:
    elements.append(Paragraph(f"<b>Step {step}:</b> {description}", body_style))

elements.append(PageBreak())

# Database Models
elements.append(Paragraph("7. Database Models", heading_style))

elements.append(Paragraph("<b>CustomUser Model</b>", section_style))
elements.append(Paragraph(
    "Stores user account information including profile pictures, authentication credentials, and agent status.",
    body_style
))

elements.append(Paragraph("<b>Order Model</b>", section_style))
elements.append(Paragraph(
    "Tracks all orders including item details, status, customer information, and payment references.",
    body_style
))

elements.append(Paragraph("<b>AgentRequest Model</b>", section_style))
elements.append(Paragraph(
    "Manages agent registration requests with approval workflow.",
    body_style
))

elements.append(PageBreak())

# Getting Started
elements.append(Paragraph("8. Getting Started", heading_style))
elements.append(Paragraph(
    "To set up and run K-DATAHUB locally:",
    body_style
))
elements.append(Spacer(1, 0.1*inch))

setup_steps = [
    ("1. Clone the repository", "cd K-DATAHUB"),
    ("2. Create virtual environment", "python -m venv venv"),
    ("3. Activate venv", "source venv/bin/activate  # Windows: venv\\Scripts\\activate"),
    ("4. Install dependencies", "pip install -r requirements.txt"),
    ("5. Run migrations", "python manage.py migrate"),
    ("6. Create superuser", "python manage.py createsuperuser"),
    ("7. Start server", "python manage.py runserver"),
    ("8. Access application", "http://localhost:8000")
]

for step, command in setup_steps:
    elements.append(Paragraph(f"<b>{step}</b>", body_style))
    elements.append(Paragraph(f"<font face='Courier'>{command}</font>", ParagraphStyle('code', parent=styles['Normal'], fontSize=9, fontName='Courier', textColor=colors.HexColor('#333333'))))
    elements.append(Spacer(1, 0.08*inch))

elements.append(PageBreak())

# Support & Contact
elements.append(Paragraph("9. Support & Contact", heading_style))

support_data = [
    ["Channel", "Contact", "Availability"],
    ["WhatsApp", "https://wa.me/233594715103", "24/7"],
    ["Email", "support@kdatahub.com", "Business Hours"],
    ["Phone", "+233594715103", "Mon-Fri 8am-6pm"]
]

support_table = Table(support_data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch])
support_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
elements.append(support_table)

# FAQ Section
elements.append(Spacer(1, 0.3*inch))
elements.append(Paragraph("Frequently Asked Questions", section_style))
elements.append(Spacer(1, 0.1*inch))

faqs = [
    ("How long does delivery take?", 
     "MTN and Airtel packages are delivered within 1-5 minutes. Telecel packages may take up to 15 minutes during peak hours."),
    ("What if I don't receive my data?",
     "Contact support on WhatsApp within 30 minutes with your Order ID for verification and manual fulfillment."),
    ("Is my payment secure?",
     "Yes, all payments are processed through Paystack (PCI-DSS Level 1). Card details are never stored on our servers.")
]

for question, answer in faqs:
    elements.append(Paragraph(f"<b>Q: {question}</b>", body_style))
    elements.append(Paragraph(f"<b>A:</b> {answer}", body_style))
    elements.append(Spacer(1, 0.1*inch))

# Footer
elements.append(Spacer(1, 0.5*inch))
elements.append(Paragraph(
    f"© 2026 K-DATAHUB. All rights reserved. | Documentation generated on {datetime.now().strftime('%B %d, %Y')}",
    ParagraphStyle('footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)
))

# Build PDF
doc.build(elements)
print(f"✅ PDF generated successfully: {pdf_filename}")
print(f"📍 Location: {pdf_filename}")
print(f"💾 Size: Check file size in explorer")
print(f"📥 Ready to download!")
