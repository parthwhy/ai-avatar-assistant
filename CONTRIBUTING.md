# Contributing to SAGE

Thank you for your interest in contributing to SAGE! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Git
- API keys for Groq and Picovoice (see `.env.example`)

### Setup Development Environment
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/sage.git
   cd sage
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and add your API keys

## 📝 How to Contribute

### Reporting Bugs
1. Check if the bug is already reported in [Issues](https://github.com/yourusername/sage/issues)
2. Create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Error logs if applicable

### Suggesting Features
1. Check existing [Issues](https://github.com/yourusername/sage/issues) for similar requests
2. Create a new issue with:
   - Clear feature description
   - Use case and benefits
   - Possible implementation approach

### Code Contributions

#### Branch Naming
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

#### Pull Request Process
1. Create a new branch from `main`
2. Make your changes
3. Test your changes thoroughly
4. Update documentation if needed
5. Submit a pull request with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots/videos for UI changes

## 🏗️ Project Structure

```
sage/
├── main.py                 # Entry point
├── config/                 # Configuration management
├── core/                   # Core AI and orchestration
├── tools/                  # Tool implementations
│   ├── system/            # System control tools
│   ├── productivity/      # Productivity tools
│   ├── communication/     # Communication tools
│   ├── media/             # Media control tools
│   └── ai/                # AI-powered tools
├── voice/                 # Voice processing
├── recorder/              # Task recording/playback
├── ui/                    # User interface
├── routines/              # Predefined routines
└── data/                  # User data and generated content
```

## 🔧 Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Adding New Tools
1. Create tool file in appropriate `tools/` subdirectory
2. Follow the tool template:
   ```python
   def tool_function(param1: str, param2: int = None) -> Dict[str, Any]:
       """
       Tool description.
       
       Args:
           param1: Description
           param2: Optional description
           
       Returns:
           Dictionary with success status and result
       """
       try:
           # Tool implementation
           return {
               'success': True,
               'message': 'Task completed',
               'result': result_data
           }
       except Exception as e:
           return {
               'success': False,
               'message': f'Error: {str(e)}'
           }
   ```
3. Add tool to `__init__.py` in the subdirectory
4. Register tool in `core/orchestrator.py`
5. Add usage examples in orchestrator prompt
6. Update documentation

### Testing
- Test all new features manually
- Ensure existing functionality isn't broken
- Test with different API key configurations
- Test error handling and edge cases

### Documentation
- Update README.md for new features
- Add docstrings to all new functions
- Update PROJECT_DESCRIPTION.md for major changes
- Include usage examples

## 🎯 Areas for Contribution

### High Priority
- **Cross-platform support** (macOS, Linux)
- **Additional AI model integrations**
- **Enhanced error handling and recovery**
- **Performance optimizations**
- **Accessibility improvements**

### Medium Priority
- **New tool implementations**
- **UI/UX improvements**
- **Additional voice commands**
- **Integration with more services**
- **Mobile companion app**

### Low Priority
- **Code refactoring**
- **Documentation improvements**
- **Test coverage expansion**
- **Localization support**

## 🐛 Debugging

### Common Issues
1. **API Rate Limits**: Implement proper rate limiting and fallbacks
2. **PyAutoGUI Failures**: Add coordinate validation and error recovery
3. **Voice Recognition**: Handle microphone permissions and audio issues
4. **TTS Problems**: Ensure Windows Speech is enabled

### Debug Mode
Set environment variable for verbose logging:
```bash
export SAGE_DEBUG=1  # Linux/Mac
set SAGE_DEBUG=1     # Windows
```

## 📋 Code Review Checklist

- [ ] Code follows project style guidelines
- [ ] All functions have proper docstrings
- [ ] Error handling is implemented
- [ ] No hardcoded values (use configuration)
- [ ] No API keys or sensitive data in code
- [ ] Tests pass (if applicable)
- [ ] Documentation is updated
- [ ] No breaking changes to existing functionality

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the code of conduct
- Ask questions if you're unsure

## 📞 Getting Help

- **Issues**: Create a GitHub issue for bugs or questions
- **Discussions**: Use GitHub Discussions for general questions
- **Email**: Contact maintainers for sensitive issues

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special mentions for major features

Thank you for contributing to SAGE! 🚀