# BTG Client Project Structure

## 📁 Directory Organization

```
btg_client/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── btg_main.py              # Main CLI interface
│   ├── btg_upload_module.py     # File upload functionality
│   ├── btg_task_module.py       # Task creation and management
│   ├── btg_status_module.py     # Status checking and monitoring
│   └── btg_batch_module.py      # Batch processing functionality
│
├── tests/                        # Test files and debugging tools
│   ├── test_*.py                # Unit tests
│   ├── debug_*.py               # Debugging scripts
│   └── diagnose_*.py            # Diagnostic tools
│
├── docs/                         # Documentation
│   ├── README.md                # Main documentation
│   ├── CHANGELOG.md             # Version history
│   ├── RELEASE_NOTES.md         # Release notes
│   └── BATCH_USAGE.md           # Batch processing guide
│
├── examples/                     # Example files and configurations
│   ├── *.json                   # Configuration examples
│   ├── test_*.vcf*              # Sample VCF files
│   └── test_*.txt               # Sample text files
│
├── scripts/                      # Utility scripts
│   └── (future utility scripts)
│
├── data/                         # User data directory
│   └── samplesheet.csv          # User CSV files
│
├── btg_client.py                # Main entry point
├── setup.py                     # Package installation
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore rules
└── PROJECT_STRUCTURE.md         # This file
```

## 🎯 Usage

### Development
```bash
# Run from project root
python btg_client.py --token token.txt

# Run specific module
python btg_client.py upload --token token.txt --file-path data/file.vcf.gz
```

### Installation
```bash
# Install in development mode
pip install -e .

# Install globally
pip install .
```

### Testing
```bash
# Run tests
python -m pytest tests/

# Run specific test
python tests/test_upload.py
```

## 📋 Key Features

- **Modular Design**: Each functionality is in its own module
- **Clean Structure**: Organized directories for different purposes
- **Easy Installation**: Proper Python package structure
- **Comprehensive Testing**: Dedicated test directory
- **Good Documentation**: All docs in one place
- **Example Files**: Sample configurations and data

## 🔧 Development Workflow

1. **Source Code**: All main code goes in `src/`
2. **Tests**: All test files go in `tests/`
3. **Documentation**: All docs go in `docs/`
4. **Examples**: Sample files go in `examples/`
5. **User Data**: User files go in `data/`

## 📦 Package Structure

The project is organized as a proper Python package with:
- **Entry Point**: `btg_client.py` for easy execution
- **Setup**: `setup.py` for installation
- **Dependencies**: `requirements.txt` for dependencies
- **Version Control**: Proper `.gitignore` for clean repos 