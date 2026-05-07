from src.prompt_builder import montar_prompt, adicionar_exemplos, adicionar_cot

def zero_shot(tarefa, input_usuario):
    """
    Técnica Zero-Shot: Prompt direto e claro.
    """
    prompt = montar_prompt(
        instrucao=tarefa['instrucao'],
        contexto=tarefa['contexto'],
        input_dados=input_usuario,
        formato_output=tarefa['formato_output']
    )
    return prompt

def few_shot(tarefa, input_usuario):
    """
    Técnica Few-Shot: Adiciona 2-3 exemplos reais.
    Os exemplos vêm do dicionário da tarefa.
    """
    prompt_base = montar_prompt(
        instrucao=tarefa['instrucao'],
        contexto=tarefa['contexto'],
        input_dados=input_usuario,
        formato_output=tarefa['formato_output']
    )
    
    exemplos = tarefa.get('exemplos_few_shot', [])
    return adicionar_exemplos(prompt_base, exemplos)

def chain_of_thought(tarefa, input_usuario):
    """
    Técnica Chain-of-Thought: Força o raciocínio explícito.
    """
    prompt_base = montar_prompt(
        instrucao=tarefa['instrucao'],
        contexto=tarefa['contexto'],
        input_dados=input_usuario,
        formato_output=tarefa['formato_output']
    )
    
    passos = tarefa.get('passos_cot', "1. Analise os dados brutos; 2. Identifique padrões; 3. Formule a conclusão.")
    return adicionar_cot(prompt_base, passos)

def role_prompting(tarefa, input_usuario, persona):
    """
    Técnica Role Prompting: Retorna tupla (system, user).
    Conforme Aula 07: Usa persona detalhada.
    """
    system_prompt = persona
    
    user_prompt = montar_prompt(
        instrucao=tarefa['instrucao'],
        contexto=tarefa['contexto'],
        input_dados=input_usuario,
        formato_output=tarefa['formato_output']
    )
    
    return (system_prompt, user_prompt)