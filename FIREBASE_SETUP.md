# Firebase Integration Setup Guide for K-DATAHUB

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter your project name (e.g., "K-DATAHUB")
4. Configure Firebase settings as needed
5. Create the project

## Step 2: Get Your Firebase Config

1. In Firebase Console, go to **Project Settings** (gear icon)
2. Scroll down to "Your apps" section
3. Click on the **Web** icon to add a web app
4. Register your app with a name (e.g., "K-DATAHUB Web")
5. Copy the Firebase configuration object

Your config should look like:
```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

## Step 3: Update Frontend Configuration

1. Open `static/js/firebase-config.js`
2. Replace the placeholder values with your Firebase config from Step 2
3. Save the file

## Step 4: Enable Firebase Authentication Methods

In Firebase Console:
1. Go to **Build** → **Authentication**
2. Click **Get started**
3. Enable sign-in methods:
   - **Email/Password**: Click "Email/Password", enable both options, save
   - (Optional) **Google**, **GitHub**, or other providers

## Step 5: Setup Firebase Admin SDK (Backend - Optional)

For server-side token verification:

1. In Firebase Console, go to **Project Settings** → **Service Accounts**
2. Click "Generate new private key"
3. Save the JSON file as `firebase-adminsdk.json` in your project root

OR set environment variable:
```bash
# In your .env file:
FIREBASE_CREDENTIALS_JSON='{"type":"service_account",...}'
```

Install Firebase Admin SDK:
```bash
pip install firebase-admin
```

## Step 6: Update Django Settings

In `kdatahub/settings.py`, add Firebase to INSTALLED_APPS if needed:

```python
INSTALLED_APPS = [
    ...
    'accounts',  # Already there
    ...
]
```

## Step 7: Test Your Setup

1. Run Django server: `python manage.py runserver`
2. Go to http://localhost:8000
3. Check browser console for any Firebase errors
4. Try signing up with email/password

## Frontend Usage Examples

### Sign Up with Firebase
```javascript
const result = await firebaseSignUp('user@example.com', 'password123', 'username');
if (result.success) {
  console.log('Signed up successfully');
  // User will be automatically synced to Django
}
```

### Login
```javascript
const result = await firebaseLogin('user@example.com', 'password123');
if (result.success) {
  console.log('Logged in successfully');
}
```

### Logout
```javascript
await firebaseLogout();
```

### Get Current User
```javascript
const user = getCurrentUser();
if (user) {
  console.log('Currently logged in as:', user.email);
}
```

### Get ID Token for API Calls
```javascript
const token = await getIdToken();
// Use this token in Authorization header for protected API endpoints
```

## File Structure

```
K-DATAHUB/
├── static/js/
│   ├── firebase-config.js        # Firebase configuration
│   ├── firebase-auth.js          # Authentication handler
│   └── main.js
├── accounts/
│   ├── firebase_views.py         # Backend API endpoints
│   └── urls.py                   # Updated with Firebase URLs
├── templates/
│   └── base.html                 # Updated with Firebase scripts
└── firebase-adminsdk.json        # (Optional) Service account key
```

## API Endpoints

### Sync User with Django
**POST** `/api/firebase/sync-user/`
```json
{
  "firebase_uid": "...",
  "email": "...",
  "display_name": "...",
  "id_token": "..."
}
```

### Verify Firebase Token
**POST** `/api/firebase/verify-token/`
```json
{
  "id_token": "..."
}
```

## Troubleshooting

### Firebase scripts not loading
- Check browser console for errors
- Ensure Firebase config is correct in `firebase-config.js`
- Verify API keys are enabled in Google Cloud Console

### Token verification fails
- Ensure Firebase Admin SDK credentials are set correctly
- Check that ID token hasn't expired
- Verify token format

### User not syncing to Django
- Check Django error logs
- Verify CSRF token is being sent
- Ensure API endpoint is accessible

### CORS Issues
- If calling API from different domain, add to Django CORS settings
- Firebase URLs should be in ALLOWED_HOSTS

## Next Steps

1. **Custom Authentication Flow**: Update your login/signup templates to use Firebase
2. **Social Login**: Add Google/GitHub sign-in buttons
3. **Custom Claims**: Add admin/manager roles in Firebase
4. **Email Verification**: Enable email verification in auth flow
5. **Real-time Database**: Use Firebase for real-time order updates

## Resources

- [Firebase Console](https://console.firebase.google.com/)
- [Firebase Auth Documentation](https://firebase.google.com/docs/auth)
- [Firebase JS SDK](https://firebase.google.com/docs/web/setup)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
