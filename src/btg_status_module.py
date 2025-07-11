"""
Virtual Geneticist API - Status Checking Module
Handles checking and monitoring task status using the Virtual Geneticist API.
"""

import requests
import json
import time
import sys
from datetime import datetime

# === CONFIGURATION ===
BASE_URL = "https://vg-api.btgenomics.com:8082/api"
GET_STATUS_URL = f"{BASE_URL}/getstatus"

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

def check_task_status(submission_id, token):
    """Check the status of a task using the Virtual Geneticist API."""
    
    if not submission_id or submission_id == "your_submission_id_here":
        print("❌ Please set a valid submission_id")
        return None
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Prepare query parameters
    params = {
        "submission_id": submission_id
    }
    
    try:
        print(f"Checking status for submission ID: {submission_id}")
        print("-" * 50)
        
        response = requests.get(GET_STATUS_URL, headers=headers, params=params)
        
        # Handle response
        if response.status_code == 200:
            result = response.json()
            print("✅ Status retrieved successfully!")
            return result
        else:
            print(f"❌ Status check failed with status code: {response.status_code}")
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

def format_status_output(status_data):
    """Format and display the status information in a readable way."""
    
    print("\n" + "="*60)
    print("📊 TASK STATUS REPORT")
    print("="*60)
    
    # Basic task information
    print(f"📋 Title: {status_data.get('title', 'N/A')}")
    print(f"📁 Project: {status_data.get('project', 'N/A')}")
    print(f"🔬 Analysis Mode: {status_data.get('vcf_mode', 'N/A')}")
    print(f"🧬 Assembly: {status_data.get('assembly', 'N/A')}")
    print(f"🆔 Task ID: {status_data.get('task_id', 'N/A')}")
    print(f"📅 Creation Time: {status_data.get('creation_time', 'N/A')}")
    print(f"🔧 Pipeline Version: {status_data.get('version', 'N/A')}")
    
    # Status with emoji
    status = status_data.get('status', 'UNKNOWN')
    status_emoji = {
        'CREATED': '🟡',
        'INITIALIZED': '🟡', 
        'RUNNING': '🟢',
        'COMPLETED': '✅',
        'FAILED': '❌',
        'CANCELLED': '⏹️'
    }
    emoji = status_emoji.get(status, '❓')
    print(f"📊 Status: {emoji} {status}")
    
    # File information
    print("\n📁 FILES:")
    print("-" * 30)
    files = [
        ('Proband VCF', 'upload_vcf'),
        ('Father VCF', 'upload_father'), 
        ('Mother VCF', 'upload_mother'),
        ('Clinical File', 'upload_clinical'),
        ('CNV File', 'upload_cnv')
    ]
    
    for file_desc, file_key in files:
        file_path = status_data.get(file_key)
        if file_path:
            print(f"  ✅ {file_desc}: {file_path}")
        else:
            print(f"  ❌ {file_desc}: Not provided")
    
    print("="*60)

def get_status_description(status):
    """Get a human-readable description of the status."""
    descriptions = {
        'CREATED': 'Task has been created and is waiting to be processed',
        'INITIALIZED': 'Task has been initialized and is being prepared for processing',
        'RUNNING': 'Task is currently being processed by the analysis pipeline',
        'COMPLETED': 'Task has been completed successfully',
        'FAILED': 'Task processing failed - check error logs',
        'CANCELLED': 'Task was cancelled by user or system'
    }
    return descriptions.get(status, f'Unknown status: {status}')

def monitor_task(submission_id, token, interval=30, max_checks=20):
    """Monitor a task status with periodic checks."""
    print(f"🔍 Starting task monitoring...")
    print(f"⏱️  Check interval: {interval} seconds")
    print(f"🔄 Maximum checks: {max_checks}")
    print("-" * 50)
    
    check_count = 0
    last_status = None
    
    while check_count < max_checks:
        check_count += 1
        print(f"\n🔄 Check #{check_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        status_data = check_task_status(submission_id, token)
        if not status_data:
            print("❌ Failed to retrieve status, stopping monitoring")
            break
        
        current_status = status_data.get('status', 'UNKNOWN')
        
        # Show full status on first check or status change
        if last_status != current_status:
            format_status_output(status_data)
            print(f"\n📝 Status Description: {get_status_description(current_status)}")
            last_status = current_status
        else:
            print(f"📊 Status: {current_status} (no change)")
        
        # Check if task is finished
        if current_status in ['COMPLETED', 'FAILED', 'CANCELLED']:
            print(f"\n🎉 Task monitoring complete! Final status: {current_status}")
            break
        
        # Wait before next check (except on last iteration)
        if check_count < max_checks:
            print(f"⏳ Waiting {interval} seconds before next check...")
            time.sleep(interval)
    
    if check_count >= max_checks:
        print(f"\n⏰ Maximum monitoring time reached ({max_checks} checks)")

def run_status_check_module(token_file_path=None, submission_id=None):
    """Run the status checking module."""
    print("\n" + "="*60)
    print("📊 STATUS CHECKING MODULE")
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
    
    # Get submission ID
    if submission_id:
        print(f"🆔 Submission ID provided: {submission_id}")
    else:
        submission_id = input("Enter submission ID: ").strip()
        if not submission_id:
            print("❌ Submission ID is required")
            return
    
    if submission_id == "your_submission_id_here":
        print("❌ Please provide a valid submission ID")
        return
    
    # Ask user what they want to do
    print("\nChoose an option:")
    print("1. Check status once")
    print("2. Monitor status continuously")
    print("3. Back to main menu")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        # Single status check
        status_data = check_task_status(submission_id, token)
        if status_data:
            format_status_output(status_data)
            print(f"\n📝 Status Description: {get_status_description(status_data.get('status', 'UNKNOWN'))}")
    
    elif choice == "2":
        # Continuous monitoring
        try:
            interval = int(input("Enter check interval in seconds (default 30): ") or "30")
            max_checks = int(input("Enter maximum number of checks (default 20): ") or "20")
            monitor_task(submission_id, token, interval, max_checks)
        except ValueError:
            print("❌ Invalid input, using defaults")
            monitor_task(submission_id, token)
    
    elif choice == "3":
        return
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    token_file = sys.argv[1] if len(sys.argv) > 1 else None
    submission_id = sys.argv[2] if len(sys.argv) > 2 else None
    run_status_check_module(token_file, submission_id) 