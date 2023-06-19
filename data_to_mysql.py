import pandas as pd
import mysql.connector
from keys import user_db, pw_db, local_host

def criar_conexao(user, password, host, database):
    # Cria e retorna uma conexão com o banco de dados MySQL
    return mysql.connector.connect(
            user=user, 
            password=password, 
            host=host, 
            database=database
        )

def criar_tabela(cursor):
    # Função para criar a tabela serie_historica no banco de dados
    print("Criando tabela...")
    create_table_query = """
    CREATE TABLE IF NOT EXISTS serie_historica (
        id INT AUTO_INCREMENT PRIMARY KEY,
        data_pregao DATE,
        sigla_acao VARCHAR(10),
        nome_acao VARCHAR(50),
        preco_abertura FLOAT,
        preco_maximo FLOAT,
        preco_minimo FLOAT,
        preco_fechamento FLOAT,
        qtd_negocios INT,
        volume_negocios BIGINT

    )
    """
    cursor.execute(create_table_query)
    print('Tabela criada com sucesso!')

def inserir_dados(cursor, df):
    # Função para inserir o DataFrame no banco de dados
    print("Inserindo dados...")
    insert_query = """
    INSERT IGNORE INTO serie_historica (data_pregao, sigla_acao, nome_acao, preco_abertura, preco_maximo, 
                                        preco_minimo, preco_fechamento, qtd_negocios, volume_negocios)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for index, row in df.iterrows():
        data = row['data_pregao']
        sigla_acao = row['sigla_acao']
        nome_acao = row['nome_acao']
        abertura = row['preco_abertura']
        maximo = row['preco_maximo']
        minimo = row['preco_minimo']
        fechamento = row['preco_fechamento']
        qtd_negocios = row['qtd_negocios']
        volume_negocios = row['volume_negocios']
        values = (data, sigla_acao, nome_acao, abertura, maximo, minimo, fechamento, qtd_negocios, volume_negocios)
        # Executar a query de inserção no banco de dados
        cursor.execute(insert_query, values)
    print('Dados inseridos com sucesso!')

def main():
    arquivo_origem = 'all_bovespa.csv'
    user = user_db
    password = pw_db
    host = local_host
    database = 'bovespa'

    # Carregar os dados do arquivo CSV diretamente para um DataFrame
    df = pd.read_csv(arquivo_origem)

    # Estabelecer a conexão com o banco de dados
    cnx = criar_conexao(user, password, host, database)

    # Criar a tabela no banco de dados
    cursor = cnx.cursor()
    criar_tabela(cursor)

    # Inserir os dados no banco de dados
    inserir_dados(cursor, df)

    # Confirmar as alterações e fechar a conexão
    cnx.commit()
    cnx.close()

if __name__ == '__main__':
    main()
