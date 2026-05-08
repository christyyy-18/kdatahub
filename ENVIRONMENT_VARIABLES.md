# Environment Variables Configuration

## Overview

K-DATAHUB requires specific environment variables for different deployment environments. This guide covers all necessary configurations.

---

## Development Environment (.env file)

Create a `.env` file in the project root (NOT COMMITTED TO GIT):

```bash
# Django Configuration
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here-only-for-dev

# Database (Local PostgreSQL)
DATABASE_URL=postgresql://postgres:password@localhost:5432/k_datahub_dev
USE_POSTGRES=True

# Domain Configuration
BASE_DOMAIN=http://localhost:8000
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app,.onrender.com

# Paystack (Test Keys)
PAYSTACK_PUBLIC_KEY=pk_test_XXXXXXXXXXXXXXXXXX
PAYSTACK_SECRET_KEY=sk_test_XXXXXXXXXXXXXXXXXX

# SMS Configuration (Arkesel)
ARKESEL_API_KEY=your_arkesel_api_key
SMS_SENDER_ID=KDATAHUB
MANAGER_PHONE=+233594715103
ADMIN_PHONE=0552514207
```

---

## Production Environment (Render)

Set these environment variables in Render dashboard:

### 1. Django Settings
```
DEBUG=False
SECRET_KEY=<generate new key - see below>
ALLOWED_HOSTS=kdatahub.onrender.com
```

**To generate a new SECRET_KEY:**
```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Database Configuration
```
DATABASE_URL=postgresql://username:password@hostname:5432/dbname
```

Get this from Render PostgreSQL addon:
- Create PostgreSQL addon in Render
- Copy the database URL from addon page
- This will be something like: `postgresql://user:pass@host:5432/db`

### 3. Domain Configuration
```
BASE_DOMAIN=https://kdatahub.onrender.com
```

Replace with your actual Render domain.

### 4. Paystack (Live Keys Only for Production!)
```
PAYSTACK_PUBLIC_KEY=pk_live_XXXXXXXXXXXXXXXXXX
PAYSTACK_SECRET_KEY=sk_live_XXXXXXXXXXXXXXXXXX
```

**⚠️ WARNING:** 
- Use **LIVE keys** (pk_live_) in production, not test keys
- Never expose SECRET_KEY in code
- Keep these secure in Render environment only

### 5. SMS Configuration (Arkesel)
```
ARKESEL_API_KEY=your_production_arkesel_key
SMS_SENDER_ID=KDATAHUB
MANAGER_PHONE=+233594715103
ADMIN_PHONE=0552514207
```

---

## Complete Render Environment Variables Checklist

Use this as a reference when setting up Render:

| Variable | Value | Source |
|----------|-------|--------|
| `DEBUG` | `False` | Generated |
| `SECRET_KEY` | Generated value | `python manage.py shell` |
| `ALLOWED_HOSTS` | `kdatahub.vercel.app` | Vercel domain |
| `BASE_DOMAIN` | `https://kdatahub.vercel.app` | Vercel domain |
| `DATABASE_URL` | From PostgreSQL addon | Render addon |
| `PAYSTACK_PUBLIC_KEY` | `pk_live_...` | Paystack dashboard |
| `PAYSTACK_SECRET_KEY` | `sk_live_...` | Paystack dashboard |
| `ARKESEL_API_KEY` | Your API key | Arkesel dashboard |
| `SMS_SENDER_ID` | `KDATAHUB` | Your choice |
| `MANAGER_PHONE` | `+233594715103` | Your phone |
| `ADMIN_PHONE` | `0552514207` | Your phone |
| `USE_SUPABASE` | `True` | Boolean |
| `SUPABASE_URL` | `https://...supabase.co` | Supabase project URL |
| `SUPABASE_KEY` | Service Role Secret | Supabase API key |
| `SUPABASE_STORAGE_BUCKET` | `kdatahub-media` | Bucket name |

---

## How to Add Environment Variables in Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Select your K-DATAHUB service
3. Go to **Environment** tab
4. Click **Add Environment Variable**
5. Enter:
   - **Key**: Variable name (e.g., `DEBUG`)
   - **Value**: Variable value (e.g., `False`)
6. Click **Save**
7. Service will auto-redeploy

---

## Environment Variables by Feature

### Feature: Payment Processing (Paystack)
```
PAYSTACK_PUBLIC_KEY=pk_live_XXXXXXXXXXXXXXXXXX
PAYSTACK_SECRET_KEY=sk_live_XXXXXXXXXXXXXXXXXX
BASE_DOMAIN=https://kdatahub.onrender.com
```

