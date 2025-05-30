import requests

def test_ollama():
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma3:4b",
                "prompt": "Say hello!",
                "stream": False
            }
        )
        response.raise_for_status()
        print("Ollama Response:", response.json()["response"])
        print("✅ Ollama is working!")
    except Exception as e:
        print("❌ Error connecting to Ollama:", str(e))
        print("\nMake sure Ollama is running by:")
        print("1. Opening a terminal")
        print("2. Running 'ollama serve'")
        print("3. In another terminal, run 'ollama pull mistral'")

if __name__ == "__main__":
    test_ollama() 