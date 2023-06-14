import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def formatar_dados(arquivo_origem):
    print('Formatação iniciada...')
    # Carregando o arquivo .csv
    df = pd.read_csv(arquivo_origem)

    # Formatando os campos
    df['data_pregao'] = pd.to_datetime(df['data_pregao'])
    df['preco_abertura'] = df['preco_abertura'].astype(float)
    df['preco_maximo'] = df['preco_maximo'].astype(float)
    df['preco_minimo'] = df['preco_minimo'].astype(float)
    df['preco_fechamento'] = df['preco_fechamento'].astype(float)
    df['qtd_negocios'] = df['qtd_negocios'].astype(int)
    df['volume_negocios'] = df['volume_negocios'].astype(int)

    # Remover o índice do DataFrame
    df = df.reset_index(drop=True)

    print('Formatação Concluída!')
    print(df)
    
    return df

def analisar_media(df):
    # Calcular a média do preço de fechamento
    media_fechamento = df['preco_fechamento'].mean()
    media_fechamento_formatada = round(media_fechamento, 2)
    print("Média do preço de fechamento:", media_fechamento_formatada)

def maior_valor(df):
    # Ordernar por maior valor do preço máximo
    maiores_valores = df.sort_values('preco_maximo', ascending=False)
    print(maiores_valores)

def plot_data_preco(df):
    df.plot(x='data_pregao', y='preco_fechamento')
    plt.xlabel('Data do Pregão')
    plt.ylabel('Preço do Fechamento')
    plt.show()

def plot_media_por_semestre(df):
    # Adicionando coluna de semestre ao DataFrame
    df['semestre'] = df['data_pregao'].dt.year.astype(str) + 'S' + ((df['data_pregao'].dt.month - 1) // 6 + 1).astype(str)

    # Agrupando por semestre e calculando a média do preço de fechamento
    df_media_semestre = df.groupby('semestre')['preco_fechamento'].mean().reset_index()

    # Plotando o gráfico de linha da média por semestre
    df_media_semestre.plot(x='semestre', y='preco_fechamento', marker='o', linestyle='-', figsize=(10, 6))
    plt.xlabel('Semestre')
    plt.ylabel('Média do Preço de Fechamento')
    plt.title('Média do Preço de Fechamento por Semestre')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

def plot_dispersao(df):
    plt.scatter(df['data_pregao'], df['preco_fechamento'])
    plt.xlabel('Data de Pregão')
    plt.ylabel('Preço de Fechamento')
    plt.title('Dispersão: Data de Pregão vs Preço de Fechamento')
    plt.xticks(rotation=45)
    plt.show()

def plot_dispersao_por_semestre(df):
    # Adicionando coluna de semestre ao DataFrame
    df['semestre'] = df['data_pregao'].dt.year.astype(str) + 'S' + ((df['data_pregao'].dt.month - 1) // 6 + 1).astype(str)

    # Agrupando por semestre e calculando a média do preço de fechamento
    df_media_semestre = df.groupby('semestre')['preco_fechamento'].mean().reset_index()

    # Plotando o gráfico de dispersão por semestre
    plt.scatter(df_media_semestre['semestre'], df_media_semestre['preco_fechamento'])
    plt.xlabel('Semestre')
    plt.ylabel('Média do Preço de Fechamento')
    plt.title('Dispersão: Média do Preço de Fechamento por Semestre')
    plt.xticks(rotation=45)
    plt.show()

def verificar_maior_queda(df):
    # Adicionando coluna de semestre ao DataFrame
    df['semestre'] = df['data_pregao'].dt.year.astype(str) + 'S' + ((df['data_pregao'].dt.month - 1) // 6 + 1).astype(str)

    # Agrupando por semestre e calculando a diferença entre máximo e mínimo do preço de fechamento
    df_queda_semestre = df.groupby('semestre')['preco_fechamento'].apply(lambda x: x.max() - x.min()).reset_index()

    # Encontrando o semestre com a maior queda
    semestre_maior_queda = df_queda_semestre.loc[df_queda_semestre['preco_fechamento'].idxmax()]

    # Obtendo ação correspondente ao semestre com a maior queda
    acao_maior_queda = df.loc[df['semestre'] == semestre_maior_queda['semestre']]

    # Plotando o gráfico de linha da queda ao longo dos semestres com formatação de duas casas decimais
    df_queda_semestre['preco_fechamento'] = (df_queda_semestre['preco_fechamento'] / 1000).round(2)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_queda_semestre['semestre'], df_queda_semestre['preco_fechamento'], marker='o', linestyle='-')

    plt.xlabel('Semestre')
    plt.ylabel('Queda (Preço Máximo - Preço Mínimo)')
    plt.title('Queda ao Longo dos Semestres')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Formatando os valores no eixo y com duas casas decimais
    formatter = ticker.FormatStrFormatter('%.2f')
    ax.yaxis.set_major_formatter(formatter)

    plt.show()

    return acao_maior_queda

    return acao_maior_queda

if __name__ == '__main__':
    # Chamando a função para formatar os dados da Bovespa
    df_formatado = formatar_dados('all_bovespa.csv')
    analisar_media(df_formatado)
    maior_valor(df_formatado)
    plot_data_preco(df_formatado)
    plot_dispersao(df_formatado)
    plot_dispersao_por_semestre(df_formatado)
    plot_media_por_semestre(df_formatado)
    verificar_maior_queda(df_formatado)


