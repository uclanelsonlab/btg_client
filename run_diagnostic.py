#!/usr/bin/env python3
"""
Run diagnostic upload to test connectivity and identify issues.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Run diagnostic upload."""
    if len(sys.argv) != 4:
        print("Usage: python run_diagnostic.py <token_file> <file_path> <prefix>")
        print("Example: python run_diagnostic.py token.txt file.vcf.gz UDN080299-P")
        sys.exit(1)
    
    token_file = sys.argv[1]
    file_path = sys.argv[2]
    prefix = sys.argv[3]
    
    # Check if files exist
    if not os.path.exists(token_file):
        print(f"❌ Token file not found: {token_file}")
        sys.exit(1)
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    print("🔍 Running Diagnostic Upload Test")
    print("=" * 50)
    
    try:
        from btg_upload_module_diagnostic import run_upload_module_diagnostic
        run_upload_module_diagnostic(token_file, file_path, prefix)
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