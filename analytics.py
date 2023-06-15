import pandas as pd

def formatar_dados(arquivo_origem):
    print('Formatação iniciada...')
    # Carregando o arquivo .csv
    df = pd.read_csv(arquivo_origem)

    # Formatando os campos
    df['data_pregao'] = pd.to_datetime(df['data_pregao']).dt.strftime('%d/%m/%Y')
    df['preco_abertura'] = df['preco_abertura'].astype(float)
    df['preco_maximo'] = df['preco_maximo'].astype(float)
    df['preco_minimo'] = df['preco_minimo'].astype(float)
    df['preco_fechamento'] = df['preco_fechamento'].astype(float)
    df['qtd_negocios'] = df['qtd_negocios'].astype(int)
    df['volume_negocios'] = df['volume_negocios'].astype(int)

    # Remover o índice do DataFrame
    df = df.reset_index(drop=True)

    # Adicionar as colunas 'sigla_acao' e 'nome_acao' ao DataFrame, se necessário
    if 'sigla_acao' not in df.columns:
        df['sigla_acao'] = ''
    if 'nome_acao' not in df.columns:
        df['nome_acao'] = ''
    
    print('Formatação Concluída!')

    return df

## Funções de análise de dados
def analisar_media(df):
    # Calcular a média do preço de fechamento ao longo do tempo
    media_fechamento = df['preco_fechamento'].mean()
    media_fechamento_formatada = round(media_fechamento, 2)
    print("Média do preço de fechamento:")
    print(media_fechamento_formatada)

    return media_fechamento_formatada

def maior_valor(df, quantidade):
    # Ordernar por maior valor do preço máximo
    maiores_valores = df.sort_values('preco_maximo', ascending=False).head(quantidade)
    print('Preços máximos registrados: ')
    print(maiores_valores.to_string(index=False))

    return maiores_valores

def menor_valor(df):
    # Ordenar por menor valor do preço mínimo
    menores_valores = df.sort_values('preco_minimo', ascending=True).head()
    print('Preços mínimos registrados:')
    print(menores_valores.to_string(index=False))

    return menores_valores

def maior_volume(df, quantidade):
    # Ordernar por maior volume de negócios
    maiores_volumes = df.sort_values('volume_negocios', ascending=False).head(quantidade)
    print('Maior volume de negócios registrados:')
    print(maiores_volumes.to_string(index=False))

    return maiores_volumes

def maior_negocio(df, quantidade):
    # Ordenar o DataFrame pelo campo 'qtd_negocios' em ordem decrescente
    df_sorted = df.sort_values('qtd_negocios', ascending=False)

    # Selecionar as n primeiras linhas do DataFrame ordenado
    top_dates = df_sorted.head(quantidade)[['data_pregao', 'sigla_acao', 'nome_acao', 'preco_fechamento', 'qtd_negocios']].copy()
    
    # Formatando as datas
    top_dates['data_pregao'] = top_dates['data_pregao']

    print('Datas comos maiores números de negócios:') 
    print (top_dates.to_string(index=False))

    return top_dates

def encontrar_maiores_variacoes_percentuais(df, quantidade):
    # Ordenar o DataFrame pela coluna 'data_pregao' em ordem crescente
    df.sort_values('data_pregao', inplace=True)

    # Criar a coluna 'variacao_percentual'
    df['variacao_percentual'] = ((df['preco_fechamento'] - df['preco_abertura']) / df['preco_abertura']) * 100

    # Ordenar o DataFrame pela coluna 'variacao_percentual' em ordem decrescente
    df.sort_values('variacao_percentual', ascending=False, inplace=True)

    # Selecionar as 5 ações com maior variação percentual
    top_variacoes = df.head(quantidade)[['sigla_acao', 'nome_acao', 'variacao_percentual']]

    print(top_variacoes)

    return top_variacoes

