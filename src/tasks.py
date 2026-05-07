# src/tasks.py

TASKS = {
    "classificacao_sentimento_mercado": {
        "nome": "Classificação de Sentimento de Notícias",
        "tipo": "classificacao",
        "instrucao": "Analise o título da notícia financeira e classifique o impacto esperado no mercado.",
        "contexto": "Você atua na mesa de operações da Braúna Investimentos e precisa filtrar notícias rapidamente.",
        "formato_output": "Responda APENAS com uma das etiquetas: POSITIVO, NEGATIVO, NEUTRO ou MISTO.",
        "exemplos_few_shot": [
            {"input": "IPCA cai mais que o esperado em abril.", "esperado": "POSITIVO"},
            {"input": "Tensões geopolíticas elevam preço do barril de petróleo.", "esperado": "NEGATIVO"}
        ],
        "passos_cot": "1. Identifique o ativo ou índice mencionado; 2. Avalie se o fato é favorável à economia; 3. Compare com as expectativas de mercado; 4. Emita a classificação final.",
        "persona_chave": "analista_senior"
    },
    
    "extracao_dados_financeiros": {
        "nome": "Extração de Dados de Relatórios (NER)",
        "tipo": "extracao",
        "instrucao": "Extraia os dados estruturados do texto fornecido sobre ativos da B3.",
        "contexto": "Você é um engenheiro de dados automatizando a leitura de relatórios diários.",
        "formato_output": "JSON com as chaves: 'ticker', 'preco_fechamento', 'variacao_percentual'.",
        "exemplos_few_shot": [
            {"input": "PETR4 fechou o dia a R$ 38,50 com alta de 1,2%.", "esperado": '{"ticker": "PETR4", "preco_fechamento": "38,50", "variacao_percentual": "1,2%"}'}
        ],
        "passos_cot": "1. Localize os códigos de 4 letras e 1 número (tickers); 2. Identifique valores monetários; 3. Capture a porcentagem de variação; 4. Formate tudo como JSON.",
        "persona_chave": "engenheiro_dados"
    },
    
    "sumarizacao_executiva": {
        "nome": "Sumarização de Reunião de Comitê",
        "tipo": "sumarizacao",
        "instrucao": "Resuma os pontos principais da ata de reunião em tópicos executivos.",
        "contexto": "Resumo destinado à diretoria para tomada de decisão rápida.",
        "formato_output": "Lista de bullet points (máximo 3 tópicos).",
        "exemplos_few_shot": [
            {"input": "Discussão sobre Selic e manutenção da taxa devido à inflação persistente.", "esperado": "* Manutenção da Taxa Selic\n* Foco na inflação persistente\n* Decisão do comitê"}
        ],
        "passos_cot": "1. Leia o texto completo; 2. Filtre apenas decisões concretas; 3. Escreva de forma concisa e direta.",
        "persona_chave": "analista_senior"
    }
}