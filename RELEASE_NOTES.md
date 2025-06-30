# Release Notes - BTG Virtual Geneticist API Client v1.0.0

## 🎉 Initial Release

This is the first official release of the BTG Virtual Geneticist API Client, a comprehensive Python tool for interacting with the BT Genomics Virtual Geneticist platform.

## ✨ Features

### Core Functionality
- **File Upload Module**: Upload VCF files and other genetic data files to the Virtual Geneticist platform
- **Task Creation Module**: Create genetic analysis tasks with configurable parameters
- **Status Monitoring Module**: Check the status of submitted tasks and retrieve results

### User Interface
- **Interactive Mode**: User-friendly menu-driven interface
- **Command Line Interface**: Direct module execution with command-line arguments
- **Modular Design**: Separate modules for different functionalities

### Analysis Modes
- **SNP Mode**: Proband-only analysis
- **TRIO Mode**: Family trio analysis (proband + parents)
- **CARRIER Mode**: Carrier analysis (parents only)

## 🔧 Technical Details

### Supported File Types
- `.vcf` - Variant Call Format files
- `.vcf.gz` - Compressed VCF files
- `.pdf` - PDF documents
- `.txt` - Text files

### Genome Assemblies
- `hg19` - Human Genome Build 19
- `hg38` - Human Genome Build 38

### API Endpoints
- **Base URL**: `https://vg-api.btgenomics.com:8082/api`
- **Upload**: `/upload` - File upload endpoint
- **Tasks**: `/tasks` - Task creation and management
- **Status**: `/status/{submission_id}` - Status checking

## 📋 Configuration Options

### Required Fields
- `title`: Analysis task name (max 256 characters)
- `project`: Project identifier (max 256 characters)
- `vcf_mode`: Analysis mode (SNP/TRIO/CARRIER)
- `assembly`: Genome assembly (hg19/hg38)

### VCF File Fields
- `upload_vcf`: Proband VCF file path
- `upload_father`: Father's VCF file path
- `upload_mother`: Mother's VCF file path
- `upload_cnv`: CNV file path (optional)

### Clinical Information
- `clinical_info`: Clinical description text (max 4096 characters)
- `upload_clinical`: Clinical file path

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- Valid API token from BT Genomics Virtual Geneticist platform

### Quick Start
```bash
# Clone the repository
git clone https://github.com/uclanelsonlab/btg_client.git
cd btg_client

# Install dependencies
pip install requests

# Set up your API token
echo "your_api_token_here" > token.txt

# Run in interactive mode
python btg_main.py --token token.txt
```

## 📖 Usage Examples

### Upload Files
```bash
python btg_main.py upload --token token.txt --file-path /path/to/file.vcf.gz --prefix sample-P
```

### Create Analysis Task
```bash
python btg_main.py task --token token.txt --task-config task_config.json
```

### Check Task Status
```bash
python btg_main.py status --token token.txt --submission-id <submission_id>
```

## 🔒 Security Features

- **Token Management**: Secure token file handling with proper permissions
- **File Validation**: Comprehensive file type and format validation
- **Error Handling**: Detailed error messages and validation feedback
- **Input Sanitization**: Protection against invalid configuration data

## 🛠️ Error Handling

The client provides comprehensive error handling for:
- Network connectivity issues
- API authentication failures
- File validation errors
- Configuration validation errors
- Invalid analysis mode combinations

## 📚 Documentation

- **README.md**: Comprehensive user guide with examples
- **Configuration Guide**: Detailed task_config.json documentation
- **API Documentation**: Complete endpoint and parameter reference
- **Troubleshooting**: Common issues and solutions

## 🔄 Version History

### v1.0.0 (Initial Release)
- Initial implementation of all core modules
- Interactive and command-line interfaces
- Comprehensive configuration system
- Complete documentation suite
- Error handling and validation
- Support for all analysis modes

## 🤝 Contributing

This is the initial release of the BTG Virtual Geneticist API Client. For issues related to the API itself, please contact BT Genomics support.

## 📄 License

This project is provided as-is for use with the BT Genomics Virtual Geneticist platform.

---

**Release Date**: June 30, 2025  
**Version**: 1.0.0  
**Compatibility**: Python 3.6+  
**Platform**: Cross-platform (Windows, macOS, Linux) 