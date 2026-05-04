# Supabase Storage Setup Guide

## Why Supabase?

✅ **Best Free Tier** - 1GB free storage (generous!)  
✅ **Easiest Setup** - 5 minutes to get started  
✅ **PostgreSQL Included** - Great for future growth  
✅ **Authentication Ready** - Built-in user management  
✅ **Real-time Capabilities** - Future-proof  
✅ **No Cost Initially** - Free tier is genuinely useful  

---

## Step 1: Create Supabase Account

1. Go to [https://supabase.com](https://supabase.com)
2. Click **Sign Up**
3. Create account with email or GitHub
4. Verify email
5. Create organization (optional name)

---

## Step 2: Create Project

1. Click **New Project**
2. Configure:
   - **Name**: `kdatahub`
   - **Database Password**: Create strong password (save it!)
   - **Region**: `us-east-1` (closest to users)
3. Click **Create new project**
4. Wait 2-3 minutes for project to initialize

✅ You now have a free PostgreSQL database!

---

## Step 3: Get Your Project Credentials

1. Go to **Project Settings** (gear icon)
2. Click **API**
3. Copy:
   - **Project URL** (starts with `https://`)
   - **Anon Public Key** (for client-side)
   - **Service Role Secret** (for server-side)

**⚠️ Important:** 
- Use **Service Role Secret** for backend (Django)
- Keep these secure in environment variables only

---

## Step 4: Create Storage Bucket

1. In Supabase dashboard, go to **Storage** section (left sidebar)
2. Click **Create a new bucket**
3. Configure:
   - **Bucket name**: `kdatahub-media`
   - **Privacy**: Select **Public** (users can view images)
4. Click **Create bucket**

---

## Step 5: Configure Bucket Policy

1. Open `kdatahub-media` bucket
2. Click **Policies** tab
3. Under **Other policies**, click **Create policy**
4. Choose template: **For public access**
5. Configure:
   - **Allowed operations**: 
     - ✅ SELECT (read)
     - ✅ INSERT (upload)
   - **Targeting**: All files
6. Click **Review**, then **Create**

---

## Step 6: Environment Variables Setup

### For Development (Local):

Create `.env`:
```
USE_SUPABASE=False
```

### For Production (Render):

You'll add these later:
```
USE_SUPABASE=True
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGc... (Service Role Secret)
SUPABASE_STORAGE_BUCKET=kdatahub-media
```

---

## Step 7: Install Supabase Package

The requirements are already updated. Just run:

```bash
pip install -r requirements.txt
```

This installs:
- `supabase==2.4.2`
- `django-storages==1.14.2`

---

## Step 8: Test Locally

```bash
# Create a test user
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.create_user('testuser', 'test@example.com', 'password123')

# Try uploading from admin
python manage.py runserver
# Navigate to http://localhost:8000/admin
# Login with testuser
# Try uploading a profile picture
```

❌ **Expected:** Upload fails because `USE_SUPABASE=False` locally (uses local storage instead)

✅ **This is correct!** Development uses local storage for faster testing.

---

## Step 9: Deploy to Render

### Prerequisites:
- Render account (free tier works)
- PostgreSQL addon created
- Paystack keys ready

### Steps:

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Select your K-DATAHUB service
3. Go to **Environment** tab
4. Add environment variables:

| Key | Value |
|-----|-------|
| `USE_SUPABASE` | `True` |
| `SUPABASE_URL` | Your Project URL |
| `SUPABASE_KEY` | Service Role Secret |
| `SUPABASE_STORAGE_BUCKET` | `kdatahub-media` |

5. Click **Save**
6. Service auto-redeploys

---

## Step 10: Test in Production

After Render deploys:

1. Navigate to your app: `https://kdatahub.onrender.com`
2. Sign up for new account
3. Upload a profile picture
4. Go back to Supabase dashboard
5. Go to **Storage** → `kdatahub-media`
6. You should see your uploaded image in the `profile_pics/` folder

✅ **Success!** Image is stored in Supabase.

---

## Verify It Works

### Check in Supabase Dashboard:

1. **Storage** → `kdatahub-media`
2. Click the uploaded image
3. You should see image preview
4. Copy public URL and open in browser
5. ✅ Image displays

### Check in K-DATAHUB:

1. Go to user profile page
2. Profile picture should load
3. ✅ Image displays

---

## Troubleshooting

### "SUPABASE_URL not found"
- Check environment variables in Render
- Verify `SUPABASE_URL` starts with `https://`
- No trailing slash at end

### "Connection refused" or timeout
- Verify `SUPABASE_KEY` is correct
- Check it's the **Service Role Secret**, not Anon Public Key
- Verify bucket is **Public**

### Image uploads fail
- Check bucket policy allows INSERT
- Verify bucket name is `kdatahub-media`
- Check file size < 100MB

### Images don't load
- Verify bucket is **Public**
- Check image URL in Supabase dashboard
- Try accessing URL directly in browser

### File already exists error
- Supabase prevents overwriting by default
- Solution: Use unique filenames with timestamps
- Already implemented in Django's default behavior

---

## Storage Limits

### Free Tier:
- **Storage**: 1 GB
- **Bandwidth**: 3 GB/month
- **Database**: 500 MB PostgreSQL

### After Free Tier:
- **Storage**: $0.12/GB (generous!)
- **Bandwidth**: Included with database plan
- **Database**: $9/month additional storage

---

## How Storage Works

```
User uploads profile picture
         ↓
Django saves to Supabase bucket: profile_pics/username_123.jpg
         ↓
Supabase returns public URL
         ↓
Django stores URL in database
         ↓
User profile page displays image from URL
```

---

## Scaling Beyond Free Tier

If you hit limits (unlikely initially):

| Need | Solution | Cost |
|------|----------|------|
| More storage | Upgrade plan | $0.12/GB |
| More bandwidth | Pro plan | $25/month |
| Database | Larger plan | $9/month |
| **Total for small app** | **Pro Plan** | **~$40/month** |

---

## Security Best Practices

1. **Never commit** `.env` file
2. **Use Service Role Secret** for backend (Django)
3. **Use Anon Key** for frontend only (if adding JavaScript)
4. **Make bucket Public** only for viewing (not writing)
5. **Rotate keys** if ever exposed
6. **Use HTTPS only** for all requests

---

## Comparison: Supabase vs Alternatives

| Feature | Supabase | AWS S3 | Cloudinary |
|---------|----------|--------|-----------|
| Free storage | 1 GB | 5 GB | 25 GB |
| Setup time | 5 min | 15 min | 5 min |
| Database included | ✅ PostgreSQL | ❌ | ❌ |
| Auth included | ✅ | ❌ | ❌ |
| Cost after free | $0.12/GB | $0.023/GB | Low/GB |
| Best for | Full stack | Scale | Images |
| Our pick | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## Next Steps

1. ✅ Create Supabase account (Step 1)
2. ✅ Create project (Step 2)
3. ✅ Get credentials (Step 3)
4. ✅ Create bucket (Step 4)
5. ✅ Configure policy (Step 5)
6. ⏳ Deploy to Render (Step 9)
7. ⏳ Test in production (Step 10)

---

## Useful Links

- Supabase Docs: https://supabase.com/docs
- Supabase Storage: https://supabase.com/docs/guides/storage
- Python Client: https://github.com/supabase/supabase-py
- Pricing: https://supabase.com/pricing

---

## Support

- Supabase Community: https://discord.supabase.io
- GitHub Issues: https://github.com/supabase/supabase/issues
- Email Support: support@supabase.io

---

**Status: Ready for Supabase deployment!**

Follow Steps 1-5 now, then Steps 9-10 when deploying to Render.
