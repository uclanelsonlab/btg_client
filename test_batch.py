#!/usr/bin/env python3
"""
Test script for batch processing functionality
"""

import json
from btg_batch_module import read_csv_file, validate_csv_structure, process_samples_individual

def test_csv_processing():
    """Test CSV processing functionality."""
    print("🧪 Testing CSV Processing")
    print("=" * 50)
    
    # Read CSV
    csv_file = "data/samplesheet.csv"
    data = read_csv_file(csv_file)
    print(f"✅ Loaded {len(data)} rows from {csv_file}")
    
    # Validate structure
    errors = validate_csv_structure(data)
    if errors:
        print("❌ Validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ CSV structure is valid")
    
    # Process samples individually
    processed_samples = process_samples_individual(data)
    print(f"✅ Found {len(processed_samples)} samples to process")
    
    # Show sample details
    for i, config in enumerate(processed_samples):
        print(f"\n📊 Sample {i+1}: {config['title']}")
        print(f"   Mode: {config['vcf_mode']}")
        print(f"   Assembly: {config['assembly']}")
        print(f"   Project: {config['project']}")
        
        if config['vcf_mode'] == 'TRIO':
            files = []
            if 'upload_vcf' in config:
                files.append(f"Proband: {config['upload_vcf']}")
            if 'upload_father' in config:
                files.append(f"Father: {config['upload_father']}")
            if 'upload_mother' in config:
                files.append(f"Mother: {config['upload_mother']}")
            print(f"   Files: {', '.join(files)}")
        else:
            if 'upload_vcf' in config:
                print(f"   File: {config['upload_vcf']}")
    
    return True

def simulate_batch_process():
    """Simulate the batch process without actual API calls."""
    print("\n🚀 Simulating Batch Process")
    print("=" * 50)
    
    # Read CSV
    data = read_csv_file("data/samplesheet.csv")
    processed_samples = process_samples_individual(data)
    
    # Simulate upload results
    uploaded_files = {}
    for row in data:
        # Upload proband VCF
        vcf_file = row['upload_vcf']
        title = row['title']
        remote_path = f"{title}/{vcf_file}"
        uploaded_files[vcf_file] = remote_path
        print(f"📤 Would upload: {vcf_file} → {remote_path}")
        
        # Upload father VCF for TRIO mode
        if row['vcf_mode'] == 'TRIO' and row.get('upload_father') and row['upload_father'] != 'NA':
            father_file = row['upload_father']
            remote_path = f"{title}/{father_file}"
            uploaded_files[father_file] = remote_path
            print(f"📤 Would upload: {father_file} → {remote_path}")
        
        # Upload mother VCF for TRIO mode
        if row['vcf_mode'] == 'TRIO' and row.get('upload_mother') and row['upload_mother'] != 'NA':
            mother_file = row['upload_mother']
            remote_path = f"{title}/{mother_file}"
            uploaded_files[mother_file] = remote_path
            print(f"📤 Would upload: {mother_file} → {remote_path}")
    
    # Simulate task creation
    created_tasks = []
    for i, config in enumerate(processed_samples):
        # Update config with uploaded paths
        if config['vcf_mode'] == 'TRIO':
            if 'upload_vcf' in config and config['upload_vcf'] in uploaded_files:
                config['upload_vcf'] = uploaded_files[config['upload_vcf']]
            if 'upload_father' in config and config['upload_father'] in uploaded_files:
                config['upload_father'] = uploaded_files[config['upload_father']]
            if 'upload_mother' in config and config['upload_mother'] in uploaded_files:
                config['upload_mother'] = uploaded_files[config['upload_mother']]
        elif config['vcf_mode'] == 'SNP':
            if 'upload_vcf' in config and config['upload_vcf'] in uploaded_files:
                config['upload_vcf'] = uploaded_files[config['upload_vcf']]
        
        # Simulate task creation
        submission_id = f"sim_{config['title'].replace('_', '')[:8]}"
        created_tasks.append({
            'title': config['title'],
            'submission_id': submission_id,
            'vcf_mode': config['vcf_mode']
        })
        print(f"🔬 Would create task: {config['title']} → {submission_id}")
    
    # Save simulation results
    simulation_results = {
        'uploaded_files': uploaded_files,
        'created_tasks': created_tasks
    }
    
    with open('simulation_results.json', 'w') as f:
        json.dump(simulation_results, f, indent=2)
    
    print(f"\n📄 Simulation results saved to: simulation_results.json")
    print(f"✅ Would upload {len(uploaded_files)} files")
    print(f"✅ Would create {len(created_tasks)} tasks")

if __name__ == "__main__":
    print("🧬 Virtual Geneticist Batch Processing Test")
    print("=" * 60)
    
    # Test CSV processing
    if test_csv_processing():
        # Run simulation
        simulate_batch_process()
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n❌ Tests failed. Please check the CSV file format.") 