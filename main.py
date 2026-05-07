import json
import os
import pandas as pd
from dotenv import load_dotenv
from src.llm_client import LLMClient
from src.techniques import zero_shot, few_shot, chain_of_thought, role_prompting
from src.tasks import TASKS
from src.evaluator import medir_acuracia
from src.report import ReportGenerator

# 1. Carregar configurações
load_dotenv()

def carregar_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def executar_toolkit():
    client = LLMClient()
    report = ReportGenerator()
    
    # Carregando dados e personas
    inputs_data = carregar_json('data/inputs.json')
    personas = carregar_json('prompts/system_prompts.json')
    
    historico_resultados = []

    # 2. Para cada TAREFA definida em tasks.py
    for task_id, task_info in TASKS.items():
        print(f"\nIniciando Tarefa: {task_info['nome']}")
        
        # a. Carregar os inputs (o PDF pede 5, nosso JSON já tem 5 por tarefa)
        exemplos_da_vez = inputs_data.get(task_id, [])

        # b. Aplicar as 4 técnicas
        for item in exemplos_da_vez:
            input_texto = item['input']
            esperado = item['esperado']

            tecnicas = [
                ("Zero-Shot", zero_shot(task_info, input_texto)),
                ("Few-Shot", few_shot(task_info, input_texto)),
                ("Chain-of-Thought", chain_of_thought(task_info, input_texto)),
                ("Role-Prompting", role_prompting(task_info, input_texto, personas.get("analista_senior")))
            ]

            for nome_tec, prompt_final in tecnicas:
                res = client.chat(prompt_final)
                
                if res:
                    acuracia = medir_acuracia(res['resposta'], esperado)
                    
                    historico_resultados.append({
                        "tarefa": task_id,
                        "tecnica": nome_tec,
                        "input": input_texto,
                        "resposta": res['resposta'],
                        "acuracia": acuracia,
                        "tokens_totais": res['tokens_prompt'] + res['tokens_resposta'],
                        "tempo_ms": res['tempo_ms'],
                        "temperatura": os.getenv("DEFAULT_TEMPERATURE", 0.5)
                    })

    # 3. Gerar relatório
    df_geral = report.salvar_csv(historico_resultados)
    print("\nTABELA COMPARATIVA")
    print(df_geral.groupby(['tarefa', 'tecnica'])[['acuracia', 'tempo_ms']].mean())
    
    report.gerar_grafico_acuracia(df_geral)
    report.gerar_grafico_custo(df_geral)
    melhor_tecnica_texto = report.recomendacao_automatica(df_geral)

    # 4. Executar teste de temperatura (0.1, 0.5, 1.0) no melhor prompt
    print("\nIniciando Teste de Temperatura no melhor cenário...")
    teste_input = exemplos_da_vez[0]['input']
    temperaturas = [0.1, 0.5, 1.0]
    
    for temp in temperaturas:
        os.environ["DEFAULT_TEMPERATURE"] = str(temp)
        res_temp = client.chat(zero_shot(task_info, teste_input)) # Usando a técnica base
        print(f"Temp {temp}: {res_temp['resposta'][:50]}... (Tokens: {res_temp['tokens_resposta']})")

if __name__ == "__main__":
    executar_toolkit()