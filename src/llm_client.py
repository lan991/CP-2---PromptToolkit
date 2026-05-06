import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434/api/chat")
        self.model = os.getenv("LLM_MODEL", "gpt-oss:120b")

    def chat(self, prompt, system_prompt=None, timeout=60):
        payload = {
            "model": self.model,
            "messages": [],
            "stream": False,
            "options": {
                "temperature": float(os.getenv("DEFAULT_TEMPERATURE", 0.5))
            }
        }

        if system_prompt:
            payload["messages"].append({"role": "system", "content": system_prompt})
        
        payload["messages"].append({"role": "user", "content": prompt})

        try:
            start_time = time.time()
            response = requests.post(self.host, json=payload, timeout=timeout)
            response.raise_for_status()
            end_time = time.time()

            data = response.json()
            
            return {
                "resposta": data.get("message", {}).get("content", ""),
                "tokens_prompt": data.get("prompt_eval_count", 0),
                "tokens_resposta": data.get("eval_count", 0),
                "tempo_ms": int((end_time - start_time) * 1000)
            }
        except Exception as e:
            print(f"Erro na conexão com o Ollama: {e}")
            return None