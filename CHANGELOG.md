# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2025-01-16

### Changed
- **Simplified upload process**: Rolled back to v1.0.0-style uploads without timeouts or retry logic
- **Removed progress bars**: Eliminated progress bar functionality to improve reliability
- **Removed timestamp from project names**: Task titles now use exact CSV values without timestamp suffixes
- **Streamlined batch processing**: Removed separate batch-upload and batch-task modules, consolidated into single batch-full module
- **Fixed import issues**: Updated module imports to match available functions

### Removed
- `run_batch_upload_module` and `run_batch_task_module` functions
- Progress bar functionality from upload modules
- Timestamp generation for task titles
- Separate batch upload and batch task creation options from CLI

### Fixed
- Import errors when running batch-full command
- Module compatibility issues between main client and batch module

## [1.2.0] - 2025-01-15

### Added
- **Docker support**: Added Dockerfile, docker-compose.yml, and Docker usage documentation
- **Project reorganization**: Moved source files to src/ directory with proper package structure
- **New entry point**: Created btg_client.py as the main entry point
- **Setup.py**: Added proper Python package setup with entry points
- **Documentation**: Added comprehensive documentation in docs/ directory

### Changed
- **Project structure**: Reorganized files into logical directories (src/, tests/, docs/, examples/, scripts/, data/)
- **Main entry point**: Changed from btg_main.py to btg_client.py
- **CLI help**: Updated all help text and examples to use btg_client.py

## [1.1.0] - 2025-01-14

### Added
- **Progress bars**: Added upload progress tracking with tqdm
- **Batch processing**: Added CSV-based batch upload and task creation
- **Task title uniqueness**: Automatic timestamp addition to prevent duplicate task errors

### Changed
- **Upload reliability**: Improved upload handling with progress tracking
- **Batch operations**: Added support for processing multiple samples from CSV files

## [1.0.0] - 2025-01-13

### Added
- **Initial release**: Basic upload, task creation, and status checking functionality
- **Modular design**: Separate modules for upload, task, status, and batch operations
- **Interactive mode**: Menu-driven interface for easy operation
- **Command-line interface**: Direct module execution with parameters 