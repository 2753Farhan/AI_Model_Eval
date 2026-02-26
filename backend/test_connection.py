# test_connection.py
import asyncio
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_ollama_connection():
    """Test Ollama connection"""
    try:
        async with aiohttp.ClientSession() as session:
            # Test 1: Check if Ollama is responding
            logger.info("Testing connection to Ollama...")
            async with session.get("http://localhost:11434/api/tags", timeout=5) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    models = [m['name'] for m in data.get('models', [])]
                    logger.info(f"✅ Connected to Ollama")
                    logger.info(f"📦 Available models: {models}")
                    
                    if 'codellama:7b' in models:
                        logger.info("✅ codellama:7b is available")
                    else:
                        logger.warning("⚠️ codellama:7b not found")
                        return False
                else:
                    logger.error(f"❌ Ollama returned status {resp.status}")
                    return False
            
            # Test 2: Try a simple generation
            logger.info("\nTesting code generation...")
            payload = {
                'model': 'codellama:7b',
                'prompt': 'Write a Python function that returns "hello world"',
                'stream': False,
                'options': {
                    'temperature': 0.7,
                    'max_tokens': 100
                }
            }
            
            async with session.post("http://localhost:11434/api/generate", 
                                   json=payload, timeout=30) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    response = result.get('response', '')
                    logger.info(f"✅ Generation successful!")
                    logger.info(f"📝 Response: {response[:200]}...")
                    return True
                else:
                    error_text = await resp.text()
                    logger.error(f"❌ Generation failed: {resp.status} - {error_text}")
                    return False
                    
    except asyncio.TimeoutError:
        logger.error("❌ Connection timeout")
        return False
    except aiohttp.ClientConnectorError:
        logger.error("❌ Cannot connect to Ollama. Make sure it's running")
        return False
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_ollama_connection())
    if result:
        print("\n✅ Ollama is working correctly! You can now run the evaluation.")
    else:
        print("\n❌ There are issues with Ollama. Fix them before running evaluation.")