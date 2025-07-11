# Release Notes

## [1.2.0] - 2025-07-10

### 🎉 Major Release: Project Reorganization & Docker Support

This release represents a significant milestone in the BT Genomics Virtual Geneticist API Client, introducing major architectural improvements, Docker containerization, and enhanced user experience features.

### 🚀 New Features

#### **Docker Containerization**
- **Complete Docker Support**: Full containerization with Dockerfile and docker-compose.yml
- **Easy Deployment**: One-command deployment with `docker-compose up`
- **Consistent Environment**: Eliminates "works on my machine" issues
- **Production Ready**: Optimized for production deployment
- **Documentation**: Comprehensive Docker usage guide in `docs/DOCKER_USAGE.md`

#### **Project Structure Reorganization**
- **Modular Architecture**: Moved source files to `src/` directory for better organization
- **Proper Package Structure**: Added `__init__.py` with version information
- **Separated Concerns**: Tests in `tests/`, docs in `docs/`, examples in `examples/`
- **Setup.py**: Proper Python package configuration with dependencies
- **Distribution Ready**: Package can now be installed via pip

#### **Enhanced CLI Experience**
- **New Entry Point**: `btg_client.py` as the primary application entry point
- **Updated Help Text**: All examples now reference the new entry point
- **Consistent Interface**: Improved command-line interface across all modules
- **Better Documentation**: Updated all usage examples and help text

#### **Progress Bars for Uploads**
- **Visual Feedback**: Real-time progress indicators during file uploads
- **Transfer Rate**: Shows upload speed and estimated time remaining
- **Batch Progress**: Tracks progress across multiple files in batch operations
- **Configurable**: Can be disabled with `--no-progress` flag
- **Cross-platform**: Works on Windows, macOS, and Linux

### 🔧 Technical Improvements

#### **Code Organization**
- **Modular Design**: Improved separation of concerns with proper package structure
- **Import System**: Updated all imports to use the new `src/` module structure
- **Error Handling**: Enhanced error handling and user feedback
- **Documentation**: Comprehensive documentation covering all aspects

#### **Docker Implementation**
- **Multi-stage Build**: Optimized Docker image size
- **Security**: Non-root user execution for better security
- **Volume Mounting**: Easy data access and configuration
- **Environment Variables**: Configurable container behavior
- **Health Checks**: Container health monitoring

#### **Package Distribution**
- **Setup.py**: Proper Python package configuration
- **Dependencies**: Clear dependency specification
- **Metadata**: Complete package metadata and description
- **Installation**: Can be installed via pip or from source

### 📚 Documentation Enhancements

#### **New Documentation**
- **Docker Usage Guide**: Complete Docker setup and usage instructions
- **Project Structure**: Detailed explanation of the new directory structure
- **Quick Start Guide**: Step-by-step getting started instructions
- **Examples**: Comprehensive examples for all features

#### **Updated Documentation**
- **README.md**: Updated with new features and Docker support
- **CLI Help**: All help text updated to reference new entry point
- **Usage Examples**: Updated examples to reflect new structure

### 🎯 User Experience Improvements

#### **Easier Installation**
- **Docker**: One-command installation and setup
- **Pip Installation**: Can be installed as a Python package
- **Source Installation**: Clear instructions for source installation

#### **Better Organization**
- **Clear Structure**: Logical organization of files and directories
- **Easy Navigation**: Intuitive directory structure
- **Separation of Concerns**: Tests, docs, and examples properly organized

#### **Enhanced CLI**
- **Consistent Interface**: Unified command-line experience
- **Better Help**: Comprehensive help text and examples
- **Clear Entry Point**: Obvious main application file

### 🔄 Migration Guide

#### **For Existing Users**
1. **Update Entry Point**: Use `btg_client.py` instead of `btg_main.py`
2. **Docker Option**: Consider using Docker for easier deployment
3. **New Structure**: Familiarize with the new directory organization
4. **Documentation**: Check the updated documentation for new features

#### **For New Users**
1. **Docker First**: Start with Docker for the easiest setup
2. **Quick Start**: Follow the quick start guide in `docs/QUICK_START.md`
3. **Examples**: Check the examples directory for usage patterns
4. **Documentation**: Refer to the comprehensive documentation

