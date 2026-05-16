# 🚀 Professional Deployment Guide: Vercel + Neon + Firebase

We have successfully migrated your project configuration to a modern, 100% free-tier-friendly stack. This setup is highly reliable and provides professional performance for K-DATAHUB.

## Step 1: Set up Neon.tech (Database)
1.  Go to [Neon.tech](https://neon.tech/) and sign up for a free account.
2.  Create a new project (e.g., `kdatahub-db`).
3.  In the dashboard, you will see a **Connection String**.
4.  Copy the URL (it looks like `postgresql://alex:password@ep-cool-darkness-123.us-east-2.aws.neon.tech/neondb?sslmode=require`).
5.  **Save this for Step 3.**

---

## Step 2: Set up Firebase Storage (Media Files)
1.  Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project.
2.  Navigate to **Build > Storage** and click **Get Started**.
3.  Choose **Production Mode** (or Test Mode, but Production is safer; you just need to set the rules later).
4.  Once setup, you will see a bucket name like `your-project-id.firebasestorage.app`. **Copy this bucket name**.
5.  **Generate Credentials**:
    *   Go to **Project Settings** (gear icon) > **Service accounts**.
    *   Click **Generate new private key**.
    *   Download the JSON file. Open it and **copy the entire text inside**.

---

## Step 3: Configure Vercel
1.  Go to your project on [Vercel](https://vercel.com/).
2.  Go to **Settings > Environment Variables**.
3.  Add the following variables:

| Key | Value |
| :--- | :--- |
| `DATABASE_URL` | *Paste your Neon Connection String from Step 1* |
| `USE_FIREBASE_STORAGE` | `True` |
| `GS_BUCKET_NAME` | *Paste your bucket name from Step 2* |
| `GS_CREDENTIALS` | *Paste the entire JSON content of the file from Step 2* |
| `SECRET_KEY` | *Your Django secret key* |
| `DEBUG` | `False` |

4.  **Redeploy**: Go to the **Deployments** tab and click **Redeploy** on your latest build.

---

## ✅ Benefits of this New Stack
*   **100% Free**: No monthly fees for hosting, database, or storage.
*   **High Availability**: Google (Firebase) and Vercel infrastructure ensure your site stays up.
*   **Easy Maintenance**: No complex server setup required; just environment variables.
*   **Scalable**: If your project grows, these services can scale with you seamlessly.

---

## Troubleshooting Storage Permissions
If your images don't show up, you may need to allow public read access in Firebase.
Go to **Firebase Storage > Rules** and update them to:
```javascript
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read; // Allows anyone to view images
      allow write: if request.auth != null; // Only allows authenticated users to upload
    }
  }
}
```
