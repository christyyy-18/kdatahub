/**
 * Firebase Configuration
 * Replace these values with your Firebase project credentials
 * You can get these from Firebase Console -> Project Settings
 */

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// Export config for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = firebaseConfig;
}
