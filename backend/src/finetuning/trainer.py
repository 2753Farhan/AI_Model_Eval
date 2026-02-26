# src/finetuning/trainer.py
"""
Fine-tunes models using Ollama based on training data
"""

import json
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
import requests

logger = logging.getLogger(__name__)

class OllamaTrainer:
    """Fine-tunes models using Ollama"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.modelfile_dir = Path("data/finetuning/modelfiles")
        self.modelfile_dir.mkdir(parents=True, exist_ok=True)
    
    def prepare_modelfile(
        self,
        base_model: str,
        training_file: str,
        output_model: str
    ) -> str:
        """Create a Modelfile for fine-tuning"""
        
        modelfile_content = f"""
FROM {base_model}

# Set parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER stop "</s>"

# Training data
TRAINING {training_file}

# System prompt
SYSTEM You are a code generation model. Write Python functions based on the given problem description.
"""
        
        modelfile_path = self.modelfile_dir / f"{output_model}.Modelfile"
        with open(modelfile_path, 'w') as f:
            f.write(modelfile_content)
        
        logger.info(f"Created Modelfile at {modelfile_path}")
        return str(modelfile_path)
    
    def fine_tune(
        self,
        base_model: str,
        training_file: str,
        output_model: str,
        wait_for_completion: bool = True
    ) -> Dict[str, Any]:
        """Fine-tune a model using Ollama"""
        
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code != 200:
                return {"success": False, "error": "Ollama not running"}
            
            # Prepare Modelfile
            modelfile_path = self.prepare_modelfile(base_model, training_file, output_model)
            
            # Create the model
            logger.info(f"Creating model {output_model} from {base_model}")
            
            # For Ollama, we use the create command with a Modelfile
            cmd = [
                "ollama", "create", output_model,
                "-f", modelfile_path
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if wait_for_completion:
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    logger.info(f"Successfully created model {output_model}")
                    return {
                        "success": True,
                        "model": output_model,
                        "base_model": base_model,
                        "output": stdout
                    }
                else:
                    logger.error(f"Failed to create model: {stderr}")
                    return {
                        "success": False,
                        "error": stderr
                    }
            else:
                # Don't wait for completion
                return {
                    "success": True,
                    "model": output_model,
                    "status": "started"
                }
                
        except Exception as e:
            logger.error(f"Fine-tuning failed: {e}")
            return {"success": False, "error": str(e)}
    
    def list_finetuned_models(self) -> List[Dict[str, Any]]:
        """List all fine-tuned models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                # Filter to show only fine-tuned models (you might have a naming convention)
                finetuned = [
                    m for m in models 
                    if 'fine' in m['name'].lower() or 'tuned' in m['name'].lower()
                ]
                return finetuned
            return []
        except:
            return []
    
    def delete_model(self, model_name: str) -> bool:
        """Delete a fine-tuned model"""
        try:
            cmd = ["ollama", "rm", model_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False