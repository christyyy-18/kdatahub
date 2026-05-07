#!/usr/bin/env python
"""
Supabase Integration Verification Script
Run this to test if Supabase is properly configured
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kdatahub.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.conf import settings
from io import BytesIO


def check_settings():
    """Check if Supabase settings are configured"""
    print("\n" + "="*60)
    print("SUPABASE CONFIGURATION CHECK")
    print("="*60 + "\n")
    
    print("1. Checking Django Settings:")
    use_supabase = getattr(settings, 'USE_SUPABASE', False)
    print(f"   ✓ USE_SUPABASE: {use_supabase}")
    print(f"   ✓ DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"   ✓ MEDIA_URL: {settings.MEDIA_URL}")
    
    if use_supabase:
        supabase_url = getattr(settings, 'SUPABASE_URL', 'Not set')
        supabase_key = getattr(settings, 'SUPABASE_KEY', 'Not set')
        supabase_bucket = getattr(settings, 'SUPABASE_STORAGE_BUCKET', 'Not set')
        
        print(f"   ✓ SUPABASE_URL: {supabase_url[:30] + '...' if supabase_url != 'Not set' else 'Not set'}")
        print(f"   ✓ SUPABASE_KEY: {'*' * 10 + '...' if supabase_key != 'Not set' else 'Not set'}")
        print(f"   ✓ SUPABASE_STORAGE_BUCKET: {supabase_bucket}")
    else:
        print("   ℹ  Supabase is disabled (USE_SUPABASE=False)")
        print("   ℹ  Files will be stored locally in /media/")
    
    return use_supabase


def test_file_operations():
    """Test file upload and download"""
    print("\n2. Testing File Operations:")
    
    if not settings.USE_SUPABASE:
        print("   ⊘ Supabase not enabled - skipping remote tests")
        print("   ✓ Local file storage is ready")
        return True
    
    try:
        from kdatahub.storage import SupabaseStorage
        storage = SupabaseStorage()
        
        # Test connection by checking if we can instantiate
        print(f"   ✓ SupabaseStorage backend loaded")
        print(f"   ✓ Base URL: {storage.base_url[:50] + '...'}")
        
        # Try to test file operations
        test_content = b"Supabase integration test file"
        test_filename = "test-integration.txt"
        
        print(f"\n   Testing upload to bucket '{storage.bucket_name}'...")
        storage._save(test_filename, BytesIO(test_content))
        print(f"   ✓ File uploaded successfully")
        
        # Check if file exists
        if storage.exists(test_filename):
            print(f"   ✓ File verified in bucket")
            url = storage.url(test_filename)
            print(f"   ✓ Public URL: {url}")
        else:
            print(f"   ⚠ File uploaded but verification failed")
        
        # Clean up
        storage.delete(test_filename)
        print(f"   ✓ Test file cleaned up")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        print(f"   ⚠ Check your Supabase credentials in .env file")
        return False


def test_django_models():
    """Test file field in Django models"""
    print("\n3. Testing Django Model Integration:")
    
    try:
        from accounts.models import CustomUser
        
        # Get first user if exists
        user = CustomUser.objects.first()
        if user:
            print(f"   ✓ Found user: {user.username}")
            if user.profile_picture:
                print(f"   ✓ Profile picture URL: {user.profile_picture.url}")
            else:
                print(f"   ℹ User has no profile picture yet")
        else:
            print(f"   ℹ No users in database yet")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return False


def show_recommendations():
    """Show next steps based on configuration"""
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60 + "\n")
    
    if settings.USE_SUPABASE:
        print("✓ Supabase is ENABLED")
        print("\nYour system is ready for cloud file storage!")
        print("\n📋 Recommended actions:")
        print("  1. Test file upload by logging in as a user")
        print("  2. Try uploading a profile picture")
        print("  3. Check Supabase dashboard to verify files appear in the bucket")
        print("  4. Deploy to production with same Supabase credentials")
    else:
        print("⊘ Supabase is DISABLED (local file storage active)")
        print("\nTo enable Supabase:")
        print("  1. Create account at https://supabase.com")
        print("  2. Create new project named 'kdatahub'")
        print("  3. Get credentials from Settings → API")
        print("  4. Create storage bucket 'kdatahub-media'")
        print("  5. Update .env file:")
        print("     USE_SUPABASE=True")
        print("     SUPABASE_URL=your-url")
        print("     SUPABASE_KEY=your-key")
        print("  6. Re-run this script to verify")
        print("\n📖 Detailed guide: See SUPABASE_INTEGRATION_CHECKLIST.md")


def main():
    """Run all checks"""
    try:
        supabase_enabled = check_settings()
        test_django_models()
        
        if supabase_enabled:
            test_file_operations()
        
        show_recommendations()
        
        print("\n" + "="*60)
        print("✓ Configuration check complete!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error during verification: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
