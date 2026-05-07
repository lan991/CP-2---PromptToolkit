import tiktoken
import os

def contar_tokens(texto):
    """Conta tokens usando a codificação do cl100k_base (padrão GPT-4)."""
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(texto))
    except:
        return len(texto.split()) // 3

def medir_acuracia(resposta, esperado):
    """Valida se a resposta contém o esperado (case insensitive)."""
    resp = str(resposta).lower().strip()
    esp = str(esperado).lower().strip()
    return 1.0 if esp in resp else 0.0

def medir_consistencia(respostas):
    """Calcula a % de respostas idênticas em N tentativas."""
    if not respostas: return 0
    total = len(respostas)
    mais_comum = max(set(respostas), key=respostas.count)
    frequencia = respostas.count(mais_comum)
    return (frequencia / total) * 100

def testar_temperatura(client, prompt, temps=[0.1, 0.5, 1.0]):
    """Roda o mesmo prompt em diferentes temperaturas para o Report."""
    resultados_temp = []
    for t in temps:
        res = client.chat(prompt, temp=t)
        resultados_temp.append({
            "temperatura": t,
            "resposta": res['resposta'],
            "tokens": res['tokens_prompt'] + res['tokens_resposta']
        })
    return resultados_temp