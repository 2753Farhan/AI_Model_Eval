# **CodeQualBench: Technical Documentation (Microsoft Word Format)**

Here's a comprehensive Microsoft Word-formatted technical documentation that you can copy and paste into Word or any word processor:

---

# **CodeQualBench: Comprehensive AI Code Generation Evaluation Framework**

## **Technical Documentation v2.0**

**Document Version:** 2.0  
**Last Updated:** December 25, 2024  
**Document Status:** Final  
**Classification:** Public  
**Prepared By:** CodeQualBench Team

---

## **Table of Contents**

### **1. Executive Summary**
1.1. Project Overview  
1.2. Business Value  
1.3. Key Differentiators  
1.4. Target Audience

### **2. System Architecture**
2.1. Architectural Overview  
2.2. Component Diagram  
2.3. Data Flow Architecture  
2.4. Deployment Architecture

### **3. Core Components**
3.1. Evaluation Engine  
3.2. Model Integration Layer  
3.3. Metrics Calculation System  
3.4. Error Analysis Framework  
3.5. Model Tuning Pipeline  
3.6. Dashboard Interface

### **4. Advanced Features**
4.1. Perplexity Analysis  
4.2. CodeBLEU Scoring  
4.3. Error Pattern Recognition  
4.4. Automated Model Tuning  
4.5. Real-time Monitoring

### **5. Technical Specifications**
5.1. System Requirements  
5.2. Performance Benchmarks  
5.3. Security Implementation  
5.4. Scalability Features

### **6. Installation & Configuration**
6.1. Prerequisites  
6.2. Step-by-Step Installation  
6.3. Configuration Management  
6.4. Environment Setup

### **7. API Documentation**
7.1. REST API Endpoints  
7.2. WebSocket Interface  
7.3. CLI Commands  
7.4. SDK Integration

### **8. User Guide**
8.1. Getting Started  
8.2. Running Evaluations  
8.3. Analyzing Results  
8.4. Advanced Features

### **9. Developer Guide**
9.1. Architecture Patterns  
9.2. Adding New Models  
9.3. Custom Metrics  
9.4. Extension Points

### **10. Deployment Guide**
10.1. Development Environment  
10.2. Production Deployment  
10.3. Kubernetes Setup  
10.4. Monitoring & Logging

### **11. Troubleshooting**
11.1. Common Issues  
11.2. Performance Tuning  
11.3. Debug Guide  
11.4. Recovery Procedures

### **12. Appendices**
12.1. Glossary of Terms  
12.2. Reference Architecture  
12.3. Performance Metrics  
12.4. Best Practices

---

## **1. Executive Summary**

### **1.1. Project Overview**
CodeQualBench is an enterprise-grade evaluation framework designed to systematically assess, compare, and improve AI-powered code generation models. The framework provides comprehensive metrics, real-time analysis, and automated tuning capabilities for Large Language Models (LLMs) specializing in code generation tasks.

### **1.2. Business Value**
- **Model Selection**: Objective comparison of different AI models
- **Quality Assurance**: Ensure generated code meets quality standards
- **Cost Optimization**: Identify most efficient models for specific tasks
- **Risk Mitigation**: Detect security vulnerabilities in generated code
- **Continuous Improvement**: Automated tuning based on error patterns

### **1.3. Key Differentiators**
1. **Multi-dimensional Evaluation**: Beyond pass/fail to include quality, security, and maintainability
2. **Error-aware Tuning**: Automatically fine-tune models based on failure patterns
3. **Real-time Analysis**: Live monitoring and immediate feedback
4. **Enterprise-ready**: Scalable, secure, and production-tested

### **1.4. Target Audience**
- **AI Researchers**: Model evaluation and comparison
- **Software Engineers**: Integration into development workflows
- **DevOps Teams**: CI/CD pipeline integration
- **Product Managers**: Model selection and performance tracking
- **Security Teams**: Code security analysis

---

## **2. System Architecture**

### **2.1. Architectural Overview**

```
┌─────────────────────────────────────────────────────────┐
│                 Presentation Layer                       │
├─────────────────────────────────────────────────────────┤
│  Web Dashboard │ CLI Interface │ REST API │ WebSocket   │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                Application Layer                         │
├─────────────────────────────────────────────────────────┤
│ Evaluation │ Analysis │ Tuning │ Reporting │ Monitoring │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                Service Layer                             │
├─────────────────────────────────────────────────────────┤
│ Model Mgmt │ Code Exec │ Metrics │ Security │ Storage   │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                Infrastructure Layer                      │
├─────────────────────────────────────────────────────────┤
│  Database  │  Cache   │  Queue  │ Storage  │ Container  │
└─────────────────────────────────────────────────────────┘
```

### **2.2. Component Diagram**

**Figure 1: System Components**

| Component | Purpose | Technologies |
|-----------|---------|--------------|
| **Evaluation Engine** | Coordinates all evaluation activities | Python, AsyncIO |
| **Model Manager** | Handles multiple AI model backends | Ollama, HuggingFace |
| **Sandbox Executor** | Safe code execution environment | Docker, Security Policies |
| **Metrics Calculator** | Computes comprehensive metrics | NumPy, SciPy |
| **Error Analyzer** | Classifies and analyzes failures | Pattern Matching, ML |
| **Tuning Pipeline** | Fine-tunes models based on errors | PyTorch, Transformers |
| **Dashboard** | Web-based visualization | Flask, Plotly, Vue.js |
| **API Gateway** | External interface | FastAPI, WebSocket |

### **2.3. Data Flow Architecture**

**Figure 2: Evaluation Pipeline Flow**

1. **Input**: Problem definitions + Model specifications
2. **Processing**: 
   - Code generation → Secure execution → Metrics calculation
   - Error analysis → Pattern recognition → Tuning dataset creation
3. **Output**: 
   - Comprehensive reports
   - Tuned models
   - Improvement recommendations

### **2.4. Deployment Architecture**

**Figure 3: Production Deployment**

```
Internet → Load Balancer → API Gateway → Microservices
    ↓           ↓              ↓            ↓
           Cache Layer   Database Cluster   Storage
    ↓           ↓              ↓            ↓
       Monitoring Stack   Logging System   Alerting
```

---

## **3. Core Components**

### **3.1. Evaluation Engine**

#### **Primary Responsibilities:**
- Orchestrates complete evaluation pipeline
- Manages resource allocation
- Handles error recovery
- Tracks progress and status

#### **Key Classes:**
- `AIModelEval`: Main orchestrator
- `EvaluationPipeline`: Pipeline management
- `ResourceManager`: Resource allocation
- `ProgressTracker`: Real-time progress monitoring

#### **Configuration:**
```yaml
evaluation:
  max_concurrent: 10
  timeout_seconds: 30
  retry_attempts: 3
  result_persistence: true
```

### **3.2. Model Integration Layer**

#### **Supported Backends:**
1. **Ollama** (Primary): Local model inference
2. **HuggingFace**: Transformer models
3. **OpenAI API**: GPT models
4. **Anthropic**: Claude models
5. **Google**: Gemini models

#### **Model Adapter Pattern:**
```python
class ModelAdapter(ABC):
    @abstractmethod
    async def generate(self, prompt: str, options: dict) -> str:
        pass
    
    @abstractmethod
    async def get_capabilities(self) -> dict:
        pass
```

