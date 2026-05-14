# Prompt Engineering Toolkit - Domínio Financeiro

Este projeto é um toolkit de Engenharia de Prompt desenvolvido para o **CP2 (CheckPoint 2)**. O objetivo é avaliar e comparar sistematicamente diferentes técnicas de prompting aplicadas a tarefas do mercado financeiro, utilizando modelos de linguagem locais via API do Ollama.

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

* **Python 3.10 ou superior**: O projeto utiliza recursos de tipagem e manipulação de dados que exigem versões recentes.

* **Ollama API Key**: É necessário realizar o login no site oficial [Ollama.com](https://ollama.com), acessar as configurações (**Settings > Keys**) e gerar uma chave de API para autenticação no modelo remoto.

* **Modelo gpt-oss:120b**: O projeto utiliza este modelo via infraestrutura de nuvem, dispensando a necessidade de download local (pull) ou hardware de alta performance.

* **Bibliotecas Necessárias**: O toolkit exige as dependências listadas no `requirements.txt` (ollama, pandas, matplotlib, tiktoken e python-dotenv).

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

# Instalar todas as dependências necessárias
pip install -r requirements.txt
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
OLLAMA_API_KEY=insira_sua_chave_gerada_no_site
DEFAULT_TEMPERATURE=0.3
TIMEOUT_SECONDS=180
```


### 4. Executar o Toolkit
Para iniciar os testes e gerar os gráficos, execute o comando abaixo na raiz do projeto:
```bash
python main.py
```

### 5. Verificar os Resultados
Após a execução, o toolkit criará automaticamente a pasta /output. Verifique:

output/relatorio_final.csv: Tabela com todos os dados e métricas.

output/graficos/: Gráficos PNG comparando a performance das técnicas.