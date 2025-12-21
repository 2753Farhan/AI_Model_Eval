#!/usr/bin/env python3
"""
Quick start script for AI_ModelEval
"""

import subprocess
import sys
import os

def run_command(command, description):
    print(f"\n🔧 {description}...")
    print(f"   Command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"   ✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ {description} failed: {e}")
        return False

def main():
    print("🚀 AI_ModelEval Quick Start")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("❌ Please activate your virtual environment first!")
        print("   On Windows: venv\\Scripts\\activate")
        print("   On Linux/Mac: source venv/bin/activate")
        return
    
    # Step 1: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return
    
    # Step 2: Check Ollama
    if not run_command("ollama --version", "Checking Ollama"):
        print("⚠️  Ollama not found. Please install it from https://ollama.ai/")
        return
    
    # Step 3: Pull a model
    if not run_command("ollama pull codellama:7b", "Downloading CodeLlama model"):
        return
    
    # Step 4: Run baseline analysis
    if not run_command("python baseline_analysis.py", "Running baseline analysis"):
        return
    
    # Step 5: Run AI evaluation
    if not run_command("python ai_model_eval.py", "Running AI model evaluation"):
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n📊 Next steps:")
    print("   1. Start the dashboard: python dashboard/app_enhanced.py")
    print("   2. Open http://localhost:5000 in your browser")
    print("   3. Explore the model comparison and evaluation results")

if __name__ == "__main__":
    main()