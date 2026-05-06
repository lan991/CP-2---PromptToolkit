import json
import os
from dotenv import load_dotenv
from src.llm_client import LLMClient
from src.techniques import zero_shot, few_shot, chain_of_thought, role_prompting
from src.tasks import TASKS

load_dotenv()

def carregar_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def executar_toolkit():
    client = LLMClient()
    inputs_data = carregar_json('data/inputs.json')
    personas = carregar_json('prompts/system_prompts.json')
    
    resultados_finais = []

    print("Iniciando processamento das tarefas...")

    for task_id, info in TASKS.items():
        print(f"\nProcessando Tarefa: {info['nome']}")
        inputs_da_tarefa = inputs_data.get(task_id, [])

        for item in inputs_da_tarefa:
            # Exemplo de execução Zero-Shot
            prompt_zs = zero_shot(info, item['input'])
            res_zs = client.chat(prompt_zs)
            
            if res_zs:
                print(f"Input: {item['input'][:30]}... | Resposta ZS: {res_zs['resposta']}")
                # Aqui depois adicionaremos a lógica de salvar no relatório

if __name__ == "__main__":
    executar_toolkit()