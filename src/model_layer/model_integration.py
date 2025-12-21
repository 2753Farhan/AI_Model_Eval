import requests
import ollama
from huggingface_hub import InferenceClient
import time
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, config):
        self.config = config
        self.hf_client = None
        self.ollama_client = None
        self.setup_clients()
    
    def setup_clients(self):
        """Initialize model clients"""
        try:
            # Setup Ollama
            self.ollama_client = ollama.Client(
                host=self.config.get("models.ollama_base_url", "http://localhost:11434")
            )
            logger.info("✅ Ollama client initialized")
        except Exception as e:
            logger.warning(f"⚠️ Ollama client failed: {e}")
        
        # Setup HuggingFace (optional)
        hf_key = self.config.get("models.hf_api_key")
        if hf_key:
            try:
                self.hf_client = InferenceClient(token=hf_key)
                logger.info("✅ HuggingFace client initialized")
            except Exception as e:
                logger.warning(f"⚠️ HuggingFace client failed: {e}")
    
    def get_available_models(self) -> List[str]:
        """Get list of available models with updated Ollama API response handling"""
        available_models = []
    
        # Check Ollama models
        if self.ollama_client:
            try:
                response = self.ollama_client.list()
                logger.debug(f"Ollama API response type: {type(response)}")
            
                #Debug: Print the actual response structure
                if hasattr(response, '__dict__'):
                    logger.debug(f"Response attributes: {response.__dict__}")
            
                # Handle different response structures
                ollama_models = []
            
                # Method 1: Check if response has 'models' attribute (new Ollama version)
                if hasattr(response, 'models'):
                    models_list = response.models
                    logger.debug(f"Using response.models, found {len(models_list)} models")
                # Method 2: Check if response is a dictionary with 'models' key
                elif isinstance(response, dict) and 'models' in response:
                    models_list = response['models']
                    logger.debug(f"Using response['models'], found {len(models_list)} models")
                # Method 3: Response might be the list directly
                elif isinstance(response, list):
                    models_list = response
                    logger.debug(f"Using response as list directly, found {len(models_list)} models")
                else:
                    logger.warning(f"Unexpected response structure: {response}")
                    models_list = []
            
                # Extract model names from the list
                for model in models_list:
                    # Try different possible field names for model name
                    model_name = None
                
                    if hasattr(model, 'name'):
                        model_name = model.name
                    elif hasattr(model, 'model'):
                        model_name = model.model
                    elif isinstance(model, dict):
                        model_name = model.get('name') or model.get('model')
                    elif isinstance(model, str):
                        model_name = model
                
                    if model_name:
                        ollama_models.append(model_name)
                        logger.debug(f"Found model: {model_name}")
                    else:
                        logger.warning(f"Could not extract name from model object: {model}")
            
                available_models.extend(ollama_models)
                logger.info(f"Found Ollama models: {ollama_models}")
            
            except Exception as e:
                logger.error(f"Failed to get Ollama models: {e}")
            
                # Fallback: Try direct API call
                try:
                    logger.info("Attempting fallback API call...")
                    ollama_url = self.config.get("models.ollama_base_url", "http://localhost:11434")
                    response = requests.get(f"{ollama_url}/api/tags", timeout=10)
                
                    if response.status_code == 200:
                        data = response.json()
                        logger.debug(f"Fallback API response: {data}")
                    
                        if 'models' in data:
                            fallback_models = []
                            for model in data['models']:
                                # Try different field names in the fallback
                                model_name = model.get('name') or model.get('model')
                                if model_name:
                                    fallback_models.append(model_name)
                        
                            available_models.extend(fallback_models)
                            logger.info(f"Fallback found models: {fallback_models}")
                        else:
                            logger.warning("No 'models' key in fallback response")
                    else:
                        logger.error(f"Fallback API call failed with status: {response.status_code}")
                    
                except Exception as fallback_error:
                    logger.error(f"Fallback API call also failed: {fallback_error}")
    
        # If no models found via API, provide some common defaults
        if not available_models:
            logger.warning("No models detected via API, using common fallback models")
            available_models = ["codellama:7b", "llama2:7b", "starcoder:1b"]
            logger.info(f"Using fallback models: {available_models}")
    
        return available_models 
       
    def generate_with_ollama(self, prompt: str, model: str, max_tokens: int = 512) -> str:
        """Generate code using Ollama"""
        try:
            response = self.ollama_client.generate(
                model=model,
                prompt=prompt,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'max_tokens': max_tokens
                }
            )
            return response['response']
        except Exception as e:
            logger.error(f"❌ Ollama generation failed: {e}")
            return f"# Generation failed: {str(e)}"
    
    def generate_with_huggingface(self, prompt: str, model: str) -> str:
        """Generate code using HuggingFace (placeholder)"""
        # This would require proper API setup
        return f"# HuggingFace generation for {model} not yet implemented\n# Prompt: {prompt[:100]}..."
    
    def generate_code(self, prompt: str, model: str) -> str:
        """Unified code generation interface"""
        if model in [m for m in self.get_available_models()]:
            return self.generate_with_ollama(prompt, model)
        elif self.hf_client and "huggingface" in model:
            return self.generate_with_huggingface(prompt, model)
        else:
            return f"# Model {model} not available"