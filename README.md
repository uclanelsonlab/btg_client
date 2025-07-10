# BTG Virtual Geneticist API Client

A modular Python client for interacting with the BT Genomics Virtual Geneticist API. This tool provides a comprehensive interface for uploading VCF files, creating genetic analysis tasks, and monitoring task status.

## 🧬 Features

- **File Upload**: Upload VCF files and other genetic data files to the Virtual Geneticist platform
- **Task Creation**: Create genetic analysis tasks with configurable parameters
- **Status Monitoring**: Check the status of submitted tasks and retrieve results
- **Batch Processing**: Process multiple files and create tasks from CSV files
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
├── btg_batch_module.py      # Batch processing functionality
├── task_config.json         # Default task configuration
├── token.txt               # API token file (create this)
├── data/                   # Sample data directory
│   └── samplesheet.csv     # Sample CSV file for batch processing
├── vcf_files/              # Sample VCF files directory
│   ├── sample-M_trim_biallelic.vcf.gz
│   ├── sample-MGF_trim_biallelic.vcf.gz
│   ├── sample-MG_trim_biallelic.vcf.gz
│   └── sample-P_trim_biallelic.vcf.gz
├── BATCH_USAGE.md          # Batch processing documentation
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
4. 🚀 Batch Upload Files
5. 🔬 Batch Create Tasks
6. 🚀 Full Batch Process (Upload + Tasks)
7. ⚙️ Show Current Configuration
8. 🚪 Exit

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

#### Batch Processing

```bash
# Batch upload files from CSV
python btg_main.py batch-upload --token token.txt --csv-file samples.csv --data-directory /path/to/vcfs

# Batch create tasks from CSV (after upload)
python btg_main.py batch-task --token token.txt --csv-file samples.csv

# Full batch process (upload + create tasks)
python btg_main.py batch-full --token token.txt --csv-file samples.csv --data-directory /path/to/vcfs
```

#### Show Configuration

```bash
python btg_main.py config --token token.txt
```

## ⚙️ Configuration

### Task Configuration

The `task_config.json` file contains parameters for genetic analysis tasks. Here's a comprehensive guide to all available options:

#### Required Fields

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `title` | string | Name of the analysis task | Max 256 characters |
| `project` | string | Project identifier | Max 256 characters |
| `vcf_mode` | string | Analysis mode | Must be: `SNP`, `TRIO`, or `CARRIER` |
| `assembly` | string | Genome assembly version | Must be: `hg19` or `hg38` |

#### VCF Mode-Specific Requirements

**SNP Mode (Proband Analysis):**
- Requires: `upload_vcf` (proband VCF file)
- Optional: `upload_father`, `upload_mother`

**TRIO Mode (Family Trio Analysis):**
- Requires: `upload_vcf` (proband), `upload_father`, `upload_mother`
- All three VCF files must be provided

**CARRIER Mode (Carrier Analysis):**
- Requires: `upload_father`, `upload_mother`
- Optional: `upload_vcf` (proband)

#### Clinical Information (Choose One)

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `clinical_info` | string | Clinical description text | Max 4096 characters |
| `upload_clinical` | string | Path to clinical file | File must exist |

#### File Path Fields

| Field | Type | Description | Required For |
|-------|------|-------------|--------------|
| `upload_vcf` | string | Path to proband VCF file | SNP, TRIO modes |
| `upload_father` | string | Path to father's VCF file | TRIO, CARRIER modes |
| `upload_mother` | string | Path to mother's VCF file | TRIO, CARRIER modes |
| `upload_cnv` | string | Path to CNV file | Optional for all modes |

#### Example Configurations

**TRIO Analysis Example:**
```json
{
  "title": "sample_cohort_test",
  "project": "samples",
  "vcf_mode": "TRIO",
  "assembly": "hg38",
  "upload_vcf": "sample-P/sample-M_trim_biallelic.vcf.gz",
  "clinical_info": "Sample clinical description for demonstration purposes. Replace with actual clinical information.",
  "upload_father": "sample-P/sample-MGF_trim_biallelic.vcf.gz",
  "upload_mother": "sample-P/sample-MG_trim_biallelic.vcf.gz"
}
```

**SNP Analysis Example:**
```json
{
  "title": "proband_analysis",
  "project": "research_study",
  "vcf_mode": "SNP",
  "assembly": "hg38",
  "upload_vcf": "data/proband.vcf.gz",
  "clinical_info": "Patient presents with developmental delay and seizures. Family history of similar conditions.",
  "upload_cnv": "data/cnv_data.txt"
}
```

**CARRIER Analysis Example:**
```json
{
  "title": "carrier_screening",
  "project": "family_study",
  "vcf_mode": "CARRIER",
  "assembly": "hg19",
  "upload_father": "data/father.vcf.gz",
  "upload_mother": "data/mother.vcf.gz",
  "upload_clinical": "data/clinical_summary.pdf"
}
```

#### Field Validation Rules

