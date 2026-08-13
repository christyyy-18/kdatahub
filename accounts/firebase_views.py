"""
Firebase API views for user synchronization
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
import firebase_admin
from firebase_admin import credentials, auth
import json
import os

User = get_user_model()

# Initialize Firebase Admin SDK (if not already initialized)
def init_firebase_admin():
    if not firebase_admin._apps:
        try:
            # Try to load from environment variable or file
            firebase_creds = os.environ.get('FIREBASE_CREDENTIALS_JSON')
            if firebase_creds:
                cred = credentials.Certificate(json.loads(firebase_creds))
            else:
                # Fallback to file if it exists
                cred = credentials.Certificate('firebase-adminsdk.json')
            
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Firebase Admin SDK initialization skipped: {e}")
            return False
    return True

@csrf_exempt
@require_http_methods(["POST"])
def sync_user(request):
    """
    Sync Firebase user with Django backend
    Expected POST data:
    {
        "firebase_uid": "...",
        "email": "...",
        "display_name": "...",
        "id_token": "..."
    }
    """
    try:
        data = json.loads(request.body)
        
        firebase_uid = data.get('firebase_uid')
        email = data.get('email')
        display_name = data.get('display_name')
        id_token = data.get('id_token')
        
        if not all([firebase_uid, email, id_token]):
            return JsonResponse({
                'success': False,
                'message': 'Missing required fields'
            }, status=400)
        
        # Verify Firebase ID token
        if init_firebase_admin():
            try:
                decoded_token = auth.verify_id_token(id_token)
                if decoded_token.get('uid') != firebase_uid:
                    return JsonResponse({
                        'success': False,
                        'message': 'Token verification failed'
                    }, status=401)
            except Exception as e:
                print(f"Token verification error: {e}")
                # Continue anyway if Firebase not fully configured
        
        # Get or create Django user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0] if not User.objects.filter(username=email.split('@')[0]).exists() else f"{email.split('@')[0]}{firebase_uid[:4]}",
                'first_name': display_name or '',
            }
        )
        
        # Update user info if it exists
        if not created:
            if display_name:
                user.first_name = display_name
            user.save()
        
        # Store Firebase UID in user profile
        # You might want to extend the CustomUser model to include firebase_uid field
        
        return JsonResponse({
            'success': True,
            'message': 'User synced successfully',
            'user_id': user.id,
            'username': user.username
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        print(f"Sync error: {e}")
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def verify_firebase_token(request):
    """
    Verify Firebase token for API requests
    """
    try:
        data = json.loads(request.body)
        id_token = data.get('id_token')
        
        if not id_token:
            return JsonResponse({
                'success': False,
                'message': 'No token provided'
            }, status=400)
        
        if init_firebase_admin():
            try:
                decoded_token = auth.verify_id_token(id_token)
                return JsonResponse({
                    'success': True,
                    'uid': decoded_token.get('uid'),
                    'email': decoded_token.get('email')
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': f'Token verification failed: {str(e)}'
                }, status=401)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Firebase not configured'
            }, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON'
        }, status=400)
