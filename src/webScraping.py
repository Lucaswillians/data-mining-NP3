import pandas as pd
import os

def scrape_f1_results():
    url = 'https://en.wikipedia.org/wiki/2024_Formula_One_World_Championship'
    try:
        tables = pd.read_html(url)
    except Exception as e:
        print(f"Erro ao ler as tabelas da página: {e}")
        return
    
    # Procurar tabela que contém resultados de corridas — geralmente a primeira tabela grande é a classificação das corridas
    # Vamos salvar a primeira tabela como exemplo
    if tables:
        df = tables[0]
        os.makedirs('./files', exist_ok=True)
        csv_path = './files/f1_results.csv'
        df.to_csv(csv_path, index=False)
        print(f"Dados de corridas de F1 salvos em {csv_path}")
    else:
        print("Nenhuma tabela encontrada na página.")
