/**
 * Example: Firebase Authentication Form Handler
 * Shows how to integrate Firebase auth with your HTML forms
 */

// Example: Firebase Login Form
function setupFirebaseLoginForm() {
  const loginForm = document.getElementById('firebase-login-form');
  if (!loginForm) return;
  
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('firebase-email').value;
    const password = document.getElementById('firebase-password').value;
    const errorDiv = document.getElementById('firebase-login-error');
    
    try {
      const result = await firebaseLogin(email, password);
      
      if (result.success) {
        // Redirect to dashboard or home
        window.location.href = '/orders/track/';
      } else {
        errorDiv.textContent = result.error;
        errorDiv.style.display = 'block';
      }
    } catch (error) {
      errorDiv.textContent = 'An error occurred during login';
      errorDiv.style.display = 'block';
    }
  });
}

// Example: Firebase Sign Up Form
function setupFirebaseSignUpForm() {
  const signupForm = document.getElementById('firebase-signup-form');
  if (!signupForm) return;
  
  signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('firebase-username').value;
    const email = document.getElementById('firebase-email').value;
    const password = document.getElementById('firebase-password').value;
    const confirmPassword = document.getElementById('firebase-confirm-password').value;
    const errorDiv = document.getElementById('firebase-signup-error');
    const successDiv = document.getElementById('firebase-signup-success');
    
    // Reset messages
    errorDiv.style.display = 'none';
    successDiv.style.display = 'none';
    
    // Validate passwords match
    if (password !== confirmPassword) {
      errorDiv.textContent = 'Passwords do not match';
      errorDiv.style.display = 'block';
      return;
    }
    
    // Validate password strength
    if (password.length < 8) {
      errorDiv.textContent = 'Password must be at least 8 characters';
      errorDiv.style.display = 'block';
      return;
    }
    
    try {
      const result = await firebaseSignUp(email, password, username);
      
      if (result.success) {
        successDiv.textContent = 'Account created successfully! Redirecting...';
        successDiv.style.display = 'block';
        
        // Redirect after delay
        setTimeout(() => {
          window.location.href = '/orders/track/';
        }, 2000);
      } else {
        errorDiv.textContent = result.error;
        errorDiv.style.display = 'block';
      }
    } catch (error) {
      errorDiv.textContent = 'An error occurred during sign up';
      errorDiv.style.display = 'block';
    }
  });
}

// Example: Logout
function setupFirebaseLogout() {
  const logoutButton = document.getElementById('firebase-logout-btn');
  if (!logoutButton) return;
  
  logoutButton.addEventListener('click', async (e) => {
    e.preventDefault();
    
    const result = await firebaseLogout();
    if (result.success) {
      // Redirect to home
      window.location.href = '/';
    }
  });
}

// Example: Protected content
function setupProtectedContent() {
  firebase.auth().onAuthStateChanged((user) => {
    const protectedContent = document.getElementById('protected-content');
    const guestContent = document.getElementById('guest-content');
    
    if (user) {
      if (protectedContent) protectedContent.style.display = 'block';
      if (guestContent) guestContent.style.display = 'none';
      
      const userEmail = document.getElementById('user-email');
      if (userEmail) {
        userEmail.textContent = user.email;
      }
    } else {
      if (protectedContent) protectedContent.style.display = 'none';
      if (guestContent) guestContent.style.display = 'block';
    }
  });
}

// Example: API call with Firebase token
async function makeProtectedAPICall(endpoint, method = 'GET', data = null) {
  const user = getCurrentUser();
  if (!user) {
    console.error('User not authenticated');
    return null;
  }
  
  const token = await getIdToken();
  
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'X-CSRFToken': getCsrfToken()
    }
  };
  
  if (data) {
    options.body = JSON.stringify(data);
  }
  
  try {
    const response = await fetch(endpoint, options);
    return await response.json();
  } catch (error) {
    console.error('API call failed:', error);
    return null;
  }
}

// Initialize all forms when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  setupFirebaseLoginForm();
  setupFirebaseSignUpForm();
  setupFirebaseLogout();
  setupProtectedContent();
});
