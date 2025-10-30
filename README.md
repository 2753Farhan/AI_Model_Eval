gitpython
pandas
numpy
radon
bandit
pylint
complexipy
pyyaml
tqdm
# LLM_CodeEval

This project evaluates code quality for HumanEval tasks using static analysis tools to establish a human-written baseline before comparing LLM-generated solutions.

## 🧩 Setup Instructions (Windows)

```bash
# 1. Create environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run baseline analysis
python baseline_analysis.py
