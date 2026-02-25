# DOCKER SUPPORT

This document describes how to run the AI Model Evaluation Framework in Docker.

## Quick Start with Docker

### 1. Build the Docker Image

```bash
docker build -t ai-model-eval:latest .
```

### 2. Run the Container

```bash
docker run -it \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/results:/app/results \
  -p 5000:5000 \
  ai-model-eval:latest
```

### 3. Run Specific Commands

```bash
# Run evaluation
docker run ai-model-eval:latest python main.py eval --models ollama

# Start dashboard
docker run -p 5000:5000 ai-model-eval:latest python main.py dashboard
```

## Docker Compose

### Development Setup

```bash
docker-compose up
```

This will start:

- Main application container
- Ollama container (if configured)
- Result storage volumes

### Production Setup

```bash
docker-compose -f docker-compose.prod.yml up
```

## Dockerfile Example

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

CMD ["python", "main.py", "dashboard"]
```

## Volume Mapping

- `/app/data` - Dataset storage
- `/app/results` - Evaluation results
- `/app/config` - Configuration files

## Environment Variables in Docker

```bash
docker run \
  -e LOG_LEVEL=DEBUG \
  -e TIMEOUT_SECONDS=60 \
  -e MEMORY_LIMIT_GB=8 \
  ai-model-eval:latest
```

## Networking

For multi-container setups, services communicate via network names:

```yaml
services:
  app:
    networks:
      - eval-network
  ollama:
    networks:
      - eval-network
networks:
  eval-network:
    driver: bridge
```

## Debugging in Docker

```bash
# View logs
docker logs <container_id>

# Interactive shell
docker exec -it <container_id> /bin/bash

# Check running processes
docker top <container_id>
```

## Resource Limits

```bash
docker run \
  -m 4g \
  --cpus 2 \
  ai-model-eval:latest
```

## GPU Support

```bash
docker run --gpus all \
  ai-model-eval:latest
```

Requires NVIDIA Container Toolkit.

## Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:5000/health || exit 1
```

## Troubleshooting

### Out of memory

- Increase Docker memory limits
- Reduce batch sizes in configuration
- Use external cache storage

### Slow performance

- Check resource allocation
- Verify volume mount performance
- Monitor network latency

### Port conflicts

- Change port mapping: `-p 8000:5000`
- Use dynamic port assignment: `-p :5000`
