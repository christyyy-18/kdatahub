#!/usr/bin/env python3
"""
K-DATAHUB Documentation PDF Generator (Simple Version)
Uses fpdf2 - lightweight alternative to reportlab
"""

import sys

try:
    from fpdf import FPDF
    print("FPDF2 found, proceeding with PDF generation...")
except ImportError:
    print("Installing fpdf2...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf2", "-q"])
    from fpdf import FPDF

from datetime import datetime

class K_DATAHUB_PDF(FPDF):
    def header(self):
        # Logo/Title area
        self.set_font("Arial", "B", 20)
        self.set_text_color(102, 126, 234)
        self.cell(0, 10, "K-DATAHUB", ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.set_text_color(118, 75, 162)
        self.cell(0, 5, "Complete Website Documentation", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_text_color(102, 126, 234)
        self.set_fill_color(240, 244, 255)
        self.cell(0, 10, title, ln=True, fill=True)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font("Arial", "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, text)
        self.ln()

    def add_section(self, title, content):
        self.set_font("Arial", "B", 12)
        self.set_text_color(118, 75, 162)
        self.cell(0, 8, title, ln=True)
        self.set_font("Arial", "", 9)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 4, content)
        self.ln(2)

# Create PDF
pdf = K_DATAHUB_PDF()
pdf.add_page()

# Title
pdf.set_font("Arial", "B", 24)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 15, "K-DATAHUB", ln=True, align="C")
pdf.set_font("Arial", "", 12)
pdf.set_text_color(118, 75, 162)
pdf.cell(0, 8, "Complete Website Documentation", ln=True, align="C")
pdf.ln(10)

pdf.set_font("Arial", "", 10)
pdf.set_text_color(100, 100, 100)
pdf.multi_cell(0, 5, f"Buy MTN, Airtel and Telecel plans instantly with the best prices, fast delivery, and support\n\nGenerated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}\nDjango Version: 5.0.2\nDatabase: SQLite3")

pdf.ln(10)

# Overview Section
pdf.chapter_title("Project Overview")
pdf.chapter_body(
    "K-DATAHUB is a modern Django web application that enables users to purchase telecom data plans "
    "(MTN, Airtel, and Telecel) with competitive pricing and fast delivery. The platform provides seamless "
    "payment integration through Paystack, user authentication, and agent registration system with automated "
    "account upgrades upon successful payment."
)

# Pages Section
pdf.chapter_title("Pages & Routes")
pages = [
    ("Homepage", "http://localhost:8000/", "Landing page with navigation and hero section"),
    ("Login", "http://localhost:8000/accounts/login/", "User authentication page"),
    ("Sign Up", "http://localhost:8000/accounts/signup/", "New user registration page"),
    ("Become Agent", "http://localhost:8000/accounts/become-agent/", "Agent registration with 25 GHS payment"),
    ("Support", "http://localhost:8000/support/", "Customer support and FAQ section")
]

for name, url, desc in pages:
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(102, 126, 234)
    pdf.cell(0, 6, name, ln=True)
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 4, f"URL: {url}\n{desc}")
    pdf.ln(2)

pdf.add_page()

# Technical Stack
pdf.chapter_title("Technical Stack")
tech_items = [
    ("Framework", "Django 5.0.2"),
    ("Language", "Python 3.8+"),
    ("Database", "SQLite3"),
    ("Frontend", "HTML5, CSS3, JavaScript"),
    ("Payment", "Paystack API"),
    ("SMS Service", "SMS notifications"),
    ("Deployment", "Vercel")
]

for tech, desc in tech_items:
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(102, 126, 234)
    pdf.cell(50, 5, tech + ":", 0)
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 5, desc)

pdf.ln(5)

# Project Structure
pdf.chapter_title("Project Structure")
pdf.set_font("Arial", "", 9)
pdf.set_text_color(50, 50, 50)
structure = """K-DATAHUB/
├── accounts/ - User authentication, profiles, agent requests
├── orders/ - Order management and tracking
├── payments/ - Payment processing with Paystack
├── kdatahub/ - Main project settings
├── static/ - CSS, JavaScript, images
├── templates/ - HTML templates
└── media/ - User uploads (profile pictures)"""
pdf.multi_cell(0, 4, structure)

pdf.add_page()

# Security Features
pdf.chapter_title("Security Features")
pdf.set_font("Arial", "", 9)
pdf.set_text_color(50, 50, 50)

security = [
    "CSRF protection on all forms",
    "Secure password hashing using Django's PBKDF2",
    "Session-based user authentication",
    "PCI-DSS Level 1 compliant payment processing",
    "SSL/TLS encryption for data in transit",
    "User data isolation and access controls",
    "Webhook verification for payment confirmations",
    "Admin-only access to sensitive information"
]

for i, feature in enumerate(security, 1):
    pdf.cell(5, 5, f"{i}.", 0)
    pdf.multi_cell(0, 5, feature)

pdf.ln(3)

