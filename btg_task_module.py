"""
Virtual Geneticist API - Task Creation Module
Handles creating analysis tasks using the Virtual Geneticist API.
"""

import requests
import json
import sys
import os

# === CONFIGURATION ===
BASE_URL = "https://vg-api.btgenomics.com:8082/api"
CREATE_TASK_URL = f"{BASE_URL}/createtask"

def read_config_from_file(config_file_path):
    """Read configuration from a JSON file."""
    try:
        with open(config_file_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file: {e}")
    except Exception as e:
        raise Exception(f"Error reading configuration file: {e}")

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

def validate_task_config(config):
    """Validate the task configuration based on VCF mode requirements."""
    errors = []
    
    # Check required fields
    required_fields = ["title", "project", "vcf_mode", "assembly"]
    for field in required_fields:
        if not config.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Validate vcf_mode
    valid_modes = ["SNP", "TRIO", "CARRIER"]
    if config.get("vcf_mode") not in valid_modes:
        errors.append(f"Invalid vcf_mode: {config.get('vcf_mode')}. Must be one of: {', '.join(valid_modes)}")
    
    # Validate assembly
    valid_assemblies = ["hg19", "hg38"]
    if config.get("assembly") not in valid_assemblies:
        errors.append(f"Invalid assembly: {config.get('assembly')}. Must be one of: {', '.join(valid_assemblies)}")
    
    # Check clinical information (either upload_clinical or clinical_info is required)
    if not config.get("upload_clinical") and not config.get("clinical_info"):
        errors.append("Either upload_clinical or clinical_info is required")
    
    # Check VCF file requirements based on mode
    vcf_mode = config.get("vcf_mode")
    if vcf_mode in ["SNP", "TRIO"]:
        if not config.get("upload_vcf"):
            errors.append(f"upload_vcf is required for {vcf_mode} mode")
    
    if vcf_mode in ["TRIO", "CARRIER"]:
        if not config.get("upload_father"):
            errors.append(f"upload_father is required for {vcf_mode} mode")
        if not config.get("upload_mother"):
            errors.append(f"upload_mother is required for {vcf_mode} mode")
    
    # Check field length limits
    if config.get("title") and len(config["title"]) > 256:
        errors.append("title must be 256 characters or less")
    
    if config.get("project") and len(config["project"]) > 256:
        errors.append("project must be 256 characters or less")
    
    if config.get("clinical_info") and len(config["clinical_info"]) > 4096:
        errors.append("clinical_info must be 4096 characters or less")
    
    return errors

def create_task(config, token):
    """Create a new analysis task using the Virtual Geneticist API."""
    
    # Validate configuration
    errors = validate_task_config(config)
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return None
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Remove None values from config
    task_data = {k: v for k, v in config.items() if v is not None}
    
    try:
        print("Creating analysis task...")
        print(f"Mode: {task_data['vcf_mode']}")
        print(f"Assembly: {task_data['assembly']}")
        print(f"Title: {task_data['title']}")
        print("-" * 40)
        
        response = requests.post(CREATE_TASK_URL, headers=headers, json=task_data)
        
        # Handle response
        if response.status_code == 200:
            result = response.json()
            print("✅ Task created successfully!")
            print(f"Submission ID: {result.get('submission_id', 'N/A')}")
            print(f"Message: {result.get('message', 'N/A')}")
            return result
        else:
            print(f"❌ Task creation failed with status code: {response.status_code}")
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

def get_task_config_from_user(default_config):
    """Get task configuration from user input."""
    config = {}
    
    print("\n📝 Enter task configuration:")
    print("-" * 30)
    
    config['title'] = input(f"Title (default: {default_config['title']}): ").strip() or default_config['title']
    config['project'] = input(f"Project (default: {default_config['project']}): ").strip() or default_config['project']
    
    print("\nAnalysis mode options:")
    print("1. SNP - Proband analysis")
    print("2. TRIO - Family trio analysis")
    print("3. CARRIER - Carrier analysis")
    mode_choice = input(f"Mode (default: {default_config['vcf_mode']}): ").strip() or default_config['vcf_mode']
    config['vcf_mode'] = mode_choice.upper()
    
    print("\nAssembly options:")
    print("1. hg19")
    print("2. hg38")
    assembly_choice = input(f"Assembly (default: {default_config['assembly']}): ").strip() or default_config['assembly']
    config['assembly'] = assembly_choice.lower()
    
    # File paths
    print("\n📁 File paths:")
    if config['vcf_mode'] in ['SNP', 'TRIO']:
        config['upload_vcf'] = input(f"Proband VCF path (default: {default_config['upload_vcf']}): ").strip() or default_config['upload_vcf']
    
    if config['vcf_mode'] in ['TRIO', 'CARRIER']:
        config['upload_father'] = input(f"Father VCF path (default: {default_config['upload_father']}): ").strip() or default_config['upload_father']
        config['upload_mother'] = input(f"Mother VCF path (default: {default_config['upload_mother']}): ").strip() or default_config['upload_mother']
    
    # Handle clinical information (either upload_clinical or clinical_info)
    if 'clinical_info' in default_config:
        # Use clinical_info if it exists in default config
        default_clinical = default_config.get('clinical_info', '')
        clinical_input = input(f"Clinical information (default: {default_clinical[:100]}{'...' if len(default_clinical) > 100 else ''}): ").strip()
        if clinical_input:
            config['clinical_info'] = clinical_input
        else:
            config['clinical_info'] = default_clinical
    elif 'upload_clinical' in default_config:
        # Use upload_clinical if it exists in default config
        config['upload_clinical'] = input(f"Clinical file path (default: {default_config['upload_clinical']}): ").strip() or default_config['upload_clinical']
    else:
        # Ask user to choose
        print("\nClinical information:")
        print("1. Upload clinical file (upload_clinical)")
        print("2. Provide clinical information text (clinical_info)")
        clinical_choice = input("Choose option (1 or 2): ").strip()
        
        if clinical_choice == "1":
            config['upload_clinical'] = input("Clinical file path: ").strip()
        elif clinical_choice == "2":
            config['clinical_info'] = input("Clinical information: ").strip()
        else:
            print("Invalid choice, skipping clinical information")
    
    # Optional CNV file
    cnv_path = input("CNV file path (optional, press Enter to skip): ").strip()
    if cnv_path:
        config['upload_cnv'] = cnv_path
    
    return config

def run_create_task_module(token_file_path=None, config_file_path=None):
    """Run the task creation module."""
    print("\n" + "="*60)
    print("🔬 TASK CREATION MODULE")
    print("="*60)
    
    # Get token
    if token_file_path:
        try:
            token = read_token_from_file(token_file_path)
            print(f"✅ Token loaded from: {token_file_path}")
        except Exception as e:
            print(f"❌ Error loading token: {e}")
            return None
    else:
        token_file_path = input("Enter token file path: ").strip()
        if not token_file_path:
            print("❌ Token file path is required")
            return None
        try:
            token = read_token_from_file(token_file_path)
        except Exception as e:
            print(f"❌ Error loading token: {e}")
            return None
    
    # Get configuration
    if config_file_path:
        try:
            default_config = read_config_from_file(config_file_path)
            print(f"✅ Configuration loaded from: {config_file_path}")
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return None
    else:
        config_file_path = input("Enter configuration file path: ").strip()
        if not config_file_path:
            print("❌ Configuration file path is required")
            return None
        try:
            default_config = read_config_from_file(config_file_path)
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return None
    
    # Show current configuration
    print("Current default configuration:")
    print(json.dumps(default_config, indent=2))
    print("-" * 40)
    
    # Ask user if they want to use defaults or customize
    use_defaults = input("Use default configuration? (y/n): ").lower().strip()
    
    if use_defaults in ['y', 'yes']:
        task_config = default_config.copy()
    else:
        task_config = get_task_config_from_user(default_config)
    
    print("\n📋 Final task configuration:")
    print(json.dumps(task_config, indent=2))
    print("-" * 40)
    
    # Ask user if they want to proceed
    response = input("Do you want to create this task? (y/n): ").lower().strip()
    if response not in ['y', 'yes']:
        print("Task creation cancelled.")
        return None
    
    # Create the task
    result = create_task(task_config, token)
    
    if result:
        print("\n🎉 Task created successfully!")
        print("You can now use the submission_id to check the task status.")
        print(f"Submission ID: {result.get('submission_id')}")
        return result.get('submission_id')
    else:
        print("\n💥 Task creation failed. Please check the error messages above.")
        return None

if __name__ == "__main__":
    token_file = sys.argv[1] if len(sys.argv) > 1 else None
    config_file = sys.argv[2] if len(sys.argv) > 2 else None
    run_create_task_module(token_file, config_file) 