
import shutil
import psutil
import logging
from typing import List, Dict, Optional, Tuple, Any

logger = logging.getLogger(__name__)


class DiskSpaceManager:
    """Manages disk space and model selection based on available space"""
    
    # Model hierarchy from largest to smallest (approximate sizes in GB)
    MODEL_HIERARCHY = [
        {"name": "codellama:34b", "size_gb": 20, "priority": 1},
        {"name": "codellama:13b", "size_gb": 7, "priority": 2},
        {"name": "codellama:7b", "size_gb": 4, "priority": 3},
        {"name": "deepseek-coder:6.7b", "size_gb": 4, "priority": 3},
        {"name": "mistral:7b", "size_gb": 4, "priority": 3},
        {"name": "llama2:7b", "size_gb": 4, "priority": 3},
        {"name": "phi:2.7b", "size_gb": 2, "priority": 4},
        {"name": "tinyllama:1.1b", "size_gb": 0.7, "priority": 5},
        {"name": "starcoder:1b", "size_gb": 0.6, "priority": 5},
        {"name": "qwen:0.5b", "size_gb": 0.3, "priority": 6},
    ]
    
    # Required buffer space in GB
    REQUIRED_BUFFER_GB = 2.0
    
    def __init__(self, base_path: str = "."):
        self.base_path = base_path

    @staticmethod
    def get_available_space_gb(path: str = ".") -> Optional[float]:
        """Get available disk space in GB"""
        try:
            disk_usage = shutil.disk_usage(path)
            available_gb = disk_usage.free / (1024**3)
            return available_gb
        except Exception as e:
            logger.warning(f"Could not check disk space: {e}")
            return None

    @staticmethod
    def get_available_ram_gb() -> Optional[float]:
        """Get available RAM in GB"""
        try:
            mem = psutil.virtual_memory()
            available_ram_gb = mem.available / (1024**3)
            return available_ram_gb
        except Exception as e:
            logger.warning(f"Could not check RAM: {e}")
            return None

    @staticmethod
    def get_disk_usage_percent(path: str = ".") -> Optional[float]:
        """Get disk usage percentage"""
        try:
            disk_usage = shutil.disk_usage(path)
            return (disk_usage.used / disk_usage.total) * 100
        except Exception as e:
            logger.warning(f"Could not check disk usage: {e}")
            return None

    def select_models_based_on_space(
        self,
        requested_models: List[str],
        available_gb: Optional[float] = None,
        available_ram_gb: Optional[float] = None
    ) -> List[str]:
        """Select appropriate models based on available space"""
        if available_gb is None:
            available_gb = self.get_available_space_gb(self.base_path)
        
        if available_ram_gb is None:
            available_ram_gb = self.get_available_ram_gb()
        
        logger.info(f"System Resources - Disk: {available_gb:.2f} GB free, "
                   f"RAM: {available_ram_gb:.2f} GB available")
        
        if available_gb is None:
            logger.warning("Could not determine disk space, using requested models")
            return requested_models
        
        # Check minimum space for smallest model
        smallest_model = min(self.MODEL_HIERARCHY, key=lambda x: x["size_gb"])
        min_required = smallest_model["size_gb"] + self.REQUIRED_BUFFER_GB
        
        if available_gb < min_required:
            logger.error(f"Insufficient disk space. Need at least {min_required:.1f} GB, "
                        f"but only {available_gb:.1f} GB available")
            return []
        
        # Sort models by priority
        sorted_models = sorted(self.MODEL_HIERARCHY, key=lambda x: x["priority"])
        
        # Filter to requested models
        available_models = [
            m for m in sorted_models
            if m["name"] in requested_models or not requested_models
        ]
        
        if not available_models and requested_models:
            logger.warning("Requested models not in hierarchy, using defaults")
            available_models = sorted_models
        
        # Select models that fit
        selected_models = []
        total_size_gb = 0
        
        for model in available_models:
            model_size = model["size_gb"]
            
            # Check if model fits
            required_space = total_size_gb + model_size + self.REQUIRED_BUFFER_GB
            required_ram = model_size * 1.5  # Models need RAM for loading
            
            if required_space <= available_gb and required_ram <= available_ram_gb:
                selected_models.append(model["name"])
                total_size_gb += model_size
                logger.debug(f"Selected model: {model['name']} ({model_size} GB)")
        
        if not selected_models:
            # Try smallest model
            for model in reversed(available_models):
                if model["size_gb"] + self.REQUIRED_BUFFER_GB <= available_gb:
                    selected_models = [model["name"]]
                    logger.info(f"Selected minimal model: {model['name']}")
                    break
        
        logger.info(f"Selected {len(selected_models)} models: {selected_models}")
        logger.info(f"Estimated total model size: {total_size_gb:.1f} GB")
        
        return selected_models

    def estimate_file_space(
        self,
        num_models: int,
        num_problems: int,
        samples_per_problem: int,
        bytes_per_file: int = 5000
    ) -> Dict[str, float]:
        """Estimate space needed for generated files"""
        total_files = num_models * num_problems * samples_per_problem
        total_bytes = total_files * bytes_per_file
        
        return {
            'files': total_files,
            'bytes': total_bytes,
            'kb': total_bytes / 1024,
            'mb': total_bytes / (1024 * 1024),
            'gb': total_bytes / (1024 * 1024 * 1024)
        }

    # src/utils/disk_space_manager.py

