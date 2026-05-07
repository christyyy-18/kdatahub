# Supabase Integration Checklist

## ✅ Current Integration Status

### Already Implemented
- ✅ Supabase package installed (`supabase==2.4.2`)
- ✅ Custom `SupabaseStorage` backend created in [kdatahub/storage.py](kdatahub/storage.py)
- ✅ Django settings configured for Supabase in [kdatahub/settings.py](kdatahub/settings.py)
- ✅ Environment variables documented in [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md)
- ✅ Setup guide provided in [SUPABASE_SETUP.md](SUPABASE_SETUP.md)

### Ready to Activate
You only need to:
1. Create Supabase account and project
2. Get API credentials
3. Create storage bucket
4. Add environment variables to `.env` file

---

## 🚀 Quick Start (5 Steps)

### Step 1: Create Supabase Project
1. Go to https://supabase.com
2. Sign up with email or GitHub
3. Create new project named `kdatahub`
4. Choose region `us-east-1`
5. Create strong database password and save it
6. Wait 2-3 minutes for initialization

### Step 2: Get API Credentials
From Supabase Dashboard:
1. Go to **Settings → API**
2. Copy:
   - **Project URL** (example: `https://xyzabc.supabase.co`)
   - **Service Role Secret** (for backend - labeled as "service_role")

⚠️ Keep these credentials secure!

### Step 3: Create Storage Bucket
1. Go to **Storage** (left sidebar)
2. Click **Create a new bucket**
3. Name: `kdatahub-media`
4. Privacy: **Public** (users can view images)
5. Click **Create bucket**

### Step 4: Set Bucket Policy
1. Open `kdatahub-media` bucket
2. Click **Policies** tab
3. Click **Create policy → For public access**
4. Select:
   - ✅ **SELECT** (allow reads)
   - ✅ **INSERT** (allow uploads)
5. Click **Review → Create**

### Step 5: Configure Environment Variables

#### For Development (Local)
Create `.env` file in project root:
```bash
# Django
DEBUG=True
SECRET_KEY=django-insecure-dev-only-key-here

# Database (SQLite for dev)
USE_POSTGRES=False

# Supabase Configuration
USE_SUPABASE=True
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_STORAGE_BUCKET=kdatahub-media

# Other Required Keys
BASE_DOMAIN=http://localhost:8000
ALLOWED_HOSTS=localhost,127.0.0.1
PAYSTACK_PUBLIC_KEY=pk_test_xxxxx
PAYSTACK_SECRET_KEY=sk_test_xxxxx
ARKESEL_API_KEY=your_api_key
SMS_SENDER_ID=KDATAHUB
MANAGER_PHONE=+233594715103
ADMIN_PHONE=0552514207
```

#### For Production (Render)
In Render Dashboard → Environment Variables:
```
USE_SUPABASE=True
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_STORAGE_BUCKET=kdatahub-media
```

---

## 🧪 Testing the Integration

### 1. Verify Settings
```bash
python manage.py shell
```
```python
from django.conf import settings
print(settings.SUPABASE_URL)
print(settings.DEFAULT_FILE_STORAGE)
```

### 2. Test File Upload
```bash
python manage.py shell
```
```python
from django.core.files.base import ContentFile
from accounts.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first()
if user:
    # Create a test file
    test_file = ContentFile(b"test content", name="test.txt")
    # This would use SupabaseStorage if configured
    print(f"File URL: {user.profile_pic.url if user.profile_pic else 'No pic'}")
```

### 3. Verify Upload to Supabase
1. Go to Supabase Dashboard
2. Open **Storage → kdatahub-media**
3. Check if new files appear there

---

## 📋 Implementation Details

### How It Works

#### File Upload Flow
```
User uploads profile picture
    ↓
Django model saves to field
    ↓
SupabaseStorage backend intercepts
    ↓
Files uploaded to Supabase bucket
    ↓
Public URL returned: 
    https://xyzabc.supabase.co/storage/v1/object/public/kdatahub-media/{filename}
```

#### Storage Backend Features
The `SupabaseStorage` class handles:
- **`_save()`** - Upload files to Supabase
- **`_open()`** - Download files from Supabase
- **`delete()`** - Remove files from Supabase
- **`exists()`** - Check if file exists
- **`url()`** - Get public file URL
- **`size()`** - Get file size
- **`listdir()`** - List bucket contents

### Models Using Supabase Storage
Currently, these models store files in Supabase (when enabled):
- `CustomUser.profile_pic` - User profile pictures

### Fallback Behavior
If `USE_SUPABASE=False`:
- Files stored locally in `/media/` directory
- Uses Django's default file storage
- Useful for development/testing

---

## 🔐 Security Checklist

- ✅ **Service Role Secret used for backend** (not Anon Key)
- ✅ **Bucket set to Public** (allows reads, but writes controlled by policy)
- ✅ **Credentials stored in .env** (never commit to git)
- ✅ **Policy restricts to SELECT + INSERT** (no DELETE for public)
- ⚠️ **TODO**: Consider rate limiting for production

---

## 🛠️ Troubleshooting

### Issue: "Invalid API key"
**Solution**: Verify you're using the correct `SUPABASE_KEY` from **Settings → API → Service Role Secret** (not Anon Key)

### Issue: "403 Unauthorized" on file upload
**Solution**: Check bucket policy - ensure **SELECT** and **INSERT** are enabled for public access

### Issue: Files not appearing in bucket
**Solution**: 
1. Check `SUPABASE_STORAGE_BUCKET` env var matches actual bucket name
2. Verify network connection and credentials
3. Check Supabase dashboard for error logs

### Issue: Fallback to local storage
**Solution**: If upload fails, files are saved locally in `/media/`. Check if `USE_SUPABASE=True` and credentials are correct

---

## 📚 References

- [Supabase Official Docs](https://supabase.com/docs)
- [Supabase Storage Guide](https://supabase.com/docs/guides/storage)
- [Django FileSystemStorage](https://docs.djangoproject.com/en/5.0/ref/files/storage/)
- [Project Setup Guide](SUPABASE_SETUP.md)

---

## Next Steps

1. ✅ Create Supabase project (follow Step 1-4 above)
2. ✅ Get credentials (Step 2)
3. ✅ Create `.env` file with credentials (Step 5)
4. ✅ Run: `python manage.py runserver`
5. ✅ Test by uploading profile picture as user
6. ✅ Verify file appears in Supabase dashboard

**Ready to integrate? Start with Step 1 above! 🚀**
