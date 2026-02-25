
from typing import Dict, List, Any, Optional, Type
import logging

from .model_adapter import ModelAdapter
from .ollama_adapter import OllamaAdapter
from .huggingface_adapter import HuggingFaceAdapter

logger = logging.getLogger(__name__)


class ModelRegistry:
    """Registry for managing model adapters"""
    
    def __init__(self):
        self.adapters: Dict[str, ModelAdapter] = {}
        self.adapter_classes: Dict[str, Type[ModelAdapter]] = {
            'ollama': OllamaAdapter,
            'huggingface': HuggingFaceAdapter
        }
        self.model_configs: Dict[str, Dict[str, Any]] = {}

    def register_adapter_class(
        self,
        provider: str,
        adapter_class: Type[ModelAdapter]
    ) -> None:
        """Register a new adapter class"""
        self.adapter_classes[provider.lower()] = adapter_class
        logger.info(f"Registered adapter class for provider: {provider}")

    def register_model(
        self,
        model_id: str,
        provider: str,
        config: Dict[str, Any]
    ) -> None:
        """Register a model with configuration"""
        self.model_configs[model_id] = {
            'provider': provider.lower(),
            'config': config
        }
        logger.info(f"Registered model: {model_id} with provider {provider}")

    def get_model(self, model_id: str) -> Optional[ModelAdapter]:
        """Get or create a model adapter"""
        # Check if already created
        if model_id in self.adapters:
            return self.adapters[model_id]
        
        # Get model config
        if model_id not in self.model_configs:
            logger.error(f"Model {model_id} not found in registry")
            return None
        
        config_info = self.model_configs[model_id]
        provider = config_info['provider']
        config = config_info['config'].copy()
        config['model_name'] = model_id
        
        # Create adapter
        if provider in self.adapter_classes:
            adapter_class = self.adapter_classes[provider]
            try:
                adapter = adapter_class(config)
                self.adapters[model_id] = adapter
                logger.info(f"Created adapter for model: {model_id}")
                return adapter
            except Exception as e:
                logger.error(f"Failed to create adapter for {model_id}: {e}")
                return None
        else:
            logger.error(f"Unknown provider: {provider}")
            return None

    def list_models(self) -> List[Dict[str, Any]]:
        """List all registered models"""
        models = []
        for model_id, config_info in self.model_configs.items():
            models.append({
                'model_id': model_id,
                'provider': config_info['provider'],
                'config': config_info['config'],
                'active': model_id in self.adapters
            })
        return models


    def remove_model(self, model_id: str) -> bool:
        """Remove a model from registry"""
        if model_id in self.adapters:
            # Clean up adapter
            adapter = self.adapters[model_id]
            if hasattr(adapter, 'close'):
                try:
                    import asyncio
                    asyncio.create_task(adapter.close())
                except:
                    pass
            
            del self.adapters[model_id]
            
        if model_id in self.model_configs:
            del self.model_configs[model_id]
            
        logger.info(f"Removed model: {model_id}")
        return True

    def clear_cache(self, model_id: Optional[str] = None) -> None:
        """Clear cache for specific model or all models"""
        if model_id:
            if model_id in self.adapters:
                self.adapters[model_id].clear_cache()
        else:
            for adapter in self.adapters.values():
                adapter.clear_cache()
        
        logger.info("Cache cleared")

    async def close_all(self):
        """Close all adapter sessions"""
        for model_id, adapter in self.adapters.items():
            if hasattr(adapter, 'close'):
                try:
                    await adapter.close()
                except Exception as e:
                    logger.error(f"Error closing adapter for {model_id}: {e}")
        
        self.adapters.clear()
        logger.info("All adapters closed")

    def load_from_config(self, config: Dict[str, Any]) -> None:
        """Load models from configuration"""
        models_config = config.get('models', {})
        
        # Load custom models
        custom_models = models_config.get('custom_models', [])
        for model_config in custom_models:
            model_id = model_config['name']
            provider = model_config['adapter']
            config = model_config.get('config', {})
            self.register_model(model_id, provider, config)
        
        # Load default models
        default_models = models_config.get('default_models', [])
        for model_id in default_models:
            if model_id not in self.model_configs:
                # Assume Ollama for default models
                self.register_model(
                    model_id,
                    'ollama',
                    {'base_url': models_config.get('ollama_base_url', 'http://localhost:11434')}
                )

    # src/adapters/registry.py
    
    def get_active_models(self) -> List[str]:
        """Get list of active (initialized) models"""
        return list(self.adapters.keys())
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List all registered models"""
        models = []
        for model_id, config_info in self.model_configs.items():
            models.append({
                'model_id': model_id,
                'provider': config_info['provider'],
                'config': config_info['config'],
                'active': model_id in self.adapters
            })
        return models
    
    def get_model(self, model_id: str) -> Optional[ModelAdapter]:
        """Get or create a model adapter"""
        # Check if already created
        if model_id in self.adapters:
            return self.adapters[model_id]
        
        # Get model config
        if model_id not in self.model_configs:
            logger.error(f"Model {model_id} not found in registry")
            return None
        
        config_info = self.model_configs[model_id]
        provider = config_info['provider']
        config = config_info['config'].copy()
        config['model_name'] = model_id
        
        # Create adapter
        if provider in self.adapter_classes:
            adapter_class = self.adapter_classes[provider]
            try:
                adapter = adapter_class(config)
                self.adapters[model_id] = adapter
                logger.info(f"Created adapter for model: {model_id}")
                return adapter
            except Exception as e:
                logger.error(f"Failed to create adapter for {model_id}: {e}")
                return None
        else:
            logger.error(f"Unknown provider: {provider}")
            return None