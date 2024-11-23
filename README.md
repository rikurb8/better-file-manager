# Better File Manager

A comprehensive file management system that helps organize files intelligently with metadata, automated categorization, and seamless integrations.

## Overview

Better File Manager is designed to solve the common problem of file organization and accessibility. It automatically manages files based on their type, content, and metadata, making them easily findable when needed. The system includes features like automated screenshot organization, email integration, and intelligent document categorization.

## Key Features

- 📁 Intelligent file organization and metadata management
- 📸 Automated screenshot categorization with custom metadata
- 📧 Email integration for document management
- 🏢 Company document organization (financial statements, bookkeeping)
- 🔍 Smart search capabilities
- 🔄 Integration with popular storage providers
- 💾 Robust backup and restore functionality

## Technical Stack

- **Backend**: Python with strict typing
- **Package Management**: uv
- **Testing**: Comprehensive test suite
- **Deployment**: CI/CD pipeline with robust release management
- **Cross-Platform**: Available on all major operating systems

## Development Philosophy

- Type-safe Python code
- Test-driven development
- AI-assisted development practices
- Cross-platform compatibility
- Modular and maintainable architecture

## Getting Started

1. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
```

2. Install dependencies using uv:
```bash
uv pip install -r requirements.txt
```

3. Run tests:
```bash
python -m pytest
```

## Project Structure

```
better-file-manager/
├── better_file_manager/     # Main package directory
│   ├── __init__.py
│   ├── main.py             # Core application logic
│   └── text_to_mds.py      # Text processing utilities
├── tests/                  # Test suite
├── docs/                   # Documentation
└── pyproject.toml         # Project configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[License details to be added]
