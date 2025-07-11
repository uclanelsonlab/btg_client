# 🚀 Quick Start Guide

## 📦 Installation

### Option 1: Direct Usage (No Installation)
```bash
# Clone or download the repository
git clone <repository-url>
cd btg_client

# Run directly
python btg_client.py --token token.txt
```

### Option 2: Install as Package
```bash
# Install in development mode
pip install -e .

# Run from anywhere
btg-client --token token.txt
```

## 🎯 Basic Usage

### Interactive Mode (Recommended)
```bash
python btg_client.py --token token.txt
```

### Command Line Mode
```bash
# Upload a file
python btg_client.py upload --token token.txt --file-path data/file.vcf.gz --prefix sample

# Create a task
python btg_client.py task --token token.txt --task-config examples/task_config.json

# Check status
python btg_client.py status --token token.txt --submission-id <submission_id>

# Batch upload
python btg_client.py batch-upload --token token.txt --csv data/samplesheet.csv

# Batch create tasks
python btg_client.py batch-task --token token.txt --csv data/samplesheet.csv
```

## 📁 Project Structure

```
btg_client/
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation
├── examples/               # Example files
├── data/                   # Your data files
├── btg_client.py          # Main entry point
└── setup.py               # Package setup
```

## 🔧 Configuration

1. **Token**: Place your API token in `token.txt`
2. **Data**: Put your VCF files in `data/` directory
3. **CSV**: Create your batch CSV in `data/samplesheet.csv`

## 📋 Example CSV Format

```csv
samples,title,project,vcf_mode,assembly,upload_vcf,upload_father,upload_mother,clinical_info
SAMPLE1,SAMPLE1_cohort,PROJECT,TRIO,hg38,data/sample1.vcf.gz,data/father.vcf.gz,data/mother.vcf.gz,Clinical description
SAMPLE2,SAMPLE2_cohort,PROJECT,SNP,hg38,data/sample2.vcf.gz,,,Clinical description
```

## 🆘 Need Help?

- **Documentation**: Check `docs/README.md`
- **Examples**: Look in `examples/` directory
- **Tests**: Run `python tests/test_*.py`
- **Issues**: Check `docs/README.md` troubleshooting section

## 🎉 Success!

Your BTG Virtual Geneticist API Client is now organized and ready to use! 