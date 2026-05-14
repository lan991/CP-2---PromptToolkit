import json
import os
import time
import pandas as pd
import tiktoken
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from src.techniques import zero_shot, few_shot, chain_of_thought, role_prompting
from src.tasks import TASKS
from src.evaluator import medir_acuracia
from src.report import ReportGenerator

load_dotenv()

# Configuracao do Cliente API
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = os.getenv("LLM_MODEL", "meta-llama/Meta-Llama-3.1-70B-Instruct")

if not HF_TOKEN:
    print("Erro: HF_TOKEN nao encontrado no arquivo .env")
    client_hf = None
else:
    client_hf = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

def carregar_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def chat_hf(prompt, temp=0.5):
    if not client_hf:
        return None
    
    inicio = time.time()
    try:
        response = client_hf.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=float(temp)
        )
        resposta_texto = response.choices[0].message.content
        fim = time.time()
        
        enc = tiktoken.get_encoding("cl100k_base")
        tokens_p = len(enc.encode(prompt))
        tokens_r = len(enc.encode(resposta_texto))
        
        return {
            "resposta": resposta_texto,
            "tokens_prompt": tokens_p,
            "tokens_resposta": tokens_r,
            "tempo_ms": int((fim - inicio) * 1000)
        }
    except Exception as e:
        print(f"Erro na API: {e}")
        return None

def executar_toolkit():
    report = ReportGenerator()
    inputs_data = carregar_json('data/inputs.json')
    personas = carregar_json('prompts/system_prompts.json')
    historico_resultados = []

    for task_id, task_info in TASKS.items():
        print(f"Tarefa: {task_info['nome']}")
        exemplos = inputs_data.get(task_id, [])

        for item in exemplos:
            input_texto = item['input']
            esperado = item['esperado']

            tecnicas = [
                ("Zero-Shot", zero_shot(task_info, input_texto)),
                ("Few-Shot", few_shot(task_info, input_texto)),
                ("Chain-of-Thought", chain_of_thought(task_info, input_texto)),
                ("Role-Prompting", role_prompting(task_info, input_texto, personas.get("analista_senior")))
            ]

            for nome_tec, prompt_final in tecnicas:
                print(f"Executando {nome_tec}...")
                temp_atual = os.getenv("DEFAULT_TEMPERATURE", 0.5)
                res = chat_hf(prompt_final, temp=temp_atual)
                
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
        df_geral = report.salvar_csv(historico_resultados)
        print("\nResultados Consolidados:")
        print(df_geral.groupby(['tarefa', 'tecnica'])[['acuracia', 'tempo_ms']].mean())
        
        report.gerar_grafico_acuracia(df_geral)
        report.gerar_grafico_custo(df_geral)
        report.recomendacao_automatica(df_geral)

        print("\nTeste de Variacao de Temperatura:")
        teste_input = exemplos[0]['input']
        for temp in [0.1, 0.5, 1.0]:
            res_temp = chat_hf(zero_shot(task_info, teste_input), temp=temp)
            if res_temp:
                print(f"Temp {temp}: {res_temp['resposta'][:50]}...")
    else:
        print("Falha ao processar resultados.")

if __name__ == "__main__":
    executar_toolkit()