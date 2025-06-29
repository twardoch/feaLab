# feaLab TODO List

## Critical Priority - Python 3 Migration

- [ ] Update setup.py to target Python 3.8+
- [ ] Remove fontTools.misc.py23 imports and use Python 3 equivalents
- [ ] Convert all string handling to proper Unicode/bytes distinction
- [ ] Replace `sh` module with `subprocess` calls
- [ ] Update harfpy dependency or find maintained alternative
- [ ] Fix any Python 2 specific syntax (print statements, etc.)
- [ ] Add type hints to all function signatures

## High Priority - Testing Infrastructure

- [ ] Set up pytest framework with basic configuration
- [ ] Create test directory structure
- [ ] Write unit tests for hb_render.py
- [ ] Write unit tests for hb_scripts3.py
- [ ] Write unit tests for writer modules
- [ ] Add test fixtures and sample fonts
- [ ] Set up GitHub Actions for CI/CD
- [ ] Add code coverage reporting
- [ ] Configure linting with flake8 or ruff
- [ ] Set up black for code formatting
- [ ] Add pre-commit hooks

## High Priority - Feature Implementation

- [ ] Implement actual KernFeatureWriter (not placeholder)
- [ ] Implement actual MarkFeatureWriter (not placeholder)
- [ ] Add proper error handling to all modules
- [ ] Add logging throughout the codebase
- [ ] Complete hb_scripts3.py implementation
- [ ] Add input validation for all public functions

## Medium Priority - Documentation

- [ ] Write comprehensive README.md with examples
- [ ] Add docstrings to all classes and functions
- [ ] Create CONTRIBUTING.md guide
- [ ] Set up Sphinx documentation
- [ ] Write installation guide for all platforms
- [ ] Create usage examples directory
- [ ] Add API reference documentation
- [ ] Document HarfBuzz dependency installation

## Medium Priority - Package Management

- [ ] Create pyproject.toml for modern packaging
- [ ] Update requirements.txt with all dependencies
- [ ] Create requirements-dev.txt for development dependencies
- [ ] Add MANIFEST.in for package data
- [ ] Prepare for PyPI publication
- [ ] Create GitHub release workflow
- [ ] Add version management system

## Low Priority - Cross-Platform Support

- [ ] Create Windows installation script (batch/PowerShell)
- [ ] Test on Linux distributions
- [ ] Add Docker support with Dockerfile
- [ ] Create conda-forge recipe
- [ ] Document platform-specific requirements

## Low Priority - Enhancements

- [ ] Consider using uharfbuzz instead of command-line tools
- [ ] Add caching for repeated operations
- [ ] Implement batch processing capabilities
- [ ] Add progress reporting for long operations
- [ ] Create simple GUI for font testing
- [ ] Add performance benchmarks

## Maintenance Tasks

- [ ] Remove compiled Python files (.pyc) from repo
- [ ] Update .gitignore to be more comprehensive
- [ ] Fix any existing linting issues
- [ ] Standardize code style across all modules
- [ ] Remove or update outdated documentation
- [ ] Clean up unused imports
- [ ] Review and update all dependencies

## Documentation Files to Create

- [ ] CONTRIBUTING.md - Contribution guidelines
- [ ] SECURITY.md - Security policy
- [ ] CODE_OF_CONDUCT.md - Community guidelines
- [ ] examples/ directory with sample scripts
- [ ] docs/ directory reorganization

## Future Considerations

- [ ] Add support for variable fonts
- [ ] Implement more feature writers
- [ ] Add font validation capabilities
- [ ] Create plugin system for extensions
- [ ] Add web service API
- [ ] Implement font comparison tools