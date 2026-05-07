# Render Deployment Guide - K-DATAHUB

**Date:** May 7, 2026  
**Status:** Ready for Deployment ✅  
**Test Keys Configured:** ✅  

---

## 🚀 Pre-Deployment Checklist

- ✅ Test Paystack keys added to `.env`
- ✅ `build.sh` configured for auto-migrations
- ✅ `Procfile` ready for gunicorn
- ✅ `requirements.txt` complete
- ✅ Django settings support PostgreSQL
- ✅ Static files and WhiteNoise configured
- ✅ `.gitignore` properly configured

---

## 📋 Step 1: Prepare Your Render Account

1. Go to [render.com](https://render.com)
2. Sign up for a free account
3. Verify your email
4. Add payment method (for upgrade if needed)

---

## 📋 Step 2: Create a PostgreSQL Database

### 2.1 Create Database Service
1. In Render dashboard, click **New +** → **PostgreSQL**
2. Configure:
   - **Name:** `k-datahub-db`
   - **Database:** `k_datahub`
   - **User:** `kdatahub_user`
   - **Region:** Choose closest to your users (e.g., Frankfurt)
   - **PostgreSQL Version:** 15
   - **Plan:** Free (for testing)
3. Click **Create Database**

### 2.2 Save Database URL
- Copy the **Internal Database URL** (not external)
- Format: `postgresql://user:password@host:5432/dbname`
- You'll need this in Step 4

---

## 📋 Step 3: Deploy the Web Service

### 3.1 Connect Your GitHub Repository
1. In Render, click **New +** → **Web Service**
2. Click **Connect GitHub repository**
3. Search for your K-DATAHUB repo and connect
4. Select the main/master branch

### 3.2 Configure Web Service
**Basic Settings:**
- **Name:** `k-datahub-api`
- **Environment:** Python 3
- **Region:** Same as database (e.g., Frankfurt)
- **Branch:** main
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn kdatahub.wsgi:application`

**Plan:** Free (for testing)

---

## 📋 Step 4: Set Environment Variables

In the Render web service settings, add these environment variables:

### Django Configuration
```
DEBUG=False
SECRET_KEY=<generate-new-secret>
ALLOWED_HOSTS=<your-render-domain>.onrender.com,*.onrender.com
```

**To generate SECRET_KEY locally:**
```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Database (from Step 2)
```
DATABASE_URL=<copy-from-postgresql-service>
```

### Paystack - TEST KEYS (Current Configuration)
```
PAYSTACK_PUBLIC_KEY=pk_test_e1d08c6ef49e121abfbe793624ace1a7d3a52247
PAYSTACK_SECRET_KEY=sk_test_4ee6970338e7b5f88a35b6bf6cf0a40036c38022
```

### Domain & Callbacks
```
BASE_DOMAIN=https://<your-render-domain>.onrender.com
```

### SMS Configuration (Arkesel)
```
ARKESEL_API_KEY=WlBRT0hubWFmWVJXTWlKSnl4UU8
SMS_SENDER_ID=KDATAHUB
MANAGER_PHONE=+233594715103
ADMIN_PHONE=0552514207
```

### Email
```
DEFAULT_FROM_EMAIL=noreply@kdataflow.com
SENDGRID_API_KEY=<leave-blank-for-now>
```

### Optional: Supabase for File Storage (Not Required for Testing)
```
USE_SUPABASE=False
```

---

## 📋 Step 5: Deploy

1. In Render web service, click **Deploy** or **Manual Deploy**
2. Wait for build to complete (2-5 minutes)
3. Check build logs for any errors
4. Once deployed, you'll get a URL like: `https://k-datahub-api.onrender.com`

### Monitor Deployment
- Click **Logs** to watch the build process
- Look for messages like:
  ```
  Running migrations...
  Collecting static files...
  ```

---

## 🧪 Step 6: Test the Deployment

### 6.1 Access Your Live Application
```
https://<your-service-name>.onrender.com
```

### 6.2 Test Pages (After Deployment)

**Homepage:**
```
https://<your-service-name>.onrender.com/
```

**Registration:**
```
https://<your-service-name>.onrender.com/accounts/signup/
```

**Login:**
```
https://<your-service-name>.onrender.com/accounts/login/
```

**Dashboard:**
```
https://<your-service-name>.onrender.com/dashboard/ (requires login)
```

**Test Payment:**
1. Sign up for new account
2. Click on "Become Agent" or similar payment option
3. Proceed to Paystack payment page
4. Use test card: `4111111111111111`
5. Expiry: `01/25`
6. CVV: `123`
7. OTP: Any 6 digits

### 6.3 Check Payment Webhook
After successful payment:
1. Log into Paystack Dashboard (test mode)
2. Go to **Transactions**
3. Verify payment status is "Successful"
4. Check if user agent status updated

---

## 🔗 Testing Links

Replace `<YOUR_RENDER_DOMAIN>` with your actual domain (e.g., `k-datahub-api`):

| Feature | URL |
|---------|-----|
| **Homepage** | `https://<YOUR_RENDER_DOMAIN>.onrender.com/` |
| **Register** | `https://<YOUR_RENDER_DOMAIN>.onrender.com/accounts/signup/` |
| **Login** | `https://<YOUR_RENDER_DOMAIN>.onrender.com/accounts/login/` |
| **Dashboard** | `https://<YOUR_RENDER_DOMAIN>.onrender.com/dashboard/` |
| **My Orders** | `https://<YOUR_RENDER_DOMAIN>.onrender.com/orders/my-orders/` |
| **Become Agent** | `https://<YOUR_RENDER_DOMAIN>.onrender.com/accounts/become_agent/` |
| **Profile** | `https://<YOUR_RENDER_DOMAIN>.onrender.com/accounts/profile/` |
| **Admin Panel** | `https://<YOUR_RENDER_DOMAIN>.onrender.com/admin/` |

---

## 🧪 Test Paystack Test Card Credentials

| Card Type | Number | Expiry | CVV | Use Case |
|-----------|--------|--------|-----|----------|
| Visa (Success) | `4111111111111111` | 01/25 | 123 | Successful payment |
| Visa (Failed) | `4000000000000002` | 01/25 | 123 | Failed transaction |
| Mastercard (Success) | `5555555555554444` | 01/25 | 123 | Successful payment |

**OTP:** Use any 6 digits (e.g., 123456)

---

## 🔐 Security Notes - AFTER Testing

Once testing is complete and you want production:

1. **Switch to LIVE Paystack Keys:**
   - Update `PAYSTACK_PUBLIC_KEY` and `PAYSTACK_SECRET_KEY`
   - Use live keys only (pk_live_, sk_live_)
   - Set `DEBUG=False` in environment

2. **Set a Secure SECRET_KEY:**
   - Generate new key: `python manage.py shell` → `from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())`
   - Update in Render environment

3. **Enable HTTPS Only:**
   - Render enables HTTPS by default ✅

4. **Configure Paystack Webhook:**
   - In Paystack Dashboard → **Settings → API Keys & Webhooks**
   - Add webhook URL: `https://<YOUR_RENDER_DOMAIN>.onrender.com/payments/webhook/paystack/`
   - Select events: `charge.success`, `charge.failed`

---

## 🚨 Troubleshooting

### Build Failed
1. Check **Logs** for errors
2. Common issues:
   - Missing PostgreSQL connection
   - Static file collection failed
   - Python package not installed

**Fix:**
```bash
# Run locally to test:
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

### 500 Error on Page
1. Check Render **Logs** for Django errors
2. Database connection issues?
3. Missing environment variables?

### Payment Not Working
1. Verify `PAYSTACK_PUBLIC_KEY` and `PAYSTACK_SECRET_KEY` are set
2. Check Paystack Dashboard - is account in test/live mode?
3. Use Paystack test cards only in test mode
4. Check webhook logs in Paystack Dashboard

### Static Files Not Loading
- WhiteNoise is configured ✅
- Run locally to test: `python manage.py collectstatic --no-input`

---

## 📞 Support

- **Render Docs:** https://render.com/docs
- **Django Deployment:** https://docs.djangoproject.com/en/5.0/howto/deployment/
- **Paystack Docs:** https://paystack.com/docs
- **Python Version:** 3.9+

---

**Next Steps:**
1. ✅ Add test Paystack keys (DONE)
2. Create Render account
3. Set up PostgreSQL database
4. Deploy web service with environment variables
5. Test payment flow with test cards
6. Monitor logs for any issues