def encontrar_aumento_preco_fechamento(df, quantidade):
    # Ordenar o DataFrame pela coluna 'data_pregao' em ordem crescente
    df.sort_values('data_pregao', inplace=True)

    # Calcular a variação percentual de preço de fechamento em relação ao dia anterior
    df['variacao_percentual'] = ((df['preco_fechamento'] - df['preco_fechamento'].shift(1)) / df['preco_fechamento'].shift(1)) * 100

    # Selecionar as linhas em que a variação percentual é positiva
    aumento_preco_fechamento = df[df['variacao_percentual'] > 0][['sigla_acao', 'nome_acao']].head(quantidade)

    # Imprimir as informações das ações com aumento de preço de fechamento
    print("Ações com aumento percentual de preço de fechamento em relação ao dia anterior:")
    print(aumento_preco_fechamento)

    return aumento_preco_fechamento

def encontrar_maiores_quedas(df):
    # Ordenar o DataFrame pela coluna 'data_pregao' em ordem crescente
    df.sort_values('data_pregao', inplace=True)

    # Calcular a variação percentual de preço de fechamento em relação ao dia anterior
    df['variacao_percentual'] = ((df['preco_fechamento'] - df['preco_fechamento'].shift(1)) / df['preco_fechamento'].shift(1)) * 100

    # Agrupar o DataFrame por 'sigla_acao' e encontrar os índices dos dias de maior queda percentual para cada ação
    indices_maiores_quedas = df.groupby('sigla_acao')['variacao_percentual'].idxmin()

    # Selecionar as linhas correspondentes aos índices encontrados
    maiores_quedas = df.loc[indices_maiores_quedas, ['sigla_acao', 'nome_acao', 'data_pregao', 'variacao_percentual']].head()
    
    # Imprimir as informações dos dias de maior queda percentual
    print("Dias de maior queda percentual para cada ação:")
    print(maiores_quedas)

    return maiores_quedas

def calcular_volume_medio(df):
    # Calcular o volume médio de negociação por dia
    volume_medio = df['volume_negocios'].mean()
    
    # Imprimir o volume médio de negociação por dia
    print("Volume médio de negociação por dia:")
    print(volume_medio)

    return volume_medio

def encontrar_acoes_acima_da_media(df):
    # Calcular o número médio de negócios por ação
    media_negocios = df.groupby('sigla_acao')['qtd_negocios'].mean()

    # Selecionar as ações com número de negócios acima da média
    acoes_acima_da_media = media_negocios[media_negocios > media_negocios.mean()].head()

    # Imprimir as ações com número de negócios acima da média
    print("Ações com número de negócios acima da média:")
    print(acoes_acima_da_media.to_string(index=True))

    return acoes_acima_da_media

def exibir_resultado_titulo(titulo):
    print()
    print(titulo)
    print()

if __name__ == '__main__':
    # Chamando a função para formatar os dados da Bovespa
    df_formatado = formatar_dados('all_bovespa.csv')

    analises = [
        ("Analisar Média", lambda: analisar_media(df_formatado)),
        ("Maior Valor", lambda: maior_valor(df_formatado, 10)),
        ("Menor Valor", lambda: menor_valor(df_formatado)),
        ("Maior Volume", lambda: maior_volume(df_formatado, 10)),
        ("Maior Negócio", lambda: maior_negocio(df_formatado, 5)),
        ("Maiores Variações Percentuais", lambda: encontrar_maiores_variacoes_percentuais(df_formatado, 5)),
        ("Aumento de Preço de Fechamento", lambda: encontrar_aumento_preco_fechamento(df_formatado, 5)),
        ("Maiores Quedas", lambda: encontrar_maiores_quedas(df_formatado)),
        ("Volume Médio", lambda: calcular_volume_medio(df_formatado)),
        ("Ações Acima da Média", lambda: encontrar_acoes_acima_da_media(df_formatado))
    ]

    for titulo, funcao in analises:
        exibir_resultado_titulo(titulo)
        funcao()

