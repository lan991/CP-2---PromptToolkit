# src/prompt_builder.py

def limpar_texto(texto):
    """Remove espaços extras e garante que o texto esteja limpo para o prompt."""
    return " ".join(texto.split()) if isinstance(texto, str) else str(texto)

def montar_prompt(instrucao, contexto, input_dados, formato_output):
    """
    Monta o prompt seguindo a anatomia rigorosa da Aula 05.
    Garante a separação clara entre blocos para evitar injeção de dados.
    """
    # Validação rigorosa dos componentes
    componentes = {
        "Instrução": instrucao,
        "Contexto": contexto,
        "Dados": input_dados,
        "Formato": formato_output
    }
    
    for nome, valor in componentes.items():
        if not valor or str(valor).strip() == "":
            raise ValueError(f"Erro Crítico: O componente '{nome}' está vazio e é obrigatório.")

    # Construção com delimitadores claros (Markdown Headers)
    prompt = f"""### 1. OBJETIVO E INSTRUÇÃO
{limpar_texto(instrucao)}

### 2. CONTEXTO E REGRAS
{limpar_texto(contexto)}

### 3. DADOS DE ENTRADA (INPUT)
{limpar_texto(input_dados)}

### 4. FORMATO DE RESPOSTA ESPERADO
{limpar_texto(formato_output)}

---
Sua resposta deve seguir estritamente o formato acima:"""

    return prompt.strip()

def adicionar_exemplos(prompt_base, exemplos):
    """
    Implementa a técnica Few-Shot (Aula 06).
    Adiciona demonstrações de padrão de entrada e saída.
    """
    if not exemplos or not isinstance(exemplos, list):
        return prompt_base

    secao_exemplos = "\n\n### 5. EXEMPLOS DE REFERÊNCIA (FEW-SHOT)\n"
    for i, ex in enumerate(exemplos, 1):
        secao_exemplos += f"Exemplo {i}:\n- Entrada: {ex.get('input')}\n- Saída: {ex.get('output')}\n"
    
    return prompt_base + secao_exemplos

def adicionar_cot(prompt_base, passos):
    """
    Implementa Chain of Thought (Aula 07).
    Força o modelo a seguir um caminho lógico antes da resposta final.
    """
    if not passos or not isinstance(passos, list):
        return prompt_base

    instrucao_cot = "\n\n### 6. PROCESSO DE RACIOCÍNIO (Chain of Thought)\n"
    instrucao_cot += "Para resolver esta tarefa, execute mentalmente os seguintes passos:\n"
    
    for i, passo in enumerate(passos, 1):
        instrucao_cot += f"Passo {i}: {limpar_texto(passo)}\n"
    
    instrucao_cot += "\nInicie sua resposta detalhando o raciocínio aplicado."
    
    return prompt_base + instrucao_cot