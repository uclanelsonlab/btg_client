#!/usr/bin/env python3
"""
Simple Batch Upload Script (No Progress Bar)
Run this to test batch upload without progress bars.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Run simple batch upload."""
    if len(sys.argv) != 3:
        print("Usage: python run_simple_batch.py <token_file> <csv_file>")
        print("Example: python run_simple_batch.py token.txt batch.csv")
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
    
    print("🚀 Starting Simple Batch Upload (No Progress Bar)")
    print("=" * 60)
    
    try:
        from btg_batch_module_simple import run_batch_full_simple_module
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