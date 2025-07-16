"""
Virtual Geneticist API - v1.0.0 Style Upload Module
Simple upload without timeouts or retry logic (like the original working version).
"""

import requests
import os
import sys

# === CONFIGURATION ===
BASE_URL = "https://vg-api.btgenomics.com:8082/api"
UPLOAD_URL = f"{BASE_URL}/upload"

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

def upload_file_v1(file_path, token, prefix=None):
    """Upload a file using v1.0.0 style - simple, no timeouts, no retries."""
    
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
    files = {
        'file': open(file_path, 'rb')
    }
    
    data = {}
    if prefix:
        data['prefix'] = prefix
    
    print(f"📤 Uploading {os.path.basename(file_path)} ({file_size_mb:.1f}MB)...")
    print("🔄 Using v1.0.0 style - no timeouts, no retries")
    
    try:
        # Simple request - NO TIMEOUTS SPECIFIED (like v1.0.0)
        response = requests.post(UPLOAD_URL, headers=headers, files=files, data=data)
        
        # Close the file
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
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def run_upload_module_v1(token_file_path=None, file_path=None, prefix=None):
    """Run the v1.0.0 style file upload module."""
    print("\n" + "="*60)
    print("📤 V1.0.0 STYLE FILE UPLOAD MODULE")
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
    result = upload_file_v1(file_path, token, prefix)
    
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
    run_upload_module_v1(token_file, file_path, prefix) 