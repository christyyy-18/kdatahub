# 🚀 K-DATAHUB Quick Deployment Card

**Status:** ✅ READY TO DEPLOY | **Date:** May 7, 2026

---

## 📋 Deployment Commands

### One-Click Deploy (Recommended)
```bash
# Just push to GitHub and follow these steps:
1. Go to: https://render.com/dashboard
2. Click: "New +" → "Blueprint"
3. Select: Your GitHub repo
4. Deploy: render.yaml will auto-configure everything
```

### Manual Setup (If render.yaml doesn't work)
```bash
# Step 1: Create PostgreSQL
Dashboard → New → PostgreSQL → Configure → Create

# Step 2: Create Web Service
Dashboard → New → Web Service → GitHub Connect

# Step 3: Configure
Build Command:  ./build.sh
Start Command:  gunicorn kdatahub.wsgi:application

# Step 4: Add Environment Variables
(See table below)
```

---

## 🔐 Environment Variables (Copy-Paste Ready)

| Variable | Value | Notes |
|----------|-------|-------|
| `DEBUG` | `False` | Production setting |
| `SECRET_KEY` | [GENERATE] | Run: `python manage.py shell` |
| `ALLOWED_HOSTS` | `*.onrender.com` | Auto-includes your domain |
| `DATABASE_URL` | [AUTO-FROM-DB] | Render fills this automatically |
| `PAYSTACK_PUBLIC_KEY` | `pk_test_e1d08c6ef49e121abfbe793624ace1a7d3a52247` | ✅ Test key (current) |
| `PAYSTACK_SECRET_KEY` | `sk_test_4ee6970338e7b5f88a35b6bf6cf0a40036c38022` | ✅ Test key (current) |
| `BASE_DOMAIN` | `https://YOUR-SERVICE.onrender.com` | Replace YOUR-SERVICE |
| `ARKESEL_API_KEY` | `WlBRT0hubWFmWVJXTWlKSnl4UU8` | SMS Provider |
| `SMS_SENDER_ID` | `KDATAHUB` | SMS identifier |
| `MANAGER_PHONE` | `+233594715103` | Manager notifications |
| `ADMIN_PHONE` | `0552514207` | Admin notifications |
| `DEFAULT_FROM_EMAIL` | `noreply@kdataflow.com` | Email sender |
| `USE_SUPABASE` | `False` | Skip file storage for now |

---

## 🧪 Testing URLs

Once deployed, test these URLs:

```
Homepage:      https://YOUR-SERVICE.onrender.com/
Register:      https://YOUR-SERVICE.onrender.com/accounts/signup/
Login:         https://YOUR-SERVICE.onrender.com/accounts/login/
Dashboard:     https://YOUR-SERVICE.onrender.com/dashboard/
Become Agent:  https://YOUR-SERVICE.onrender.com/accounts/become_agent/
My Orders:     https://YOUR-SERVICE.onrender.com/orders/my-orders/
Admin:         https://YOUR-SERVICE.onrender.com/admin/
```

---

## 💳 Test Payment Cards

Use these cards to test payment flow:

| Card | Number | Expiry | CVV | Result |
|------|--------|--------|-----|--------|
| Visa Success | `4111111111111111` | 01/25 | 123 | ✅ Payment succeeds |
| Visa Fail | `4000000000000002` | 01/25 | 123 | ❌ Payment fails |
| Mastercard | `5555555555554444` | 01/25 | 123 | ✅ Payment succeeds |

**OTP:** Use any 6 digits (e.g., 123456)

---

## ✅ Pre-Deployment Checks (Done)

```
✅ Django check:              python manage.py check
✅ Paystack keys loaded:      Verified in .env
✅ Build script ready:         build.sh includes migrations
✅ Procfile configured:        gunicorn setup done
✅ Static files config:        WhiteNoise enabled
✅ Database support:           PostgreSQL ready
✅ render.yaml created:        IaC file ready
```

---

## 🚀 Deployment Checklist

- [ ] Create Render account at https://render.com
- [ ] Deploy using render.yaml (easiest) OR manual setup
- [ ] Wait for build to complete (2-5 minutes)
- [ ] Check logs for errors
- [ ] Test homepage loads: `https://YOUR-SERVICE.onrender.com/`
- [ ] Create test account and register
- [ ] Test payment with `4111111111111111` card
- [ ] Verify agent status activated after payment
- [ ] Check Paystack dashboard for transaction record

---

## 🔗 Important Links

| Resource | URL |
|----------|-----|
| Render Dashboard | https://render.com/dashboard |
| Paystack Dashboard | https://paystack.com/dashboard |
| Render Docs | https://render.com/docs |
| Django Docs | https://docs.djangoproject.com/en/5.0/ |

---

## 🆘 Quick Troubleshooting

| Issue | Fix |
|-------|-----|
| Build failed | Check build logs: `Dashboard → Service → Logs` |
| 500 error | Check Django logs in Render logs section |
| Payment not working | Verify `PAYSTACK_PUBLIC_KEY` is in environment |
| Static files not loading | WhiteNoise is configured ✅, run `collectstatic` |
| Database error | Verify `DATABASE_URL` is set from PostgreSQL service |

---

## 📝 Current Configuration Summary

```
✅ Application: K-DATAHUB (Django 5.0.2)
✅ Database: PostgreSQL (ready)
✅ Payments: Paystack (test keys loaded)
✅ SMS: Arkesel (configured)
✅ Hosting: Render.com
✅ Test Status: Ready for deployment
```

---

## 🎯 Deployment Timeline

| Step | Time | Status |
|------|------|--------|
| Create Render account | 2 min | ⏳ TODO |
| Deploy with render.yaml | 2 min | ⏳ TODO |
| Build & migrations | 3 min | ⏳ TODO |
| Test payment flow | 5 min | ⏳ TODO |
| **Total** | **12 min** | ⏳ READY |

---

**Files Created/Updated:**
- `.env` - ✅ Test keys added
- `render.yaml` - ✅ IaC configuration
- `RENDER_DEPLOYMENT_GUIDE.md` - ✅ Detailed guide
- `DEPLOYMENT_READY.md` - ✅ Full testing documentation

**Status:** 🚀 Ready to deploy immediately!

