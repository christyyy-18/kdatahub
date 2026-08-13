@echo off
REM Quick Deployment Script for K-DATAHUB to Firebase Cloud Run (Windows)
REM Make sure you're authenticated: firebase login

setlocal enabledelayedexpansion

set PROJECT_ID=kdata-365aa
set SERVICE_NAME=kdatahub
set REGION=us-central1

cls
echo ================================
echo K-DATAHUB Cloud Run Deployment
echo ================================
echo.

REM Check if gcloud is installed
where gcloud >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [X] gcloud CLI not found.
    echo Install from: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM Step 1: Set GCP Project
echo [*] Setting GCP project to %PROJECT_ID%...
call gcloud config set project %PROJECT_ID%
if %ERRORLEVEL% NEQ 0 (
    echo [X] Failed to set project
    pause
    exit /b 1
)

REM Step 2: Build Docker image
echo.
echo [*] Building Docker image...
call gcloud builds submit --tag gcr.io/%PROJECT_ID%/%SERVICE_NAME%
if %ERRORLEVEL% NEQ 0 (
    echo [X] Docker build failed
    pause
    exit /b 1
)

REM Step 3: Deploy to Cloud Run
echo.
echo [*] Deploying to Cloud Run (this may take a few minutes)...
call gcloud run deploy %SERVICE_NAME% ^
  --image gcr.io/%PROJECT_ID%/%SERVICE_NAME% ^
  --platform managed ^
  --region %REGION% ^
  --allow-unauthenticated ^
  --memory 512Mi ^
  --cpu 1 ^
  --timeout 3600 ^
  --set-env-vars DJANGO_SETTINGS_MODULE=kdatahub.settings,DEBUG=False

if %ERRORLEVEL% NEQ 0 (
    echo [X] Deployment failed
    pause
    exit /b 1
)

REM Step 4: Get service URL
echo.
echo [+] Deployment complete!
echo.

for /f "tokens=*" %%a in ('gcloud run services describe %SERVICE_NAME% --region %REGION% --format="value(status.url)"') do (
    set SERVICE_URL=%%a
)

echo [+] Your app is live at: %SERVICE_URL%
echo.
echo [*] Next steps:
echo    1. Update ALLOWED_HOSTS with: %SERVICE_URL%
echo    2. Run migrations and create superuser
echo    3. View logs for any errors
echo.
echo [*] Useful commands:
echo    View logs: gcloud run logs read %SERVICE_NAME% --region %REGION% --limit 50
echo    View service details: gcloud run services describe %SERVICE_NAME% --region %REGION%
echo.
pause