#### **Model Registry:**
```json
{
  "codellama:7b": {
    "backend": "ollama",
    "parameters": 7000000000,
    "context_window": 4096,
    "capabilities": ["code", "completion"]
  }
}
```

### **3.3. Metrics Calculation System**

#### **Metric Categories:**

**Table 1: Metric Categories**

| Category | Metrics | Purpose |
|----------|---------|---------|
| **Functional** | Pass Rate, Pass@k, Error Rate | Correctness assessment |
| **Quality** | Cyclomatic Complexity, Maintainability Index | Code quality measurement |
| **Performance** | Execution Time, Memory Usage | Efficiency evaluation |
| **Semantic** | CodeBLEU, AST Similarity | Semantic correctness |
| **Confidence** | Perplexity, Entropy | Model uncertainty |

#### **Calculation Pipeline:**
1. Raw results collection
2. Metric computation
3. Normalization
4. Aggregation
5. Reporting

### **3.4. Error Analysis Framework**

#### **Error Classification Hierarchy:**

**Figure 4: Error Types**

```
Errors
├── Syntax Errors (35%)
│   ├── Missing tokens (15%)
│   ├── Indentation (12%)
│   └── Invalid syntax (8%)
├── Semantic Errors (45%)
│   ├── Type errors (20%)
│   ├── Logic errors (15%)
│   └── Name errors (10%)
└── Performance Errors (20%)
    ├── Timeouts (12%)
    └── Memory limits (8%)
```

#### **Error Analysis Process:**
1. **Detection**: Identify error patterns
2. **Classification**: Categorize error type
3. **Analysis**: Find root causes
4. **Correlation**: Link similar errors
5. **Recommendation**: Suggest fixes

### **3.5. Model Tuning Pipeline**

#### **Tuning Workflow:**

**Figure 5: Tuning Pipeline**

```
Collect Errors → Analyze Patterns → Create Dataset
    ↓                ↓                ↓
Fine-tune Model → Evaluate → Deploy → Monitor
```

#### **Tuning Strategies:**
1. **Error-specific Tuning**: Target specific error types
2. **Curriculum Learning**: Easy to hard examples
3. **Contrastive Learning**: Good vs bad examples
4. **Reinforcement Learning**: Reward-based tuning

### **3.6. Dashboard Interface**

#### **Main Sections:**
1. **Dashboard Home**: Overview and key metrics
2. **Model Comparison**: Side-by-side comparison
3. **Error Analysis**: Detailed error breakdown
4. **Tuning Status**: Tuning progress and results
5. **Reports**: Exportable reports and charts

#### **Features:**
- Real-time updates via WebSocket
- Interactive visualizations
- Export functionality
- Custom report generation

---

## **4. Advanced Features**

### **4.1. Perplexity Analysis**

#### **Definition:**
Perplexity measures how "surprised" a language model is by a given sequence of tokens. Lower perplexity indicates the model finds the sequence more predictable.

#### **Calculation:**
```
Perplexity = exp(-1/N * Σ log P(token_i | context_i))
```

#### **Implementation:**
```python
class PerplexityCalculator:
    def calculate(self, code: str, context: str = None) -> dict:
        """
        Returns:
        {
            "perplexity": 15.2,
            "token_perplexities": [12.1, 18.3, ...],
            "confidence": 0.85,
            "high_uncertainty_regions": [...]
        }
        """
```

#### **Use Cases:**
- Identify ambiguous code sections
- Measure model confidence
- Detect potential errors
- Guide model selection

### **4.2. CodeBLEU Scoring**

#### **Components:**
1. **N-gram Match** (25%): Traditional BLEU score
2. **Weighted N-gram** (25%): Syntax-aware matching
3. **AST Match** (25%): Abstract Syntax Tree similarity
4. **Dataflow Match** (25%): Variable usage patterns

#### **Implementation:**
```python
class CodeBLEUScorer:
    def compute(self, hypothesis: str, references: list) -> dict:
        return {
            "codebleu": 0.78,
            "components": {
                "bleu": 0.80,
                "weighted_bleu": 0.75,
                "syntax_match": 0.82,
                "dataflow_match": 0.75
            }
        }
```

#### **Advantages:**
- Better correlation with human judgment
- Language-agnostic
- Syntax-aware
- Semantic understanding

### **4.3. Error Pattern Recognition**

#### **Pattern Types:**
1. **Syntactic Patterns**: Missing parentheses, indentation
2. **Semantic Patterns**: Type mismatches, undefined variables
3. **Logical Patterns**: Off-by-one errors, infinite loops
4. **Performance Patterns**: Timeouts, memory overflows

#### **Recognition Algorithm:**
1. Tokenize error messages
2. Extract error patterns
3. Match against known patterns
4. Cluster similar errors
5. Generate signatures

#### **Database Schema:**
```sql
CREATE TABLE error_patterns (
    id SERIAL PRIMARY KEY,
    pattern_hash VARCHAR(64),
    error_type VARCHAR(50),
    frequency INTEGER,
    model_affected VARCHAR(100),
    suggested_fix TEXT,
    examples JSONB,
    created_at TIMESTAMP
);
```

### **4.4. Automated Model Tuning**

#### **Tuning Pipeline:**
1. **Error Collection**: Gather failed examples
2. **Dataset Creation**: Build training dataset
3. **Model Selection**: Choose base model
4. **Fine-tuning**: Adjust model weights
5. **Evaluation**: Test improvements
6. **Deployment**: Deploy tuned model

#### **Dataset Generation:**
```python
class TuningDataset:
    def create(self, errors: list) -> list:
        return [
            {
                "input": "def func(a, b: return a + b",  # Incorrect
                "output": "def func(a, b): return a + b", # Correct
                "error_type": "missing_parenthesis",
                "difficulty": "easy"
            }
        ]
```

#### **Hyperparameters:**
```yaml
tuning:
  learning_rate: 5e-5
  batch_size: 8
  epochs: 3
  warmup_steps: 100
  evaluation_steps: 50
  save_steps: 1000
```

### **4.5. Real-time Monitoring**

#### **Monitoring Components:**
1. **Metrics Collection**: System and application metrics
2. **Alerting**: Threshold-based alerts
3. **Dashboard**: Real-time visualization
4. **Logging**: Structured logging
5. **Tracing**: Request tracing

#### **Key Metrics:**
```python
monitoring_metrics = {
    "system": ["cpu_usage", "memory_usage", "disk_io"],
    "application": ["request_rate", "error_rate", "latency"],
    "business": ["evaluations_completed", "models_tested"],
    "quality": ["pass_rate", "code_quality_score"]
}
```

#### **Alert Rules:**
```yaml
alerts:
  - name: "High Error Rate"
    condition: "error_rate > 0.1"
    duration: "5m"
    severity: "warning"
    
  - name: "Model Unavailable"
    condition: "model_health == 0"
    duration: "1m"
    severity: "critical"
```

---

## **5. Technical Specifications**

### **5.1. System Requirements**

