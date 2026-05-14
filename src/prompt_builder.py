import os

def montar_prompt(instrucao, contexto, input_dados, formato_output):
    """
    Constrói o prompt seguindo a anatomia da Aula 05.
    Separa explicitamente instrução, contexto e dados.
    """
    componentes = {
        "instrução": instrucao,
        "contexto": contexto,
        "dados de entrada": input_dados,
        "formato de saída": formato_output
    }
    
    for nome, valor in componentes.items():
        if not valor or str(valor).strip() == "":
            raise ValueError(f"Erro: O componente '{nome}' não pode estar vazio.")

    prompt_estruturado = f"""### 1. INSTRUÇÃO
{instrucao}

### 2. CONTEXTO
{contexto}

### 3. DADOS DE ENTRADA
{input_dados}

### 4. FORMATO DE SAÍDA ESPERADO
{formato_output}
"""
    return prompt_estruturado

def adicionar_exemplos(prompt_base, exemplos):
    if not exemplos:
        return prompt_base
        
    # Inicializando a variável corretamente
    secao_exemplos = "\n### 5. EXEMPLOS DE REFERÊNCIA (FEW-SHOT)\n"
    
    for i, ex in enumerate(exemplos, 1):
        entrada = ex.get('input', 'N/A')
        saida = ex.get('esperado', 'N/A')
        secao_exemplos += f"Exemplo {i}:\nEntrada: {entrada}\nSaída: {saida}\n---\n"
    
    return prompt_base + secao_exemplos

def adicionar_cot(prompt_base, passos=None):
    diretriz_cot = "\n### 6. RACIOCÍNIO PASSO A PASSO (CHAIN-OF-THOUGHT)\n"
    if passos:
        diretriz_cot += f"Siga estes passos para resolver o problema:\n{passos}\n"
    else:
        diretriz_cot += "Pense passo a passo antes de chegar à conclusão final e apresente o seu raciocínio.\n"
    
    return prompt_base + diretriz_cot