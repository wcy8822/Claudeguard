# Contributing to ClaudeGuard

Thank you for your interest in contributing to ClaudeGuard! 🎉

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please:
- Check existing issues first
- Describe the use case clearly
- Explain why this feature would be useful

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/claudeguard.git
   cd claudeguard
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Make your changes**
   - Follow PEP 8 style guidelines
   - Add tests for new functionality
   - Update documentation as needed

5. **Run tests**
   ```bash
   pytest
   pytest --cov=claudeguard  # With coverage
   ```

6. **Format your code**
   ```bash
   black .
   flake8 .
   mypy .
   ```

7. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   Commit message format:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `test:` for tests
   - `refactor:` for refactoring
   - `chore:` for maintenance

8. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Development Setup

### Prerequisites
- Python 3.8+
- Git
- pytest (for testing)

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=claudeguard --cov-report=html

# Specific test file
pytest tests/test_guard.py

# Verbose mode
pytest -v
```

### Code Style
We use:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

Run all checks:
```bash
make lint  # Or manually:
black .
flake8 .
mypy .
```

## 🎯 Areas We Need Help

- **Testing**: More test coverage, edge cases
- **Documentation**: Examples, tutorials, translations
- **Features**: See issues labeled "good first issue"
- **Integrations**: VS Code extension, other AI tools
- **Performance**: Optimization, benchmarking

## 📚 Code Structure

```
claudeguard/
├── core/
│   ├── guard.py         # Main backup engine
│   ├── rollback.py      # Rollback logic (planned)
│   └── verifier.py      # Compliance checker (planned)
├── cli/
│   └── main.py          # CLI interface
├── tests/
│   ├── test_guard.py
│   └── test_cli.py
└── docs/
    └── ...
```

## ✅ Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] PR description clearly explains changes

## 🌟 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

## 📞 Questions?

- **Discord**: Join our community
- **Issues**: Ask in GitHub issues
- **Email**: dev@claudeguard.dev

Thank you for making ClaudeGuard better! 🚀