#### **Minimum Requirements:**
- **CPU**: 4 cores (x86_64)
- **RAM**: 8 GB
- **Storage**: 20 GB
- **OS**: Linux/Windows/macOS
- **Python**: 3.8+
- **Docker**: 20.10+

#### **Recommended Requirements:**
- **CPU**: 8+ cores
- **RAM**: 16+ GB
- **Storage**: 100+ GB SSD
- **GPU**: NVIDIA with 8+ GB VRAM
- **Network**: 100+ Mbps

#### **Dependencies:**
```txt
Core Dependencies:
- Python 3.8+
- Docker Engine
- PostgreSQL 13+
- Redis 6+
- Ollama (for local models)

Python Packages:
- transformers>=4.30.0
- torch>=2.0.0
- flask>=2.3.0
- pandas>=1.5.0
- numpy>=1.24.0
```

### **5.2. Performance Benchmarks**

#### **Table 2: Performance Metrics**

| Metric | Value | Target |
|--------|-------|--------|
| Evaluation Throughput | 100 problems/hour | 500 problems/hour |
| Model Inference Latency | 2-5 seconds | < 2 seconds |
| Code Execution Time | < 30 seconds | < 10 seconds |
| Memory Usage (per eval) | 512 MB | 256 MB |
| Database Query Time | < 100ms | < 50ms |

#### **Scaling Characteristics:**
- **Linear scaling** with CPU cores
- **Memory-bound** for large models
- **I/O bound** for database operations
- **Network-bound** for API calls

### **5.3. Security Implementation**

#### **Security Layers:**

**Figure 6: Security Architecture**

```
┌─────────────────────────────────┐
│      Application Security        │
├─────────────────────────────────┤
│ Authentication │ Authorization  │
└─────────────────────────────────┘
                │
┌─────────────────────────────────┐
│        Runtime Security          │
├─────────────────────────────────┤
│   Sandboxing  │  Resource Limits│
└─────────────────────────────────┘
                │
┌─────────────────────────────────┐
│      Infrastructure Security     │
├─────────────────────────────────┤
│   Network     │   Data          │
└─────────────────────────────────┘
```

#### **Security Features:**
1. **Code Execution**: Docker containers with resource limits
2. **Authentication**: JWT-based authentication
3. **Authorization**: Role-based access control
4. **Data Encryption**: TLS for transit, encryption at rest
5. **Audit Logging**: Comprehensive activity logging

#### **Security Policies:**
```python
security_policies = {
    "code_execution": {
        "max_memory": "512m",
        "max_cpu": "0.5",
        "network_disabled": True,
        "readonly_filesystem": True,
        "user_namespace": True
    },
    "api_security": {
        "rate_limiting": "100 requests/minute",
        "input_validation": True,
        "output_sanitization": True
    }
}
```

### **5.4. Scalability Features**

#### **Horizontal Scaling:**
```yaml
# Kubernetes deployment for horizontal scaling
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

#### **Database Scaling:**
```sql
-- Partitioned tables for large datasets
CREATE TABLE evaluation_results PARTITION BY RANGE (created_at);

-- Read replicas for query offloading
CREATE SUBSCRIPTION evaluation_readonly 
CONNECTION 'host=replica dbname=codequal'
PUBLICATION evaluation_updates;
```

#### **Caching Strategy:**
```python
# Multi-level caching
cache_layers = {
    "L1": {"type": "memory", "size": "1GB", "ttl": "60s"},
    "L2": {"type": "redis", "size": "10GB", "ttl": "3600s"},
    "L3": {"type": "database", "ttl": "86400s"}
}
```

---

## **6. Installation & Configuration**

### **6.1. Prerequisites**

#### **System Requirements Checklist:**
- [ ] Python 3.8 or higher installed
- [ ] Docker Engine running
- [ ] 8+ GB free disk space
- [ ] 8+ GB RAM available
- [ ] Network connectivity

#### **Software Installation:**
```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo systemctl start docker
sudo systemctl enable docker

# Install Python dependencies
sudo apt-get update
sudo apt-get install python3.9 python3-pip python3-venv
```

### **6.2. Step-by-Step Installation**

#### **Step 1: Clone Repository**
```bash
git clone https://github.com/codequalbench/codequalbench.git
cd codequalbench
```

#### **Step 2: Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

#### **Step 3: Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

#### **Step 4: Configure Environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

#### **Step 5: Initialize Database**
```bash
python scripts/init_database.py
```

#### **Step 6: Pull AI Models**
```bash
# Pull required models
ollama pull codellama:7b
ollama pull starcoder:1b

# Verify models
ollama list
```

#### **Step 7: Start Services**
```bash
# Start database and cache
docker-compose up -d postgres redis

# Run initial evaluation
python baseline_analysis.py

# Start dashboard
python dashboard/app.py
```

### **6.3. Configuration Management**

#### **Main Configuration File (`config/settings.yaml`):**
```yaml
# Paths configuration
paths:
  data_dir: "data/human_eval_repo"
  results_dir: "results"
  cache_dir: "cache"
  log_dir: "logs"

# Models configuration
models:
  ollama_base_url: "http://localhost:11434"
  default_models:
    - "codellama:7b"
    - "starcoder:1b"
  hf_api_key: ""  # Optional

# Evaluation configuration
evaluation:
  num_samples_per_task: 5
  timeout_seconds: 30
  max_memory_mb: 512
  prompt_strategies: ["zero_shot", "few_shot"]

# Metrics configuration
metrics:
  enable_perplexity: true
  enable_codebleu: true
  enable_error_analysis: true

# Dashboard configuration
dashboard:
  host: "0.0.0.0"
  port: 5000
  debug: false
  secret_key: "change-this-in-production"
```

#### **Environment Variables:**
```bash
# Required
export DATABASE_URL="postgresql://user:pass@localhost:5432/codequal"
export REDIS_URL="redis://localhost:6379"
export OLLAMA_HOST="http://localhost:11434"

# Optional
export LOG_LEVEL="INFO"
export MAX_WORKERS="4"
export CACHE_TTL="3600"
```

### **6.4. Environment Setup**

#### **Development Environment:**
```bash
# Using Docker Compose
docker-compose -f docker-compose.dev.yml up -d

# Run tests
pytest tests/ -v --cov=src

# Start development server
python dashboard/app.py --debug
```

#### **Production Environment:**
```bash
# Using production Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
alembic upgrade head

# Start production server
gunicorn --workers 4 --bind 0.0.0.0:5000 dashboard.app:app
```

#### **Kubernetes Deployment:**
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/config.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

---

## **7. API Documentation**

### **7.1. REST API Endpoints**

#### **Base URL:** `https://api.codequalbench.com/v1`

#### **Authentication:**
```http
POST /auth/login
Content-Type: application/json

{
    "username": "admin",
    "password": "password123"
}

Response:
{
    "access_token": "eyJ0eXAiOiJKV1Qi...",
    "token_type": "bearer",
    "expires_in": 3600
}
```

#### **Evaluation Management:**

**Create Evaluation:**
```http
POST /evaluations
Authorization: Bearer {token}
Content-Type: application/json

{
    "models": ["codellama:7b", "starcoder:1b"],
    "problems": ["HumanEval/0", "HumanEval/1"],
    "config": {
        "num_samples": 5,
        "timeout": 30,
        "metrics": ["perplexity", "codebleu"]
    }
}

Response:
{
    "evaluation_id": "eval_123abc",
    "status": "pending",
    "estimated_completion": "2024-12-25T12:00:00Z",
    "progress_url": "/evaluations/eval_123abc/progress"
}
```