### 🐛 Bug Fixes

- **Upload Progress**: Fixed issues with progress bar display
- **Module Imports**: Resolved import issues with new structure
- **CLI Consistency**: Fixed help text and example references
- **File Organization**: Resolved file path issues in new structure

### 📦 Installation Options

#### **Docker (Recommended)**
```bash
# Clone the repository
git clone <repository-url>
cd btg_client

# Run with Docker
docker-compose up
```

#### **Pip Installation**
```bash
# Install from source
pip install -e .
```

#### **Source Installation**
```bash
# Clone and run directly
git clone <repository-url>
cd btg_client
python btg_client.py --help
```

### 🎊 What's Next

- **Configuration GUI**: Planning a graphical configuration interface
- **Additional File Formats**: Support for more genetic data formats
- **Enhanced Logging**: Improved logging and debugging capabilities
- **Advanced Progress Tracking**: More detailed progress reporting
- **Plugin System**: Extensible architecture for custom modules

---

## [1.1.0] - 2025-07-10

### 🚀 Major Release: Batch Processing & Progress Tracking

This release introduces comprehensive batch processing capabilities and enhanced user experience features, making the client more powerful and user-friendly for large-scale operations.

### ✨ New Features

#### **Batch Processing Module**
- **CSV File Support**: Process multiple samples from CSV files
- **Flexible CSV Structure**: Support for one-row-per-task format
- **TRIO and SNP Modes**: Automatic handling of family and individual samples
- **Automatic File Organization**: Upload files with title-based directory structure
- **Intelligent Task Creation**: Group TRIO samples and create individual SNP tasks

#### **Progress Bars for Uploads**
- **Real-time Progress**: Visual progress indicators during file uploads
- **Transfer Rate Display**: Shows upload speed and estimated time remaining
- **Batch Progress Tracking**: Tracks progress across multiple files
- **Configurable**: Can be disabled with `--no-progress` flag
- **Cross-platform**: Works on Windows, macOS, and Linux

#### **Enhanced CSV Support**
- **Flexible Format**: Support for `upload_vcf`, `upload_father`, `upload_mother` columns
- **TRIO Mode**: Automatic handling of family trio data
- **SNP Mode**: Individual sample processing
- **Empty Value Handling**: Automatic handling of empty/NA values
- **Validation**: Comprehensive CSV structure validation

### 🔧 Technical Improvements

#### **Upload Progress System**
- **Custom Progress Bar**: `UploadProgressBar` class with tqdm integration
- **Graceful Fallback**: Falls back to simple output if tqdm is not available
- **Transfer Rate**: Real-time upload speed calculation
- **ETA Calculation**: Estimated time to completion
- **File Size Display**: Shows total file size and bytes transferred

#### **Batch Processing Architecture**
- **Modular Design**: Separate batch upload and task creation modules
- **Error Handling**: Robust validation and error reporting
- **Output Generation**: JSON result files for tracking
- **Flexible Configuration**: Support for various CSV formats

#### **CLI Enhancements**
- **New Batch Commands**: `batch-upload`, `batch-task`, `batch-full`
- **Interactive Menu**: Updated menu with batch processing options
- **Help Text**: Comprehensive help and usage examples
- **Parameter Validation**: Better validation of command-line arguments

### 📊 CSV Format Support

#### **Required Columns**
- `upload_vcf`: Path to the VCF file for the sample
- `upload_father`: Path to father's VCF file (optional for SNP)
- `upload_mother`: Path to mother's VCF file (optional for SNP)

#### **Usage Examples**
```csv
upload_vcf,upload_father,upload_mother
data/sample1.vcf.gz,data/father1.vcf.gz,data/mother1.vcf.gz
data/sample2.vcf.gz,NA,NA
```

### 🎯 User Experience Improvements

#### **Visual Feedback**
- **Progress Bars**: Real-time upload progress with transfer rate
- **Batch Progress**: Overall progress for batch operations
- **Error Messages**: Clear and informative error messages
- **Success Indicators**: Clear confirmation of successful operations

