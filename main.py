import json
import os
import time
import pandas as pd
import tiktoken
from dotenv import load_dotenv
from ollama import Client

from src.techniques import zero_shot, few_shot, chain_of_thought, role_prompting
from src.tasks import TASKS
from src.evaluator import medir_acuracia
from src.report import ReportGenerator

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configuração Ollama Cloud
client_ollama = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.getenv('OLLAMA_API_KEY')}
)

MODEL_ID = "gpt-oss:120b"

def carregar_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def chat_ollama(prompt, temp=0.3):
    inicio = time.time()
    try:
        # Se for Role Prompting (tupla), separamos system e user
        if isinstance(prompt, tuple):
            system_msg = str(prompt[0])
            user_msg = str(prompt[1])
            messages = [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ]
            prompt_para_token = system_msg + user_msg # Para contar tokens
        else:
            # Caso comum (string única)
            messages = [{"role": "user", "content": str(prompt)}]
            prompt_para_token = str(prompt)

        response = client_ollama.chat(
            model=MODEL_ID,
            messages=messages,
            options={
                "num_predict": 500, 
                "temperature": float(temp)
            },
            stream=False
        )
        
        resposta_texto = response['message']['content'].strip()
        fim = time.time()
        
        enc = tiktoken.get_encoding("cl100k_base")
        tokens_p = len(enc.encode(prompt_para_token))
        tokens_r = len(enc.encode(resposta_texto))
        
        return {
            "resposta": resposta_texto,
            "tokens_prompt": tokens_p,
            "tokens_resposta": tokens_r,
            "tempo_ms": int((fim - inicio) * 1000)
        }
    except Exception as e:
        print(f"Erro na API Ollama: {e}")
        return None

def executar_toolkit():
    report = ReportGenerator()
    inputs_data = carregar_json('data/inputs.json')
    personas = carregar_json('prompts/system_prompts.json')
    historico_resultados = []

    for task_id, task_info in TASKS.items():
        print(f"\n--- Tarefa: {task_info['nome']} ---")
        exemplos = inputs_data.get(task_id, [])

        for item in exemplos:
            input_texto = item['input']
            esperado = item['esperado']

            # Define as técnicas a serem testadas
            tecnicas = [
                ("Zero-Shot", zero_shot(task_info, input_texto)),
                ("Few-Shot", few_shot(task_info, input_texto)),
                ("Chain-of-Thought", chain_of_thought(task_info, input_texto)),
                ("Role-Prompting", role_prompting(task_info, input_texto, personas.get("analista_senior")))
            ]

            for nome_tec, prompt_final in tecnicas:
                print(f"Executando {nome_tec}...")
                # Pega temperatura do .env ou usa 0.3
                temp_atual = os.getenv("DEFAULT_TEMPERATURE", 0.3)
                
                res = chat_ollama(prompt_final, temp=temp_atual)
                
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
                        "temperatura": temp_atual
                    })

    if historico_resultados:
        # Gera o CSV e os relatórios finais
        df_geral = report.salvar_csv(historico_resultados)
        
        print("\n>>> Resultados Consolidados:")
        print(df_geral.groupby(['tarefa', 'tecnica'])[['acuracia', 'tempo_ms']].mean())
        
        report.gerar_grafico_acuracia(df_geral)
        report.gerar_grafico_custo(df_geral)
        report.recomendacao_automatica(df_geral)
    else:
        print("\n[Erro] Falha ao processar resultados: Nenhum dado coletado.")

if __name__ == "__main__":
    executar_toolkit()