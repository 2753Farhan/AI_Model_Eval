# src/adapters/ollama_adapter.py

from typing import List, Dict, Any, Optional, AsyncGenerator
import asyncio
import aiohttp
import json
import logging
import re

from .model_adapter import ModelAdapter
from src.utils.code_formatter import CodeFormatter

logger = logging.getLogger(__name__)


class OllamaAdapter(ModelAdapter):
    """Adapter for Ollama local models"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.session: Optional[aiohttp.ClientSession] = None
        self.max_retries = config.get('max_retries', 1)  # Reduced retries
        self.retry_delay = config.get('retry_delay', 0.5)

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure aiohttp session exists"""
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    def _extract_function_name(self, prompt: str) -> Optional[str]:
        """Extract function name from prompt"""
        # Look for function definition in prompt
        match = re.search(r'def\s+(\w+)\s*\(', prompt)
        if match:
            return match.group(1)
        return None

    async def generate_code(
        self,
        prompt: str,
        config: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate code using Ollama"""
        config = config or {}

        # Check cache
        cache_key = self._get_cache_key(prompt, config)
        cached = self._check_cache(cache_key)
        if cached:
            return cached

        # Extract function name from prompt
        function_name = self._extract_function_name(prompt)

        # Prepare request
        url = f"{self.base_url}/api/generate"

        # Simple prompt - just ask to complete the function
        # HumanEval prompts already contain the function signature
        enhanced_prompt = prompt.strip()

        payload = {
            'model': self.model_name,
            'prompt': enhanced_prompt,
            'stream': False,
            'options': {
                'temperature': 0.1,  # Lower temperature for deterministic output
                'top_p': 0.9,
                'max_tokens': 512,
                'stop': ['\n\n\n', '```', 'def ']  # Stop at next function or markdown
            }
        }

        try:
            session = await self._ensure_session()
            logger.info(f"Sending request to Ollama for model {self.model_name}")

            async with session.post(url, json=payload, timeout=60) as response:
                if response.status == 200:
                    result = await response.json()
                    generated_text = result.get('response', '').strip()

                    # Clean up the response
                    generated_text = self._clean_model_output(generated_text, function_name)

                    # If still empty or too short, try once with a simpler prompt
                    if not generated_text or len(generated_text) < 20:
                        logger.warning("Generated code too short, trying simpler prompt")
                        simple_prompt = f"Complete this Python function:\n\n{prompt}\n\n"
                        
                        async with session.post(url, json={
                            'model': self.model_name,
                            'prompt': simple_prompt,
                            'stream': False,
                            'options': {
                                'temperature': 0.2,
                                'max_tokens': 512
                            }
                        }, timeout=60) as retry_response:
                            if retry_response.status == 200:
                                retry_result = await retry_response.json()
                                generated_text = retry_result.get('response', '').strip()
                                generated_text = self._clean_model_output(generated_text, function_name)

                    # If still no valid code, return a simple valid function
                    if not generated_text or generated_text.startswith('# Error'):
                        return self._create_valid_function(prompt, function_name)

                    # Cache response
                    self._update_cache(cache_key, generated_text)

                    logger.info(f"Generation successful, got {len(generated_text)} chars")
                    return generated_text
                else:
                    error_text = await response.text()
                    logger.error(f"Ollama API error: {response.status} - {error_text}")
                    return self._create_valid_function(prompt, function_name)

        except asyncio.TimeoutError:
            logger.error("Ollama request timed out")
            return self._create_valid_function(prompt, function_name)
        except aiohttp.ClientConnectorError:
            logger.error("Failed to connect to Ollama")
            return "# Error: Cannot connect to Ollama"
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return self._create_valid_function(prompt, function_name)

    def _clean_model_output(self, text: str, function_name: Optional[str] = None) -> str:
        """Clean model output to extract just the code"""
        if not text:
            return ""
        
        # Remove markdown code blocks
        if '```python' in text:
            parts = text.split('```python')
            if len(parts) > 1:
                text = parts[1].split('```')[0]
        elif '```' in text:
            parts = text.split('```')
            if len(parts) > 1:
                text = parts[1].split('```')[0]
        
        # Remove any [PYTHON] tags
        text = text.replace('[PYTHON]', '').replace('[/PYTHON]', '')
        
        # Split into lines
        lines = text.split('\n')
        
        # Find where the function starts
        start_idx = -1
        for i, line in enumerate(lines):
            if 'def ' in line or line.strip().startswith('def '):
                start_idx = i
                break
        
        if start_idx >= 0:
            # Take from function definition to the end
            code_lines = lines[start_idx:]
            
            # Remove trailing empty lines
            while code_lines and not code_lines[-1].strip():
                code_lines.pop()
            
            # Ensure proper indentation
            formatted_lines = []
            for line in code_lines:
                if line.strip() and not line.startswith((' ', '\t')) and 'def ' not in line:
                    # This line might be outside the function - add indentation
                    formatted_lines.append('    ' + line)
                else:
                    formatted_lines.append(line)
            
            return '\n'.join(formatted_lines)
        
        # If no function found, try to extract any Python code
        code_lines = []
        for line in lines:
            if line.strip() and not line.strip().startswith(('#', '"""', "'''")):
                code_lines.append(line)
        
        if code_lines:
            return '\n'.join(code_lines)
        
        return text.strip()

    def _create_valid_function(self, prompt: str, function_name: Optional[str]) -> str:
        """Create a valid Python function when generation fails"""
        if not function_name:
            # Try to extract from prompt again
            match = re.search(r'def\s+(\w+)\s*\(', prompt)
            if match:
                function_name = match.group(1)
            else:
                function_name = "solution"
        
        # Extract parameters from prompt if possible
        params_match = re.search(r'def\s+\w+\s*\((.*?)\):', prompt, re.DOTALL)
        if params_match:
            params = params_match.group(1)
        else:
            params = "*args, **kwargs"
        
        # Extract return type if present
        return_match = re.search(r'->\s*(\w+)', prompt)
        return_type = return_match.group(1) if return_match else "Any"
        
        # Create a simple but valid function
        return f"""def {function_name}({params}):
    # TODO: Implement this function
    # This is a placeholder - model generation failed
    pass"""
    async def generate_stream(
        self,
        prompt: str,
        config: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[str, None]:
        """Generate code as a stream"""
        config = config or {}
        
        url = f"{self.base_url}/api/generate"
        payload = {
            'model': self.model_name,
            'prompt': prompt,
            'stream': True,
            'options': {
                'temperature': config.get('temperature', self.temperature),
                'top_p': config.get('top_p', self.top_p),
                'max_tokens': config.get('max_tokens', self.max_tokens)
            }
        }
        
        try:
            session = await self._ensure_session()
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    async for line in response.content:
                        if line:
                            try:
                                chunk = json.loads(line)
                                if 'response' in chunk:
                                    yield chunk['response']
                                if chunk.get('done', False):
                                    break
                            except json.JSONDecodeError:
                                continue
                else:
                    yield f"# Error: HTTP {response.status}"
                    
        except Exception as e:
            logger.error(f"Ollama stream generation failed: {e}")
            yield f"# Error: {str(e)}"

    async def get_capabilities(self) -> Dict[str, Any]:
        """Get Ollama model capabilities"""
        try:
            url = f"{self.base_url}/api/show"
            payload = {'name': self.model_name}
            
            session = await self._ensure_session()
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    info = await response.json()
                    return {
                        'context_length': info.get('context_length', 2048),
                        'parameters': info.get('parameters', 'unknown'),
                        'quantization': info.get('quantization', 'unknown'),
                        'families': info.get('families', []),
                        'template': info.get('template', ''),
                        'license': info.get('license', 'unknown')
                    }
        except Exception as e:
            logger.error(f"Failed to get model capabilities: {e}")
        
        return {
            'context_length': 2048,
            'parameters': 'unknown',
            'supports_code': True,
            'languages': ['python']
        }

    async def list_models(self) -> List[Dict[str, Any]]:
        """List available models"""
        try:
            url = f"{self.base_url}/api/tags"
            
            session = await self._ensure_session()
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('models', [])
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
        
        return []

    async def pull_model(self, model_name: str) -> bool:
        """Pull a model"""
        try:
            url = f"{self.base_url}/api/pull"
            payload = {'name': model_name}
            
            session = await self._ensure_session()
            async with session.post(url, json=payload) as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"Failed to pull model {model_name}: {e}")
            return False

    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()