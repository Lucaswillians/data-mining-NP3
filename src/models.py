import re
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings

warnings.filterwarnings("ignore")

def load_dataset(path):
    df = pd.read_csv(path, encoding='latin-1', on_bad_lines='skip', sep=';')

    df.columns = [c.lower().strip() for c in df.columns]
    date_col = [col for col in df.columns if 'date' in col or 'data' in col]

    print("Colunas do dataset:", df.columns.tolist())
    print("Colunas de data detectadas:", date_col)

    value_cols = [col for col in df.columns if col not in date_col]
    if not value_cols:
        raise ValueError("Nenhuma coluna de valor encontrada além da coluna de data.")
    value_col = value_cols[0]

    if date_col:
        df[date_col[0]] = pd.to_datetime(df[date_col[0]], errors='coerce')
        df = df.dropna(subset=[date_col[0]])  
        df.set_index(date_col[0], inplace=True)

    return df, value_col


def plot_series(df, value_col, title='Série Temporal'):
    plt.figure(figsize=(10, 4))
    plt.plot(df[value_col])
    plt.title(title)
    plt.xlabel('Tempo')
    plt.ylabel('Valor')
    plt.tight_layout()
    plt.show()


def plot_acf_pacf(df, value_col):
    plot_acf(df[value_col])
    plot_pacf(df[value_col])
    plt.show()


def apply_arima(df, value_col, order=(1, 1, 1), steps=10):
    model = ARIMA(df[value_col], order=order)
    results = model.fit()
    forecast = results.forecast(steps=steps)

    plt.figure(figsize=(10, 4))
    plt.plot(df[value_col], label='Original')
    plt.plot(forecast.index, forecast, label='ARIMA Previsão', color='orange')
    plt.title(f'Previsão com ARIMA{order}')
    plt.legend()
    plt.tight_layout()
    plt.show()

    return results


def apply_sarima(df, value_col, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12), steps=10):
    model = SARIMAX(df[value_col], order=order, seasonal_order=seasonal_order)
    results = model.fit()
    forecast = results.forecast(steps=steps)

    plt.figure(figsize=(10, 4))
    plt.plot(df[value_col], label='Original')
    plt.plot(forecast.index, forecast, label='SARIMA Previsão', color='green')
    plt.title(f'Previsão com SARIMA{order}{seasonal_order}')
    plt.legend()
    plt.tight_layout()
    plt.show()

    return results


# --- Mineração de texto ---

def tokenizacao(texto):
    """Tokeniza o texto em palavras, removendo pontuação e convertendo para minúsculas."""
    tokens = re.findall(r'\b\w+\b', texto.lower())
    return tokens


def frequencia_palavras(textos):
    """Conta as frequências das palavras em uma lista de textos."""
    all_tokens = []
    for texto in textos:
        all_tokens.extend(tokenizacao(texto))
    return Counter(all_tokens)


def remover_stopwords(tokens, stopwords=None):
    """Remove palavras comuns (stopwords) da lista de tokens."""
    if stopwords is None:
        stopwords = set(['de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'com', 'não', 'uma', 'os', 'no', 'se'])
    return [token for token in tokens if token not in stopwords]


def extrair_bigramas(tokens):
    """Extrai bigramas (pares de palavras consecutivas) dos tokens."""
    return [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]


def exemplo_mineracao_texto():
    """
    Exemplos de técnicas de mineração de texto:
    1) Tokenização (vista em aula)
    2) Frequência de palavras
    3) Remoção de stopwords + frequência
    """
    textos = [
        "O ChatGPT é uma ferramenta incrível para processamento de linguagem natural.",
        "Mineração de texto permite extrair informações valiosas de grandes volumes de texto.",
        "Redes sociais são uma fonte rica de dados para análise de sentimentos e tendências."
    ]

    print("\n=== Mineração de Texto: Exemplos ===")

    tokens = [tokenizacao(texto) for texto in textos]
    print("\n1) Tokenização dos textos:")
    for i, tks in enumerate(tokens, 1):
        print(f"Texto {i}: {tks}")

    freq = frequencia_palavras(textos)
    print("\n2) Frequência total das palavras:")
    for palavra, cont in freq.most_common(10):
        print(f"{palavra}: {cont}")

    tokens_sem_stop = [remover_stopwords(tokenizacao(texto)) for texto in textos]
    freq_sem_stop = Counter()
    for tks in tokens_sem_stop:
        freq_sem_stop.update(tks)
    print("\n3) Frequência das palavras sem stopwords:")
    for palavra, cont in freq_sem_stop.most_common(10):
        print(f"{palavra}: {cont}")
