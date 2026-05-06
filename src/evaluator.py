import tiktoken

def contar_tokens(texto):
    """Conta tokens usando o encoder padrão da OpenAI como base para o gpt-oss."""
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(texto))
    except:
        return 0

def medir_acuracia(resposta, esperado):
    """Compara a resposta da IA com o esperado do teu JSON."""
    resp = str(resposta).strip().lower()
    
    # Se o esperado for um dicionário (como na extração de ativos)
    if isinstance(esperado, dict):
        total_chaves = len(esperado)
        acertos = sum(1 for chave in esperado.keys() if chave.lower() in resp)
        return acertos / total_chaves if total_chaves > 0 else 0.0
    
    # Se for texto (como na classificação)
    esp = str(esperado).strip().lower()
    return 1.0 if esp in resp else 0.0