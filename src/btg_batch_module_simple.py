"""
Virtual Geneticist API - Simple Batch Processing Module (No Progress Bar)
Handles batch uploads and task creation from CSV files without progress tracking.
"""

import csv
import os
import json
import requests
import time
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

def upload_file_simple_batch(file_path: str, token: str, prefix: str = None) -> Optional[str]:
    """Upload a file and return the remote path without progress bar."""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None
    
    # Import the simple upload function
    try:
        from btg_upload_module_simple import upload_file_simple
        result = upload_file_simple(file_path, token, prefix)
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
            response = requests.post(UPLOAD_URL, headers=headers, files=files, data=data, timeout=(30, 600))
            
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

def create_task_simple_batch(config: Dict[str, str], token: str) -> Optional[str]:
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
        
        response = requests.post(CREATE_TASK_URL, headers=headers, json=task_data, timeout=(30, 120))
        
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

def run_batch_full_simple_module(token_file_path: str, csv_file_path: str):
    """Run the simple batch full module (upload + task creation) without progress bars."""
    print("\n" + "="*60)
    print("🚀 SIMPLE BATCH PROCESSING MODULE (No Progress Bar)")
    print("="*60)
    print("This will upload all files and create tasks in one operation")
    print("="*60)
    
    try:
        # Load token
        token = read_token_from_file(token_file_path)
        print(f"✅ Token loaded from: {token_file_path}")
        
        # Load CSV
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
        
        print()
        
        # Step 1: Upload all files
        print("📤 BATCH UPLOAD MODULE")
        print("="*60)
        
        uploaded_files = {}
        failed_uploads = []
        
        for i, row in enumerate(data, 1):
            print(f"\n📁 Processing file {i}/{len(data)}")
            
            # Get file path
            file_path = row['upload_vcf']
            if not file_path or file_path == 'NA':
                print(f"⚠️  Skipping row {i}: No file path provided")
                continue
            
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                failed_uploads.append(file_path)
                continue
            
            # Upload file
            remote_path = upload_file_simple_batch(file_path, token)
            
            if remote_path:
                uploaded_files[file_path] = remote_path
                print(f"✅ Uploaded: {os.path.basename(file_path)}")
            else:
                failed_uploads.append(file_path)
                print(f"❌ Failed to upload: {file_path}")
        
        # Report upload results
        print(f"\n📊 Upload Summary:")
        print(f"✅ Successful: {len(uploaded_files)}")
        print(f"❌ Failed: {len(failed_uploads)}")
        
        if failed_uploads:
            print(f"\n❌ Failed uploads:")
            for file_path in failed_uploads:
                print(f"  - {file_path}")
        
        if not uploaded_files:
            print("❌ No files were uploaded successfully. Cannot proceed with task creation.")
            return
        
        # Step 2: Create tasks
        print(f"\n🔬 BATCH TASK CREATION MODULE")
        print("="*60)
        
        # Process samples for task creation
        processed_samples = process_samples_individual(data)
        
        created_tasks = []
        failed_tasks = []
        
        for i, sample_config in enumerate(processed_samples, 1):
            print(f"\n📋 Processing task {i}/{len(processed_samples)}")
            
            # Update file paths with remote paths
            if sample_config['upload_vcf'] in uploaded_files:
                sample_config['upload_vcf'] = uploaded_files[sample_config['upload_vcf']]
            
            if 'upload_father' in sample_config and sample_config['upload_father'] in uploaded_files:
                sample_config['upload_father'] = uploaded_files[sample_config['upload_father']]
            
            if 'upload_mother' in sample_config and sample_config['upload_mother'] in uploaded_files:
                sample_config['upload_mother'] = uploaded_files[sample_config['upload_mother']]
            
            # Create task
            submission_id = create_task_simple_batch(sample_config, token)
            
            if submission_id:
                created_tasks.append({
                    'title': sample_config['title'],
                    'submission_id': submission_id
                })
                print(f"✅ Task created: {sample_config['title']}")
            else:
                failed_tasks.append(sample_config['title'])
                print(f"❌ Failed to create task: {sample_config['title']}")
        
        # Final summary
        print(f"\n🎉 BATCH PROCESSING COMPLETE")
        print("="*60)
        print(f"📤 Files uploaded: {len(uploaded_files)}/{len(data)}")
        print(f"🔬 Tasks created: {len(created_tasks)}/{len(processed_samples)}")
        
        if created_tasks:
            print(f"\n✅ Successfully created tasks:")
            for task in created_tasks:
                print(f"  - {task['title']}: {task['submission_id']}")
        
        if failed_tasks:
            print(f"\n❌ Failed task creations:")
            for title in failed_tasks:
                print(f"  - {title}")
        
        if failed_uploads:
            print(f"\n⚠️  Note: {len(failed_uploads)} files failed to upload and were skipped")
        
    except Exception as e:
        print(f"❌ Error in batch processing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python btg_batch_module_simple.py <token_file> <csv_file>")
        sys.exit(1)
    
    token_file = sys.argv[1]
    csv_file = sys.argv[2]
    run_batch_full_simple_module(token_file, csv_file) 