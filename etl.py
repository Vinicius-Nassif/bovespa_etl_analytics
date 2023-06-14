import pandas as pd
from tqdm import tqdm 
from keys import diretorio

def read_files(path, name_file, year_date, type_file):
    _file = f'{path}{name_file}{year_date}.{type_file}'
    # Especificação das posições das colunas no arquivo
    colspecs = [
        (2,10),         
        (10,12),
        (12,24),
        (27,39),
        (56,69),
        (69,82),
        (82,95),
        (108,121),
        (152, 170),
        (170,188)
    ]

    names = ['data_pregao', 
             'codbdi', 
             'sigla_acao', 
             'nome_acao', 
             'preco_abertura', 
             'preco_maximo', 
             'preco_minimo', 
             'preco_fechamento', 
             'qtd_negocios', 
             'volume_negocios'
    ]

    # Leitura do arquivo utilizando as colspecs e os nomes das colunas
    df = pd.read_fwf(_file, colspecs=colspecs, names=names, skiprows=1)  
    return df

def filter_stocks(df):
    # Filtragem das ações pelo código BDI
    df = df[df['codbdi'] == 2]   
    df = df.drop('codbdi', axis=1)  # Remoção da coluna codbdi
    return df

def parse_date(df):
    # Conversão do campo data_pregao para formato de data
    df['data_pregao'] = pd.to_datetime(df['data_pregao'], format='%Y%m%d')  
    return df

def parse_values(df):
    # Ajuste dos campos numéricos
    ## Divisão dos campos numéricos por 100 e conversão para float
    df['preco_abertura'] = (df['preco_abertura'] / 100).astype(float)  
    df['preco_maximo'] = (df['preco_maximo'] / 100).astype(float)
    df['preco_minimo'] = (df['preco_minimo'] / 100).astype(float)
    df['preco_fechamento'] = (df['preco_fechamento'] / 100).astype(float)
    ## Conversão do campo qnd_negocios e volume_negocios para int
    df['qtd_negocios'] = df['qtd_negocios'].astype('int64') 
    df['volume_negocios'] = df['volume_negocios'].astype('int64')  
    return df

def concat_files(path, name_file, year_date, type_file, final_file):
    # Juntando os arquivos
    print('ETL iniciado...')
    total_files = len(year_date) # Calcula um total de arquivos a serem processados
    with tqdm(total=total_files) as pbar: # Cria uma barra de progresso total
        for i, y in enumerate(year_date): # Itera sobre os arquivos de dados
            df = read_files(path, name_file, y, type_file)  # Leitura do arquivo
            df = filter_stocks(df)  # Filtragem das ações
            df = parse_date(df)  # Ajuste do campo de data
            df = parse_values(df)  # Ajuste dos campos numéricos
            
            if i == 0:
                df_final = df # Se for o primeiro arquivo, atribui diretamente a variável
            else:
                df_final = pd.concat([df_final, df])  # Concatenação dos dataframes
            
            ## Barra de progresso
            pbar.set_postfix(file=f'{i+1}/{total_files}') # Atualiza o texto na barra de progresso
            pbar.set_description(f'Arquivo {y}') # Atualiza a descrição na barra de progresso
            pbar.update(1)# Atualiza a barra de progresso
            print() # Quebra de linha
            print(f'Arquivo {y} processado...')

    df_final.to_csv(f'{path}/{final_file}', index=False)  # Salvar o dataframe final em um arquivo CSV
    print('csv criado com sucesso!')
    print('ETL concluído!')

if __name__ == '__main__':
    # Executando programa de ETL
    year_date = ['2020', '2021', '2022', '2023']
    path = diretorio
    name_file = 'COTAHIST_A'
    type_file = 'txt'
    final_file = 'all_bovespa.csv'
    concat_files(path, name_file, year_date, type_file, final_file)