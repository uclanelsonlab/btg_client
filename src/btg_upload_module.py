"""
Virtual Geneticist API - Upload Module
Handles file uploads to the Virtual Geneticist API.
"""

import requests
import os
import sys
import time
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# === CONFIGURATION ===
BASE_URL = "https://vg-api.btgenomics.com:8082/api"
UPLOAD_URL = f"{BASE_URL}/upload"

# Timeout configuration for large files
CONNECT_TIMEOUT = 30  # seconds to establish connection
READ_TIMEOUT = 600    # seconds for read operations (10 minutes for large files)
UPLOAD_TIMEOUT = 900  # seconds for complete upload (15 minutes)

# Retry configuration
MAX_RETRIES = 3
BACKOFF_FACTOR = 2
STATUS_FORCELIST = [500, 502, 503, 504, 408, 429]

def create_session_with_retries():
    """Create a requests session with retry logic and timeouts."""
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=MAX_RETRIES,
        status_forcelist=STATUS_FORCELIST,
        backoff_factor=BACKOFF_FACTOR,
        allowed_methods=["POST", "GET", "HEAD"]
    )
    
    # Mount adapter with retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

class UploadProgressBar:
    """Custom progress bar for file uploads."""
    
    def __init__(self, filename, total_size):
        self.filename = filename
        self.total_size = total_size
        self.pbar = None
        self.uploaded_bytes = 0
        
    def __enter__(self):
        self.pbar = tqdm(
            total=self.total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            desc=f"📤 Uploading {os.path.basename(self.filename)}",
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
        )
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.pbar:
            self.pbar.close()
            
    def update(self, chunk_size):
        """Update progress bar with uploaded chunk."""
        self.uploaded_bytes += chunk_size
        if self.pbar:
            self.pbar.update(chunk_size)
            
    def set_description(self, desc):
        """Update the progress bar description."""
        if self.pbar:
            self.pbar.set_description(desc)

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

def upload_file(file_path, token, prefix=None, show_progress=True, max_retries=3):
    """Upload a file to the Virtual Geneticist API with progress bar and retry logic."""
    
    # Validate the file
    validate_file(file_path)
    
    # Get file size for progress bar
    file_size = os.path.getsize(file_path)
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Prepare form data
    data = {}
    if prefix:
        data['prefix'] = prefix
    
    # Calculate timeouts based on file size
    # For large files (>100MB), use longer timeouts
    if file_size > 100 * 1024 * 1024:  # 100MB
        connect_timeout = CONNECT_TIMEOUT
        read_timeout = READ_TIMEOUT
        upload_timeout = UPLOAD_TIMEOUT
    else:
        connect_timeout = 30
        read_timeout = 300
        upload_timeout = 600
    
    for attempt in range(max_retries):
        try:
            # Create session with retry logic
            session = create_session_with_retries()
            
            # Use progress bar if requested and tqdm is available
            if show_progress and 'tqdm' in sys.modules:
                with UploadProgressBar(file_path, file_size) as progress_bar:
                    # Create a custom file object that tracks progress
                    class ProgressFile:
                        def __init__(self, file_path, progress_bar):
                            self.file = open(file_path, 'rb')
                            self.progress_bar = progress_bar
                            self.name = os.path.basename(file_path)
                            
                        def read(self, size=-1):
                            chunk = self.file.read(size)
                            if chunk and self.progress_bar:
                                self.progress_bar.update(len(chunk))
                            return chunk
                            
                        def close(self):
                            self.file.close()
                            
                        def __enter__(self):
                            return self
                            
                        def __exit__(self, exc_type, exc_val, exc_tb):
                            self.close()
                    
                    files = {
                        'file': ProgressFile(file_path, progress_bar)
                    }
                    
                    # Use session with timeouts
                    response = session.post(
                        UPLOAD_URL, 
                        headers=headers, 
                        files=files, 
                        data=data,
                        timeout=(connect_timeout, upload_timeout)
                    )
                    files['file'].close()
            else:
                # Fallback to regular upload without progress bar
                files = {
                    'file': open(file_path, 'rb')
                }
                response = session.post(
                    UPLOAD_URL, 
                    headers=headers, 
                    files=files, 
                    data=data,
                    timeout=(connect_timeout, upload_timeout)
                )
                files['file'].close()
            
            # Handle response
            if response.status_code == 200:
                result = response.json()
                if not show_progress:
                    print("✅ Upload successful!")
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
                wait_time = BACKOFF_FACTOR ** attempt
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("❌ Max retries exceeded. Upload failed.")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = BACKOFF_FACTOR ** attempt
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("❌ Max retries exceeded. Upload failed.")
                return None
                
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    return None

def run_upload_module(token_file_path=None, file_path=None, prefix=None, show_progress=True):
    """Run the file upload module."""
    print("\n" + "="*60)
    print("📤 FILE UPLOAD MODULE")
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
    result = upload_file(file_path, token, prefix, show_progress)
    
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
    run_upload_module(token_file, file_path, prefix) 