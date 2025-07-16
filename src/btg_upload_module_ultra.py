"""
Virtual Geneticist API - Ultra Reliable Upload Module
Handles file uploads with very long timeouts for large files.
"""

import requests
import os
import sys
import time

# === CONFIGURATION ===
BASE_URL = "https://vg-api.btgenomics.com:8082/api"
UPLOAD_URL = f"{BASE_URL}/upload"

# Ultra-long timeouts for large files
CONNECT_TIMEOUT = 60    # 60 seconds to establish connection
READ_TIMEOUT = 1800     # 30 minutes for read operations
UPLOAD_TIMEOUT = 3600   # 60 minutes for complete upload

def read_token_from_file(token_file_path):
    """Read token from a text file."""
    try:
        with open(token_file_path, 'r') as f:
            token = f.read().strip()
        if not token:
            raise ValueError("Token file is empty")
        return token
    except FileNotFoundError:
        raise FileNotFoundError(f"Token file not found: {token_file_path}")
    except Exception as e:
        raise Exception(f"Error reading token file: {e}")

def validate_file(file_path):
    """Validate that the file exists and has a supported extension."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check file extension
    supported_extensions = ['.vcf', '.vcf.gz', '.pdf', '.txt']
    file_ext = os.path.splitext(file_path)[1]
    
    # Handle .vcf.gz files (double extension)
    if file_ext == '.gz':
        base_name = os.path.splitext(file_path)[0]
        file_ext = os.path.splitext(base_name)[1] + file_ext
    
    if file_ext not in supported_extensions:
        raise ValueError(f"Unsupported file type: {file_ext}. Supported types: {', '.join(supported_extensions)}")

def upload_file_ultra(file_path, token, prefix=None, max_retries=2):
    """Upload a file with ultra-long timeouts for large files."""
    
    # Validate the file
    validate_file(file_path)
    
    # Get file size for info
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / (1024 * 1024)
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Prepare form data
    data = {}
    if prefix:
        data['prefix'] = prefix
    
    print(f"📤 Uploading {os.path.basename(file_path)} ({file_size_mb:.1f}MB)...")
    print(f"⏱️  Using ultra-long timeouts: {CONNECT_TIMEOUT}s connect, {READ_TIMEOUT//60}min read")
    
    for attempt in range(max_retries):
        try:
            # Simple upload with ultra-long timeouts
            files = {
                'file': open(file_path, 'rb')
            }
            
            # Use ultra-long timeout for all files
            timeout = (CONNECT_TIMEOUT, UPLOAD_TIMEOUT)
            
            print(f"🔄 Attempt {attempt + 1}/{max_retries} - Starting upload...")
            
            response = requests.post(
                UPLOAD_URL, 
                headers=headers, 
                files=files, 
                data=data,
                timeout=timeout
            )
            
            files['file'].close()
            
            # Handle response
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Upload successful!")
                print(f"Remote path: {result.get('upload_path', 'N/A')}")
                return result
            else:
                print(f"❌ Upload failed with status code: {response.status_code}")
                try:
                    error_msg = response.json().get('message', 'Unknown error')
                    print(f"Error message: {error_msg}")
                except:
                    print(f"Response text: {response.text}")
                
                # Don't retry on client errors (4xx)
                if 400 <= response.status_code < 500:
                    return None
                    
        except requests.exceptions.Timeout as e:
            print(f"❌ Timeout error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = 5 * (attempt + 1)  # 5s, then 10s
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("❌ Max retries exceeded. Upload failed.")
                print("💡 Try uploading during off-peak hours or check your network connection.")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = 5 * (attempt + 1)
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("❌ Max retries exceeded. Upload failed.")
                return None
                
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    return None

def run_upload_module_ultra(token_file_path=None, file_path=None, prefix=None):
    """Run the ultra-reliable file upload module."""
    print("\n" + "="*60)
    print("📤 ULTRA-RELIABLE FILE UPLOAD MODULE")
    print("="*60)
    
    # Get token
    if token_file_path:
        try:
            token = read_token_from_file(token_file_path)
            print(f"✅ Token loaded from: {token_file_path}")
        except Exception as e:
            print(f"❌ Error loading token: {e}")
            return
    else:
        token_file_path = input("Enter token file path: ").strip()
        if not token_file_path:
            print("❌ Token file path is required")
            return
        try:
            token = read_token_from_file(token_file_path)
        except Exception as e:
            print(f"❌ Error loading token: {e}")
            return
    
    # Get file path
    if file_path:
        print(f"📁 File path provided: {file_path}")
    else:
        file_path = input("Enter file path: ").strip()
        if not file_path:
            print("❌ File path is required")
            return
    
    # Get prefix
    if prefix:
        print(f"📂 Prefix provided: {prefix}")
    else:
        prefix = input("Enter prefix (optional, press Enter to skip): ").strip()
        if not prefix:
            prefix = None
    
    print(f"\n📁 File: {file_path}")
    print(f"📂 Prefix: {prefix if prefix else 'None'}")
    print("-" * 40)
    
    # Check if file path is still the default
    if file_path == "path/to/sample.vcf.gz":
        print("⚠️  Please update the file_path with your actual file path")
        return
    
    # Perform upload
    result = upload_file_ultra(file_path, token, prefix)
    
    if result:
        print("\n🎉 Upload completed successfully!")
        print("You can now use the remote path in your task creation requests.")
    else:
        print("\n💥 Upload failed. Please check the error messages above.")

if __name__ == "__main__":
    import sys
    token_file = sys.argv[1] if len(sys.argv) > 1 else None
    file_path = sys.argv[2] if len(sys.argv) > 2 else None
    prefix = sys.argv[3] if len(sys.argv) > 3 else None
    run_upload_module_ultra(token_file, file_path, prefix) 