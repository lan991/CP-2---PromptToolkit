# Prompt Engineering Toolkit - Domínio Financeiro

Este projeto é um toolkit de Engenharia de Prompt desenvolvido para o **CP2 (CheckPoint 2)**. O objetivo é avaliar e comparar sistematicamente diferentes técnicas de prompting aplicadas a tarefas do mercado financeiro, utilizando modelos de linguagem locais via API do Ollama.

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

* **Python 3.10 ou superior**: O projeto utiliza recursos de tipagem e manipulação de dicionários que exigem versões recentes.
* **Ollama**: O motor de execução de modelos locais deve estar instalado e **ativo** (verifique o ícone na barra de tarefas).
* **Modelo gpt-oss:120b**: É necessário realizar o pull do modelo via terminal antes da execução:
    ```bash
    ollama pull gpt-oss:120b
    ```
    *(Nota: Caso seu hardware não suporte o modelo de 120b, você pode alterar o `LLM_MODEL` no arquivo `.env` para outro modelo como `llama3`).*
* **Bibliotecas de Dados**: O toolkit exige as dependências listadas no `requirements.txt` (Pandas, Matplotlib, Tiktoken).

## Como Rodar o Projeto

Siga os passos abaixo para preparar o ambiente e executar o toolkit:

### 1. Clonar e Preparar o Ambiente
Recomendamos o uso de um ambiente virtual (venv) para isolar as dependências e evitar conflitos no sistema:
```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente (Windows)
.\venv\Scripts\activate

# Ativar o ambiente (Linux/Mac)
source venv/bin/activate
```


### 2. Instalar Dependências

Com o ambiente virtual ativo, instale todos os pacotes necessários listados no arquivo de requisitos:
```bash
pip install -r requirements.txt
```


### 3. Configurar Variáveis de Ambiente (.env)
O sistema precisa saber onde o Ollama está rodando.
1. Na raiz do projeto, crie um arquivo chamado `.env`.
2. Adicione as seguintes configurações:
```text
OLLAMA_HOST=http://localhost:11434/api/chat
LLM_MODEL=gpt-oss:120b
TIMEOUT_SECONDS=180
```


### 4. Executar o Toolkit
Para iniciar os testes e gerar os gráficos, execute o comando abaixo na raiz do projeto:
```bash
python main.py
```

###5. Verificar os Resultados
Após a execução, o toolkit criará automaticamente a pasta /output. Verifique:

output/relatorio_final.csv: Tabela com todos os dados e métricas.

output/graficos/: Gráficos PNG comparando a performance das técnicas.