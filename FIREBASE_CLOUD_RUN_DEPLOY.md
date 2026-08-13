# Firebase Cloud Run Deployment Guide for K-DATAHUB

## Prerequisites

1. **Firebase Project**: Already set up (kdata-365aa-66188)
2. **Google Cloud Project**: Same as Firebase project
3. **Firebase CLI**: Installed and authenticated
4. **Docker**: Installed on your machine
5. **Git**: For version control

## Step 1: Install Firebase CLI

```bash
# Global installation
npm install -g firebase-tools

# Verify installation
firebase --version
```

## Step 2: Authenticate with Firebase

```bash
firebase login
```

This will open a browser window to authenticate with your Google account.

## Step 3: Initialize Firebase Project Locally

From your project root:

```bash
firebase init
```

Choose these options:
- **Features**: Select "Cloud Run" and "Hosting"
- **Project**: Select your existing project "kdata-365aa-66188"
- **Cloud Run region**: Choose the closest region (e.g., "us-central1")
- **Hosting directory**: "public" (we'll use static files)
- **Single page app**: No

## Step 4: Set Up Environment Variables

### Option A: Using Google Cloud Secret Manager (Recommended)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your Firebase project
3. Go to **Secret Manager**
4. Create secrets for:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `PAYSTACK_PUBLIC_KEY`
   - `PAYSTACK_SECRET_KEY`
   - `FIREBASE_CREDENTIALS_JSON`

### Option B: Using Cloud Run Environment Variables

Add to `.env` (local only, don't commit):
```bash
SECRET_KEY=your-very-secure-random-key
DATABASE_URL=postgresql://user:password@host:5432/dbname
DEBUG=False
ALLOWED_HOSTS=kdata-365aa-66188.run.app
PAYSTACK_PUBLIC_KEY=your-key
PAYSTACK_SECRET_KEY=your-key
```

## Step 5: Prepare Your Django Settings

Update `kdatahub/settings.py` to handle Cloud Run:

```python
# Already configured in settings.py
if os.getenv('CLOUD_RUN_DEPLOYMENT') or 'run.app' in os.getenv('ALLOWED_HOSTS', ''):
    # Use Cloud SQL for production
    import urllib.parse
    
    # Ensure SSL for database
    if 'DATABASE_URL' in os.environ:
        db_url = urllib.parse.urlparse(os.environ['DATABASE_URL'])
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require'
        }
```

## Step 6: Update ALLOWED_HOSTS

In `kdatahub/settings.py`:

```python
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

Set environment variable:
```bash
export ALLOWED_HOSTS=localhost,127.0.0.1,kdata-365aa-66188.run.app
```

## Step 7: Configure Dockerfile (Already Created)

The Dockerfile is already created in your project root. It:
- Uses Python 3.11 slim image
- Installs dependencies
- Collects static files
- Runs Gunicorn on port 8080

## Step 8: Deploy to Cloud Run

### First Deployment:

```bash
# From project root
firebase deploy --only functions:kdatahub --region us-central1
```

Or deploy directly with gcloud:

```bash
# Set up gcloud
gcloud config set project kdata-365aa-66188

# Build and deploy
gcloud run deploy kdatahub \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SECRET_KEY=$SECRET_KEY,DATABASE_URL=$DATABASE_URL,PAYSTACK_PUBLIC_KEY=$PAYSTACK_PUBLIC_KEY
```

## Step 9: Run Migrations

After deployment, run migrations:

```bash
# Connect to Cloud Run service
gcloud run services describe kdatahub --region us-central1

# Run migrations
gcloud run services exec kdatahub \
  --region us-central1 \
  -- python manage.py migrate
```

## Step 10: Access Your App

Your deployed app will be at:
```
https://kdatahub-{hash}.run.app
```

Or configured via custom domain in Firebase.

## Troubleshooting

### Check Cloud Run Logs

```bash
gcloud run logs read kdatahub --region us-central1 --limit 50
```

### Check Service Status

```bash
gcloud run services describe kdatahub --region us-central1
```

### View All Cloud Run Services

```bash
gcloud run services list
```

### Common Issues

#### 1. Database Connection Failed
- Ensure DATABASE_URL is correct
- Check Cloud SQL Proxy is configured
- Verify SSL certificates

#### 2. Static Files Not Serving
- Run: `python manage.py collectstatic --noinput`
- Ensure STATIC_ROOT is set correctly

#### 3. 502 Bad Gateway
- Check logs: `gcloud run logs read kdatahub`
- Verify Gunicorn is starting
- Check memory/CPU allocation

#### 4. Environment Variables Not Found
- Verify variables are set in Cloud Run
- Check Secret Manager is accessible

## Database Setup for Cloud Run

### Using Cloud SQL (Recommended):

1. Create Cloud SQL instance:
```bash
gcloud sql instances create kdatahub-db \
  --database-version POSTGRES_15 \
  --tier db-f1-micro \
  --region us-central1
```

2. Create database:
```bash
gcloud sql databases create kdatahub --instance kdatahub-db
```

3. Create user:
```bash
gcloud sql users create kdatahub-user \
  --instance kdatahub-db \
  --password
```

4. Get connection string:
```bash
gcloud sql instances describe kdatahub-db --format="value(connectionName)"
```

5. Update DATABASE_URL format for Cloud SQL Proxy:
```
postgresql://user:password@/database?unix_socket_dir=/cloudsql/PROJECT:REGION:INSTANCE
```

## Scaling Configuration

Update `gcloud run deploy` with:

```bash
--memory 512Mi \        # RAM
--cpu 1 \              # CPU cores
--max-instances 10 \   # Max concurrent instances
--timeout 3600 \       # Request timeout in seconds
--concurrency 80       # Concurrent requests per instance
```

## Monitoring

- **Cloud Monitoring**: Available in Google Cloud Console
- **Cloud Logging**: View real-time logs
- **Cloud Trace**: Analyze performance
- **Cloud Profiler**: Identify bottlenecks

## Rollback Deployment

```bash
gcloud run deploy kdatahub \
  --region us-central1 \
  --revision=<previous-revision-hash>
```

## Next Steps

1. ✅ Set up custom domain (optional)
2. ✅ Configure CDN with Cloud Armor
3. ✅ Set up continuous deployment with Cloud Build
4. ✅ Configure alerts and monitoring
5. ✅ Set up backup strategy for database

## Quick Deploy Script

Save as `deploy.sh`:

```bash
#!/bin/bash

echo "Building Docker image..."
gcloud builds submit --tag gcr.io/kdata-365aa-66188/kdatahub

echo "Deploying to Cloud Run..."
gcloud run deploy kdatahub \
  --image gcr.io/kdata-365aa-66188/kdatahub \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DJANGO_SETTINGS_MODULE=kdatahub.settings

echo "Deployment complete!"
gcloud run services describe kdatahub --region us-central1
```

Then run:
```bash
chmod +x deploy.sh
./deploy.sh
```

## Support

- [Firebase Cloud Run Docs](https://firebase.google.com/docs/functions/cloudrun)
- [Google Cloud Run Docs](https://cloud.google.com/run/docs)
- [Django Deployment Guide](https://docs.djangoproject.com/en/6.0/howto/deployment/)
