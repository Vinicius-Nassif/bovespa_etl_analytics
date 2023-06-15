import pandas as pd

## Setando configurações iniciais do dataframe
# Definir a largura máxima de exibição das colunas
#pd.set_option('display.max_columns', None)
# Definir a largura máxima de exibição das linhas
#pd.set_option('display.max_rows', None)
# Definir o formato de exibição dos floats com duas casas decimais
#pd.set_option('display.float_format', lambda x: '{:.2f}'.format(x/1000))

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

    print('Formatação Concluída!')

    # Adicionar as colunas 'sigla_acao' e 'nome_acao' ao DataFrame, se necessário
    if 'sigla_acao' not in df.columns:
        df['sigla_acao'] = ''
    if 'nome_acao' not in df.columns:
        df['nome_acao'] = ''
    
    return df

## Funções de análise de dados
def analisar_media(df):
    # Calcular a média do preço de fechamento ao longo do tempo
    media_fechamento = df['preco_fechamento'].mean()
    media_fechamento_formatada = round(media_fechamento, 2)
    print("Média do preço de fechamento:")
    print(media_fechamento_formatada)

def maior_valor(df, quantidade):
    # Ordernar por maior valor do preço máximo
    maiores_valores = df.sort_values('preco_maximo', ascending=False).head(quantidade)
    print('Preços máximos registrados: ')
    print(maiores_valores.to_string(index=False))

def menor_valor(df):
    # Ordenar por menor valor do preço mínimo
    menores_valores = df.sort_values('preco_minimo', ascending=True).head()
    print('Preços mínimos registrados:')
    print(menores_valores.to_string(index=False))

def maior_volume(df, quantidade):
    # Ordernar por maior volume de negócios
    maiores_volumes = df.sort_values('volume_negocios', ascending=False).head(quantidade)
    print('Maior volume de negócios registrados:')
    print(maiores_volumes.to_string(index=False))

def maior_negocio(df, quantidade):
    # Ordenar o DataFrame pelo campo 'qtd_negocios' em ordem decrescente
    df_sorted = df.sort_values('qtd_negocios', ascending=False)

    # Selecionar as n primeiras linhas do DataFrame ordenado
    top_dates = df_sorted.head(quantidade)[['data_pregao', 'sigla_acao', 'nome_acao', 'preco_fechamento', 'qtd_negocios']].copy()
    
    # Formatando as datas
    top_dates['data_pregao'] = top_dates['data_pregao']

    return top_dates

if __name__ == '__main__':
    # Chamando a função para formatar os dados da Bovespa
    df_formatado = formatar_dados('all_bovespa.csv')
    print()
    analisar_media(df_formatado)
    print()
    maior_valor(df_formatado, 10)
    print()
    menor_valor(df_formatado)
    print()
    maior_volume(df_formatado, 10)
    print()
    maiores_numeros_negocios = maior_negocio(df_formatado, 10)
    print('Datas comos maiores números de negócios:') 
    print (maiores_numeros_negocios.to_string(index=False))