# src/adapters/ollama_adapter.py

from typing import List, Dict, Any, Optional, AsyncGenerator
import asyncio
import aiohttp
import json
import logging

from .model_adapter import ModelAdapter

logger = logging.getLogger(__name__)


class OllamaAdapter(ModelAdapter):
    """Adapter for Ollama local models"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.session: Optional[aiohttp.ClientSession] = None

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure aiohttp session exists"""
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

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

        # Check rate limit
        await self._check_rate_limit()

        # Prepare request
        url = f"{self.base_url}/api/generate"

        # Better prompt for code generation
        enhanced_prompt = f"""{prompt}

Write ONLY the Python function code. No explanations, no markdown, no [PYTHON] tags.
Just the raw function definition. Make sure to handle edge cases.

Example format:
def function_name(parameters):
    # implementation
    return result

Now write the code:"""

        payload = {
            'model': self.model_name,
            'prompt': enhanced_prompt,
            'stream': False,
            'options': {
                'temperature': 0.2,  # Lower temperature for more deterministic output
                'top_p': 0.9,
                'max_tokens': 512,
                'stop': ['\n\n', 'def ']  # Stop at next function definition
            }
        }

        try:
            session = await self._ensure_session()
            logger.info(f"Sending request to Ollama for model {self.model_name}")

            async with session.post(url, json=payload, timeout=60) as response:
                if response.status == 200:
                    result = await response.json()
                    generated_text = result.get('response', '')

                    # Clean up the response
                    generated_text = generated_text.strip()

                    # Remove any markdown code blocks
                    if '```python' in generated_text:
                        generated_text = generated_text.split('```python')[1].split('```')[0].strip()
                    elif '```' in generated_text:
                        generated_text = generated_text.split('```')[1].split('```')[0].strip()

                    # Remove [PYTHON] tags
                    generated_text = generated_text.replace('[PYTHON]', '').replace('[/PYTHON]', '')

                    # Remove any explanatory text before the function
                    lines = generated_text.split('\n')
                    code_lines = []
                    found_def = False

                    for line in lines:
                        if line.strip().startswith('def '):
                            found_def = True
                            code_lines.append(line)
                        elif found_def:
                            code_lines.append(line)
                        elif not found_def and line.strip() and not line.strip().startswith('#'):
                            # If we haven't found def yet but line has content, check if it might be the function
                            if 'def ' in line:
                                # Extract the function definition
                                def_part = line[line.find('def '):]
                                code_lines.append(def_part)
                                found_def = True

                    if code_lines:
                        generated_text = '\n'.join(code_lines)

                    # Ensure the function name matches what the tests expect
                    # HumanEval tests use the function name from the prompt
                    # The code already has the correct function name

                    # Cache response
                    self._update_cache(cache_key, generated_text)

                    logger.info(f"Generation successful, got {len(generated_text)} chars")
                    return generated_text
                else:
                    error_text = await response.text()
                    logger.error(f"Ollama API error: {response.status} - {error_text}")
                    return f"# Error: Failed to generate code (HTTP {response.status})"

        except asyncio.TimeoutError:
            logger.error("Ollama request timed out after 60 seconds")
            return "# Error: Request timed out"
        except aiohttp.ClientConnectorError:
            logger.error("Failed to connect to Ollama")
            return "# Error: Cannot connect to Ollama"
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return f"# Error: {str(e)}"

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
        
        # Default capabilities
        return {
            'context_length': 2048,
            'parameters': 'unknown',
            'supports_code': True,
            'languages': ['python', 'javascript', 'java', 'c', 'cpp', 'go', 'rust']
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