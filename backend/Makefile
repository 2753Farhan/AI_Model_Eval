.PHONY: help install install-dev test test-cov format lint clean build docs run-dashboard

help:
	@echo "AI Model Evaluation - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install dependencies"
	@echo "  make install-dev      Install dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run tests"
	@echo "  make test-cov         Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format           Format code with black and isort"
	@echo "  make lint             Run pylint and flake8"
	@echo "  make clean            Remove build artifacts and cache"
	@echo ""
	@echo "Running:"
	@echo "  make run-dashboard    Start the web dashboard"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs             Generate documentation"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

format:
	black src tests
	isort src tests

lint:
	pylint src
	flake8 src tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf build dist *.egg-info
	rm -rf htmlcov .coverage

build:
	python setup.py sdist bdist_wheel

docs:
	cd docs && make html

run-dashboard:
	python main.py --mode dashboard --host 0.0.0.0 --port 5000

run-eval:
	python main.py --mode eval --models ollama huggingface

.DEFAULT_GOAL := help
