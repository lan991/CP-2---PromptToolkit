import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434/api/chat")
        self.model = os.getenv("LLM_MODEL", "gpt-oss:120b")

    def chat(self, prompt, system=None, temp=0.5, max_tokens=1000):
        """
        Método conforme PDF: envia prompt para Ollama e retorna estatísticas.
        Inclui tratamento de erros (timeout, rate limit, retry).
        """
        payload = {
            "model": self.model,
            "messages": [],
            "stream": False,
            "options": {
                "temperature": temp,
                "num_predict": max_tokens
            }
        }

        if system:
            payload["messages"].append({"role": "system", "content": system})
        
        if isinstance(prompt, tuple):
            payload["messages"] = [
                {"role": "system", "content": prompt[0]},
                {"role": "user", "content": prompt[1]}
            ]
        else:
            payload["messages"].append({"role": "user", "content": prompt})

        tentativas = 3
        timeout_val = int(os.getenv("TIMEOUT_SECONDS", 120))

        for i in range(tentativas):
            try:
                start_time = time.time()
                
                response = requests.post(
                    self.host, 
                    json=payload, 
                    timeout=timeout_val
                )
                
                if response.status_code in [429, 503]:
                    time.sleep(5)
                    continue
                
                response.raise_for_status()
                end_time = time.time()
                
                data = response.json()
                
                return {
                    "resposta": data.get("message", {}).get("content", ""),
                    "tokens_prompt": data.get("prompt_eval_count", 0),
                    "tokens_resposta": data.get("eval_count", 0),
                    "tempo_ms": int((end_time - start_time) * 1000)
                }

            except requests.exceptions.RequestException as e:
                print(f"Tentativa {i+1}/{tentativas} falhou: {e}")
                if i == tentativas - 1:
                    return {
                        "resposta": f"ERRO DE CONEXÃO: {str(e)}",
                        "tokens_prompt": 0,
                        "tokens_resposta": 0,
                        "tempo_ms": 0
                    }
                time.sleep(2)

        return None