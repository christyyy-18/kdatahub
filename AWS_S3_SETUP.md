# AWS S3 Setup Guide for K-DATAHUB Media Storage

## Why AWS S3?

- **Persistent Storage**: Files survive server restarts (Render uses ephemeral storage)
- **Scalability**: Handles unlimited media files
- **Cost-Effective**: Only pay for what you store/transfer
- **Global CDN**: Fast delivery of media files worldwide
- **Secure**: Encrypted storage with access controls

---

## Step 1: Create AWS Account

1. Visit [https://aws.amazon.com](https://aws.amazon.com)
2. Click **Create AWS Account**
3. Enter your email and password
4. Choose **Personal** account type
5. Add payment method (credit/debit card)
6. Complete phone verification
7. Choose **Basic Support** plan (free tier)

**✅ AWS Free Tier Benefits:**
- 5 GB storage for 12 months
- Perfect for development and small deployments

---

## Step 2: Create S3 Bucket

1. Log in to [AWS Console](https://console.aws.amazon.com/)
2. Search for and open **S3** service
3. Click **Create bucket**
4. Configure bucket:
   - **Bucket name**: `kdatahub-media` (must be globally unique)
   - **Region**: Select closest to your users (e.g., `us-east-1`)
5. **Block Public Access Settings:**
   - Uncheck `Block all public access` (we need public read)
   - Check `Block public access (account level)` - NO
   - Acknowledge the warning
6. Click **Create bucket**

---

## Step 3: Configure Bucket Policy (Public Read)

1. Open your new bucket `kdatahub-media`
2. Go to **Permissions** tab
3. Click **Bucket Policy**
4. Paste this policy (replace `kdatahub-media` with your bucket name):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::kdatahub-media/*"
        }
    ]
}
```

5. Click **Save**

---

## Step 4: Enable CORS (for frontend access)

1. In your S3 bucket, go to **Permissions** tab
2. Scroll to **CORS**
3. Click **Edit**
4. Paste this configuration:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": ["ETag"],
        "MaxAgeSeconds": 3000
    }
]
```

5. Click **Save**

---

## Step 5: Create IAM User for Application

1. Open **IAM** service from AWS Console
2. Click **Users** on the left sidebar
3. Click **Create user**
4. Enter username: `kdatahub-app`
5. Click **Next**
6. Choose **Attach policies directly**
7. Search for and select: **AmazonS3FullAccess**
   - (For production, you'd create a more restrictive policy)
8. Click **Next** → **Create user**

---

## Step 6: Generate Access Keys

1. Click on the new user `kdatahub-app`
2. Go to **Security credentials** tab
3. Scroll to **Access keys** section
4. Click **Create access key**
5. Choose **Application running outside AWS**
6. Click **Next**
7. You'll see:
   - **Access Key ID** (starts with `AKIA`)
   - **Secret Access Key** (long string)
8. **⚠️ IMPORTANT:** Download CSV or copy both keys immediately - you can't view the secret again!

**Store these securely:**
```
AWS_S3_ACCESS_KEY_ID = AKIA...
AWS_S3_SECRET_ACCESS_KEY = wJal...
```

---

## Step 7: Update K-DATAHUB Requirements

The requirements.txt has already been updated with:
```
boto3==1.28.85
django-storages==1.14.2
```

Install these packages:
```bash
pip install -r requirements.txt
```

---

## Step 8: Configure K-DATAHUB Settings

The `settings.py` is already configured for S3. You just need to set environment variables.

**Key settings in settings.py:**
```python
if env('USE_S3', default=False):
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ACCESS_KEY_ID = env('AWS_S3_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = env('AWS_S3_SECRET_ACCESS_KEY')
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-east-1')
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

## Step 9: Set Environment Variables

### For Local Development (using local storage):
```
USE_S3=False
```

### For Production (using S3):
```
USE_S3=True
AWS_STORAGE_BUCKET_NAME=kdatahub-media
AWS_S3_ACCESS_KEY_ID=AKIA...
AWS_S3_SECRET_ACCESS_KEY=wJal...
AWS_S3_REGION_NAME=us-east-1
```

---

## Step 10: Deploy to Render

1. Go to Render dashboard
2. Select your K-DATAHUB service
3. Go to **Environment** tab
4. Add these environment variables:
   - `USE_S3` = `True`
   - `AWS_STORAGE_BUCKET_NAME` = `kdatahub-media`
   - `AWS_S3_ACCESS_KEY_ID` = Your Access Key ID
   - `AWS_S3_SECRET_ACCESS_KEY` = Your Secret Access Key
   - `AWS_S3_REGION_NAME` = `us-east-1`
5. Click **Deploy** (automatic redeploy)

---

## Step 11: Test S3 Integration

### Local Testing:
```bash
# Set environment to use S3
export USE_S3=True
export AWS_STORAGE_BUCKET_NAME=kdatahub-media
export AWS_S3_ACCESS_KEY_ID=AKIA...
export AWS_S3_SECRET_ACCESS_KEY=wJal...

# Run Django development server
python manage.py runserver
```

Then:
1. Create a user profile and upload a profile picture
2. Check if file is stored in S3:
   - Go to AWS Console → S3 → kdatahub-media
   - You should see `media/profile_pics/` folder with your image
3. Visit user profile page - image should load from S3 URL

### Production Testing:
After deployment to Render:
1. Navigate to your Render app
2. Create a test user and upload profile picture
3. Verify image appears on profile page
4. Check AWS S3 bucket for the uploaded file

---

## Step 12: Monitor S3 Usage

1. Go to **AWS Console** → **S3**
2. Click your bucket `kdatahub-media`
3. Go to **Metrics** tab to see:
   - Total storage used
   - Upload/download requests
   - Cost estimates

**Free Tier Limits:**
- First 5 GB: Free
- Beyond 5 GB: ~$0.023/GB per month
- Download: First 1 GB/month free, then ~$0.09/GB

---

## Troubleshooting

### "ClientError: An error occurred (NoSuchBucket)"
- Verify bucket name is correct
- Verify bucket exists in the region you specified
- Check AWS_STORAGE_BUCKET_NAME environment variable

### "An error occurred (AccessDenied)"
- Verify Access Key ID and Secret are correct
- Check IAM user has S3 permissions
- Verify bucket policy allows public read

### Images not loading from S3
- Check if file is actually in S3 bucket
- Verify bucket policy includes public read permission
- Check CORS configuration is correct
- Try accessing S3 URL directly in browser

### Large image uploads failing
- Default max file size: 100MB (should be fine for profile pics)
- Increase in Django: `DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880` (5MB)

### S3 URL shows as 404
- Verify Object URL is public: Right-click object → Open → should load
- Check file permissions in S3
- Verify CORS settings are correct

---

## Monitoring Costs

**Estimated Monthly Costs (small app):**
- Storage (100 users × 5MB avg profile pic = 500MB): ~$0.01
- Data Transfer (out): ~$0.05
- **Total: ~$0.06/month** (well within free tier)

Monitor at: AWS Console → S3 → Storage → View storage analytics

---

## Security Best Practices

1. **Rotate Access Keys Periodically**
   - AWS recommends every 90 days
   - Create new keys, update environment variables, delete old ones

2. **Use IAM Policies**
   - For production, create restricted policy (only S3 bucket, not full access)
   - Principle of least privilege

3. **Enable Versioning** (optional)
   - S3 → Bucket → Properties → Versioning
   - Protects against accidental deletion

4. **Enable Logging** (optional)
   - Track who accessed files and when
   - Useful for auditing

---

## AWS CLI Alternative (Advanced)

If you prefer command line:

```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure
# Enter: Access Key ID, Secret, Region (us-east-1), Output (json)

# Create bucket
aws s3 mb s3://kdatahub-media --region us-east-1

# Upload a file
aws s3 cp local-file.jpg s3://kdatahub-media/media/profile_pics/

# List bucket contents
aws s3 ls s3://kdatahub-media/
```

---

## Useful Links

- AWS S3 Documentation: https://docs.aws.amazon.com/s3/
- Django Storages Docs: https://django-storages.readthedocs.io/en/latest/
- Boto3 Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- AWS Free Tier: https://aws.amazon.com/free/

---

## Summary

| Step | Task | Time |
|------|------|------|
| 1-2 | Create AWS account & S3 bucket | 10 min |
| 3-6 | Configure bucket & create IAM user | 15 min |
| 7-8 | Setup K-DATAHUB (already done!) | 2 min |
| 9-10 | Set environment variables | 5 min |
| 11 | Test integration | 10 min |
| **Total** | | **~40 minutes** |

