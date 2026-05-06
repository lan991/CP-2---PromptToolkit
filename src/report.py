import pandas as pd
import matplotlib.pyplot as plt
import os

class ReportGenerator:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self.graficos_dir = os.path.join(output_dir, "graficos")
        
        os.makedirs(self.graficos_dir, exist_ok=True)

    def salvar_csv(self, resultados, filename="relatorio_final.csv"):
        """Salva a lista de dicionários em um CSV."""
        df = pd.DataFrame(resultados)
        caminho = os.path.join(self.output_dir, filename)
        df.to_csv(caminho, index=False, encoding='utf-8')
        print(f"CSV gerado em: {caminho}")
        return df

    def gerar_grafico_acuracia(self, df):
        """Gera gráfico de barras comparando a acurácia por técnica."""
        plt.figure(figsize=(10, 6))
        acuracia_media = df.groupby('tecnica')['acuracia'].mean()
        
        acuracia_media.plot(kind='bar', color=['skyblue', 'salmon', 'lightgreen', 'orange'])
        plt.title('Acurácia Média por Técnica de Prompting')
        plt.ylabel('Acurácia (0 a 1)')
        plt.xlabel('Técnica')
        plt.ylim(0, 1.1)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        path = os.path.join(self.graficos_dir, "comparativo_acuracia.png")
        plt.savefig(path)
        plt.close()
        print(f"Gráfico de acurácia salvo em: {path}")

    def gerar_grafico_custo(self, df):
        """Gera gráfico de custo (tokens totais) por técnica."""
        plt.figure(figsize=(10, 6))
        tokens_medios = df.groupby('tecnica')['tokens_totais'].mean()
        
        tokens_medios.plot(kind='line', marker='o', color='red')
        plt.title('Consumo Médio de Tokens por Técnica')
        plt.ylabel('Total de Tokens (Prompt + Resposta)')
        plt.grid(True, alpha=0.3)
        
        path = os.path.join(self.graficos_dir, "consumo_tokens.png")
        plt.savefig(path)
        plt.close()
        print(f"Gráfico de tokens salvo em: {path}")

    def recomendacao_automatica(self, df):
        """Lógica simples para recomendar a melhor técnica (Melhor acurácia com menos tokens)."""
        resumo = df.groupby('tecnica').agg({
            'acuracia': 'mean',
            'tokens_totais': 'mean'
        }).reset_index()
        
        melhor = resumo.sort_values(by=['acuracia', 'tokens_totais'], ascending=[False, True]).iloc[0]
        
        rec_text = f"RECOMENDAÇÃO: A técnica '{melhor['tecnica']}' foi a mais eficiente."
        print(f"{rec_text}")
        return rec_text