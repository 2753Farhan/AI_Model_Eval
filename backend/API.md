# API Documentation

## Overview

This document provides detailed API documentation for the AI Model Evaluation Framework.

## Core Modules

### 1. Entities (`src.entities`)

Data models representing core concepts in the evaluation framework.

#### User

```python
from src.entities import User

user = User(
    username='user_name',
    email='user@example.com',
    password='password123'
)
```

#### Evaluation

```python
from src.entities import Evaluation

evaluation = Evaluation(
    name='My Evaluation',
    model='ollama',
    dataset='humaneval'
)
```

#### Problem

```python
from src.entities import Problem

problem = Problem(
    title='Problem Title',
    description='Problem description',
    input_spec='Input specification',
    output_spec='Output specification'
)
```

#### EvaluationResult

```python
from src.entities import EvaluationResult

result = EvaluationResult(
    problem_id='p1',
    solution='def f():\n    pass',
    status='passed'
)
```

### 2. Managers (`src.managers`)

Business logic for managing evaluations and aggregating results.

#### EvaluationManager

```python
from src.managers import EvaluationManager

manager = EvaluationManager()
results = manager.run_evaluation(
    loader=dataset_loader,
    adapter=model_adapter,
    timeout=30
)
```

#### ResultAggregator

```python
from src.managers import ResultAggregator

aggregator = ResultAggregator()
aggregated = aggregator.aggregate(results)
stats = aggregator.calculate_statistics(results)
```

### 3. Adapters (`src.adapters`)

Interface implementations for different model providers.

#### ModelAdapter (Abstract Base)

```python
from src.adapters import ModelAdapter

class CustomAdapter(ModelAdapter):
    def load_model(self):
        # Load your model
        pass

    def generate(self, prompt):
        # Generate output
        return response
```

#### ModelRegistry

```python
from src.adapters import ModelRegistry, OllamaAdapter

registry = ModelRegistry()
registry.register('ollama', OllamaAdapter)
adapter_class = registry.get('ollama')
```

### 4. Loaders (`src.loaders`)

Dataset loaders for different benchmarks.

#### DatasetLoader (Abstract Base)

```python
from src.loaders import DatasetLoader

class CustomLoader(DatasetLoader):
    def load(self):
        # Load dataset
        pass

    def get_problems(self):
        # Return problems
        return problems
```

#### HumanEvalLoader

```python
from src.loaders import HumanEvalLoader

loader = HumanEvalLoader()
problems = loader.get_problems()
```

### 5. Executors (`src.executors`)

Safe code execution with resource management.

#### SandboxExecutor

```python
from src.executors import SandboxExecutor

executor = SandboxExecutor()
result = executor.execute('print("hello")')
result = executor.execute_with_timeout('code', timeout=30)
```

#### ResourceManager

```python
from src.executors import ResourceManager

manager = ResourceManager()
manager.set_memory_limit('4GB')
manager.set_cpu_limit('2')
manager.set_timeout(30)
```

### 6. Calculators (`src.calculators`)

Metric calculation for different evaluation types.

```python
from src.calculators import (
    FunctionalMetrics,
    QualityMetrics,
    SemanticMetrics
)

# Calculate Pass@k
functional = FunctionalMetrics()
pass_k = functional.calculate(results, k=1)

# Calculate quality metrics
quality = QualityMetrics()
metrics = quality.calculate(code)

# Calculate semantic metrics
semantic = SemanticMetrics()
similarity = semantic.calculate(generated, reference)
```

### 7. Analyzers (`src.analyzers`)

Error analysis and pattern detection.

```python
from src.analyzers import (
    ErrorAnalyzer,
    PatternDetector,
    FixSuggester
)

# Analyze errors
analyzer = ErrorAnalyzer()
analysis = analyzer.analyze(error)

# Detect patterns
detector = PatternDetector()
patterns = detector.detect_patterns(results)

# Suggest fixes
suggester = FixSuggester()
suggestions = suggester.suggest_fixes(error)
```

### 8. Generators (`src.generators`)

Report generation in multiple formats.

```python
from src.generators import ReportGenerator

generator = ReportGenerator()
report = generator.generate_report(results)
generator.export_report(report, format='html')
```

### 9. Prompts (`src.prompts`)

Prompt strategies and generation.

```python
from src.prompts import PromptEngine

engine = PromptEngine()
prompt = engine.generate_prompt(problem, strategy='zero_shot')
```

### 10. Dashboard (`src.dashboard`)

Web interface for visualization.

```python
from src.dashboard import create_app

app = create_app()
app.run(host='0.0.0.0', port=5000)
```

## Configuration

### Configuration Management

```python
from src.config import config

# Get configuration
timeout = config.get('evaluation.timeout', 30)

# Set configuration
config.set('evaluation.timeout', 60)

# Dictionary-style access
timeout = config['evaluation.timeout']
config['evaluation.memory_limit'] = '8GB'
```

## Utilities

### Disk Space Manager

```python
from src.utils import DiskSpaceManager

manager = DiskSpaceManager()
space = manager.check_available_space()
manager.cleanup_old_results()
```

### Debug Timer

```python
from src.utils import DebugTimer

# Context manager usage
with DebugTimer('operation'):
    # Your code here
    pass

# Manual timing
timer = DebugTimer('operation')
timer.start()
# Your code here
timer.stop()
```

### Validators

```python
from src.utils import Validators

Validators.validate_problem(problem)
Validators.validate_result(result)
Validators.validate_config(config)
```

## Exception Handling

All modules may raise custom exceptions. Handle them appropriately:

```python
try:
    result = executor.execute(code)
except TimeoutError:
    print("Code execution timed out")
except RuntimeError as e:
    print(f"Execution error: {e}")
```

## Examples

See [examples.py](examples.py) for complete working examples.

## Best Practices

1. **Always use context managers** for resource-intensive operations
2. **Validate inputs** before passing to evaluators
3. **Use configuration** for environment-specific settings
4. **Handle exceptions** appropriately in production
5. **Monitor resource usage** when running evaluations
6. **Log important events** for debugging and monitoring

## Troubleshooting

### Common Issues

**Q: Configuration not loading**
A: Ensure `src/config/settings.yaml` exists and is valid YAML

**Q: Model adapter not found**
A: Register the adapter with ModelRegistry before use

**Q: Code execution timeout**
A: Adjust timeout value in configuration or ResourceManager

**Q: Memory issues**
A: Lower memory limits or increase available system memory

## Support

For more help, see:

- [README.md](README.md) - Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- GitHub Issues - Report problems or request features
