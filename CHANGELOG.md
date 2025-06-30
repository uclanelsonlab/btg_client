# Changelog

All notable changes to the BTG Virtual Geneticist API Client will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Add support for batch processing
- Implement progress bars for file uploads
- Add configuration validation GUI
- Support for additional file formats

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