#!/usr/bin/env python3
"""
BTG Virtual Geneticist API Client
Main entry point for the client application.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the main function from the src module
from btg_main import main

if __name__ == "__main__":
    main() 