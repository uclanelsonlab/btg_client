# BTG Virtual Geneticist API Client

A modular Python client for interacting with the BT Genomics Virtual Geneticist API. This tool provides a comprehensive interface for uploading VCF files, creating genetic analysis tasks, and monitoring task status.

## 🧬 Features

- **File Upload**: Upload VCF files and other genetic data files to the Virtual Geneticist platform
- **Task Creation**: Create genetic analysis tasks with configurable parameters
- **Status Monitoring**: Check the status of submitted tasks and retrieve results
- **Interactive Mode**: User-friendly menu-driven interface
- **Command Line Interface**: Direct module execution with command-line arguments
- **Modular Design**: Separate modules for different functionalities

## 📋 Prerequisites

- Python 3.6 or higher
- `requests` library
- Valid API token from BT Genomics Virtual Geneticist platform

## 🚀 Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install requests
```

3. Place your API token in a text file (e.g., `token.txt`)

## 📁 Project Structure

```
btg_client/
├── btg_main.py              # Main application entry point
├── btg_upload_module.py     # File upload functionality
├── btg_task_module.py       # Task creation and management
├── btg_status_module.py     # Status checking and monitoring
├── task_config.json         # Default task configuration
├── token.txt               # API token file (create this)
├── vcf_files/              # Sample VCF files directory
│   ├── sample-M_trim_biallelic.vcf.gz
│   ├── sample-MGF_trim_biallelic.vcf.gz
│   ├── sample-MG_trim_biallelic.vcf.gz
│   └── sample-P_trim_biallelic.vcf.gz
└── README.md               # This file
```

## 🎯 Usage

### Interactive Mode (Recommended)

Run the client in interactive mode for a user-friendly experience:

```bash
python btg_main.py --token token.txt
```

This will present a menu with the following options:
1. 📤 Upload File
2. 🔬 Create Analysis Task
3. 📊 Check Task Status
4. ⚙️ Show Current Configuration
5. 🚪 Exit

### Command Line Mode

You can also run specific modules directly:

#### Upload Files

```bash
# Basic upload
python btg_main.py upload --token token.txt

# Upload with specific file and prefix
python btg_main.py upload --token token.txt --file-path /path/to/file.vcf.gz --prefix UDN287643-P
```

#### Create Analysis Tasks

```bash
# Use default configuration
python btg_main.py task --token token.txt

# Use custom configuration file
python btg_main.py task --token token.txt --task-config custom_config.json
```

#### Check Task Status

```bash
python btg_main.py status --token token.txt --submission-id b48e943c42659c5011fa571d80d0e177
```

#### Show Configuration

```bash
python btg_main.py config --token token.txt
```

## ⚙️ Configuration

### Task Configuration

The `task_config.json` file contains default parameters for genetic analysis tasks:

```json
{
  "title": "sample_cohort_test",
  "project": "samples",
  "vcf_mode": "TRIO",
  "assembly": "hg38",
  "upload_vcf": "sample-P/sample-M_trim_biallelic.vcf.gz",
  "clinical_info": "Clinical description...",
  "upload_father": "sample-P/sample-MGF_trim_biallelic.vcf.gz",
  "upload_mother": "sample-P/sample-MG_trim_biallelic.vcf.gz"
}
```

### Supported File Types

The upload module supports the following file formats:
- `.vcf` - Variant Call Format files
- `.vcf.gz` - Compressed VCF files
- `.pdf` - PDF documents
- `.txt` - Text files

## 📊 API Endpoints

The client interacts with the following BT Genomics Virtual Geneticist API endpoints:

- **Base URL**: `https://vg-api.btgenomics.com:8082/api`
- **Upload**: `/upload` - File upload endpoint
- **Tasks**: `/tasks` - Task creation and management
- **Status**: `/status/{submission_id}` - Status checking

## 🔧 Module Details

### Upload Module (`btg_upload_module.py`)
- Handles file validation and upload
- Supports prefix-based file organization
- Provides detailed upload status and error handling

### Task Module (`btg_task_module.py`)
- Creates genetic analysis tasks
- Configurable via JSON configuration files
- Supports trio analysis and other genetic analysis modes

### Status Module (`btg_status_module.py`)
- Monitors task progress and status
- Retrieves analysis results
- Provides detailed status information

## 🛠️ Troubleshooting

### Common Issues

1. **Token File Not Found**
   - Ensure your token file exists and is readable
   - Check the file path is correct

2. **File Upload Failures**
   - Verify the file exists and is accessible
   - Check file format is supported
   - Ensure sufficient permissions

3. **Network Errors**
   - Check internet connectivity
   - Verify API endpoint accessibility
   - Ensure firewall settings allow HTTPS connections

### Error Messages

- `❌ Token file not found`: Check token file path
- `❌ Unsupported file type`: Verify file format is supported
- `❌ Upload failed`: Check API response for specific error details
- `❌ Network error`: Verify connectivity and API availability

## 📝 Examples

### Complete Workflow Example

1. **Upload VCF files**:
   ```bash
   python btg_main.py upload --token token.txt --file-path vcf_files/sample-M_trim_biallelic.vcf.gz --prefix sample-P
   ```

2. **Create analysis task**:
   ```bash
   python btg_main.py task --token token.txt
   ```

3. **Monitor task status**:
   ```bash
   python btg_main.py status --token token.txt --submission-id <submission_id>
   ```

## 🤝 Contributing

This is a client application for the BT Genomics Virtual Geneticist API. For issues related to the API itself, please contact BT Genomics support.

## 📄 License

This project is provided as-is for use with the BT Genomics Virtual Geneticist platform.

## 🔗 Related Documentation

- [Virtual Geneticist Task API Documentation](Virtual%20Geneticist%20Task%20API%20Documentation.html)
- BT Genomics Virtual Geneticist Platform Documentation

---

**Note**: This client requires a valid API token from BT Genomics. Please ensure you have proper authorization before using this tool.
