# Changelog

All notable changes to the BT Genomics Virtual Geneticist API Client will be documented in this file.

## [1.2.0] - 2025-07-10

### Added
- **Progress bars for file uploads**: Added visual progress indicators using `tqdm` for better user experience during file uploads
- **Docker support**: Complete Docker containerization with Dockerfile, docker-compose.yml, and comprehensive Docker usage documentation
- **Project structure reorganization**: Moved source files to `src/` directory, tests to `tests/`, documentation to `docs/`, and examples to `examples/`
- **New main entry point**: Created `btg_client.py` as the primary entry point for the application
- **Setup.py**: Added proper Python package configuration with dependencies and metadata
- **Comprehensive documentation**: Added Docker usage guide, project structure documentation, and quick start guide
- **CLI improvements**: Updated all help text and examples to reference the new `btg_client.py` entry point
- **Enhanced examples**: Added various test files and sample configurations in the examples directory

### Changed
- **CLI entry point**: Changed from `btg_main.py` to `btg_client.py` for better clarity
- **Import structure**: Updated all imports to use the new `src/` module structure
- **Documentation organization**: Moved all documentation files to `docs/` directory for better organization
- **File organization**: Reorganized project structure for better maintainability and distribution

### Fixed
- **Upload progress tracking**: Fixed issues with progress bar display during file uploads
- **Module imports**: Ensured all modules work correctly with the new directory structure

### Technical Improvements
- **Modular architecture**: Improved code organization with proper package structure
- **Docker containerization**: Full containerization support for easy deployment and distribution
- **Package distribution**: Added setup.py for proper Python package installation
- **Documentation**: Comprehensive documentation covering all aspects of the project

## [1.1.0] - 2025-07-10

### Added
- **Batch processing capabilities**: Added comprehensive batch upload and task creation functionality
- **CSV file support**: Support for processing CSV files with sample data for bulk operations
- **Progress tracking**: Visual progress bars for upload operations
- **Flexible file paths**: Support for full file paths in CSV files
- **Task title uniqueness**: Automatic timestamp suffix to prevent duplicate task titles
- **Comprehensive error handling**: Better error messages and validation for batch operations

### Changed
- **CSV format**: Updated to support one line per sample with `upload_vcf`, `upload_father`, and `upload_mother` columns
- **Upload progress**: Enhanced progress bar implementation with custom `UploadProgressBar` class
- **CLI interface**: Added new batch commands and improved help text
- **Documentation**: Updated usage examples and documentation to reflect new features

### Fixed
- **File upload issues**: Resolved problems with file uploads and API compatibility
- **Progress bar implementation**: Fixed issues with custom progress file wrapper
- **Task creation**: Resolved "Current task already been submitted!" errors with unique titles
- **File path handling**: Fixed issues with file path resolution in batch operations

### Technical Improvements
- **Upload reliability**: Improved file upload success rate and error handling
- **Batch processing**: Robust batch upload and task creation with proper validation
- **User experience**: Better progress indicators and error messages
- **Code organization**: Improved module structure and error handling

## [1.0.0] - 2025-07-10

### Added
- **Core API client functionality**: Basic upload, task creation, and status checking capabilities
- **Modular architecture**: Separate modules for upload, task, status, and batch operations
- **Interactive CLI**: Menu-driven interface for easy navigation
- **Command-line interface**: Direct command execution with various options
- **Token-based authentication**: Secure API access using token files
- **File upload support**: Support for VCF, VCF.GZ, PDF, and TXT files
- **Task configuration**: JSON-based task configuration system
- **Status monitoring**: Real-time task status checking
- **Error handling**: Comprehensive error handling and user feedback
- **Documentation**: Complete usage documentation and examples

### Features
- **Upload Module**: File upload with progress tracking and prefix support
- **Task Module**: Analysis task creation with configurable parameters
- **Status Module**: Task status monitoring and result retrieval
- **Batch Module**: Bulk operations for multiple files and tasks
- **Interactive Mode**: User-friendly menu interface
- **CLI Mode**: Direct command execution with arguments

### Technical Foundation
- **Python 3.7+ compatibility**: Modern Python features and syntax
- **HTTP client**: Robust HTTP requests with proper error handling
- **JSON processing**: Configuration and data handling
- **File operations**: Secure file handling and validation
- **Progress tracking**: Visual feedback for long-running operations 