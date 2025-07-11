"""
Virtual Geneticist API - Batch Processing Module
Handles batch uploads and task creation from CSV files.
"""

import csv
import os
import json
import requests
from collections import defaultdict
from typing import Dict, List, Tuple, Optional

# === CONFIGURATION ===
BASE_URL = "https://vg-api.btgenomics.com:8082/api"
UPLOAD_URL = f"{BASE_URL}/upload"
CREATE_TASK_URL = f"{BASE_URL}/createtask"

def read_token_from_file(token_file_path: str) -> str:
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

def read_csv_file(csv_file_path: str) -> List[Dict[str, str]]:
    """Read and parse the CSV file."""
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        raise Exception(f"Error reading CSV file: {e}")

def validate_csv_structure(data: List[Dict[str, str]]) -> List[str]:
    """Validate that the CSV has the required columns."""
    errors = []
    
    if not data:
        errors.append("CSV file is empty")
        return errors
    
    required_columns = ['samples', 'title', 'project', 'vcf_mode', 'assembly', 'upload_vcf']
    first_row = data[0]
    
    for column in required_columns:
        if column not in first_row:
            errors.append(f"Missing required column: {column}")
    
    return errors

def upload_file_batch(file_path: str, token: str, prefix: str = None, show_progress: bool = True) -> Optional[str]:
    """Upload a file and return the remote path with progress bar."""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None
    
    # Import the upload function from the upload module
    try:
        from btg_upload_module import upload_file
        result = upload_file(file_path, token, prefix, show_progress)
        if result:
            return result.get('upload_path')
        return None
    except ImportError:
        # Fallback to basic upload if import fails
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        files = {
            'file': open(file_path, 'rb')
        }
        
        data = {}
        if prefix:
            data['prefix'] = prefix
        
        try:
            print(f"📤 Uploading {file_path}...")
            response = requests.post(UPLOAD_URL, headers=headers, files=files, data=data)
            
            files['file'].close()
            
            if response.status_code == 200:
                result = response.json()
                remote_path = result.get('upload_path')
                print(f"✅ Upload successful: {remote_path}")
                return remote_path
            else:
                print(f"❌ Upload failed for {file_path}: {response.status_code}")
                try:
                    error_msg = response.json().get('message', 'Unknown error')
                    print(f"Error message: {error_msg}")
                except:
                    print(f"Response text: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error uploading {file_path}: {e}")
            return None

