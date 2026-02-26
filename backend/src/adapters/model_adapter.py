
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator
import asyncio
from datetime import datetime, timedelta
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


class ModelAdapter(ABC):
    """Abstract base class for all model adapters"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.adapter_id = self._generate_adapter_id()
        self.provider = self.__class__.__name__.replace('Adapter', '').lower()
        self.model_name = config.get('model_name', 'default')
        self.api_endpoint = config.get('api_endpoint')
        self.api_key = config.get('api_key')
        self.max_tokens = config.get('max_tokens', 512)
        self.temperature = config.get('temperature', 0.7)
        self.top_p = config.get('top_p', 0.9)
        self.cache_enabled = config.get('cache_enabled', True)
        self.cache: Dict[str, tuple] = {}  # key -> (response, timestamp)
        self.cache_ttl = config.get('cache_ttl', 3600)  # 1 hour default
        self.request_count = 0
        self.last_request_time = datetime.now()
        self.rate_limit = config.get('rate_limit', 60)  # requests per minute
        self.rate_limit_window = config.get('rate_limit_window', 60)  # seconds
        
        logger.info(f"Initialized {self.provider} adapter for model {self.model_name}")

    def _generate_adapter_id(self) -> str:
        """Generate a unique adapter ID"""
        import secrets
        return f"adapter_{secrets.token_hex(8)}"

    def _get_cache_key(self, prompt: str, config: Dict) -> str:
        """Generate cache key from prompt and config"""
        key_data = {
            'prompt': prompt,
            'model': self.model_name,
            'temperature': config.get('temperature', self.temperature),
            'max_tokens': config.get('max_tokens', self.max_tokens),
            'top_p': config.get('top_p', self.top_p)
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()

    def _check_cache(self, cache_key: str) -> Optional[str]:
        """Check if response is in cache"""
        if not self.cache_enabled:
            return None
        
        if cache_key in self.cache:
            response, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                logger.debug(f"Cache hit for key {cache_key[:8]}")
                return response
            else:
                # Remove expired entry
                del self.cache[cache_key]
        
        return None

    def _update_cache(self, cache_key: str, response: str) -> None:
        """Update cache with response"""
        if self.cache_enabled:
            self.cache[cache_key] = (response, datetime.now())
            logger.debug(f"Cached response for key {cache_key[:8]}")

    async def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting"""
        now = datetime.now()
        time_diff = (now - self.last_request_time).total_seconds()
        
        if time_diff < self.rate_limit_window:
            if self.request_count >= self.rate_limit:
                wait_time = self.rate_limit_window - time_diff
                logger.warning(f"Rate limit reached, waiting {wait_time:.2f}s")
                await asyncio.sleep(wait_time)
                self.request_count = 0
                self.last_request_time = datetime.now()
        else:
            self.request_count = 0
            self.last_request_time = now
        
        self.request_count += 1

    @abstractmethod
    async def generate_code(
        self,
        prompt: str,
        config: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate code from prompt"""
        pass

    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        config: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[str, None]:
        """Generate code as a stream"""
        pass
        yield ""  # Dummy yield for generator

    @abstractmethod
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get model capabilities"""
        pass

    async def test_connection(self) -> bool:
        """Test API connection"""
        try:
            response = await self.generate_code(
                "def hello():\n    return 'world'",
                {'max_tokens': 10}
            )
            return bool(response and len(response.strip()) > 0)
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    def estimate_cost(self, tokens: int) -> float:
        """Estimate API cost for token count"""
        # Default implementation - override in specific adapters
        rates = {
            'ollama': 0.0,  # Free local inference
            'huggingface': 0.0,  # Free tier may apply
            'openai': 0.002,  # $0.002 per 1K tokens
            'anthropic': 0.00163,  # $0.00163 per 1K tokens
            'gemini': 0.0005  # $0.0005 per 1K tokens
        }
        rate = rates.get(self.provider, 0.0)
        return (tokens / 1000) * rate

    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            'adapter_id': self.adapter_id,
            'provider': self.provider,
            'model_name': self.model_name,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'capabilities': asyncio.run(self.get_capabilities()),
            'rate_limit': self.rate_limit,
            'cache_enabled': self.cache_enabled
        }

    def validate_response(self, response: str) -> bool:
        """Validate model response"""
        if not response or not response.strip():
            return False
        
        # Check for error indicators
        error_indicators = ['error:', 'exception:', 'failed:', 'timeout']
        response_lower = response.lower()
        
        for indicator in error_indicators:
            if indicator in response_lower and len(response) < 100:
                return False
        
        return True

    async def batch_generate(
        self,
        prompts: List[str],
        config: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Generate multiple codes in batch"""
        tasks = [self.generate_code(prompt, config) for prompt in prompts]
        return await asyncio.gather(*tasks)

    def clear_cache(self) -> None:
        """Clear the response cache"""
        self.cache.clear()
        logger.info("Cache cleared")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            'size': len(self.cache),
            'enabled': self.cache_enabled,
            'ttl': self.cache_ttl,
            'keys': list(self.cache.keys())[:10]  # First 10 keys for debugging
        }