# Payment Flow
pdf.chapter_title("Agent Registration Payment Flow")
pdf.set_font("Arial", "", 9)
pdf.set_text_color(50, 50, 50)

steps = [
    "1. User navigates to /accounts/become-agent/",
    "2. User completes registration form",
    "3. User clicks 'Pay 25 GHS & Register'",
    "4. Order created with 'pending' status",
    "5. User redirected to Paystack payment page",
    "6. User enters payment details (on Paystack)",
    "7. Payment processed securely",
    "8. Paystack sends webhook notification",
    "9. Order status updated to 'paid'",
    "10. User status upgraded to agent",
    "11. SMS notification sent to user",
    "12. User redirected to tracking page"
]

for step in steps:
    pdf.multi_cell(0, 4, step)

pdf.add_page()

# Database Models
pdf.chapter_title("Database Models")

pdf.set_font("Arial", "B", 11)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 6, "CustomUser Model", ln=True)
pdf.set_font("Arial", "", 9)
pdf.set_text_color(50, 50, 50)
pdf.multi_cell(0, 4, "Stores user account information including profile pictures, authentication credentials, and agent status.")

pdf.ln(3)

pdf.set_font("Arial", "B", 11)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 6, "Order Model", ln=True)
pdf.set_font("Arial", "", 9)
pdf.set_text_color(50, 50, 50)
pdf.multi_cell(0, 4, "Tracks all orders including item details, status, customer information, and payment references.")

pdf.ln(3)

pdf.set_font("Arial", "B", 11)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 6, "AgentRequest Model", ln=True)
pdf.set_font("Arial", "", 9)
pdf.set_text_color(50, 50, 50)
pdf.multi_cell(0, 4, "Manages agent registration requests with approval workflow.")

pdf.ln(5)

# Getting Started
pdf.chapter_title("Getting Started")
pdf.set_font("Arial", "", 9)
pdf.set_text_color(50, 50, 50)

setup = """1. Clone the repository: cd K-DATAHUB
2. Create virtual environment: python -m venv venv
3. Activate venv: source venv/bin/activate (Windows: venv\\Scripts\\activate)
4. Install dependencies: pip install -r requirements.txt
5. Run migrations: python manage.py migrate
6. Create superuser: python manage.py createsuperuser
7. Start server: python manage.py runserver
8. Access application: http://localhost:8000"""

pdf.multi_cell(0, 4, setup)

pdf.add_page()

# Support & Contact
pdf.chapter_title("Support & Contact")
pdf.set_font("Arial", "", 10)
pdf.set_text_color(50, 50, 50)

support_data = [
    ("WhatsApp Support", "https://wa.me/233594715103", "24/7 - The fastest way to get help"),
    ("Email Support", "support@kdatahub.com", "Business Hours - For detailed inquiries"),
    ("Phone Hotline", "+233594715103", "Mon-Fri 8am-6pm - Direct voice assistance")
]

for channel, contact, info in support_data:
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(102, 126, 234)
    pdf.cell(0, 6, channel, ln=True)
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 4, f"Contact: {contact}", ln=True)
    pdf.multi_cell(0, 4, f"Info: {info}")
    pdf.ln(2)

pdf.ln(5)

# FAQ
pdf.set_font("Arial", "B", 12)
pdf.set_text_color(102, 126, 234)
pdf.cell(0, 8, "Frequently Asked Questions", ln=True)

faq_items = [
    ("How long does delivery take?", "MTN and Airtel packages are delivered within 1-5 minutes. Telecel packages may take up to 15 minutes during peak hours."),
    ("What if I don't receive my data?", "Contact support on WhatsApp within 30 minutes with your Order ID for verification and manual fulfillment."),
    ("Is my payment secure?", "Yes, all payments are processed through Paystack (PCI-DSS Level 1). Card details are never stored on our servers.")
]

for q, a in faq_items:
    pdf.set_font("Arial", "B", 9)
    pdf.set_text_color(102, 126, 234)
    pdf.cell(0, 5, f"Q: {q}", ln=True)
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 4, f"A: {a}")
    pdf.ln(2)

# Add final page with copyright
pdf.add_page()
pdf.set_font("Arial", "B", 14)
pdf.set_text_color(102, 126, 234)
pdf.ln(50)
pdf.cell(0, 10, "End of Documentation", ln=True, align="C")
pdf.ln(10)
pdf.set_font("Arial", "", 10)
pdf.set_text_color(100, 100, 100)
pdf.multi_cell(0, 5, "© 2026 K-DATAHUB. All rights reserved.\n\nThis comprehensive documentation covers all aspects of the K-DATAHUB web application including pages, routes, technical implementation, security features, payment integration, and support information.\n\nFor the latest updates and more information, visit http://localhost:8000")

# Save PDF
pdf_filename = "K-DATAHUB_Documentation.pdf"
pdf.output(pdf_filename)

print(f"✅ PDF generated successfully!")
print(f"📁 Filename: {pdf_filename}")
print(f"📍 Location: {pdf_filename}")
print(f"✨ Ready to download!")
