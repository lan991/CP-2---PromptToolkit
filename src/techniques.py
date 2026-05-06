from src.prompt_builder import montar_prompt, adicionar_exemplos, adicionar_cot

def zero_shot(tarefa, input_usuario):
    return montar_prompt(
        instrucao=tarefa['instrucao'],
        contexto="Você é um assistente focado em precisão técnica.",
        input_dados=input_usuario,
        formato_output=tarefa['formato_output']
    )

def few_shot(tarefa, input_usuario, exemplos):
    """Monta o prompt com 2-3 exemplos reais."""
    prompt_base = montar_prompt(
        instrucao=tarefa['instrucao'],
        contexto="Baseie sua resposta nos exemplos fornecidos abaixo.",
        input_dados=input_usuario,
        formato_output=tarefa['formato_output']
    )
    return adicionar_exemplos(prompt_base, exemplos)

def chain_of_thought(tarefa, input_usuario):
    """Monta o prompt forçando o raciocínio passo a passo."""
    prompt_base = montar_prompt(
        instrucao=tarefa['instrucao'],
        contexto="Pense de forma lógica antes de responder.",
        input_dados=input_usuario,
        formato_output=tarefa['formato_output']
    )
    return adicionar_cot(prompt_base, tarefa['passos_cot'])

def role_prompting(tarefa, input_usuario, persona):
    """Usa um system prompt (persona) detalhado."""
    user_prompt = montar_prompt(
        instrucao=tarefa['instrucao'],
        contexto=f"Sua especialidade é: {persona['especialidade']}.",
        input_dados=input_usuario,
        formato_output=tarefa['formato_output']
    )

    system_prompt = f"Persona: {persona['nome']}. Experiência: {persona['experiencia']}. Tom de voz: {persona['tom_de_voz']}."
    return system_prompt, user_prompt