# AI_ModelEval

A comprehensive framework for evaluating AI code generation models. Built according to SRS specifications with full CRC card implementation.

## Features

- **Multi-model Evaluation**: Test multiple AI models (Ollama, HuggingFace, OpenAI) side-by-side
- **Comprehensive Metrics**: Pass@k, CodeBLEU, cyclomatic complexity, maintainability index
- **Secure Execution**: Docker-based sandbox for safe code execution
- **Error Analysis**: Pattern detection, classification, and fix suggestions
- **Interactive Dashboard**: Real-time visualization of results
- **Report Generation**: Export results in HTML, PDF, CSV, JSON formats
- **Resource Management**: Automatic model selection based on available disk space

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/AI_ModelEval.git
cd AI_ModelEval

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure settings
cp config/settings.yaml.example config/settings.yaml
# Edit settings.yaml with your configuration
```

## Usage

### Start Dashboard

```bash
python main.py --mode dashboard --host 0.0.0.0 --port 5000
```

### Run Evaluation

```bash
python main.py --mode eval --models codellama:7b starcoder:1b --samples 5
```

### Generate Benchmark

```bash
python main.py --mode benchmark
```

## Project Structure

```
AI_ModelEval/
├── src/
│   ├── entities/          # Core entity classes (CRC cards)
│   ├── managers/          # Manager classes
│   ├── adapters/          # Model adapters
│   ├── loaders/           # Dataset loaders
│   ├── executors/         # Code executors
│   ├── calculators/       # Metric calculators
│   ├── analyzers/         # Error analyzers
│   ├── generators/        # Report generators
│   ├── prompts/           # Prompt strategies
│   ├── dashboard/         # Web dashboard
│   └── utils/             # Utilities
├── config/                # Configuration files
├── data/                  # Dataset storage
├── results/               # Evaluation results
├── tests/                 # Test suite
├── main.py                # Entry point
└── requirements.txt       # Dependencies
```

## Architecture

The system follows the CRC card specifications from the SRS document:

- **User**: Authentication, sessions, permissions
- **Evaluation**: Lifecycle management, progress tracking
- **ModelAdapter**: Unified interface for AI models
- **DatasetLoader**: Dataset loading and parsing
- **SandboxExecutor**: Secure code execution
- **MetricCalculator**: Multi-dimensional metrics
- **ErrorAnalyzer**: Error classification and suggestions
- **ReportGenerator**: Multi-format report generation

## Configuration

Edit `config/settings.yaml` to configure:

- Paths for data and results
- Model endpoints and API keys
- Evaluation parameters
- Dashboard settings
- Logging levels

## API Documentation

The dashboard provides REST API endpoints:

- `GET /api/health` - System health check
- `GET /api/evaluations` - List evaluations
- `POST /api/evaluations` - Create evaluation
- `GET /api/models` - List available models
- `POST /api/reports` - Generate report
- `GET /api/charts/*` - Chart data endpoints

## Testing

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Based on SRS specifications for AI_ModelEval
- Implements CRC cards from software design document
- Uses HumanEval dataset for evaluation