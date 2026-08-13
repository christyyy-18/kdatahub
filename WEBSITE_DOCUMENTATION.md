# K-DATAHUB - Complete Website Documentation

## Project Overview
**K-DATAHUB** is a modern Django web application that enables users to purchase telecom data plans (MTN, Airtel, and Telecel) with competitive pricing and fast delivery.

---

## 🏠 Pages & Routes

### 1. **Homepage**
- **URL**: `http://localhost:8000/`
- **Route**: `/`
- **Description**: Landing page showcasing K-DATAHUB services

#### Features:
- Prominent K-DATAHUB branding
- Main navigation menu
- Hero section with service description
- Call-to-action buttons
- Professional styling with responsive design

#### Navigation Links:
- Home (active)
- Login → `/accounts/login/`
- Sign Up → `/accounts/signup/`
- Become Agent → `/accounts/become-agent/`
- Support → `/support/`

---

### 2. **Login Page**
- **URL**: `http://localhost:8000/accounts/login/`
- **Route**: `/accounts/login/`
- **Description**: User authentication page

#### Form Fields:
- **Username** - Text input for username or email
- **Password** - Secure password input
- **Submit Button** - "Authorize & Login"

#### Features:
- CSRF protection enabled
- Input validation
- Link to signup page for new users
- Clear, professional form layout

#### Backend Processing:
- Validates credentials against the database
- Creates session on successful authentication
- Redirects to dashboard or home on success
- Shows error messages for invalid credentials

---

### 3. **Sign Up Page**
- **URL**: `http://localhost:8000/accounts/signup/`
- **Route**: `/accounts/signup/`
- **Description**: New user registration page

#### Form Fields:
1. **Username** - Max 150 characters (letters, digits, @, ., +, -, _)
2. **Email Address** - Valid email format required
3. **Phone Number** - For contact purposes
4. **Profile Picture** - File upload
5. **Password** - With strength requirements
6. **Confirm Password** - Must match password field

#### Password Requirements:
- At least 8 characters
- Cannot be entirely numeric
- Cannot be too similar to personal information
- Cannot be a commonly used password

#### Features:
- Client-side form validation
- Server-side validation
- File upload for profile pictures
- Link to login page for existing users
- User-friendly error messages

#### Backend Processing:
- Creates new CustomUser object
- Stores profile information
- Saves profile picture to media/profile_pics/
- Generates unique user ID
- Sends verification email (if configured)

---

### 4. **Become an Agent Page**
- **URL**: `http://localhost:8000/accounts/become-agent/`
- **Route**: `/accounts/become-agent/`
- **Description**: Agent registration with payment processing

#### Registration Fee:
- **Amount**: ₵25.00 (Ghanaian Cedis)
- **Benefits**: Unlock agent-specific features and discounted rates

#### Form Fields:
1. **Username** - Unique username
2. **Email Address** - Contact email
3. **Phone Number** - For notifications
4. **Profile Picture** - Upload image
5. **Password** - With strength requirements
6. **Password Confirmation** - Verify password

#### Payment Integration:
- **Payment Gateway**: Paystack
- **Button Text**: "Pay ₵25.00 & Register"
- **Security**: PCI-DSS Level 1 compliant
- **Process**: 
  1. User completes form
  2. Order created with "pending" status
  3. User redirected to Paystack payment page
  4. Upon successful payment, user account upgraded to agent
  5. SMS notification sent to user

#### Agent Benefits:
- Discounted rates on all data plans
- Access to agent dashboard
- Order tracking and management
- Commission structure (if applicable)
- Priority support

---

### 5. **Support Page**
- **URL**: `http://localhost:8000/support/`
- **Route**: `/support/`
- **Description**: Customer support and FAQ section

#### Support Channels:

##### 💬 WhatsApp Support
- **URL**: https://wa.me/233594715103
- **Description**: The fastest way to get help
- **Availability**: 24/7

##### 📧 Email Support
- **Email**: support@kdatahub.com
- **Description**: For detailed inquiries or complex technical issues

##### 📞 Phone Hotline
- **Phone**: +233594715103
- **Hours**: Mon-Fri, 8am to 6pm

#### FAQ Section:

**Q: How long does delivery take?**
- A: MTN and Airtel packages are usually delivered within 1-5 minutes
- Telecel packages may take up to 15 minutes during peak hours

**Q: What if I don't receive my data?**
- A: Contact support on WhatsApp within 30 minutes with your Order ID
- We'll verify and provide manual fulfillment if needed

**Q: Is my payment secure?**
- A: Yes, all payments are processed through Paystack (PCI-DSS Level 1)
- Card details are never stored on K-DATAHUB servers

---

## 🔧 Technical Stack

### Backend
- **Framework**: Django 5.0.2
- **Language**: Python
- **Database**: SQLite3 (db.sqlite3)
- **Server**: Django Development Server

### Frontend
- **Markup**: HTML5
- **Styling**: CSS3
- **Scripting**: JavaScript (ES6+)
- **Design**: Responsive & Mobile-First

### Integrations
- **Payment**: Paystack API
- **SMS**: SMS service (kdatahub/sms.py)
- **Deployment**: Vercel

