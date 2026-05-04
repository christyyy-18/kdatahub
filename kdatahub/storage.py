"""
Custom Django storage backend for Supabase
"""
import os
from django.core.files.storage import Storage
from django.conf import settings
import requests


class SupabaseStorage(Storage):
    """
    Custom storage backend for Supabase Storage
    Stores files in Supabase bucket and returns public URLs
    """
    
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        self.bucket_name = settings.SUPABASE_STORAGE_BUCKET
        self.base_url = f'{self.supabase_url}/storage/v1/object/public/{self.bucket_name}'
    
    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json'
        }
    
    def _open(self, name, mode='rb'):
        """Open a file from Supabase"""
        url = f'{self.supabase_url}/storage/v1/object/{self.bucket_name}/{name}'
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            from io import BytesIO
            return BytesIO(response.content)
        raise FileNotFoundError(f"File {name} not found in Supabase")
    
    def _save(self, name, content):
        """Save a file to Supabase"""
        # Ensure directories exist
        url = f'{self.supabase_url}/storage/v1/object/{self.bucket_name}/{name}'
        
        # Read content
        if hasattr(content, 'read'):
            file_content = content.read()
        else:
            file_content = content
        
        # Upload to Supabase
        headers = self._get_headers()
        headers.pop('Content-Type', None)  # Let requests set it
        
        response = requests.post(
            url,
            headers=headers,
            data=file_content
        )
        
        if response.status_code not in [200, 201]:
            raise IOError(f"Failed to save {name} to Supabase: {response.text}")
        
        return name
    
    def delete(self, name):
        """Delete a file from Supabase"""
        url = f'{self.supabase_url}/storage/v1/object/{self.bucket_name}/{name}'
        response = requests.delete(url, headers=self._get_headers())
        
        if response.status_code not in [200, 204]:
            raise IOError(f"Failed to delete {name} from Supabase")
    
    def exists(self, name):
        """Check if file exists in Supabase"""
        url = f'{self.supabase_url}/storage/v1/object/{self.bucket_name}/{name}'
        response = requests.head(url, headers=self._get_headers())
        return response.status_code == 200
    
    def url(self, name):
        """Return the public URL for a file"""
        return f'{self.base_url}/{name}'
    
    def get_accessed_time(self, name):
        """Not implemented for Supabase"""
        raise NotImplementedError('Supabase does not support accessed time')
    
    def get_created_time(self, name):
        """Not implemented for Supabase"""
        raise NotImplementedError('Supabase does not support created time')
    
    def get_modified_time(self, name):
        """Not implemented for Supabase"""
        raise NotImplementedError('Supabase does not support modified time')
    
    def listdir(self, path):
        """List directory contents in Supabase"""
        url = f'{self.supabase_url}/storage/v1/object/list/{self.bucket_name}/{path}'
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            items = response.json()
            dirs = []
            files = []
            for item in items:
                if item.get('name'):
                    if item.get('metadata'):
                        files.append(item['name'])
                    else:
                        dirs.append(item['name'])
            return dirs, files
        
        return [], []
    
    def size(self, name):
        """Get file size from Supabase"""
        url = f'{self.supabase_url}/storage/v1/object/info/{self.bucket_name}/{name}'
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 200:
            return response.json().get('metadata', {}).get('size', 0)
        
        raise IOError(f"Cannot get size of {name}")