def process_samples_individual(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Process each sample row individually for task creation."""
    processed_samples = []
    
    # Add timestamp to make titles unique
    import time
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    for i, row in enumerate(data):
        # Create a task config for this sample with unique title
        original_title = row['title']
        unique_title = f"{original_title}_{timestamp}"
        
        task_config = {
            'title': unique_title,
            'project': row['project'],
            'vcf_mode': row['vcf_mode'],
            'assembly': row['assembly'],
            'upload_vcf': row['upload_vcf'],
            'clinical_info': row.get('clinical_info', '')
        }
        
        # Add father and mother files for TRIO mode (skip if NA)
        if row['vcf_mode'] == 'TRIO':
            if row.get('upload_father') and row['upload_father'] != 'NA':
                task_config['upload_father'] = row['upload_father']
            if row.get('upload_mother') and row['upload_mother'] != 'NA':
                task_config['upload_mother'] = row['upload_mother']
        
        processed_samples.append(task_config)
    
    return processed_samples

def create_task_batch(config: Dict[str, str], token: str) -> Optional[str]:
    """Create a task and return the submission ID."""
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Remove None values from config
    task_data = {k: v for k, v in config.items() if v is not None}
    
    try:
        print(f"🔬 Creating task for: {task_data['title']}")
        print(f"Mode: {task_data['vcf_mode']}")
        print(f"Assembly: {task_data['assembly']}")
        
        response = requests.post(CREATE_TASK_URL, headers=headers, json=task_data)
        
        if response.status_code == 200:
            result = response.json()
            submission_id = result.get('submission_id')
            print(f"✅ Task created successfully: {submission_id}")
            return submission_id
        else:
            print(f"❌ Task creation failed: {response.status_code}")
            try:
                error_msg = response.json().get('message', 'Unknown error')
                print(f"Error message: {error_msg}")
                
                # Handle duplicate submission error
                if "already been submitted" in error_msg:
                    print(f"💡 This task has already been submitted. The API prevents duplicate submissions.")
                    print(f"💡 Try using different titles or check if the task already exists.")
                    return None
                    
            except:
                print(f"Response text: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating task: {e}")
        return None

def run_batch_upload_module(token_file_path: str, csv_file_path: str, show_progress: bool = True):
    """Run the batch upload module.
    
    Args:
        token_file_path: Path to token file
        csv_file_path: Path to CSV file
        show_progress: Whether to show upload progress bars
    """
    print("\n" + "="*60)
    print("📤 BATCH UPLOAD MODULE")
    print("="*60)
    
    try:
        # Read token
        token = read_token_from_file(token_file_path)
        print(f"✅ Token loaded from: {token_file_path}")
        
        # Read CSV
        data = read_csv_file(csv_file_path)
        print(f"✅ CSV loaded from: {csv_file_path}")
        print(f"📊 Found {len(data)} rows")
        
        # Validate CSV structure
        errors = validate_csv_structure(data)
        if errors:
            print("❌ CSV validation errors:")
            for error in errors:
                print(f"  - {error}")
            return
        
        # Upload files
        uploaded_files = {}
        total_files = len(data)
        for i, row in enumerate(data, 1):
            print(f"\n📁 Processing file {i}/{total_files}")
            
            # Upload proband VCF
            vcf_file = row['upload_vcf']
            title = row['title']
            
            # Use full path from CSV directly
            full_path = vcf_file
            
            # Upload with title as prefix
            remote_path = upload_file_batch(full_path, token, title, show_progress=show_progress)
            if remote_path:
                uploaded_files[vcf_file] = remote_path
            
            # Upload father VCF for TRIO mode
            if row['vcf_mode'] == 'TRIO' and row.get('upload_father') and row['upload_father'] != 'NA':
                father_file = row['upload_father']
                full_path = father_file  # Use full path from CSV directly
                
                remote_path = upload_file_batch(full_path, token, title, show_progress=show_progress)
                if remote_path:
                    uploaded_files[father_file] = remote_path
            
            # Upload mother VCF for TRIO mode
            if row['vcf_mode'] == 'TRIO' and row.get('upload_mother') and row['upload_mother'] != 'NA':
                mother_file = row['upload_mother']
                full_path = mother_file  # Use full path from CSV directly
                
                remote_path = upload_file_batch(full_path, token, title, show_progress=show_progress)
                if remote_path:
                    uploaded_files[mother_file] = remote_path
        
        print(f"\n📊 Upload Summary:")
        print(f"✅ Successfully uploaded: {len(uploaded_files)} files")
        print(f"❌ Failed uploads: {len(data) - len(uploaded_files)} files")
        
        # Save upload results
        results_file = "upload_results.json"
        with open(results_file, 'w') as f:
            json.dump(uploaded_files, f, indent=2)
        print(f"📄 Upload results saved to: {results_file}")
        
        return uploaded_files
        
    except Exception as e:
        print(f"❌ Error in batch upload: {e}")
        return None

def run_batch_task_module(token_file_path: str, csv_file_path: str, uploaded_files: Dict[str, str] = None):
    """Run the batch task creation module."""
    print("\n" + "="*60)
    print("🔬 BATCH TASK CREATION MODULE")
    print("="*60)
    
    try:
        # Read token
        token = read_token_from_file(token_file_path)
        print(f"✅ Token loaded from: {token_file_path}")
        
        # Read CSV
        data = read_csv_file(csv_file_path)
        print(f"✅ CSV loaded from: {csv_file_path}")
        
        # Load uploaded files if not provided
        if uploaded_files is None:
            results_file = "upload_results.json"
            if os.path.exists(results_file):
                with open(results_file, 'r') as f:
                    uploaded_files = json.load(f)
                print(f"✅ Loaded upload results from: {results_file}")
            else:
                print("❌ No upload results found. Please run batch upload first.")
                return
        
        # Process samples individually
        processed_samples = process_samples_individual(data)
        print(f"📊 Found {len(processed_samples)} samples to process")
        
        # Create tasks
        created_tasks = []
        for i, config in enumerate(processed_samples):
            print(f"\n{'='*50}")
            print(f"Processing sample {i+1}/{len(processed_samples)}: {config['title']}")
            
            # Update config with uploaded file paths
            if config['vcf_mode'] == 'TRIO':
                # For TRIO, we need proband and optionally father/mother files
                if 'upload_vcf' in config and config['upload_vcf'] in uploaded_files:
                    config['upload_vcf'] = uploaded_files[config['upload_vcf']]
                else:
                    print(f"❌ Missing proband file for TRIO: {config['upload_vcf']}")
                    continue
                
                if 'upload_father' in config and config['upload_father'] in uploaded_files:
                    config['upload_father'] = uploaded_files[config['upload_father']]
                if 'upload_mother' in config and config['upload_mother'] in uploaded_files:
                    config['upload_mother'] = uploaded_files[config['upload_mother']]
                    
            elif config['vcf_mode'] == 'SNP':
                # For SNP, we only need the proband file
                if 'upload_vcf' in config and config['upload_vcf'] in uploaded_files:
                    config['upload_vcf'] = uploaded_files[config['upload_vcf']]
                else:
                    print(f"❌ Missing proband file for SNP mode: {config['upload_vcf']}")
                    continue
            
            # Create task
            submission_id = create_task_batch(config, token)
            if submission_id:
                created_tasks.append({
                    'title': config['title'],
                    'submission_id': submission_id,
                    'vcf_mode': config['vcf_mode']
                })
        
        # Save task results
        results_file = "task_results.json"
        with open(results_file, 'w') as f:
            json.dump(created_tasks, f, indent=2)
        print(f"\n📄 Task results saved to: {results_file}")
        
        print(f"\n📊 Task Creation Summary:")
        print(f"✅ Successfully created: {len(created_tasks)} tasks")
        
        return created_tasks
        
    except Exception as e:
        print(f"❌ Error in batch task creation: {e}")
        return None

def run_batch_full_module(token_file_path: str, csv_file_path: str, show_progress: bool = True):
    """Run the complete batch process (upload + task creation)."""
    print("\n" + "="*70)
    print("🚀 BATCH PROCESSING MODULE")
    print("="*70)
    print("This will upload all files and create tasks in one operation")
    print("="*70)
    
    # Step 1: Upload files
    uploaded_files = run_batch_upload_module(token_file_path, csv_file_path, show_progress)
    if not uploaded_files:
        print("❌ Upload phase failed. Stopping batch process.")
        return
    
    # Step 2: Create tasks
    created_tasks = run_batch_task_module(token_file_path, csv_file_path, uploaded_files)
    if not created_tasks:
        print("❌ Task creation phase failed.")
        return
    
    print("\n🎉 BATCH PROCESSING COMPLETED!")
    print(f"✅ Uploaded {len(uploaded_files)} files")
    print(f"✅ Created {len(created_tasks)} tasks")
    
    # Save complete results
    complete_results = {
        'uploaded_files': uploaded_files,
        'created_tasks': created_tasks
    }
    
    results_file = "batch_results.json"
    with open(results_file, 'w') as f:
        json.dump(complete_results, f, indent=2)
    print(f"📄 Complete results saved to: {results_file}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python btg_batch_module.py <token_file> <csv_file>")
        print("Note: Use full paths in CSV file (e.g., 'data/file.vcf.gz')")
        sys.exit(1)
    
    token_file = sys.argv[1]
    csv_file = sys.argv[2]
    
    run_batch_full_module(token_file, csv_file) 