# src/utils/disk_space_manager.py

    def check_model_availability(
        self,
        model_manager,
        requested_models: List[str]
    ) -> Tuple[List[str], Dict[str, Any]]:
        """Check model availability with space-based fallback"""
        logger.info("Checking model availability with space-based fallback...")
        
        # Check available space
        available_gb = self.get_available_space_gb(self.base_path)
        available_ram_gb = self.get_available_ram_gb()
        usage_percent = self.get_disk_usage_percent(self.base_path)
        
        space_info = {
            'disk_gb': available_gb,
            'ram_gb': available_ram_gb,
            'usage_percent': usage_percent
        }
        
        # Select models based on space
        space_based_models = self.select_models_based_on_space(
            requested_models, available_gb, available_ram_gb
        )
        
        if not space_based_models:
            logger.error("No models can fit in available space!")
            return [], space_info
        
        # Check which models are available in the registry
        available_api_models = []
        
        # Try to get active models first (models that are already initialized)
        try:
            available_api_models = model_manager.get_active_models()
            logger.info(f"Active models from registry: {available_api_models}")
        except AttributeError:
            pass
        
        # If no active models, try to list all registered models
        if not available_api_models:
            try:
                models_list = model_manager.list_models()
                # Handle different return types
                if models_list:
                    if isinstance(models_list[0], dict):
                        available_api_models = [m.get('model_id') for m in models_list]
                    else:
                        available_api_models = models_list
                logger.info(f"Models from registry: {available_api_models}")
            except (AttributeError, Exception) as e:
                logger.warning(f"Could not get model list: {e}")
        
        # If we still don't have any models, assume requested models are available
        if not available_api_models:
            logger.warning("No model info from registry, assuming requested models are available")
            available_api_models = requested_models
        
        # Filter to models that are both space-appropriate and available in registry
        final_models = [
            m for m in space_based_models
            if m in available_api_models
        ]
        
        # If no intersection, try to use the space-based models directly
        if not final_models and space_based_models:
            logger.warning("No matching models in registry, using space-based selection")
            final_models = space_based_models
            
            # Try to get each model to ensure they exist
            working_models = []
            for model in final_models:
                try:
                    model_obj = model_manager.get_model(model)
                    if model_obj:
                        working_models.append(model)
                        logger.info(f"Model {model} is available")
                except Exception as e:
                    logger.warning(f"Model {model} not available: {e}")
            
            if working_models:
                final_models = working_models
        
        logger.info(f"Final model selection: {final_models}")
        return final_models, space_info

    def get_cleanup_recommendations(self) -> List[Dict[str, Any]]:
        """Get recommendations for freeing up space"""
        recommendations = []
        
        # Check temp directories
        temp_paths = ['/tmp', './cache', './logs', './results']
        for path in temp_paths:
            if os.path.exists(path):
                size = self._get_directory_size(path)
                if size > 1024 * 1024 * 1024:  # > 1GB
                    recommendations.append({
                        'path': path,
                        'size_gb': size / (1024**3),
                        'action': f"Clean up {path} directory"
                    })
        
        # Check Docker images
        try:
            import docker
            client = docker.from_env()
            images = client.images.list()
            total_size = sum(img.attrs['Size'] for img in images)
            
            if total_size > 5 * 1024**3:  # > 5GB
                recommendations.append({
                    'path': 'docker',
                    'size_gb': total_size / (1024**3),
                    'action': "Run 'docker system prune' to clean unused images"
                })
        except:
            pass
        
        return recommendations

    def _get_directory_size(self, path: str) -> int:
        """Get total size of directory in bytes"""
        total = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self._get_directory_size(entry.path)
        except:
            pass
        return total