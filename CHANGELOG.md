# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2025-06-29

### Added
- New `hb_scripts3.py` module for Unicode to OpenType script tag conversion
  - Supports conversion between ISO 15924 tags and OpenType script tags
  - Implements `updateLanguageSystemsInFea()` function to automatically update language systems in FEA files
  - Uses harfpy (Python 3 bindings for HarfBuzz)
  - Provides functions: `isoScript()`, `otScripts()`, `otScript()`, `charScript()`, `getIsoToOtScriptMap()`

### Changed
- Updated installation script (`install-macos.command`) to use more modern conventions
- Various minor updates and improvements to the codebase

### Technical Details
- The project currently targets Python 2.7 (as per setup.py)
- Uses HarfBuzz bindings for font rendering and shaping operations
- Depends on the `sh` module for command-line tool integration

## [0.3.0] - Previous Release

### Features
- HarfBuzz renderer wrapper (`hb_render.py`) for `hb-view` and `hb-shape` utilities
- Placeholder writers for kern and mark features
- Basic documentation generation using pdoc
- macOS installation helper script

### Dependencies
- sh>=1.11
- harfbuzz (system dependency)
- Optional: pdoc for documentation generation
- Optional: pandoc for README conversion