#### **Flexible Configuration**
- **File Paths**: Support for full file paths in CSV
- **Data Directory**: Optional data directory specification
- **Task Titles**: Automatic timestamp suffix for uniqueness
- **Mode Detection**: Automatic TRIO vs SNP mode detection

### 🔄 Migration from v1.0.0

#### **For Existing Users**
1. **Update CSV Format**: Use the new one-row-per-sample format
2. **Enable Progress Bars**: Remove `--no-progress` flag to see progress
3. **Check File Paths**: Ensure full paths are specified in CSV
4. **Review Documentation**: Check updated usage examples

#### **For New Users**
1. **Start with Examples**: Use the provided example CSV files
2. **Enable Progress**: Use progress bars for better feedback
3. **Test with Small Files**: Start with small test files
4. **Check Documentation**: Refer to batch usage guide

### 🐛 Bug Fixes

- **File Upload Issues**: Resolved problems with file uploads and API compatibility
- **Progress Bar Implementation**: Fixed issues with custom progress file wrapper
- **Task Creation Errors**: Resolved "Current task already been submitted!" errors
- **File Path Handling**: Fixed issues with file path resolution in batch operations

### 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd btg_client

# Run the client
python btg_main.py --help
```

### 🎊 What's Next

- **Docker Support**: Containerization for easier deployment
- **Project Reorganization**: Better code organization and structure
- **Enhanced Documentation**: More comprehensive guides and examples
- **Advanced Features**: Additional analysis modes and capabilities

---

## [1.0.0] - 2025-07-10

### 🎉 Initial Release

The first release of the BT Genomics Virtual Geneticist API Client, providing a comprehensive solution for interacting with the Virtual Geneticist API.

### ✨ Core Features

#### **Modular Architecture**
- **Upload Module**: File upload with progress tracking and prefix support
- **Task Module**: Analysis task creation with configurable parameters
- **Status Module**: Task status monitoring and result retrieval
- **Interactive Mode**: User-friendly menu interface
- **CLI Mode**: Direct command execution with arguments

#### **File Support**
- **VCF Files**: Support for VCF and VCF.GZ formats
- **PDF Files**: Support for PDF documentation
- **TXT Files**: Support for text files
- **File Validation**: Comprehensive file format validation

#### **Analysis Modes**
- **SNP Analysis**: Individual sample analysis
- **TRIO Analysis**: Family trio analysis
- **CARRIER Analysis**: Carrier screening analysis

#### **Security & Authentication**
- **Token-based Authentication**: Secure API access using token files
- **File Validation**: Comprehensive input validation
- **Error Handling**: Robust error handling and user feedback

### 🔧 Technical Foundation

#### **Python Compatibility**
- **Python 3.7+**: Modern Python features and syntax
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Dependencies**: Minimal external dependencies

#### **HTTP Client**
- **Requests Library**: Robust HTTP requests with proper error handling
- **JSON Processing**: Configuration and data handling
- **File Operations**: Secure file handling and validation

#### **User Interface**
- **Interactive Menu**: Menu-driven interface for easy navigation
- **Command-line Interface**: Direct command execution
- **Progress Tracking**: Visual feedback for long-running operations

### 📚 Documentation

#### **Complete Documentation Suite**
- **README.md**: Installation and usage instructions
- **Configuration Guide**: Task configuration reference
- **API Documentation**: Endpoint documentation
- **Troubleshooting Guide**: Common issues and solutions
- **Usage Examples**: Examples for all analysis modes

### 🎯 User Experience

#### **Easy to Use**
- **Interactive Mode**: Menu-driven interface for beginners
- **CLI Mode**: Command-line interface for automation
- **Clear Documentation**: Comprehensive guides and examples
- **Error Messages**: Informative error messages and help

#### **Flexible Configuration**
- **JSON Configuration**: Flexible task configuration system
- **Token Management**: Secure token file handling
- **File Organization**: Prefix-based file organization
- **Status Monitoring**: Real-time status checking

### 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd btg_client

# Run the client
python btg_main.py --help
```

### 🎊 What's Next

- **Batch Processing**: Support for processing multiple files
- **Progress Bars**: Visual progress indicators
- **Enhanced Error Handling**: More detailed error reporting
- **Additional File Formats**: Support for more genetic data formats 