**Get Evaluation Status:**
```http
GET /evaluations/{evaluation_id}
Authorization: Bearer {token}

Response:
{
    "evaluation_id": "eval_123abc",
    "status": "running",
    "progress": 65,
    "models_completed": ["codellama:7b"],
    "started_at": "2024-12-25T10:00:00Z",
    "estimated_completion": "2024-12-25T12:00:00Z"
}
```

**Get Evaluation Results:**
```http
GET /evaluations/{evaluation_id}/results
Authorization: Bearer {token}

Response:
{
    "summary": {
        "total_problems": 164,
        "total_evaluations": 820,
        "overall_pass_rate": 0.72,
        "average_execution_time": 2.5
    },
    "by_model": {
        "codellama:7b": {
            "pass_rate": 0.75,
            "avg_codebleu": 0.68,
            "common_errors": ["missing_parenthesis", "type_error"]
        }
    },
    "detailed_results": [...]
}
```

#### **Model Management:**

**List Available Models:**
```http
GET /models
Authorization: Bearer {token}

Response:
{
    "models": [
        {
            "name": "codellama:7b",
            "backend": "ollama",
            "parameters": 7000000000,
            "context_window": 4096,
            "status": "available"
        }
    ]
}
```

**Test Model Connection:**
```http
POST /models/{model_name}/test
Authorization: Bearer {token}
Content-Type: application/json

{
    "prompt": "def hello():",
    "max_tokens": 50
}

Response:
{
    "success": true,
    "response": "def hello():\n    return 'world'",
    "latency_ms": 2450,
    "tokens_generated": 8
}
```

#### **Error Analysis:**

**Analyze Errors:**
```http
POST /errors/analyze
Authorization: Bearer {token}
Content-Type: application/json

{
    "evaluation_ids": ["eval_123abc", "eval_456def"],
    "analysis_type": "deep",
    "group_by": ["model", "error_type"]
}

Response:
{
    "summary": {
        "total_errors": 150,
        "unique_patterns": 42,
        "most_common_error": "missing_parenthesis"
    },
    "patterns": [...],
    "recommendations": [...]
}
```

### **7.2. WebSocket Interface**

#### **Connection:**
```javascript
const ws = new WebSocket('wss://api.codequalbench.com/ws');

ws.onopen = () => {
    ws.send(JSON.stringify({
        type: 'auth',
        token: 'eyJ0eXAiOiJKV1Qi...'
    }));
    
    ws.send(JSON.stringify({
        type: 'subscribe',
        channel: 'evaluation:eval_123abc'
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Update:', data);
};
```

#### **Message Types:**

**Table 3: WebSocket Message Types**

| Type | Purpose | Data Structure |
|------|---------|----------------|
| `progress` | Evaluation progress | `{progress: 65, current_model: "codellama:7b"}` |
| `result` | Individual result | `{problem_id: "HumanEval/0", passed: true}` |
| `error` | Error occurred | `{type: "timeout", message: "Execution timed out"}` |
| `complete` | Evaluation complete | `{summary: {...}, metrics: {...}}` |
| `tuning_update` | Tuning progress | `{stage: "training", progress: 50}` |

### **7.3. CLI Commands**

#### **Basic Commands:**
```bash
# Show help
codequalbench --help

# Run evaluation
codequalbench evaluate \
    --models codellama:7b,starcoder:1b \
    --problems 0-10 \
    --samples 5 \
    --output results.json

# Analyze results
codequalbench analyze \
    --input results.json \
    --metrics all \
    --report html

# Tune model
codequalbench tune \
    --model codellama:7b \
    --errors missing_parenthesis,type_error \
    --epochs 3 \
    --output tuned-model

# Start dashboard
codequalbench dashboard \
    --host 0.0.0.0 \
    --port 5000 \
    --debug
```

#### **Advanced Commands:**
```bash
# Benchmark models
codequalbench benchmark \
    --models all \
    --iterations 10 \
    --warmup 3 \
    --output benchmark.csv

# Export data
codequalbench export \
    --format csv \
    --include metrics,errors,raw \
    --output export.zip

# Monitor system
codequalbench monitor \
    --metrics cpu,memory,disk,network \
    --interval 5 \
    --duration 300
```

### **7.4. SDK Integration**

#### **Python SDK:**
```python
from codequalbench import CodeQualBench

# Initialize client
client = CodeQualBench(
    api_key="your-api-key",
    base_url="https://api.codequalbench.com"
)

# Run evaluation
evaluation = client.evaluations.create(
    models=["codellama:7b", "starcoder:1b"],
    problem_ids=["HumanEval/0", "HumanEval/1"],
    config={
        "num_samples": 5,
        "metrics": ["perplexity", "codebleu"]
    }
)

# Monitor progress
for update in evaluation.stream_updates():
    print(f"Progress: {update.progress}%")
    if update.status == "completed":
        break

# Get results
results = evaluation.get_results()
print(f"Pass rate: {results.summary.pass_rate}")

# Analyze errors
analysis = client.errors.analyze(
    evaluation_ids=[evaluation.id],
    analysis_type="deep"
)

# Tune model
tuning_job = client.tuning.create(
    base_model="codellama:7b",
    error_types=["missing_parenthesis"],
    config={"epochs": 3}
)
```

#### **JavaScript SDK:**
```javascript
import { CodeQualBench } from 'codequalbench-sdk';

const client = new CodeQualBench({
    apiKey: 'your-api-key',
    baseURL: 'https://api.codequalbench.com'
});

// Run evaluation
const evaluation = await client.evaluations.create({
    models: ['codellama:7b', 'starcoder:1b'],
    problems: ['HumanEval/0', 'HumanEval/1'],
    config: {
        numSamples: 5,
        metrics: ['perplexity', 'codebleu']
    }
});

// Stream updates
const stream = evaluation.streamUpdates();
for await (const update of stream) {
    console.log(`Progress: ${update.progress}%`);
    if (update.status === 'completed') break;
}

// Get results
const results = await evaluation.getResults();
console.log(`Pass rate: ${results.summary.pass_rate}`);
```

---

## **8. User Guide**

### **8.1. Getting Started**

#### **Quick Start Guide:**
1. **Install CodeQualBench**
   ```bash
   pip install codequalbench
   ```

2. **Set up environment**
   ```bash
   codequalbench init
   ```

3. **Pull required models**
   ```bash
   ollama pull codellama:7b
   ```

4. **Run first evaluation**
   ```bash
   codequalbench evaluate --quick
   ```

5. **View results**
   ```bash
   codequalbench dashboard
   ```

#### **First Evaluation Example:**
```python
import codequalbench as cqb

# Initialize
cqb.init(api_key="your-key")

# Run simple evaluation
results = cqb.evaluate(
    models=["codellama:7b"],
    problems=["HumanEval/0", "HumanEval/1"],
    samples=3
)

print(f"Overall pass rate: {results.pass_rate:.2%}")
print(f"Average execution time: {results.avg_execution_time:.2f}s")
```

