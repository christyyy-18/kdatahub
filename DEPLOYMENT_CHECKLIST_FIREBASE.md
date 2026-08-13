# K-DATAHUB Firebase Cloud Run Deployment Checklist

## ✅ Pre-Deployment Setup

### Local Machine
- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] Docker installed and running
- [ ] Firebase CLI installed: `npm install -g firebase-tools`
- [ ] Google Cloud SDK (gcloud) installed
- [ ] Virtual environment activated

### Google Cloud Setup
- [ ] Firebase project created: `kdata-365aa-66188`
- [ ] Google Cloud project linked to Firebase
- [ ] Billing enabled on GCP
- [ ] Appropriate IAM permissions set

## 📋 Step-by-Step Deployment

### 1. Authenticate
```bash
firebase login
gcloud auth login
```
- [ ] Successfully authenticated to Firebase
- [ ] Successfully authenticated to gcloud
- [ ] Project set: `gcloud config set project kdata-365aa-66188`

### 2. Prepare Environment Variables
```bash
# Edit and set these values
export SECRET_KEY="your-long-random-secret-key"
export DEBUG="False"
export ALLOWED_HOSTS="localhost,127.0.0.1,kdata-365aa-66188.run.app"
export DATABASE_URL="postgresql://user:password@host:5432/dbname"
export PAYSTACK_PUBLIC_KEY="your-paystack-public-key"
export PAYSTACK_SECRET_KEY="your-paystack-secret-key"
```
- [ ] All required environment variables set
- [ ] `.env` file created (local only, not committed)

### 3. Update Django Settings
- [ ] Check `kdatahub/settings.py` for DATABASE_URL handling
- [ ] Verify STATIC_ROOT is set to `staticfiles_build/static`
- [ ] Confirm ALLOWED_HOSTS loads from environment
- [ ] Check DEBUG is set to False for production

### 4. Verify Dependencies
```bash
pip install -r requirements.txt
```
- [ ] All packages installed successfully
- [ ] Gunicorn 21.2.0+ installed
- [ ] firebase-admin 6.2.0+ installed
- [ ] psycopg2-binary installed for PostgreSQL

### 5. Test Locally
```bash
python manage.py runserver
```
- [ ] App runs without errors
- [ ] Database migration works
- [ ] Static files serve correctly
- [ ] Firebase configuration loads

### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```
- [ ] Static files collected to `staticfiles_build/static`
- [ ] No errors during collection

### 7. Push to Git (Optional but Recommended)
```bash
git add .
git commit -m "Setup Firebase Cloud Run deployment"
git push origin main
```
- [ ] Code committed and pushed
- [ ] No sensitive data in commits

## 🚀 Deployment

### Option A: Automatic Deployment (Recommended)

**Windows:**
```bash
deploy.bat
```

**Mac/Linux:**
```bash
bash deploy.sh
```

Or follow steps B below for manual deployment.

### Option B: Manual Deployment

**Step 1: Build Docker Image**
```bash
gcloud builds submit --tag gcr.io/kdata-365aa-66188/kdatahub
```
- [ ] Build completes successfully
- [ ] Image pushed to Container Registry

**Step 2: Deploy to Cloud Run**
```bash
gcloud run deploy kdatahub \
  --image gcr.io/kdata-365aa-66188/kdatahub \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SECRET_KEY=$SECRET_KEY,DEBUG=False
```
- [ ] Deployment completes successfully
- [ ] Service URL is displayed

**Step 3: Verify Deployment**
```bash
gcloud run services describe kdatahub --region us-central1
```
- [ ] Service shows "Ready" status
- [ ] URL is accessible

## 🔧 Post-Deployment Tasks

### Database Setup
```bash
# Run migrations
gcloud run services exec kdatahub --region us-central1 -- python manage.py migrate

# Create superuser
gcloud run services exec kdatahub --region us-central1 -- python manage.py createsuperuser
```
- [ ] Migrations run successfully
- [ ] Superuser created

### Update ALLOWED_HOSTS
- [ ] Get Cloud Run URL: `gcloud run services describe kdatahub --region us-central1 --format="value(status.url)"`
- [ ] Update ALLOWED_HOSTS in Django settings
- [ ] Redeploy if needed

### Test Application
- [ ] Visit Cloud Run URL in browser
- [ ] Test user registration
- [ ] Test login functionality
- [ ] Test payment flow (with Paystack test keys)
- [ ] Check Firebase authentication

### Monitor Logs
```bash
gcloud run logs read kdatahub --region us-central1 --limit 50
```
- [ ] No critical errors in logs
- [ ] Application serving requests

## 🔐 Security Checklist

- [ ] DEBUG=False in production
- [ ] SECRET_KEY is cryptographically secure
- [ ] Database credentials in environment variables (never hardcoded)
- [ ] SSL/TLS enforced (automatic with Cloud Run)
- [ ] CORS configured correctly
- [ ] CSRF protection enabled
- [ ] Sensitive data not logged
- [ ] Firewall rules configured (optional)

## 📊 Monitoring & Maintenance

### Daily Checks
```bash
# View recent logs
gcloud run logs read kdatahub --region us-central1 --limit 20

# Check service metrics
gcloud run services describe kdatahub --region us-central1
```
- [ ] Application is running
- [ ] No critical errors
- [ ] Response times acceptable

### Weekly Tasks
- [ ] Review Cloud Monitoring dashboard
- [ ] Check database performance
- [ ] Backup database (if using Cloud SQL)
- [ ] Review security logs

### Regular Maintenance
- [ ] Update Django packages
- [ ] Update dependencies monthly
- [ ] Security patches as needed
- [ ] Database optimization quarterly

## 🆘 Troubleshooting

### Deployment Fails
1. Check Docker installation: `docker --version`
2. Check gcloud auth: `gcloud auth list`
3. Review build logs: `gcloud builds log`
4. Check error: `gcloud run logs read kdatahub --limit 100`

### 502 Bad Gateway
1. Check application logs
2. Verify environment variables are set
3. Check database connectivity
4. Review Gunicorn worker configuration

### Static Files Not Loading
1. Verify collectstatic ran: `ls staticfiles_build/static`
2. Check STATIC_URL and STATIC_ROOT settings
3. Redeploy if needed

### Database Connection Issues
1. Verify DATABASE_URL format
2. Check Cloud SQL instance is running
3. Verify network connectivity
4. Check user permissions

## 📞 Support Resources

- [Firebase Cloud Run Docs](https://firebase.google.com/docs/functions/cloudrun)
- [Google Cloud Run Docs](https://cloud.google.com/run/docs)
- [Django Deployment](https://docs.djangoproject.com/en/6.0/howto/deployment/)
- [Gunicorn Docs](https://docs.gunicorn.org/)

## 🎯 Post-Deployment Features

Once deployed, consider implementing:
- [ ] Custom domain with Firebase Hosting
- [ ] Cloud CDN for static files
- [ ] Cloud Armor for DDoS protection
- [ ] Cloud Monitoring alerts
- [ ] Cloud Trace for performance analysis
- [ ] Scheduled backups
- [ ] Automated deployments with Cloud Build

## ✨ Deployment Summary

**Project**: K-DATAHUB
**Platform**: Firebase Cloud Run
**Region**: us-central1
**Project ID**: kdata-365aa-66188
**Service Name**: kdatahub

**Status**: [ ] Ready for Production

---

**Last Updated**: 2026-06-17
**Deployed By**: ___________
**Deployment Date**: ___________
**Notes**: 

