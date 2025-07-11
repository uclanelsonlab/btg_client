# Batch Processing Guide

This guide explains how to use the batch processing functionality for uploading files and creating tasks from CSV files.

## Overview

The batch processing module allows you to:
- Upload multiple VCF files from a CSV file
- Create analysis tasks for TRIO and SNP modes
- Process files in groups based on their relationships

## CSV File Format

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
UDN734331,UDN734331_cohort,UDN,TRIO,hg38,UDN734331-41_trim_biallelic.vcf.gz,UDN582748-112_trim_biallelic.vcf.gz,UDN793879-111_trim_biallelic.vcf.gz,Decreased response to growth hormone stimulation test
UDN282881,UDN282881_cohort,UDN,SNP,hg38,UDN282881-196.vcf.gz,NA,NA,Small scrotum; Abnormal pinna morphology
```

## Usage Modes

### 1. Batch Upload Only

Upload all files from the CSV without creating tasks:

```bash
python btg_main.py batch-upload --token token.txt --csv-file samples.csv --data-directory /path/to/vcfs
```

### 2. Batch Task Creation Only

Create tasks using previously uploaded files:

```bash
python btg_main.py batch-task --token token.txt --csv-file samples.csv
```

### 3. Full Batch Process

Upload files and create tasks in one operation:

```bash
python btg_main.py batch-full --token token.txt --csv-file samples.csv --data-directory /path/to/vcfs
```

### 4. Interactive Mode

Run the interactive menu and select batch options:

```bash
python btg_main.py --token token.txt --interactive
```

## How It Works

### TRIO Mode Processing

For `vcf_mode = "TRIO"`:

1. **Individual Processing**: Each row represents one complete TRIO analysis
2. **File Assignment**: 
   - `upload_vcf` → Proband VCF file
   - `upload_father` → Father VCF file (if not `NA`)
   - `upload_mother` → Mother VCF file (if not `NA`)
3. **Task Creation**: One task is created per row with available family files

### SNP Mode Processing

For `vcf_mode = "SNP"`:

1. **Individual Processing**: Each row represents one SNP analysis
2. **File Assignment**: `upload_vcf` → Proband VCF file
3. **Task Creation**: One task per row (father/mother files are `NA`)

## File Organization

### Upload Structure

Files are uploaded with the `title` as the prefix:
- `UDN734331_cohort/UDN734331-41.vcf.gz`
- `UDN734331_cohort/UDN793879-111.vcf.gz`
- `UDN734331_cohort/UDN582748-112.vcf.gz`

### Data Directory

If you specify a `--data-directory`, the script will look for VCF files in that directory:

```
/path/to/vcfs/
├── UDN734331-41.vcf.gz
├── UDN793879-111.vcf.gz
├── UDN582748-112.vcf.gz
└── UDN282881-196.vcf.gz
```

## Output Files

The batch process creates several output files:

### `upload_results.json`
Contains mapping of original filenames to remote paths:
```json
{
  "UDN734331-41_trim_biallelic.vcf.gz": "UDN734331_cohort/UDN734331-41_trim_biallelic.vcf.gz",
  "UDN582748-112_trim_biallelic.vcf.gz": "UDN734331_cohort/UDN582748-112_trim_biallelic.vcf.gz",
  "UDN793879-111_trim_biallelic.vcf.gz": "UDN734331_cohort/UDN793879-111_trim_biallelic.vcf.gz"
}
```

### `task_results.json`
Contains created task information:
```json
[
  {
    "title": "UDN734331_cohort",
    "submission_id": "b48e943c42659c5011fa571d80d0e177",
    "vcf_mode": "TRIO"
  }
]
```

### `batch_results.json`
Complete results from full batch process:
```json
{
  "uploaded_files": { ... },
  "created_tasks": [ ... ]
}
```

## Error Handling

The batch process includes comprehensive error handling:

- **Missing Files**: Files not found in the data directory are skipped
- **Upload Failures**: Failed uploads are reported but don't stop the process
- **Task Creation Failures**: Failed task creations are reported but don't stop the process
- **Missing Dependencies**: TRIO tasks with missing files are skipped

## Validation

The CSV file is validated for:
- Required columns presence
- Valid `vcf_mode` values (`TRIO`, `SNP`)
- Valid `assembly` values (`hg19`, `hg38`)
- Valid `vcf_type` values (`proband`, `father`, `mother`)

## Tips

1. **Test with Small Files**: Start with a small CSV to test the process
2. **Check File Paths**: Ensure all VCF files exist in the data directory
3. **Review Results**: Check the output JSON files for detailed results
4. **Use Interactive Mode**: For first-time users, interactive mode provides guidance
5. **Backup Data**: Always backup your CSV and VCF files before processing

## Troubleshooting

### Common Issues

1. **"File not found" errors**
   - Check that the data directory path is correct
   - Verify VCF files exist in the specified directory

2. **"Missing required column" errors**
   - Ensure your CSV has all required columns
   - Check column names match exactly (case-sensitive)

3. **"Upload failed" errors**
   - Check your API token is valid
   - Verify network connectivity
   - Check file permissions

4. **"Task creation failed" errors**
   - Verify all required files were uploaded successfully
   - Check that TRIO groups have all three family members
   - Ensure clinical information is provided

### Getting Help

If you encounter issues:
1. Check the error messages in the console output
2. Review the generated JSON result files
3. Verify your CSV file format matches the requirements
4. Test with a single file first using the individual upload/task modules 