### Feature: SMS Notifications (Arkesel)
```
ARKESEL_API_KEY=your_api_key
SMS_SENDER_ID=KDATAHUB
MANAGER_PHONE=+233594715103
ADMIN_PHONE=0552514207
```

### Feature: Media Storage (Supabase)
```
USE_SUPABASE=True
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGc... (Service Role Secret)
SUPABASE_STORAGE_BUCKET=kdatahub-media
```

### Feature: Database (PostgreSQL)
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### Feature: Django Security
```
DEBUG=False
SECRET_KEY=<unique-generated-key>
ALLOWED_HOSTS=kdatahub.onrender.com
```

---

## Development vs Production Comparison

| Setting | Development | Production |
|---------|-------------|------------|
| `DEBUG` | `True` | `False` |
| `SECRET_KEY` | Default (unsafe) | Generate new |
| `DATABASE_URL` | Local SQLite/PostgreSQL | Render PostgreSQL |
| `BASE_DOMAIN` | `http://localhost:8000` | `https://kdatahub.onrender.com` |
| Paystack Keys | Test keys (`pk_test_`) | Live keys (`pk_live_`) |
| `USE_SUPABASE` | `False` (local storage) | `True` (Supabase) |
| Media Storage | Local `media/` folder | Supabase storage |

---

## Getting Required Values

### SECRET_KEY
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
'your-generated-key-here'
```

### DATABASE_URL
1. Create PostgreSQL addon in Render
2. Copy from addon page - format: `postgresql://user:pass@host:5432/db`

### Paystack Keys
See: [PAYSTACK_SETUP.md](PAYSTACK_SETUP.md) - Step 3

### Paystack Keys

### Supabase Credentials
See: [SUPABASE_SETUP.md](SUPABASE_SETUP.md) - Steps 3-5

### Arkesel API Key
1. Log in to Arkesel dashboard: https://dashboard.arkesel.com/
2. Go to **API Keys**
3. Copy your API key

---

## Validation Commands

Check if environment variables are loaded correctly:

```bash
# On Render, check logs:
# Dashboard → Service → Logs

# Locally, test with Python:
python manage.py shell
>>> from django.conf import settings
>>> print(f"DEBUG: {settings.DEBUG}")
>>> print(f"SECRET_KEY: {settings.SECRET_KEY[:20]}...")  # First 20 chars only
>>> print(f"PAYSTACK_SECRET_KEY configured: {bool(settings.PAYSTACK_SECRET_KEY)}")
>>> print(f"Supabase configured: {bool(settings.USE_SUPABASE)}")
```

---

## Security Checklist

- [ ] `.env` file is in `.gitignore` (never commit!)
- [ ] All secret keys are stored only in Render environment
- [ ] No secret keys hardcoded in source files
- [ ] Using live Paystack keys in production
- [ ] Using test Paystack keys in development
- [ ] AWS access keys rotated if older than 90 days
- [ ] All environment variables checked before deployment
- [ ] No secrets in git history (`git log --all --source --remotes`)

---

## Troubleshooting

### "Disallowed host at /"
- Check `ALLOWED_HOSTS` matches your domain
- For Render: Should be `kdatahub.onrender.com`

### Payment initialization fails
- Verify `PAYSTACK_SECRET_KEY` is set
- Verify `BASE_DOMAIN` is correct
- Check Paystack keys are valid for the environment (test/live)

### Media files not uploading
- Check local `media/` folder writable
- If using Supabase: Verify credentials and bucket name

### SMS not sending
- Verify `ARKESEL_API_KEY` is set
- Check API key is active in Arkesel dashboard
- Verify phone numbers are in correct format

### Database connection errors
- Verify `DATABASE_URL` is correct format
- Check database server is running (for local dev)
- For Render: Verify PostgreSQL addon is created and URL is copied

---

## Environment Variable Limits

| Service | Max Length | Notes |
|---------|-----------|-------|
| SECRET_KEY | Unlimited | 50+ chars recommended |
| API Keys | Varies | Usually 50-100 chars |
| Domains | 253 chars | RFC 1035 limit |
| Phone numbers | 20 chars | Include country code |
| Database URL | 2048 chars | Typical 100-200 chars |

---

## References

- Django Environment Setup: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
- Render Environment: https://render.com/docs/environment-variables
- Paystack: See [PAYSTACK_SETUP.md](PAYSTACK_SETUP.md)

