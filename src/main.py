from models import (
    load_dataset, plot_series, plot_acf_pacf, apply_arima, apply_sarima,
    exemplo_mineracao_texto
)
from webScraping import scrape_f1_results


dataset_path = './files/dataset.csv'

# === Séries temporais ===
df, value_col = load_dataset(dataset_path)
plot_series(df, value_col, title='Série Temporal Original')
plot_acf_pacf(df, value_col)

print("Executando ARIMA...")
arima_results = apply_arima(df, value_col)

print("Executando SARIMA...")
sarima_results = apply_sarima(df, value_col)

# === Mineração de Texto ===
exemplo_mineracao_texto()

scrape_f1_results()