---

## 📂 Project Structure

```
K-DATAHUB/
│
├── accounts/                    # User authentication app
│   ├── __init__.py
│   ├── admin.py                # Django admin configuration
│   ├── apps.py                 # App configuration
│   ├── forms.py                # User forms
│   ├── models.py               # CustomUser model
│   ├── views.py                # Authentication views
│   ├── urls.py                 # URL patterns
│   ├── tests.py                # Unit tests
│   ├── migrations/             # Database migrations
│   └── static/                 # CSS and JS for accounts
│
├── orders/                      # Order management app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Order model
│   ├── views.py                # Order views
│   ├── urls.py
│   ├── tests.py
│   ├── migrations/
│   └── templates/              # Order templates
│
├── payments/                    # Payment processing app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Payment models
│   ├── views.py                # Payment views (verify, webhook)
│   ├── utils.py                # Paystack API utilities
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
│
├── kdatahub/                    # Main project settings
│   ├── __init__.py
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL routing
│   ├── asgi.py                 # ASGI configuration
│   ├── wsgi.py                 # WSGI configuration
│   ├── views.py                # Project-level views
│   ├── sms.py                  # SMS notification service
│   └── templates/              # Base templates
│
├── static/                      # Static files (CSS, JS, images)
│   ├── css/
│   │   ├── styles.css
│   │   └── js-effects.css
│   ├── img/
│   └── js/
│       └── main.js
│
├── staticfiles_build/          # Collected static files
│
├── templates/                   # HTML templates
│   ├── base.html               # Base template
│   ├── home.html               # Homepage
│   ├── dashboard.html          # Dashboard
│   ├── my_orders.html          # User orders page
│   ├── support.html            # Support page
│   ├── accounts/               # Account templates
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── become_agent.html
│   │   ├── profile.html
│   │   └── password_reset_*.html
│   └── orders/                 # Order templates
│
├── media/                       # User uploads
│   └── profile_pics/           # User profile pictures
│
├── manage.py                    # Django management script
├── db.sqlite3                  # SQLite database
├── requirements.txt            # Python dependencies
├── vercel.json                 # Vercel deployment config
├── DEPLOYMENT_GUIDE_V3.md      # Deployment documentation
└── k-datahub_pages.html        # This screenshot document
```

---

## 🔐 Security Features

### Authentication
- User registration with email and phone verification
- Secure password hashing (Django's default PBKDF2)
- Session-based authentication
- CSRF protection on all forms

### Payment Security
- Paystack integration (PCI-DSS Level 1 certified)
- Card details never stored on servers
- Webhook verification for payment confirmations
- SSL/TLS encryption for data in transit

### Database Security
- SQLite with proper access controls
- User data isolation
- Admin-only access to sensitive information

### API Security
- CSRF tokens on all POST requests
- Request validation
- Error handling without exposing sensitive information

---

## 📊 Data Models

### CustomUser Model (accounts)
```python
- id (UUID)
- username (CharField, unique)
- email (EmailField, unique)
- phone_number (CharField)
- profile_picture (ImageField)
- password (hashed)
- is_agent (Boolean) - marks user as agent after payment
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

### Order Model (orders)
```python
- order_id (UUID, primary key)
- buyer (ForeignKey to CustomUser)
- item_name (CharField)
- quantity (IntegerField)
- status (CharField: pending/paid/shipped/delivered)
- amount (DecimalField)
- customer_name (CharField)
- customer_email (EmailField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

### AgentRequest Model (accounts)
```python
- id (AutoField)
- user (ForeignKey to CustomUser)
- status (CharField: pending/approved/rejected)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip or Poetry
- Virtual environment

### Installation

1. **Clone the repository**
```bash
cd K-DATAHUB
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser (for admin)**
```bash
python manage.py createsuperuser
```

6. **Start development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Homepage: http://localhost:8000
- Admin: http://localhost:8000/admin

---

## 💳 Payment Flow

### Agent Registration Payment Flow
1. User navigates to `/accounts/become-agent/`
2. User fills in registration form
3. User clicks "Pay ₵25.00 & Register"
4. Order created with status "pending"
5. User redirected to Paystack payment page
6. User enters card details (on Paystack, not our server)
7. Payment processed
8. Paystack sends webhook notification
9. Order status updated to "paid"
10. User status upgraded to agent (is_agent = True)
11. SMS notification sent to user
12. Automatic redirect to tracking page

---

## 📞 Support & Help

For issues or questions:
- **WhatsApp**: https://wa.me/233594715103
- **Email**: support@kdatahub.com
- **Phone**: +233594715103 (Mon-Fri, 8am-6pm)

---

## 📄 Documentation Files

- `DEPLOYMENT_GUIDE_V3.md` - Full deployment instructions
- `ENVIRONMENT_VARIABLES.md` - Environment configuration
- `PAYSTACK_SETUP.md` - Paystack integration guide
- `k-datahub_pages.html` - Interactive page documentation

---

## 📝 License & Copyright

© 2026 K-DATAHUB. All rights reserved.

---

**Document Generated**: May 30, 2026
**Website Version**: 1.0
**Django Version**: 5.0.2
