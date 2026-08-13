#!/bin/bash
# Quick Deployment Script for K-DATAHUB to Firebase Cloud Run
# Make sure you're authenticated: firebase login

set -e  # Exit on any error

PROJECT_ID="kdata-365aa"
SERVICE_NAME="kdatahub"
REGION="us-central1"

echo "================================"
echo "K-DATAHUB Cloud Run Deployment"
echo "================================"
echo ""

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Install with: npm install -g firebase-tools"
    exit 1
fi

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Install with: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Step 1: Set GCP Project
echo "📌 Setting GCP project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Step 2: Build Docker image
echo ""
echo "🐳 Building Docker image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Step 3: Deploy to Cloud Run
echo ""
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600 \
  --set-env-vars DJANGO_SETTINGS_MODULE=kdatahub.settings,DEBUG=False

# Step 4: Get service URL
echo ""
echo "✅ Deployment complete!"
echo ""
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format="value(status.url)")
echo "🌐 Your app is live at: $SERVICE_URL"
echo ""
echo "📋 Next steps:"
echo "1. Update ALLOWED_HOSTS with: $SERVICE_URL"
echo "2. Run migrations: gcloud run services exec $SERVICE_NAME -- python manage.py migrate"
echo "3. Create superuser: gcloud run services exec $SERVICE_NAME -- python manage.py createsuperuser"
echo ""
echo "📚 View logs: gcloud run logs read $SERVICE_NAME --region $REGION --limit 50"