### **8.2. Running Evaluations**

#### **Basic Evaluation:**
```bash
# Evaluate single model
codequalbench evaluate \
    --model codellama:7b \
    --problems 0-50 \
    --samples 5 \
    --timeout 30

# Compare multiple models
codequalbench evaluate \
    --models codellama:7b,starcoder:1b,llama2:7b \
    --problems all \
    --samples 3 \
    --parallel
```

#### **Advanced Evaluation Options:**
```bash
# With specific metrics
codequalbench evaluate \
    --model codellama:7b \
    --metrics perplexity,codebleu,security \
    --output detailed.json

# With custom prompts
codequalbench evaluate \
    --model codellama:7b \
    --prompt-strategy few_shot \
    --few-shot-examples examples.json

# With resource limits
codequalbench evaluate \
    --model codellama:7b \
    --max-memory 1024 \
    --max-cpu 2 \
    --max-time 3600
```

#### **Evaluation Configuration File:**
```yaml
# evaluation_config.yaml
models:
  - codellama:7b
  - starcoder:1b

problems:
  range: 0-100
  filter:
    difficulty: ["easy", "medium"]
    category: ["algorithms", "data_structures"]

evaluation:
  samples_per_problem: 5
  timeout_seconds: 30
  max_memory_mb: 512
  parallel_execution: true

metrics:
  enable:
    - perplexity
    - codebleu
    - security_analysis
    - quality_metrics

output:
  format: json
  include_raw: true
  save_individual: true
```

### **8.3. Analyzing Results**

#### **Basic Analysis:**
```bash
# Show summary
codequalbench analyze summary --input results.json

# Compare models
codequalbench analyze compare \
    --input results.json \
    --by metric

# Find common errors
codequalbench analyze errors \
    --input results.json \
    --top 10
```

#### **Advanced Analysis:**
```bash
# Correlation analysis
codequalbench analyze correlate \
    --input results.json \
    --variables pass_rate,perplexity,codebleu

# Trend analysis
codequalbench analyze trends \
    --input results1.json,results2.json,results3.json \
    --group-by model

# Generate report
codequalbench analyze report \
    --input results.json \
    --format html \
    --output report.html \
    --template professional
```

#### **Interactive Analysis:**
```python
import pandas as pd
import plotly.express as px

# Load results
results = pd.read_json('results.json')

# Create visualization
fig = px.scatter(
    results,
    x='perplexity',
    y='pass_rate',
    color='model',
    size='execution_time',
    hover_data=['problem_id', 'error_type']
)

fig.update_layout(
    title='Model Performance: Perplexity vs Pass Rate',
    xaxis_title='Perplexity (lower is better)',
    yaxis_title='Pass Rate'
)

fig.show()
```

### **8.4. Advanced Features**

#### **Model Tuning:**
```bash
# Tune model for specific errors
codequalbench tune \
    --model codellama:7b \
    --error-types missing_parenthesis,type_error \
    --epochs 3 \
    --learning-rate 5e-5

# Continuous tuning
codequalbench tune continuous \
    --model codellama:7b \
    --monitor-endpoint /api/errors \
    --update-interval 3600

# Evaluate tuned model
codequalbench evaluate \
    --model tuned-codellama \
    --compare-with original
```

#### **Custom Metrics:**
```python
# Define custom metric
from codequalbench.metrics import BaseMetric

class CustomMetric(BaseMetric):
    def calculate(self, code: str, reference: str = None) -> float:
        # Your custom calculation
        return custom_score
    
    def get_metadata(self) -> dict:
        return {
            "name": "custom_metric",
            "description": "Custom code quality metric",
            "range": [0, 1],
            "higher_is_better": True
        }

# Register metric
cqb.metrics.register(CustomMetric())

# Use in evaluation
results = cqb.evaluate(
    models=["codellama:7b"],
    metrics=["custom_metric", "perplexity"]
)
```

#### **Integration with CI/CD:**
```yaml
# .github/workflows/code-quality.yml
name: Code Quality Evaluation

on:
  pull_request:
    branches: [main]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up CodeQualBench
      uses: codequalbench/setup-action@v1
      with:
        api-key: ${{ secrets.CQB_API_KEY }}
    
    - name: Evaluate generated code
      run: |
        codequalbench evaluate \
          --model codellama:7b \
          --files "**/*.py" \
          --threshold 0.7
    
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: evaluation-results
        path: results.json
    
    - name: Check quality gate
      run: |
        if [ $(jq '.summary.pass_rate' results.json) -lt 0.7 ]; then
          echo "Quality gate failed"
          exit 1
        fi
```

---

## **9. Developer Guide**

### **9.1. Architecture Patterns**

#### **Plugin Architecture:**
```python
# Plugin interface
class Plugin(ABC):
    @abstractmethod
    def initialize(self, context: dict):
        pass
    
    @abstractmethod
    def execute(self, data: dict) -> dict:
        pass
    
    @abstractmethod
    def cleanup(self):
        pass

# Plugin registry
class PluginRegistry:
    def __init__(self):
        self.plugins = {}
    
    def register(self, name: str, plugin_class):
        self.plugins[name] = plugin_class
    
    def get_plugin(self, name: str) -> Plugin:
        return self.plugins[name]()
```

#### **Strategy Pattern (Prompt Strategies):**
```python
class PromptStrategy(ABC):
    @abstractmethod
    def format_prompt(self, problem: dict) -> str:
        pass

class ZeroShotStrategy(PromptStrategy):
    def format_prompt(self, problem: dict) -> str:
        return problem["prompt"]

class FewShotStrategy(PromptStrategy):
    def __init__(self, examples: list):
        self.examples = examples
    
    def format_prompt(self, problem: dict) -> str:
        examples_text = "\n\n".join(self.examples)
        return f"{examples_text}\n\n{problem['prompt']}"

# Strategy factory
class PromptStrategyFactory:
    @staticmethod
    def create(strategy_name: str, **kwargs) -> PromptStrategy:
        strategies = {
            "zero_shot": ZeroShotStrategy,
            "few_shot": FewShotStrategy,
            "chain_of_thought": ChainOfThoughtStrategy
        }
        return strategies[strategy_name](**kwargs)
```

#### **Observer Pattern (Real-time Updates):**
```python
class Observer(ABC):
    @abstractmethod
    def update(self, event: dict):
        pass

class Subject:
    def __init__(self):
        self.observers = []
    
    def attach(self, observer: Observer):
        self.observers.append(observer)
    
    def detach(self, observer: Observer):
        self.observers.remove(observer)
    
    def notify(self, event: dict):
        for observer in self.observers:
            observer.update(event)

class ProgressObserver(Observer):
    def update(self, event: dict):
        if event["type"] == "progress":
            print(f"Progress: {event['progress']}%")

class LogObserver(Observer):
    def update(self, event: dict):
        logger.info(f"Event: {event}")
```

### **9.2. Adding New Models**

