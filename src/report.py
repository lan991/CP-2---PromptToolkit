import pandas as pd
import matplotlib.pyplot as plt
import os

class ReportGenerator:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self.graficos_dir = os.path.join(output_dir, "graficos")
        os.makedirs(self.graficos_dir, exist_ok=True)

    def salvar_csv(self, resultados):
        """Salva os resultados em CSV e retorna o DataFrame."""
        df = pd.DataFrame(resultados)
        caminho_csv = os.path.join(self.output_dir, "resultados.csv")
        df.to_csv(caminho_csv, index=False, encoding='utf-8')
        print(f"Arquivo salvo em: {caminho_csv}")
        return df

    def gerar_grafico_acuracia(self, df):
        """Gráfico de barras agrupadas por técnica."""
        plt.figure(figsize=(10, 6))
        acc_stats = df.groupby('tecnica')['acuracia'].mean()
        acc_stats.plot(kind='bar', color=['skyblue', 'orange', 'green', 'red'])
        plt.title('Acurácia Média por Técnica')
        plt.ylabel('Score (0 a 1)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.graficos_dir, "acuracia_tecnica.png"))
        plt.close()
        print(f"Gráfico de acurácia gerado em: {self.graficos_dir}")

    def gerar_grafico_custo(self, df):
        """Gráfico de tokens médios por técnica."""
        plt.figure(figsize=(10, 6))
        custo_stats = df.groupby('tecnica')['tokens_totais'].mean()
        custo_stats.plot(kind='barh', color='salmon')
        plt.title('Custo Médio de Tokens por Técnica')
        plt.xlabel('Quantidade de Tokens')
        plt.tight_layout()
        plt.savefig(os.path.join(self.graficos_dir, "custo_tokens.png"))
        plt.close()
        print(f"Gráfico de custo gerado em: {self.graficos_dir}")

    def recomendacao_automatica(self, df):
        """Gera recomendação automática no terminal conforme chamado na main."""
        print("\n" + "="*30)
        print("RECOMENDAÇÃO TÉCNICA")
        print("="*30)
        
        # Agrupa por tarefa e pega a linha com maior acurácia
        melhores = df.sort_values('acuracia', ascending=False).drop_duplicates('tarefa')
        
        for _, row in melhores.iterrows():
            print(f"Tarefa: {row['tarefa']}")
            print(f"-> Melhor Técnica: {row['tecnica']}")
            print(f"-> Justificativa: Maior acurácia observada ({row['acuracia']*100}%).")
            print("-" * 30)