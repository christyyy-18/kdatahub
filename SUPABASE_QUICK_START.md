# Supabase Setup - Quick Visual Guide

## 🎬 5-Minute Quick Start

### Step 1️⃣: Create Supabase Account
**Time: 2 minutes**

1. Go to **https://supabase.com**
2. Click **"Sign Up"** button (top right)

   ![Sign Up](https://img.shields.io/badge/Click-Sign_Up-blue)

3. Choose sign-up method:
   - Email address, or
   - GitHub account
   
4. Verify your email
5. Create organization (skip if prompted)

✅ **Account created!**

---

### Step 2️⃣: Create Project
**Time: 3 minutes**

1. In Supabase dashboard, click **"New Project"**
2. Fill in the form:

```
Name:              kdatahub
Database Password: [Create Strong Password - SAVE THIS!]
Region:            us-east-1
```

3. Click **"Create new project"**
4. ⏳ Wait 2-3 minutes for initialization...

```
Creating project...
├─ Setting up database
├─ Configuring storage
├─ Initializing API
└─ Done! ✅
```

✅ **Project created!**

---

### Step 3️⃣: Get Your API Credentials
**Time: 1 minute**

1. Go to **Settings** (gear icon in sidebar)
2. Click **"API"** tab
3. You'll see:

```
┌─────────────────────────────────────────────┐
│ Your API Credentials                        │
├─────────────────────────────────────────────┤
│                                             │
│ Project URL:                                │
│ https://xyzabc.supabase.co ←── COPY THIS   │
│                                             │
│ Service Role Secret:                        │
│ eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...   │
│ ↑ COPY THIS (scroll to see full key)       │
│                                             │
└─────────────────────────────────────────────┘
```

📝 **Copy these two values:**
- Project URL (example: `https://xyzabc.supabase.co`)
- Service Role Secret (the long key starting with `eyJ...`)

✅ **Credentials obtained!**

---

### Step 4️⃣: Create Storage Bucket
**Time: 1 minute**

1. In Supabase dashboard, go to **"Storage"** (left sidebar)
2. Click **"Create a new bucket"** button
3. Fill in:

```
Bucket name:  kdatahub-media
Privacy:      Public ✅ (select this)
```

4. Click **"Create bucket"**

✅ **Bucket created!**

---

### Step 5️⃣: Set Bucket Policy
**Time: 1 minute**

1. Open your `kdatahub-media` bucket
2. Click **"Policies"** tab
3. Click **"Create policy"** → Choose **"For public access"**
4. Leave defaults selected:
   - ✅ SELECT (allow reads)
   - ✅ INSERT (allow uploads)
5. Click **"Review"** then **"Create"**

✅ **Bucket configured!**

---

## 🔑 Adding Credentials to Your App

### Edit `.env` File

Find your `.env` file in the project root and update:

```bash
# Before (disabled)
USE_SUPABASE=False
# SUPABASE_URL=...
# SUPABASE_KEY=...

# After (enabled with your credentials)
USE_SUPABASE=True
SUPABASE_URL=https://xyzabc.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh5emFiYyIsInJvbGUiOiJzZXJ2aWNlX3JvbGUiLCJpYXQiOjE2MzAwMDAwMDAsImV4cCI6MTk0NjI5NTAwMH0.xxx
SUPABASE_STORAGE_BUCKET=kdatahub-media
```

**Replace with YOUR actual credentials from Step 3**

---

## ✅ Verify It Works

### Run Verification Script
```bash
python verify_supabase.py
```

You should see:
```
✓ USE_SUPABASE: True
✓ DEFAULT_FILE_STORAGE: kdatahub.storage.SupabaseStorage
✓ MEDIA_URL: https://xyzabc.supabase.co/storage/v1/object/public/kdatahub-media/
```

### Test by Uploading
1. Start server: `python manage.py runserver`
2. Go to http://localhost:8000
3. Log in as a user
4. Upload a profile picture
5. Check Supabase dashboard → Storage → kdatahub-media
6. Your file should appear there! ✅

---

## 🎯 File References

- **Detailed Setup**: [SUPABASE_INTEGRATION_CHECKLIST.md](SUPABASE_INTEGRATION_CHECKLIST.md)
- **Configuration Status**: [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md)
- **Environment Variables**: [.env.example](.env.example)
- **Verification Script**: `python verify_supabase.py`

---

## ❓ Common Questions

### Q: Is my data secure?
**A:** Yes! You're using the "Service Role Secret" which is for backend use only. Never expose this in frontend code.

### Q: Can I use S3 instead?
**A:** Yes! Set `USE_S3=True` in .env instead. Both work interchangeably.

### Q: What if I don't set up Supabase?
**A:** Files save locally to `/media/` directory. Works fine for development!

### Q: Can I switch back to local storage?
**A:** Yes! Set `USE_SUPABASE=False` in .env and restart. Old files stay in Supabase.

---

## 🚀 You're Ready!

Your K-DATAHUB app is ready to use Supabase for cloud file storage.

**Next Steps:**
1. ✅ Follow steps 1-5 above (5 minutes)
2. ✅ Update `.env` with credentials
3. ✅ Run `python verify_supabase.py`
4. ✅ Test with file upload
5. ✅ Deploy to production

---

## 📞 Need Help?

- **Stuck?** Run: `python verify_supabase.py` for diagnostics
- **Configuration issues?** Check [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md)
- **Supabase questions?** Visit https://supabase.com/docs

**Happy coding! 🎉**
