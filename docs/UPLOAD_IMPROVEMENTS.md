# Upload Improvements for Large Files

## Problem
Users were experiencing timeout errors when uploading large VCF files (160-168MB). The files would upload successfully (100% progress) but then timeout during the final processing phase with errors like:

```
❌ Network error: HTTPSConnectionPool(host='vg-api.btgenomics.com', port=8082): Max retries exceeded with url: /api/upload (Caused by ConnectTimeoutError(...))
```

## Solution
Implemented comprehensive timeout and retry logic for handling large file uploads:

### 1. Dynamic Timeout Configuration
- **Small files (<100MB)**: 30s connect, 5min read timeout
- **Large files (>100MB)**: 30s connect, 10min read timeout, 15min upload timeout

### 2. Automatic Retry Logic
- **Max retries**: 3 attempts
- **Backoff strategy**: Exponential backoff (2^attempt seconds)
- **Retryable errors**: 500, 502, 503, 504, 408, 429 status codes
- **Non-retryable**: Client errors (4xx status codes)

### 3. Session-Based Requests
- Uses `requests.Session()` with retry adapter
- Consistent timeout handling across all requests
- Better connection pooling

### 4. Improved Error Handling
- Specific timeout error messages with attempt numbers
- Wait time display between retries
- Graceful handling of different error types

## Files Modified

### `src/btg_upload_module.py`
- Added timeout configuration constants
- Added `create_session_with_retries()` function
- Updated `upload_file()` with retry logic and dynamic timeouts
- Enhanced error handling with attempt tracking

### `src/btg_batch_module.py`
- Updated `upload_file_batch()` to use improved session
- Updated `create_task_batch()` with retry logic
- Added timeout configuration for task creation

## Usage
The improvements are automatically applied to all upload operations:

```bash
# Single file upload
python btg_client.py upload --token token.txt --file large_file.vcf.gz

# Batch upload
python btg_client.py batch-full --token token.txt --csv-file batch.csv
```

## Testing
Run the test script to verify improvements:

```bash
python tests/test_improved_upload.py
```

## Expected Behavior
- Large files (>100MB) will have extended timeouts
- Network timeouts will trigger automatic retries
- Progress bars will show upload progress
- Clear error messages with retry attempts
- Successful uploads will complete even with network instability

## Configuration
Timeout values can be adjusted in `src/btg_upload_module.py`:

```python
CONNECT_TIMEOUT = 30  # seconds to establish connection
READ_TIMEOUT = 600    # seconds for read operations (10 minutes)
UPLOAD_TIMEOUT = 900  # seconds for complete upload (15 minutes)
MAX_RETRIES = 3       # number of retry attempts
``` 