#!/usr/bin/env python3
"""
Run ultra-reliable batch upload with very long timeouts.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Run ultra-reliable batch upload."""
    if len(sys.argv) != 3:
        print("Usage: python run_ultra_batch.py <token_file> <csv_file>")
        print("Example: python run_ultra_batch.py token.txt data/samplesheet.csv")
        sys.exit(1)
    
    token_file = sys.argv[1]
    csv_file = sys.argv[2]
    
    # Check if files exist
    if not os.path.exists(token_file):
        print(f"❌ Token file not found: {token_file}")
        sys.exit(1)
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        sys.exit(1)
    
    print("🚀 Starting Ultra-Reliable Batch Upload")
    print("=" * 50)
    
    try:
        # Import and run the ultra batch module
        from btg_batch_module_simple import run_batch_full_simple_module
        
        # Override the upload function to use ultra timeouts
        import btg_upload_module_ultra
        import btg_batch_module_simple
        
        # Replace the upload function in batch module
        btg_batch_module_simple.upload_file_simple_batch = btg_upload_module_ultra.upload_file_ultra
        
        run_batch_full_simple_module(token_file, csv_file)
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the project root directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 