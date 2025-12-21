import requests
import json
import psutil

def analyze_memory_usage():
    print("📊 Detailed Memory Analysis:")
    memory = psutil.virtual_memory()
    print(f"Total: {memory.total / (1024**3):.2f} GB")
    print(f"Available: {memory.available / (1024**3):.2f} GB")
    print(f"Used: {memory.used / (1024**3):.2f} GB")
    print(f"Percent: {memory.percent}%")
    
    print("\n🔍 Top memory consumers:")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            mem_usage = proc.info['memory_info'].rss / (1024**3)
            if mem_usage > 0.1:  # Show > 100MB
                processes.append((proc.info['name'], mem_usage))
        except:
            pass
    
    # Sort by memory usage
    processes.sort(key=lambda x: x[1], reverse=True)
    for name, usage in processes[:10]:
        print(f"   {name}: {usage:.2f} GB")

analyze_memory_usage()

def test_ollama_memory():
    """Test if Ollama can handle the model with current memory settings"""
    
    # Test with a very small prompt first
    test_payload = {
        "model": "codellama:7b",
        "prompt": "def hello(): return 'world'",
        "stream": False,
        "options": {
            "num_predict": 50,  # Very short response
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=test_payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Ollama generation successful!")
            print(f"Response: {result.get('response', '')[:100]}...")
            return True
        else:
            print(f"❌ Ollama failed with status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        return False

if __name__ == "__main__":
    analyze_memory_usage()