#### **Step 1: Create Model Adapter**
```python
from codequalbench.models import BaseModelAdapter

class NewModelAdapter(BaseModelAdapter):
    def __init__(self, config: dict):
        super().__init__(config)
        self.client = self._initialize_client(config)
    
    def _initialize_client(self, config: dict):
        # Initialize model client
        return NewModelClient(
            api_key=config.get("api_key"),
            endpoint=config.get("endpoint")
        )
    
    async def generate(self, prompt: str, options: dict = None) -> dict:
        options = options or {}
        
        response = await self.client.generate(
            prompt=prompt,
            max_tokens=options.get("max_tokens", 512),
            temperature=options.get("temperature", 0.7)
        )
        
        return {
            "text": response.text,
            "tokens": response.tokens,
            "latency": response.latency,
            "model": self.config["name"]
        }
    
    async def get_capabilities(self) -> dict:
        return {
            "max_tokens": 4096,
            "supports_code": True,
            "languages": ["python", "javascript", "java"],
            "context_window": 8192
        }
```

#### **Step 2: Register Model**
```python
# In models/__init__.py
from .new_model import NewModelAdapter

MODEL_ADAPTERS = {
    "new_model": NewModelAdapter,
    # ... existing adapters
}

# In configuration
models:
  custom_models:
    - name: "new_model"
      adapter: "new_model"
      config:
        api_key: "${NEW_MODEL_API_KEY}"
        endpoint: "https://api.newmodel.com/v1"
```

#### **Step 3: Test Integration**
```python
import pytest
from codequalbench.models import ModelManager

@pytest.mark.asyncio
async def test_new_model_integration():
    config = {
        "models": {
            "custom_models": [
                {
                    "name": "new_model",
                    "adapter": "new_model",
                    "config": {"api_key": "test-key"}
                }
            ]
        }
    }
    
    manager = ModelManager(config)
    
    # Test generation
    result = await manager.generate(
        model="new_model",
        prompt="def hello():"
    )
    
    assert "text" in result
    assert result["model"] == "new_model"
```

### **9.3. Custom Metrics**

#### **Creating Custom Metric:**
```python
from codequalbench.metrics import BaseMetric, MetricResult
from typing import Dict, Any

class CustomCodeMetric(BaseMetric):
    """Example custom metric for code quality"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.name = "custom_metric"
        self.description = "Custom code quality assessment"
        self.higher_is_better = True
        self.range = (0, 1)
    
    async def calculate(self, 
                       generated_code: str, 
                       reference_code: str = None,
                       metadata: Dict[str, Any] = None) -> MetricResult:
        """Calculate custom metric value"""
        
        # Your calculation logic
        score = self._calculate_score(generated_code, reference_code)
        
        # Additional metadata
        details = {
            "components": self._analyze_components(generated_code),
            "confidence": self._calculate_confidence(score),
            "breakdown": self._get_breakdown(generated_code)
        }
        
        return MetricResult(
            value=score,
            details=details,
            metadata={
                "metric_name": self.name,
                "calculation_time": time.time() - start_time,
                "config_used": self.config
            }
        )
    
    def _calculate_score(self, code: str, reference: str = None) -> float:
        """Core scoring logic"""
        # Implement your scoring algorithm
        pass
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate metric configuration"""
        required = ["threshold", "weights"]
        return all(key in config for key in required)
```

#### **Registering Custom Metric:**
```python
# In your application setup
from codequalbench import CodeQualBench
from my_metrics import CustomCodeMetric

# Initialize
cqb = CodeQualBench()

# Register metric
cqb.metrics.register(
    name="custom_quality",
    metric_class=CustomCodeMetric,
    config={
        "threshold": 0.7,
        "weights": {"complexity": 0.3, "readability": 0.7}
    }
)

# Use in evaluation
results = cqb.evaluate(
    models=["codellama:7b"],
    metrics=["custom_quality", "perplexity", "codebleu"]
)
```

### **9.4. Extension Points**

#### **Extension Points Overview:**

**Table 4: Available Extension Points**

| Extension Point | Interface | Purpose | Example |
|----------------|-----------|---------|---------|
| Model Adapter | `BaseModelAdapter` | Add new AI models | New LLM provider |
| Metric | `BaseMetric` | Add new metrics | Custom quality score |
| Prompt Strategy | `PromptStrategy` | New prompting techniques | Custom few-shot |
| Error Analyzer | `BaseErrorAnalyzer` | Custom error analysis | Domain-specific errors |
| Output Formatter | `BaseFormatter` | New output formats | Custom report format |
| Storage Backend | `StorageBackend` | Different storage | S3, Azure Blob |

#### **Creating Extension Point:**
```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class ExtensionPoint(ABC):
    """Base class for all extension points"""
    
    @abstractmethod
    def initialize(self, context: Dict[str, Any]):
        """Initialize extension with context"""
        pass
    
    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Execute extension logic"""
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Get extension metadata"""
        pass

class ExtensionRegistry:
    """Registry for managing extensions"""
    
    def __init__(self):
        self.extensions = {}
    
    def register(self, 
                point_name: str, 
                extension_class: type,
                config: Dict[str, Any] = None):
        """Register new extension"""
        
        if point_name not in self.extensions:
            self.extensions[point_name] = []
        
        self.extensions[point_name].append({
            "class": extension_class,
            "config": config or {}
        })
    
    def get_extensions(self, point_name: str) -> list:
        """Get all extensions for a point"""
        return self.extensions.get(point_name, [])
```

#### **Using Extensions:**
```python
# Register extensions at startup
registry = ExtensionRegistry()

registry.register(
    point_name="metric",
    extension_class=CustomCodeMetric,
    config={"threshold": 0.8}
)

registry.register(
    point_name="model_adapter",
    extension_class=NewModelAdapter,
    config={"api_key": "xxx"}
)

# Use extensions
for ext_info in registry.get_extensions("metric"):
    metric = ext_info["class"](ext_info["config"])
    score = metric.calculate(generated_code)
    print(f"{metric.name}: {score}")
```

---

## **10. Deployment Guide**

### **10.1. Development Environment**

#### **Local Development Setup:**
```bash
# Clone repository
git clone https://github.com/codequalbench/codequalbench.git
cd codequalbench

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Set up development database
docker-compose -f docker-compose.dev.yml up -d

# Run tests
pytest tests/ -v

# Start development server
python dashboard/app.py --debug --reload
```

#### **Development Configuration:**
```yaml
# config/development.yaml
debug: true
testing: true

database:
  url: postgresql://postgres:postgres@localhost:5432/codequal_dev

cache:
  url: redis://localhost:6379/1

models:
  ollama_base_url: http://localhost:11434
  
logging:
  level: DEBUG
  file: logs/development.log
```

### **10.2. Production Deployment**

#### **Docker-based Deployment:**
```dockerfile
# Dockerfile
FROM python:3.9-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Production stage
FROM python:3.9-slim

WORKDIR /app

# Copy dependencies
COPY --from=builder /root/.local /root/.local

# Copy application
COPY . .

# Create non-root user
RUN groupadd -r codequal && useradd -r -g codequal codequal
USER codequal

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/health')"

EXPOSE 5000

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "dashboard.app:app"]
```

#### **Docker Compose Production:**
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    build: .
    image: codequalbench:latest
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/codequal
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./results:/app/results
      - ./logs:/app/logs
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1'
        reservations:
          memory: 1G
          cpus: '0.5'
    restart: unless-stopped
  
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: codequal
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
    restart: unless-stopped
  
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### **10.3. Kubernetes Setup**

