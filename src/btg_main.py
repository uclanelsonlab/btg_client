#!/usr/bin/env python3
"""
Virtual Geneticist API Client - Main Script
A modular client for uploading files, creating tasks, and checking status.
"""

import sys
import json
import argparse

# Import the individual modules
try:
    from btg_upload_module import run_upload_module
    from btg_task_module import run_create_task_module
    from btg_status_module import run_status_check_module
    from btg_batch_module import run_batch_full_module
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure all module files are in the same directory:")
    print("  - btg_upload_module.py")
    print("  - btg_task_module.py") 
    print("  - btg_status_module.py")
    print("  - btg_batch_module.py")
    sys.exit(1)

def print_banner():
    """Print the application banner."""
    print("\n" + "="*70)
    print("🧬 VIRTUAL GENETICIST API CLIENT")
    print("="*70)
    print("A modular client for uploading files, creating tasks, and checking status")
    print("="*70)

def show_configuration():
    """Show current configuration settings."""
    print("\n" + "="*60)
    print("⚙️  CURRENT CONFIGURATION")
    print("="*60)
    print("📋 Task module uses external JSON configuration file")
    print("📤 Upload module accepts file_path and prefix parameters")
    print("📊 Status module accepts submission_id parameter")
    print("🚀 Batch module processes CSV files for full batch operations (upload + tasks)")

def interactive_mode(token_file_path=None):
    """Run the client in interactive mode with menu."""
    print_banner()
    
    # If no token file provided, ask for it
    if not token_file_path:
        token_file_path = input("Enter token file path: ").strip()
        if not token_file_path:
            print("❌ Token file path is required")
            return
    
    while True:
        print("\n📋 MAIN MENU")
        print("-" * 30)
        print("1. 📤 Upload File")
        print("2. 🔬 Create Analysis Task")
        print("3. 📊 Check Task Status")
        print("4. 🚀 Full Batch Process (Upload + Tasks)")
        print("5. ⚙️  Show Current Configuration")
        print("6. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            run_upload_module(token_file_path, show_progress=not args.no_progress)
        elif choice == "2":
            submission_id = run_create_task_module(token_file_path)
            if submission_id:
                print(f"✅ New submission ID saved: {submission_id}")
        elif choice == "3":
            run_status_check_module(token_file_path)
        elif choice == "4":
            csv_file = input("Enter CSV file path: ").strip()
            run_batch_full_module(token_file_path, csv_file)
        elif choice == "5":
            show_configuration()
        elif choice == "6":
            print("\n👋 Thank you for using the Virtual Geneticist API Client!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 6.")
        
        input("\nPress Enter to continue...")

def main():
    """Main function with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Virtual Geneticist API Client - Modular interface for uploading files, creating tasks, and checking status",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python btg_client.py upload --token token.txt                                                       # Run upload module
  python btg_client.py upload --token token.txt --file-path /path/to/file.vcf.gz --prefix sample-P    # Upload with parameters
  python btg_client.py task   --token token.txt --task-config task_config.json                        # Run task creation module
  python btg_client.py status --token token.txt --submission-id b48e943c42659c5011fa571d80d0e177      # Run status checking module
  python btg_client.py batch-full --token token.txt --csv-file samples.csv                            # Full batch process
  python btg_client.py config --token token.txt                                                       # Show current configuration
  python btg_client.py --token token.txt --interactive                                                # Run in interactive mode
  python btg_client.py --token token.txt                                                              # Run in interactive mode (default)
        """
    )
    
    parser.add_argument(
        '--token', '-t',
        required=True,
        help='Path to the token file containing the API token'
    )
    
    parser.add_argument(
        '--file-path', '-f',
        help='Path to the file to upload (for upload module)'
    )
    
    parser.add_argument(
        '--prefix', '-p',
        help='Prefix for file organization (for upload module)'
    )
    
    parser.add_argument(
        '--task-config', '-c',
        help='Path to the task configuration JSON file (for task module)'
    )
    
    parser.add_argument(
        '--submission-id', '-s',
        help='Submission ID to check status for (for status module)'
    )
    
    parser.add_argument(
        '--csv-file', '-csv',
        help='Path to the CSV file (for batch modules)'
    )
    

    
    parser.add_argument(
        '--no-progress', '-np',
        action='store_true',
        help='Disable progress bars for uploads'
    )
    
    parser.add_argument(
        'module',
        nargs='?',
        choices=['upload', 'task', 'status', 'config', 'batch-full'],
        help='Module to run: upload, task, status, config, or batch-full'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode with menu'
    )
    
    args = parser.parse_args()
    
    # If no module specified or interactive flag used, run interactive mode
    if not args.module or args.interactive:
        interactive_mode(args.token)
        return
    
    # Run the specified module
    print_banner()
    
    if args.module == 'upload':
        run_upload_module(args.token, args.file_path, args.prefix, show_progress=not args.no_progress)
    elif args.module == 'task':
        submission_id = run_create_task_module(args.token, args.task_config)
        if submission_id:
            print(f"✅ New submission ID saved: {submission_id}")
    elif args.module == 'status':
        run_status_check_module(args.token, args.submission_id)
    elif args.module == 'batch-full':
        if not args.csv_file:
            print("❌ CSV file path is required for batch full process. Use --csv-file option.")
            return
        run_batch_full_module(args.token, args.csv_file)
    elif args.module == 'config':
        show_configuration()

if __name__ == "__main__":
    main() 