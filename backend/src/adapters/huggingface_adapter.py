
from typing import List, Dict, Any, Optional, AsyncGenerator
import asyncio
import aiohttp
import json
import logging

from .model_adapter import ModelAdapter

logger = logging.getLogger(__name__)


class HuggingFaceAdapter(ModelAdapter):
    """Adapter for HuggingFace Inference API"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.session: Optional[aiohttp.ClientSession] = None
        self.max_retries = config.get('max_retries', 3)
        self.retry_delay = config.get('retry_delay', 1)

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure aiohttp session exists"""
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(headers=self.headers)
        return self.session

    async def generate_code(
        self,
        prompt: str,
        config: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate code using HuggingFace"""
        config = config or {}
        
        # Check cache
        cache_key = self._get_cache_key(prompt, config)
        cached = self._check_cache(cache_key)
        if cached:
            return cached
        
        # Check rate limit
        await self._check_rate_limit()
        
        # Prepare request
        payload = {
            'inputs': prompt,
            'parameters': {
                'temperature': config.get('temperature', self.temperature),
                'top_p': config.get('top_p', self.top_p),
                'max_new_tokens': config.get('max_tokens', self.max_tokens),
                'do_sample': True,
                'return_full_text': False
            },
            'options': {
                'wait_for_model': True,
                'use_cache': self.cache_enabled
            }
        }
        
        for attempt in range(self.max_retries):
            try:
                session = await self._ensure_session()
                async with session.post(self.api_url, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Handle different response formats
                        if isinstance(result, list):
                            generated_text = result[0].get('generated_text', '')
                        else:
                            generated_text = result.get('generated_text', '')
                        
                        # Cache response
                        self._update_cache(cache_key, generated_text)
                        
                        return generated_text
                        
                    elif response.status == 503:
                        # Model loading, retry
                        if attempt < self.max_retries - 1:
                            wait_time = self.retry_delay * (2 ** attempt)
                            logger.info(f"Model loading, retrying in {wait_time}s")
                            await asyncio.sleep(wait_time)
                            continue
                    
                    error_text = await response.text()
                    logger.error(f"HuggingFace API error: {response.status} - {error_text}")
                    return f"# Error: Failed to generate code (HTTP {response.status})"
                    
            except Exception as e:
                logger.error(f"HuggingFace generation failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                else:
                    return f"# Error: {str(e)}"
        
        return "# Error: Max retries exceeded"

    async def generate_stream(
        self,
        prompt: str,
        config: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[str, None]:
        """Generate code as a stream (not supported by HF Inference API)"""
        # HF Inference API doesn't support streaming, so we simulate it
        result = await self.generate_code(prompt, config)
        
        # Split into words for simulation
        words = result.split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.05)

    async def get_capabilities(self) -> Dict[str, Any]:
        """Get HuggingFace model capabilities"""
        try:
            # Try to get model info from HuggingFace API
            model_info_url = f"https://huggingface.co/api/models/{self.model_name}"
            
            session = await self._ensure_session()
            async with session.get(model_info_url) as response:
                if response.status == 200:
                    info = await response.json()
                    return {
                        'tags': info.get('tags', []),
                        'pipeline_tag': info.get('pipeline_tag', 'text-generation'),
                        'likes': info.get('likes', 0),
                        'downloads': info.get('downloads', 0),
                        'library_name': info.get('library_name', 'transformers'),
                        'languages': self._extract_languages(info.get('tags', []))
                    }
        except Exception as e:
            logger.error(f"Failed to get model capabilities: {e}")
        
        # Default capabilities
        return {
            'pipeline_tag': 'text-generation',
            'languages': ['python', 'javascript', 'java', 'c', 'cpp', 'go', 'rust'],
            'supports_code': True
        }

    def _extract_languages(self, tags: List[str]) -> List[str]:
        """Extract programming languages from tags"""
        languages = []
        lang_keywords = ['python', 'javascript', 'java', 'cpp', 'c', 'go', 'rust', 'php']
        
        for tag in tags:
            tag_lower = tag.lower()
            for lang in lang_keywords:
                if lang in tag_lower:
                    languages.append(lang)
        
        return languages or ['python']  # Default to Python

    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()