#### **Namespace Configuration:**
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: codequal
  labels:
    name: codequal
```

#### **ConfigMap and Secrets:**
```yaml
# k8s/config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: codequal-config
  namespace: codequal
data:
  database.host: postgres.codequal.svc.cluster.local
  redis.host: redis-master.codequal.svc.cluster.local
  ollama.url: http://ollama:11434
  logging.level: INFO
---
apiVersion: v1
kind: Secret
metadata:
  name: codequal-secrets
  namespace: codequal
type: Opaque
data:
  database.password: ${BASE64_ENCODED_PASSWORD}
  redis.password: ${BASE64_ENCODED_REDIS_PASSWORD}
  secret.key: ${BASE64_ENCODED_SECRET_KEY}
```

#### **Deployment Configuration:**
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: codequalbench
  namespace: codequal
spec:
  replicas: 3
  selector:
    matchLabels:
      app: codequalbench
  template:
    metadata:
      labels:
        app: codequalbench
    spec:
      serviceAccountName: codequal-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: app
        image: codequalbench:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 5000
        envFrom:
        - configMapRef:
            name: codequal-config
        - secretRef:
            name: codequal-secrets
        env:
        - name: DATABASE_URL
          value: postgresql://$(DATABASE_USER):$(DATABASE_PASSWORD)@$(DATABASE_HOST):5432/codequal
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: storage
          mountPath: /app/results
          subPath: results
        - name: storage
          mountPath: /app/logs
          subPath: logs
      volumes:
      - name: storage
        persistentVolumeClaim:
          claimName: codequal-storage-pvc
```

### **10.4. Monitoring & Logging**

#### **Logging Configuration:**
```python
# logging_config.py
import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "json",
            "level": "DEBUG"
        }
    },
    "loggers": {
        "codequalbench": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

#### **Monitoring Setup:**
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'codequalbench'
    static_configs:
      - targets: ['codequalbench:5000']
    metrics_path: '/metrics'
    
  - job_name: 'codequalbench-db'
    static_configs:
      - targets: ['postgres-exporter:9187']
      
  - job_name: 'codequalbench-redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

#### **Alert Rules:**
```yaml
# monitoring/alerts.yml
groups:
  - name: codequalbench
    rules:
      - alert: HighErrorRate
        expr: rate(codequal_errors_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} per second"
      
      - alert: ServiceDown
        expr: up{job="codequalbench"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.instance }} is not responding"
```

#### **Dashboard Panels:**
```json
{
  "dashboard": {
    "title": "CodeQualBench Monitoring",
    "panels": [
      {
        "title": "Evaluation Throughput",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(codequal_evaluations_total[5m])",
            "legendFormat": "{{model}}"
          }
        ]
      },
      {
        "title": "Success Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "codequal_success_rate",
            "format": "percent"
          }
        ],
        "thresholds": "70,85"
      }
    ]
  }
}
```

---

## **11. Troubleshooting**

### **11.1. Common Issues**

#### **Issue: Docker Container Fails to Start**

**Symptoms:**
- Container exits immediately
- "Permission denied" errors
- Port already in use

**Solutions:**
```bash
# Check Docker logs
docker logs <container_id>

# Check port conflicts
sudo netstat -tulpn | grep :5000

# Check Docker daemon
sudo systemctl status docker

# Run with more memory
docker run --memory="2g" codequalbench

# Fix permission issues
sudo chown -R $USER:$USER ./data
sudo chmod -R 755 ./data
```

#### **Issue: Model Inference Timeout**

**Symptoms:**
- Model generation takes too long
- "Timeout" errors in logs
- High CPU/memory usage

**Solutions:**
```python
# Increase timeout in config
config["evaluation"]["timeout_seconds"] = 60

# Implement retry logic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def generate_with_retry(prompt, model):
    return await model_manager.generate_code(prompt, model)

# Reduce model parameters
config["models"]["default_models"] = ["codellama:7b", "starcoder:1b"]
```

#### **Issue: High Memory Usage**

**Symptoms:**
- System becomes slow
- "Out of memory" errors
- Container killed by OOM killer

**Solutions:**
```python
# Implement memory monitoring
import psutil
import resource

def limit_memory(max_memory_mb):
    """Set memory limit for current process"""
    max_memory_bytes = max_memory_mb * 1024 * 1024
    resource.setrlimit(
        resource.RLIMIT_AS,
        (max_memory_bytes, max_memory_bytes)
    )

# Use in evaluation
limit_memory(512)  # 512MB limit

# Implement garbage collection
import gc
gc.collect()

# Use streaming for large results
async def stream_evaluation():
    for result in evaluation_results:
        yield result
        gc.collect()
```

#### **Issue: Database Connection Problems**

**Symptoms:**
- "Connection refused" errors
- Database queries timeout
- Connection pool exhausted

**Solutions:**
```python
# Configure connection pooling
DATABASE_POOL_SETTINGS = {
    "pool_size": 20,
    "max_overflow": 30,
    "pool_timeout": 30,
    "pool_recycle": 3600
}

# Implement connection retry
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(OperationalError)
)
def get_database_connection():
    return create_engine(DATABASE_URL, **DATABASE_POOL_SETTINGS)

# Monitor connection usage
SELECT count(*) FROM pg_stat_activity WHERE datname = 'codequal';
```

### **11.2. Performance Tuning**

#### **Database Performance:**
```sql
-- Create indexes for common queries
CREATE INDEX idx_evaluations_created ON evaluations(created_at DESC);
CREATE INDEX idx_metrics_model ON metrics(model_name, created_at);
CREATE INDEX idx_errors_type ON errors(error_type, created_at);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM evaluations WHERE created_at > NOW() - INTERVAL '1 day';

-- Vacuum and analyze
VACUUM ANALYZE evaluations;
VACUUM ANALYZE metrics;

-- Partition large tables
CREATE TABLE evaluations_partitioned PARTITION BY RANGE (created_at);
```

#### **Application Performance:**
```python
# Implement caching
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def compute_expensive_metric(code_hash: str) -> float:
    # Expensive computation
    pass

