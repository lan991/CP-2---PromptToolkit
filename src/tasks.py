TASKS = {
    "classificacao_sentimento_mercado": {
        "nome": "Classificação de Sentimento (Mercado)",
        "tipo": "classificacao",
        "instrucao": "Analise o sentimento do texto sobre o mercado financeiro.",
        "formato_output": "Responda APENAS com uma das opções: OTIMISTA, PESSIMISTA ou NEUTRO.", # [cite: 160]
        "passos_cot": [
            "Identifique termos relacionados a alta ou baixa de ativos.",
            "Avalie o tom geral do autor sobre a economia.",
            "Classifique o sentimento final com base nos indicadores encontrados."
        ]
    },
    "extracao_ativos_financeiros": {
        "nome": "Extração de Ativos e Valores",
        "tipo": "extracao",
        "instrucao": "Extraia tickers de ações e seus respectivos valores mencionados.",
        "formato_output": "Responda em formato JSON: {'ticker': 'valor'}.",
        "passos_cot": [
            "Localize códigos de ativos (ex: PETR4, VALE3).",
            "Identifique valores monetários próximos a esses códigos.",
            "Estruture os dados em um objeto JSON limpo."
        ]
    },
    "sumarizacao_relatorio": {
        "nome": "Sumarização de Relatório",
        "tipo": "sumarizacao",
        "instrucao": "Crie um resumo executivo em tópicos do relatório de investimentos fornecido.",
        "formato_output": "Responda com no máximo 3 bullet points.",
        "passos_cot": [
            "Identifique a principal tese de investimento do texto.",
            "Destaque os riscos mencionados.",
            "Sintetize as conclusões em frases curtas."
        ]
    }
}