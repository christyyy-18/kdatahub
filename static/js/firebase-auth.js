/**
 * Firebase Authentication Handler
 * Manages user authentication with Firebase and Django backend
 */

let authUser = null;

// Initialize Firebase (after config is loaded)
function initializeFirebase() {
  firebase.initializeApp(firebaseConfig);
  setupAuthStateListener();
}

/**
 * Listen for authentication state changes
 */
function setupAuthStateListener() {
  firebase.auth().onAuthStateChanged(async (user) => {
    if (user) {
      authUser = user;
      console.log('User authenticated:', user.email);
      
      // Get Firebase ID token and send to Django backend
      const idToken = await user.getIdToken();
      await syncUserWithDjango(user, idToken);
      
      // Update UI
      updateAuthUI(true, user);
    } else {
      authUser = null;
      console.log('User logged out');
      updateAuthUI(false);
    }
  });
}

/**
 * Firebase Sign Up with email and password
 */
async function firebaseSignUp(email, password, username) {
  try {
    const result = await firebase.auth().createUserWithEmailAndPassword(email, password);
    const user = result.user;
    
    // Update profile with username
    await user.updateProfile({
      displayName: username
    });
    
    // Get ID token and send to Django
    const idToken = await user.getIdToken();
    await syncUserWithDjango(user, idToken);
    
    console.log('Sign up successful');
    return { success: true, user };
  } catch (error) {
    console.error('Sign up error:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Firebase Login with email and password
 */
async function firebaseLogin(email, password) {
  try {
    const result = await firebase.auth().signInWithEmailAndPassword(email, password);
    const user = result.user;
    const idToken = await user.getIdToken();
    
    console.log('Login successful');
    return { success: true, user };
  } catch (error) {
    console.error('Login error:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Firebase Logout
 */
async function firebaseLogout() {
  try {
    await firebase.auth().signOut();
    console.log('Logout successful');
    return { success: true };
  } catch (error) {
    console.error('Logout error:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Sync Firebase user with Django backend
 */
async function syncUserWithDjango(firebaseUser, idToken) {
  try {
    const response = await fetch('/api/firebase/sync-user/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({
        firebase_uid: firebaseUser.uid,
        email: firebaseUser.email,
        display_name: firebaseUser.displayName,
        id_token: idToken
      })
    });
    
    const data = await response.json();
    if (data.success) {
      console.log('User synced with Django');
    } else {
      console.error('Sync failed:', data.message);
    }
  } catch (error) {
    console.error('Sync error:', error);
  }
}

/**
 * Update UI based on authentication state
 */
function updateAuthUI(isAuthenticated, user = null) {
  const authElements = document.querySelectorAll('[data-auth-required]');
  const guestElements = document.querySelectorAll('[data-guest-only]');
  
  if (isAuthenticated) {
    authElements.forEach(el => el.style.display = 'block');
    guestElements.forEach(el => el.style.display = 'none');
    
    if (user) {
      const userDisplay = document.querySelector('[data-user-display]');
      if (userDisplay) {
        userDisplay.textContent = user.email;
      }
    }
  } else {
    authElements.forEach(el => el.style.display = 'none');
    guestElements.forEach(el => el.style.display = 'block');
  }
}

/**
 * Get CSRF token from Django
 */
function getCsrfToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
         document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
}

/**
 * Get current user
 */
function getCurrentUser() {
  return authUser;
}

/**
 * Get current user's ID token
 */
async function getIdToken() {
  if (authUser) {
    return await authUser.getIdToken();
  }
  return null;
}

// Initialize Firebase when DOM is ready
document.addEventListener('DOMContentLoaded', initializeFirebase);
