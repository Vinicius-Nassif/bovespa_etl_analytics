# Projeto ETL - Bovespa B3

Este documento descreve em detalhes o código Python que realiza operações de ETL (Extração, Transformação e Carga) em arquivos de dados da bolsa de valores Bovespa. O código é projetado para ler, filtrar e processar dados de múltiplos arquivos, resultando em um único arquivo CSV contendo os dados consolidados. 

## Funcionalidades

O código implementa as seguintes funcionalidades:

### Função `read_files(path, name_file, year_date, type_file)`

Esta função é responsável por ler os arquivos de dados da bolsa de valores Bovespa. Ela recebe os seguintes parâmetros:

- `path` (string): O caminho do diretório onde os arquivos estão localizados.
- `name_file` (string): O prefixo dos nomes dos arquivos.
- `year_date` (list): Uma lista de anos para os quais os arquivos devem ser lidos.
- `type_file` (string): A extensão dos arquivos.

A função lê os arquivos usando o `pd.read_fwf()`, que é capaz de ler arquivos formatados com largura fixa. Os parâmetros `colspecs` e `names` são definidos para especificar as posições das colunas e os nomes das colunas, respectivamente. O resultado é retornado como um DataFrame do pandas contendo os dados lidos dos arquivos.

### Função `filter_stocks(df)`

Esta função filtra as ações no DataFrame com base no código BDI. Ela recebe um parâmetro:

- `df` (pandas DataFrame): O DataFrame contendo os dados das ações.

A função filtra as ações mantendo apenas aquelas com o código BDI igual a 2. Em seguida, remove a coluna `codbdi` do DataFrame resultante. O DataFrame filtrado é retornado.

### Função `parse_date(df)`

Esta função converte a coluna `data_pregao` para o formato de data. Ela recebe um parâmetro:

- `df` (pandas DataFrame): O DataFrame contendo os dados das ações.

A função usa o `pd.to_datetime()` para converter a coluna `data_pregao` para o formato de data, com base no formato especificado. O DataFrame resultante, com a coluna `data_pregao` convertida, é retornado.

### Função `parse_values(df)`

Esta função ajusta os valores numéricos no DataFrame. Ela recebe um parâmetro:

- `df` (pandas DataFrame): O DataFrame contendo os dados das ações.

A função divide os campos numéricos `preco_abertura`, `preco_maximo`, `preco_minimo` e `preco_fechamento` por 100 e os converte para o tipo de dados float. Além disso, converte as colunas `qtd_negocios` e `volume_negocios` para o tipo de dados int64. O DataFrame resultante, com os valores numéricos ajustados, é retornado.

### Função `concat_files(path, name_file, year_date, type_file, final_file)`

Esta função é responsável por realizar o processo completo de ETL. Ela recebe os seguintes parâmetros:

- `path` (string): O caminho do diretório onde os arquivos estão localizados.
- `name_file` (string): O prefixo dos nomes dos arquivos.
- `year_date` (list): Uma lista de anos para os quais os arquivos devem ser processados.
- `type_file` (string): A extensão dos arquivos.
- `final_file` (string): O nome do arquivo CSV de saída.

A função executa as seguintes etapas:

1. Itera sobre os anos fornecidos e para cada ano:
   - Lê o arquivo correspondente usando a função `read_files()`.
   - Filtra as ações usando a função `filter_stocks()`.
   - Converte a coluna `data_pregao` para o formato de data usando a função `parse_date()`.
   - Ajusta os valores numéricos usando a função `parse_values()`.
   - Se for o primeiro arquivo lido, atribui o DataFrame diretamente à variável `df_final`; caso contrário, concatena o DataFrame com `df_final`.
   - Exibe uma barra de progresso mostrando o status do processamento.
   - Salva o DataFrame final em um arquivo CSV.

## Uso

Para usar o código, siga as etapas abaixo:

1. Instale as dependências necessárias executando o seguinte comando:

```
Copy code
pip install pandas tqdm
```

1. Certifique-se de que os arquivos de dados da Bovespa estejam no formato correto e sigam as posições das colunas mencionadas no código.
2. Modifique os parâmetros no bloco `if __name__ == '__main__'` para personalizar a execução. Os parâmetros que podem ser modificados incluem:

- `year_date`: Uma lista de anos para os quais os arquivos de dados serão processados.
- `path`: O caminho do diretório onde os arquivos de dados estão localizados.
- `name_file`: O prefixo dos nomes dos arquivos de dados.
- `type_file`: A extensão dos arquivos de dados.
- `final_file`: O nome do arquivo CSV de saída.

1. Execute o script Python para iniciar o processo de ETL. Durante o processamento, uma barra de progresso será exibida, mostrando o status de cada arquivo sendo processado. O arquivo CSV final será salvo no caminho especificado.

## Exemplo

```
year_date = ['2020', '2021', '2022', '2023']
path = diretorio
name_file = 'COTAHIST_A'
type_file = 'txt'
final_file = 'all_bovespa.csv'

concat_files(path, name_file, year_date, type_file, final_file)
```

Neste exemplo, o código executará o processo de ETL para os anos de 2020, 2021, 2022 e 2023 (até o momento), lendo os arquivos de dados da Bovespa que seguem o formato especificado. Os arquivos serão filtrados, as datas serão convertidas e os valores numéricos serão ajustados. O resultado final será salvo no arquivo `all_bovespa.csv`.
