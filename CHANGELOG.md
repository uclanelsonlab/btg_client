# Changelog

All notable changes to the BTG Virtual Geneticist API Client will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Implement progress bars for file uploads
- Add configuration validation GUI
- Support for additional file formats
- Enhanced error reporting and logging

## [1.1.0] - 2025-01-27

### Added
- **Batch Processing Module**: Complete batch upload and task creation functionality
- **CSV File Support**: Process multiple samples from CSV files
- **Flexible CSV Structure**: Support for one-row-per-task format with TRIO and SNP modes
- **Automatic File Organization**: Upload files with title-based directory structure
- **Intelligent Task Creation**: Group TRIO samples and create individual SNP tasks
- **Comprehensive Error Handling**: Robust validation and error reporting for batch operations
- **Output File Generation**: JSON result files for upload and task creation tracking

### Features
- **Batch Upload**: Upload multiple VCF files from CSV specification
- **Batch Task Creation**: Create analysis tasks for multiple samples
- **Full Batch Process**: Combined upload and task creation in one operation
- **CSV Validation**: Automatic validation of CSV structure and required columns
- **File Path Handling**: Support for data directory specification and file path resolution
- **Progress Tracking**: Detailed progress reporting for batch operations

### Technical Details
- New `btg_batch_module.py` with comprehensive batch processing logic
- Enhanced main application with batch command-line options
- Updated interactive menu with batch processing options
- Support for TRIO mode with father/mother file handling
- Support for SNP mode with individual sample processing
- Automatic handling of empty/NA values in CSV columns

### Documentation
- Complete batch processing guide (`BATCH_USAGE.md`)
- Updated README with batch functionality documentation
- CSV format specification and examples
- Command-line usage examples for all batch operations
- Troubleshooting guide for batch processing issues

### CSV Format Support
- Required columns: `samples`, `title`, `project`, `vcf_mode`, `assembly`, `upload_vcf`
- Optional columns: `upload_father`, `upload_mother`, `clinical_info`
- Support for both TRIO and SNP analysis modes
- Automatic handling of empty/NA values for optional family files

## [1.0.0] - 2025-06-30

### Added
- Initial release of BTG Virtual Geneticist API Client
- File upload module with support for VCF, PDF, and TXT files
- Task creation module with configurable parameters
- Status monitoring module for tracking analysis progress
- Interactive mode with user-friendly menu interface
- Command-line interface with argument parsing
- Support for three analysis modes: SNP, TRIO, and CARRIER
- Comprehensive configuration system with JSON-based task configuration
- File validation and error handling
- Token-based authentication system
- Cross-platform compatibility (Windows, macOS, Linux)
- Complete documentation suite including README and configuration guide

### Features
- **Upload Module**: Secure file upload with prefix-based organization
- **Task Module**: Flexible task creation with mode-specific validation
- **Status Module**: Real-time status checking and result retrieval
- **Configuration System**: JSON-based configuration with validation rules
- **Error Handling**: Comprehensive error messages and troubleshooting
- **Security**: Secure token management and file validation

### Technical Details
- Python 3.6+ compatibility
- Requests library for HTTP communication
- JSON configuration format
- Modular architecture for easy maintenance
- Comprehensive input validation
- Detailed logging and error reporting

### Documentation
- Complete README with installation and usage instructions
- Configuration reference with all available options
- API endpoint documentation
- Troubleshooting guide
- Usage examples for all analysis modes

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

## Release Process

1. Update version numbers in relevant files
2. Update CHANGELOG.md with new version
3. Create and push Git tag
4. Create GitHub release with release notes
5. Update documentation if needed 