def get_code_hash(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()

# Use async I/O
async def process_evaluations(evaluations):
    tasks = []
    for evaluation in evaluations:
        task = asyncio.create_task(process_single(evaluation))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# Batch database operations
async def batch_insert(results):
    async with database.transaction():
        await database.execute_many(
            "INSERT INTO results VALUES ($1, $2, $3)",
            [(r.id, r.model, r.score) for r in results]
        )
```

#### **Memory Optimization:**
```python
# Use generators for large datasets
def read_large_file(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            yield json.loads(line)

# Clear unused variables
import gc
def process_data(data):
    result = expensive_operation(data)
    # Clear large intermediate variables
    del data
    gc.collect()
    return result

# Use memory-efficient data structures
from collections import deque
results_buffer = deque(maxlen=1000)  # Fixed size buffer
```

### **11.3. Debug Guide**

#### **Enabling Debug Mode:**
```python
# Set debug environment variable
import os
os.environ["DEBUG"] = "true"

# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug endpoints
@app.route('/debug/memory')
def debug_memory():
    import psutil
    process = psutil.Process()
    return {
        "memory_mb": process.memory_info().rss / 1024 / 1024,
        "cpu_percent": process.cpu_percent(),
        "open_files": len(process.open_files()),
        "threads": process.num_threads()
    }

@app.route('/debug/connections')
def debug_connections():
    import psutil
    connections = psutil.net_connections()
    return {
        "total": len(connections),
        "by_type": dict(Counter(c.type for c in connections))
    }
```

#### **Tracing Execution:**
```python
# Add execution tracing
import traceback
import time

def trace_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f"{func.__name__} executed in {execution_time:.2f}s")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {e}")
            logger.debug(traceback.format_exc())
            raise
    return wrapper

# Use decorator
@trace_execution
def evaluate_model(model, problem):
    # Evaluation logic
    pass
```

#### **Profiling:**
```python
# Profile CPU usage
import cProfile
import pstats

def profile_function(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 functions
        
        return result
    return wrapper

# Profile memory usage
from memory_profiler import profile

@profile
def memory_intensive_operation():
    # Your code here
    pass
```

### **11.4. Recovery Procedures**

#### **Database Recovery:**
```bash
# Backup database
pg_dump -U postgres -d codequal > backup_$(date +%Y%m%d).sql

# Restore from backup
psql -U postgres -d codequal < backup_20241225.sql

# Check database health
psql -U postgres -d codequal -c "SELECT pg_is_in_recovery();"

# Rebuild indexes
psql -U postgres -d codequal -c "REINDEX DATABASE codequal;"

# Check for corruption
psql -U postgres -d codequal -c "VACUUM VERBOSE ANALYZE;"
```

#### **Application Recovery:**
```python
# Implement graceful shutdown
import signal
import asyncio

async def graceful_shutdown():
    """Gracefully shutdown application"""
    logger.info("Starting graceful shutdown...")
    
    # Close database connections
    await database.close()
    
    # Close Redis connections
    await redis.close()
    
    # Cancel background tasks
    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():
            task.cancel()
    
    logger.info("Graceful shutdown complete")

# Handle signals
signal.signal(signal.SIGTERM, lambda s, f: asyncio.create_task(graceful_shutdown()))
signal.signal(signal.SIGINT, lambda s, f: asyncio.create_task(graceful_shutdown()))
```

#### **Data Recovery:**
```python
# Implement data validation
def validate_data_integrity():
    """Validate data integrity"""
    
    checks = [
        check_database_consistency(),
        check_file_system_integrity(),
        check_cache_consistency()
    ]
    
    return all(checks)

def check_database_consistency():
    """Check database consistency"""
    try:
        # Check foreign key constraints
        result = database.execute("""
            SELECT COUNT(*) as violations
            FROM evaluations e
            LEFT JOIN models m ON e.model_id = m.id
            WHERE m.id IS NULL
        """)
        
        return result["violations"] == 0
        
    except Exception as e:
        logger.error(f"Database consistency check failed: {e}")
        return False

# Implement data repair
def repair_corrupted_data():
    """Repair corrupted data"""
    
    # Backup current state
    create_backup()
    
    # Attempt repair
    try:
        repair_database()
        repair_files()
        clear_cache()
        
        # Verify repair
        if validate_data_integrity():
            logger.info("Data repair successful")
            return True
        else:
            logger.error("Data repair failed")
            restore_from_backup()
            return False
            
    except Exception as e:
        logger.error(f"Repair failed: {e}")
        restore_from_backup()
        return False
```

---

## **12. Appendices**

### **12.1. Glossary of Terms**

| Term | Definition |
|------|-----------|
| **Perplexity** | Measure of how well a probability model predicts a sample |
| **CodeBLEU** | Code-specific BLEU metric for evaluating code generation |
| **Pass@k** | Probability that at least one of k generated solutions passes tests |
| **Cyclomatic Complexity** | Quantitative measure of program complexity |
| **Maintainability Index** | Composite metric of code maintainability |
| **AST** | Abstract Syntax Tree - tree representation of code syntax |
| **TOPSIS** | Technique for Order Preference by Similarity to Ideal Solution |
| **Ollama** | Framework for running LLMs locally |
| **HumanEval** | Benchmark dataset for evaluating code generation |

### **12.2. Reference Architecture**

**Figure 7: Complete Reference Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │   Web    │  │   CLI    │  │   API    │  │   SDK   │ │
│  │   App    │  │   Tool   │  │  Client  │  │         │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                    API Gateway                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │   REST   │  │   Web-   │  │   Graph  │              │
│  │   API    │  │  Socket  │  │    QL    │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                 Microservices Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │Evaluation│  │ Analysis │  │  Tuning  │  │ Metrics │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                 Data Layer                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ Postgres │  │  Redis   │  │   S3     │  │   ES    │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
```

### **12.3. Performance Metrics**

**Table 5: Key Performance Indicators**

| KPI | Target | Measurement | Alert Threshold |
|-----|--------|-------------|-----------------|
| **Evaluation Throughput** | 500 problems/hour | Problems evaluated per hour | < 100 problems/hour |
| **API Response Time** | < 200ms | 95th percentile latency | > 500ms |
| **Error Rate** | < 1% | Failed requests / total | > 5% |
| **Database Query Time** | < 50ms | Average query time | > 200ms |
| **Model Inference Time** | < 2s | Time to generate code | > 10s |
| **System Uptime** | 99.9% | Percentage of time available | < 99% |

### **12.4. Best Practices**

#### **Development Best Practices:**
1. **Code Quality**: Always run tests before committing
2. **Documentation**: Update documentation with code changes
3. **Security**: Regular security scans and dependency updates
4. **Performance**: Profile and optimize critical paths
5. **Monitoring**: Implement comprehensive logging and monitoring

#### **Deployment Best Practices:**
1. **Blue-Green Deployment**: Minimize downtime during updates
2. **Rolling Updates**: Update instances one at a time
3. **Health Checks**: Implement proper health checks
4. **Backup Strategy**: Regular backups with tested restore procedures
5. **Disaster Recovery**: Plan for worst-case scenarios

#### **Operational Best Practices:**
1. **Capacity Planning**: Monitor and plan for growth
2. **Incident Response**: Establish clear incident procedures
3. **Change Management**: Document and review all changes
4. **Security Patching**: Regular security updates
5. **Performance Tuning**: Continuous performance optimization

---

## **Document Revision History**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-01-15 | Initial release | CodeQualBench Team |
| 1.1 | 2024-03-20 | Added API documentation | Development Team |
| 1.2 | 2024-06-10 | Added tuning pipeline | Research Team |
| 2.0 | 2024-12-25 | Complete rewrite with all features | Architecture Team |

---

## **Contact Information**

**Technical Support:** support@codequalbench.com  
**Documentation Issues:** docs@codequalbench.com  
**Security Issues:** security@codequalbench.com  
**General Inquiries:** info@codequalbench.com  

**Website:** https://codequalbench.com  
**Documentation:** https://docs.codequalbench.com  
**GitHub:** https://github.com/codequalbench  
**Discord:** https://discord.gg/codequalbench  

---

*This document is proprietary and confidential. Unauthorized distribution is prohibited.*

**© 2024 CodeQualBench. All rights reserved.**