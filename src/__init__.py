"""
BTG Virtual Geneticist API Client Package
"""

__version__ = "1.3.0"
__author__ = "BT Genomics"
__email__ = "support@btgenomics.com"

# Import main modules for easy access
from .btg_main import main
from .btg_upload_module import upload_file, run_upload_module
from .btg_task_module import create_task, run_create_task_module
from .btg_status_module import check_status, run_status_check_module
from .btg_batch_module import run_batch_full_module

__all__ = [
    "main",
    "upload_file",
    "run_upload_module",
    "create_task", 
    "run_create_task_module",
    "check_status",
    "run_status_check_module",
    "run_batch_full_module"
] 