The configuration system validates the following:

1. **Required Fields**: All required fields must be present and non-empty
2. **VCF Mode Validation**: File requirements are enforced based on the selected mode
3. **Clinical Information**: Either `clinical_info` or `upload_clinical` must be provided
4. **Field Length Limits**: Title (256 chars), project (256 chars), clinical_info (4096 chars)
5. **Valid Values**: vcf_mode and assembly must match allowed values

#### Error Messages

Common validation errors and their solutions:

- `Missing required field: title` → Add a title for your analysis
- `Invalid vcf_mode: INVALID` → Use one of: SNP, TRIO, CARRIER
- `Invalid assembly: hg20` → Use one of: hg19, hg38
- `upload_vcf is required for TRIO mode` → Provide proband VCF file path
- `Either upload_clinical or clinical_info is required` → Add clinical information
- `title must be 256 characters or less` → Shorten the title

#### Configuration Tips

1. **File Paths**: Use relative paths from your upload directory or absolute paths
2. **Clinical Information**: For detailed cases, use `upload_clinical` with a PDF file
3. **Project Names**: Use consistent project names for related analyses
4. **Assembly Version**: Ensure all VCF files use the same assembly version
5. **File Formats**: VCF files should be compressed (.vcf.gz) for faster uploads

### Supported File Types

The upload module supports the following file formats:
- `.vcf` - Variant Call Format files
- `.vcf.gz` - Compressed VCF files
- `.pdf` - PDF documents
- `.txt` - Text files

### Configuration Reference

For quick reference, here's a complete list of all configuration fields:

#### Core Fields
- `title` (required): Analysis task name
- `project` (required): Project identifier
- `vcf_mode` (required): Analysis mode (SNP/TRIO/CARRIER)
- `assembly` (required): Genome assembly (hg19/hg38)

#### VCF File Fields
- `upload_vcf`: Proband VCF file path
- `upload_father`: Father's VCF file path
- `upload_mother`: Mother's VCF file path
- `upload_cnv`: CNV file path (optional)

#### Clinical Information Fields
- `clinical_info`: Clinical description text
- `upload_clinical`: Clinical file path

#### Field Dependencies by Mode

| Mode | Required Files | Optional Files |
|------|----------------|----------------|
| SNP | `upload_vcf` | `upload_father`, `upload_mother`, `upload_cnv` |
| TRIO | `upload_vcf`, `upload_father`, `upload_mother` | `upload_cnv` |
| CARRIER | `upload_father`, `upload_mother` | `upload_vcf`, `upload_cnv` |

## 🚀 Batch Processing

The batch processing functionality allows you to process multiple files and create tasks from CSV files. This is especially useful for handling large datasets with family trios or multiple individual samples.

### CSV File Format

Your CSV file must contain the following columns:

| Column | Description | Required |
|--------|-------------|----------|
| `samples` | Sample identifier | Yes |
| `title` | Task title for this sample | Yes |
| `project` | Project name | Yes |
| `vcf_mode` | Analysis mode: `TRIO` or `SNP` | Yes |
| `assembly` | Genome assembly: `hg19` or `hg38` | Yes |
| `upload_vcf` | Proband VCF file name | Yes |
| `upload_father` | Father VCF file name (TRIO mode) or `NA` (SNP mode) | Yes |
| `upload_mother` | Mother VCF file name (TRIO mode) or `NA` (SNP mode) | Yes |
| `clinical_info` | Clinical information (optional) | No |

### Example CSV Structure

```csv
samples,title,project,vcf_mode,assembly,upload_vcf,upload_father,upload_mother,clinical_info
sample01,sample01_cohort,UDN,TRIO,hg38,sample01_trim_biallelic.vcf.gz,sample02_trim_biallelic.vcf.gz,sample03_trim_biallelic.vcf.gz,Decreased response to growth hormone stimulation test
sample04,sample04_cohort,UDN,SNP,hg38,sample04.vcf.gz,NA,NA,Small scrotum; Abnormal pinna morphology
```

### How Batch Processing Works

#### TRIO Mode Processing
- Each row represents one complete TRIO analysis
- `upload_vcf` → Proband VCF file
- `upload_father` → Father VCF file (if not `NA`)
- `upload_mother` → Mother VCF file (if not `NA`)
- One task is created per row with available family files

#### SNP Mode Processing
- Each row represents one SNP analysis
- `upload_vcf` → Proband VCF file
- One task per row (father/mother files are `NA`)

### Output Files

The batch process creates several output files:

- `upload_results.json`: Mapping of original filenames to remote paths
- `task_results.json`: Created task information
- `batch_results.json`: Complete results from full batch process

For detailed batch processing documentation, see [BATCH_USAGE.md](BATCH_USAGE.md).

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

### Batch Module (`btg_batch_module.py`)
- Processes CSV files for bulk operations
- Handles file uploads and task creation in batches
- Groups samples by family relationships for TRIO analysis
- Provides comprehensive error handling and reporting

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
