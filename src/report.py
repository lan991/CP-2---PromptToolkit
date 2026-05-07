import pandas as pd
import matplotlib.pyplot as plt
import os

class ReportGenerator:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self.graficos_dir = os.path.join(output_dir, "graficos")
        os.makedirs(self.graficos_dir, exist_ok=True)

    def gerar_tabela(self, resultados):
        """Cria DataFrame e salva CSV conforme PDF."""
        df = pd.DataFrame(resultados)
        caminho_csv = os.path.join(self.output_dir, "relatorio_final.csv")
        df.to_csv(caminho_csv, index=False, encoding='utf-8')
        return df

    def grafico_acuracia(self, df):
        """Gráfico de barras agrupadas por técnica."""
        plt.figure(figsize=(10, 6))
        acc_stats = df.groupby('tecnica')['acuracia'].mean()
        acc_stats.plot(kind='bar', color=['skyblue', 'orange', 'green', 'red'])
        plt.title('Acurácia Média por Técnica')
        plt.ylabel('Score (0 a 1)')
        plt.savefig(os.path.join(self.graficos_dir, "acuracia_tecnica.png"))
        plt.close()

    def grafico_custo(self, df):
        """Gráfico de tokens médios por técnica."""
        plt.figure(figsize=(10, 6))
        custo_stats = df.groupby('tecnica')['tokens_totais'].mean()
        custo_stats.plot(kind='barh', color='salmon')
        plt.title('Custo Médio de Tokens por Técnica')
        plt.xlabel('Quantidade de Tokens')
        plt.savefig(os.path.join(self.graficos_dir, "custo_tokens.png"))
        plt.close()

    def grafico_temperatura(self, df_temp):
        """Gráfico de consistência por temperatura."""
        plt.figure(figsize=(8, 5))
        plt.plot(df_temp['temperatura'], df_temp['consistencia'], marker='o', linestyle='--')
        plt.title('Consistência vs Temperatura')
        plt.xlabel('Temperatura')
        plt.ylabel('Consistência (%)')
        plt.savefig(os.path.join(self.graficos_dir, "consistencia_temp.png"))
        plt.close()

    def recomendar(self, df):
        """Gera recomendação automática com justificativa."""
        print("\nRECOMENDAÇÃO TÉCNICA")
        melhores = df.groupby('tarefa').apply(lambda x: x.loc[x['acuracia'].idxmax()])
        for index, row in melhores.iterrows():
            print(f"Tarefa: {row['tarefa']}")
            print(f"-> Melhor Técnica: {row['tecnica']}")
            print(f"-> Justificativa: Maior acurácia observada ({row['acuracia']*100}%).")
            print("-" * 30)