# Contribution Guidelines

Thank you for considering contributing to AI Model Evaluation Framework!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/AI_ModelEval.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install dev dependencies: `pip install -r requirements-dev.txt`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and commit: `git commit -am 'Add your feature'`
3. Push to your fork: `git push origin feature/your-feature`
4. Submit a pull request

## Code Standards

- Follow PEP 8 style guide
- Use type hints for all functions
- Write unit tests for new features
- Ensure all tests pass: `pytest`
- Format code with black: `black src tests`
- Check with pylint: `pylint src`

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_entities/

# Run specific test
pytest tests/test_entities/__init__.py::TestUser::test_user_creation
```

## Reporting Bugs

Please use the GitHub issue tracker to report bugs. Include:

- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

## Requesting Features

Open a GitHub issue with:

- Clear description of the feature
- Use cases and benefits
- Any relevant implementation ideas

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
