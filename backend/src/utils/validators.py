
import re
import ast
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


class Validators:
    """Collection of validation methods"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_python_code(code: str) -> Dict[str, Any]:
        """Validate Python code syntax"""
        result = {
            'valid': False,
            'error': None,
            'error_line': None,
            'error_type': None
        }
        
        try:
            ast.parse(code)
            result['valid'] = True
        except SyntaxError as e:
            result['error'] = str(e)
            result['error_line'] = e.lineno
            result['error_type'] = 'syntax_error'
        except Exception as e:
            result['error'] = str(e)
            result['error_type'] = 'unknown_error'
        
        return result

    @staticmethod
    def validate_model_name(model_name: str) -> bool:
        """Validate model name format"""
        # Model names typically: provider:name or provider/name
        pattern = r'^[a-zA-Z0-9_\-]+[:/][a-zA-Z0-9_\-]+$'
        return bool(re.match(pattern, model_name))

    @staticmethod
    def validate_file_path(path: str, must_exist: bool = False) -> bool:
        """Validate file path"""
        import os
        if must_exist:
            return os.path.exists(path)
        # Check if path is valid (no invalid characters)
        invalid_chars = '<>:"|?*'
        return not any(c in path for c in invalid_chars)

    @staticmethod
    def validate_json_schema(data: Dict, schema: Dict) -> List[str]:
        """Validate data against JSON schema"""
        errors = []
        
        def validate_type(value, expected_type, path):
            if expected_type == 'string' and not isinstance(value, str):
                errors.append(f"{path}: expected string, got {type(value).__name__}")
            elif expected_type == 'number' and not isinstance(value, (int, float)):
                errors.append(f"{path}: expected number, got {type(value).__name__}")
            elif expected_type == 'integer' and not isinstance(value, int):
                errors.append(f"{path}: expected integer, got {type(value).__name__}")
            elif expected_type == 'boolean' and not isinstance(value, bool):
                errors.append(f"{path}: expected boolean, got {type(value).__name__}")
            elif expected_type == 'array' and not isinstance(value, list):
                errors.append(f"{path}: expected array, got {type(value).__name__}")
            elif expected_type == 'object' and not isinstance(value, dict):
                errors.append(f"{path}: expected object, got {type(value).__name__}")
        
        def validate_required(data, schema, path=''):
            for key, rules in schema.get('properties', {}).items():
                if key in data:
                    value = data[key]
                    if 'type' in rules:
                        validate_type(value, rules['type'], f"{path}.{key}" if path else key)
                    if 'pattern' in rules and isinstance(value, str):
                        if not re.match(rules['pattern'], value):
                            errors.append(f"{path}.{key}: does not match pattern {rules['pattern']}")
                    if 'min' in rules and isinstance(value, (int, float)):
                        if value < rules['min']:
                            errors.append(f"{path}.{key}: less than minimum {rules['min']}")
                    if 'max' in rules and isinstance(value, (int, float)):
                        if value > rules['max']:
                            errors.append(f"{path}.{key}: greater than maximum {rules['max']}")
                elif key in schema.get('required', []):
                    errors.append(f"{path}.{key}: required field missing")
        
        validate_required(data, schema)
        return errors

    @staticmethod
    def validate_date(date_str: str, format: str = '%Y-%m-%d') -> bool:
        """Validate date string format"""
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_range(value: Union[int, float], min_val: Any, max_val: Any) -> bool:
        """Validate value is within range"""
        if min_val is not None and value < min_val:
            return False
        if max_val is not None and value > max_val:
            return False
        return True

    @staticmethod
    def validate_non_empty(value: Any) -> bool:
        """Validate value is not empty"""
        if value is None:
            return False
        if isinstance(value, str):
            return len(value.strip()) > 0
        if isinstance(value, (list, dict, tuple, set)):
            return len(value) > 0
        return True

    @staticmethod
    def validate_identifier(name: str) -> bool:
        """Validate Python identifier"""
        if not name:
            return False
        return name.isidentifier()

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*$'
        return bool(re.match(pattern, url))

    @staticmethod
    def validate_port(port: int) -> bool:
        """Validate port number"""
        return 1 <= port <= 65535

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> List[str]:
        """Validate configuration dictionary"""
        errors = []
        
        # Required sections
        required_sections = ['paths', 'models', 'evaluation', 'dashboard']
        for section in required_sections:
            if section not in config:
                errors.append(f"Missing required section: {section}")
        
        # Validate paths
        if 'paths' in config:
            paths = config['paths']
            required_paths = ['data_dir', 'results_dir']
            for path in required_paths:
                if path not in paths:
                    errors.append(f"Missing required path: {path}")
        
        # Validate models
        if 'models' in config:
            models = config['models']
            if 'default_models' in models and not isinstance(models['default_models'], list):
                errors.append("default_models must be a list")
        
        # Validate evaluation config
        if 'evaluation' in config:
            eval_config = config['evaluation']
            if 'timeout_seconds' in eval_config:
                timeout = eval_config['timeout_seconds']
                if not isinstance(timeout, (int, float)) or timeout <= 0:
                    errors.append("timeout_seconds must be positive number")
        
        return errors