# Release Notes - v1.3.0

## Overview

Version 1.3.0 focuses on **simplification and reliability improvements** by rolling back to the proven v1.0.0 upload approach and removing unnecessary complexity.

## Key Changes

### 🔄 **Simplified Upload Process**
- **Rolled back to v1.0.0-style uploads**: Removed timeouts and retry logic that were causing issues
- **Removed progress bars**: Eliminated progress tracking that was interfering with upload reliability
- **Streamlined code**: Simplified upload modules for better stability

### 🏷️ **Removed Timestamp from Project Names**
- **Exact CSV titles**: Task titles now use the exact values from your CSV file
- **No automatic suffixes**: No more timestamp additions to project names
- **User control**: You have full control over task titles in your CSV

### 🧹 **Streamlined Batch Processing**
- **Single batch module**: Consolidated batch operations into one `batch-full` module
- **Removed redundant functions**: Eliminated separate upload and task creation batch modules
- **Cleaner CLI**: Simplified command-line interface with fewer options

### 🔧 **Fixed Import Issues**
- **Module compatibility**: Fixed import errors between main client and batch module
- **Updated dependencies**: Corrected function imports to match available modules
- **Better error handling**: Improved error messages for missing functions

## Breaking Changes

⚠️ **Important**: This version removes some previously available functions:

- `run_batch_upload_module` - No longer available
- `run_batch_task_module` - No longer available
- `batch-upload` CLI option - Removed
- `batch-task` CLI option - Removed
- Progress bars - Disabled

## Migration Guide

### For Existing Users

1. **Update your scripts**: If you were using `batch-upload` or `batch-task`, switch to `batch-full`
2. **Check your CSV files**: Ensure unique titles in your CSV since timestamps are no longer added automatically
3. **Update imports**: If importing functions directly, remove references to deleted functions

### CLI Changes

**Before (v1.2.0):**
```bash
python btg_client.py batch-upload --token token.txt --csv-file samples.csv
python btg_client.py batch-task --token token.txt --csv-file samples.csv
```

**After (v1.3.0):**
```bash
python btg_client.py batch-full --token token.txt --csv-file samples.csv
```

## What's New

### ✅ **Improved Reliability**
- Uploads are now more reliable with the simplified v1.0.0 approach
- No more timeout issues with large files
- Better error handling and reporting

### ✅ **Cleaner Interface**
- Simplified menu options in interactive mode
- Fewer CLI options to choose from
- More intuitive workflow

### ✅ **Better Control**
- Full control over task titles via CSV
- No automatic modifications to your data
- Predictable behavior

## Known Issues

None at this time.

## Support

For issues or questions about this release, please:
1. Check the documentation in the `docs/` directory
2. Review the CHANGELOG.md for detailed change history
3. Contact support if you need assistance with migration

---

**Release Date**: January 16, 2025  
**Version**: 1.3.0  
**Compatibility**: Python 3.6+ 