# Automação ETL com Python <br>
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

## Configurar variáveis de ambiente
### Acesso ao Banco de Dados
``` bash
USUARIO=user # aqui vai o nome de usuário
SENHA=password # senha do usuário
HOST=host # host do banco de dados
BANCO_DE_DADOS=example-database # nome do banco de dados que será acessado
```
<br>

## Instanciar tabelas como objetos (classes.py)

### Imports
Para utilizar as tabelas de banco de dados e seus respectivos tipos de dados (data types), importaremos alguns métodos da biblioteca 'sqlalchemy' que é uma biblioteca de mapeamento de objeto-relacional (ORM):
``` python
from sqlalchemy import (
    Column, # Usado para definir colunas nas tabelas do banco de dados.
    Integer, # Tipo de dado inteiro para colunas.
    String, # Tipo de dado string para colunas
    Date, # Tipo de dado de data para colunas
    ForeignKey, #  Usado para criar uma chave estrangeira que referencia outra tabela.
    Float, # Tipo de dado de ponto flutuante para colunas.
)
```
<br>

Precisaremos também, do seguinte trecho:
``` python
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.mysql import BIT
```
- DeclarativeBase é uma classe base utilizada no modelo de mapeamento declarativo do SQLAlchemy. Esta classe é usada para definir classes de mapeamento que representam tabelas no banco de dados.
- BIT é um tipo de dado específico do MySQL que representa valores binários. Este tipo de dado é útil quando você precisa armazenar valores binários (bits) no seu banco de dados.
<br>

### Declarative Base
Será necessário instanciar uma classe 'Base' utilizando a DeclarativeBase que importamos acima.
``` python
class Base(DeclarativeBase):
    pass
```
<br>
DeclarativeBase é uma classe base fornecida pelo SQLAlchemy que habilita o uso do modelo de mapeamento declarativo e, assim, torna-se um modelo de criação de outras classes que neste caso, serão as tabelas do nosso banco de dados representadas por objetos/classes.

### Tabelas como objetos

Usaremos a classe 'Fresadora' como exemplo para a representação de tabelas como objetos no nosso programa. A representação de uma tabela exige o seguinte modelo:

``` python
class NomeTabela(Base):
   __tablename__ = "NOMETABELADOBANCODEDADOS"

   atributo1 = Column(TipoAtributo, ...)
   atributo2 = Column(TipoAtributo, ...)
   atributo3 = Column(TipoAtributo, ...)
```
Em Fresadora, faremos da seguinte forma:
``` python
class Fresadora(Base):
    __tablename__ = "FRESADORA"
    
    numero = Column(Integer, ForeignKey("UNIDADE_PRODUCAO.numero"), primary_key=True, nullable=False, autoincrement=False)
    velocidade_rotacao = Column(Float, nullable=False)
    profundidade_corte = Column(Float, nullable=False)
```
1. Começamos definindo a classe 'Fresadora' que herda da classe base 'Base'. Logo, 'Fresadora' é um modelo de tabela ORM.
2. ```__tablename__``` especifica o nome da tabela no banco de dados, neste caso 'FRESADORA'.
3. A variável ```numero``` é definida como uma coluna com o tipo de dado Integer. Esta coluna é uma chave estrangeira que referencia à uma coluna 'numero' de uma tabela 'UNIDADE_PRODUCAO'. Além disso, é chave primária de 'FRESADORA'. Possui o parâmetro ```nullable=False``` que indica que esta coluna não pode ter valores 'NULL'. Também possui o parâmetro ```autoincrement=False``` que define que a coluna não utiliza a função de auto-incremento.
4. A variável ```velocidade_rotacao``` também é definida como uma coluna que possui o tipo de dado 'Float' e um argumento ```nullable=False```, portanto, indica que não pode haver valores 'NULL'.
5. E ```profundidade_corte``` também é uma coluna do tipo 'Float' com o argumento ```nullable=False``` que indica que não pode haver valores 'NULL'.
<br>

Você pode aplicar este exemplo para todas as tabelas que deseja popular utilizando este programa. Siga o modelo e para eventuais dúvidas, consulte a [documentação oficial](https://www.sqlalchemy.org/) do SQLAlchemy.

## Classe Abstrata (abstract_etl.py)
Para instanciar a classe abstrata, é necessário preencher os parâmetros <strong>source</strong> e <strong>target</strong>.<br>
1. Source refere-se ao caminho do arquivo que será utilizado para ler os dados (no exemplo será utilizado o arquivo 'dados.json').<br>
2. Target refere-se ao destino dos dados que, no exemplo, será o caminho do banco de dados ("mssql+pymssql://{usuario}:{senha}@{host}/{banco_de_dados}"), você pode visualizar a implementação dele em [main.py](main.py).
<br>

Estes parâmetros são também atributos, mas além deles, há dois outros atributos importantes de serem mencionados que referem-se ao estado do objeto com valores Booleanos (True ou False), sendo eles o 'self.extracted' e o 'self.transformed'.
1. Extracted indica se os dados do objeto já foram extraídos
2. Transformed indica se estes mesmos dados já passaram pelo método de transformação

A classe abstrata já vem configurada de padrão com métodos úteis como:
- Extrair
``` python
@abstractmethod
    def extract(self):
        # TODO: lê os dados a serem inseridos a partir do caminho do arquivo (source)
        pass
```
- transformar
``` python
@abstractmethod
    def transform(self):
        # TODO: transforma os dados extraídos em um formato mais adequado para inserção
        pass
```
- carregar
``` python
@abstractmethod
    def load(self):
        # TODO: cria uma engine a partir do destino (target) e insere os dados transformados
        pass
```
<br>

Portanto, não há a necessidade de configurá-la, mas apenas de compreendê-la.
<br>

## Extract, Transform, Load (etl.py)

### Imports
``` python
from abstract_etl import AbstractETL # importamos a classe que criamos anteriormente em abstract_etl
from sqlalchemy import create_engine # cria conexão com o banco de dados
from sqlalchemy.orm import sessionmaker # gerencia sessões do banco de dados
import pandas as pd # biblioteca para manipulação de dados com dataframe
import json # biblioteca para trabalhar com arquivos json
from classes import * #  importa todas as classes definidas no módulo classes, ou seja, os modelos ORM que representam tabelas no banco de dados.
```

### Classe ETL
O construtor inicializa a instância da classe ETL com os parâmetros source (caminho para o arquivo de origem) e target (string de conexão do banco de dados).
```python
class ETL(AbstractETL):
    def __init__(self, source, target):
        self.source = source
        self.target = target
```

#### Método Extract
Lê dados de um arquivo JSON e os armazena em self.extracted.
```python
def extract(self):
        with open(self.source, 'r') as arquivo:
            dados_arquivo = json.load(arquivo)
            self.extracted = dados_arquivo
```

#### Método Transform
Converte os dados extraídos em dataframes pandas e os organiza em um dicionário em que a chave é o nome da tabela.
```python
def transform(self):
        dicionario_datas = {}
        for dicionario in self.extracted:
            nome_tabela = dicionario['tipo']
            atributos = dicionario['atributos']
            df = pd.DataFrame(atributos)
            dicionario_datas[nome_tabela] = df
        self.transformed = dicionario_datas
```

#### Método Load
Resumo: Este método configura a conexão com o banco de dados; Carrega dados transformados em dataframes para modelos ORM e Adiciona todas as instâncias ao banco de dados efetuando a transação.
<br>
Passo a Passo:<br>

* Conexão com o banco de dados
    - Cria uma 'engine' e uma sessão do SQLAlchemy usando a string de conexão ```self.target```.
```python
def load(self):
        engine = create_engine(self.target)
        Session = sessionmaker(bind=engine)
        session = Session()
```

* Carregar dataframe para modelo ORM
    - Para cada tipo de dado ('UNIDADE_PRODUCAO', 'PECA', 'SOPRADORA', etc), itera sobre as linhas do dataframe correspondente e cria instâncias das classes ORM.
    - Adiciona essas instâncias a listas específicas para cada tipo.
```python
df_unidade = self.transformed['UNIDADE_PRODUCAO']
        lista_unidadePd = []
        for indice, linha in df_unidade.iterrows():
            unidade_pd = Unidade_Producao(numero=linha['numero'], peca_hora_nominal=linha['peca_hora_nominal'])
            lista_unidadePd.append(unidade_pd)
```
* Adicionar as instâncias ao banco de dados e efetuar a transação
    - Utiliza o ```session.add_all``` para adicionar todas as instâncias de cada lista à sessão.
    ```python
    session.add_all(lista_unidadePd)
    ```
    - Efetua a transação com o ```commit``` para salvar os dados no banco de dados.
    ```python
    session.commit()
    ```

Este processo é altamente configurável e permite a definição da fonte e do alvo no momento da instância da classe ETL. <br>

## Programa principal (main.py)
Resumo: Script de automação para executar um processo ETL completo utilizando o programa que criamos anteriormente (etl.py).
### Imports
Começamos importando bibliotecas e arquivos necessários para o funcionamento do programa principal:
```python
import os # permite interagir com o sistema operacional, como acessar variáveis de ambiente
from etl import ETL # importa a classe ETL definida no arquivo etl.py
from dotenv import load_dotenv # Importa a função load_dotenv da biblioteca dotenv, que é usada para carregar variáveis de ambiente de um arquivo .env
```

#### Carregando variáveis de ambiente
Permite que as variáveis definidas no arquivo .env sejam acessíveis através do módulo os. (Configuradas anteriormente na primeira sessão deste documento).
```python
load_dotenv()
```

#### Obtendo os parâmetros para instanciar o objeto ETL

```python
# gera os parâmetros para instanciar o objeto ETL
usuario = os.getenv("USUARIO")
senha = os.getenv("SENHA")
host = os.getenv("HOST")
banco_de_dados = os.getenv("BANCO_DE_DADOS")

source = "dados.json"
target = f"mssql+pymssql://{usuario}:{senha}@{host}/{banco_de_dados}"
etl = ETL(source, target)
print(target)
```

* Obtendo as variáveis de ambiente (fonte: arquivo .env)
    - ```os.getenv("USUARIO")``` obtém o valor da variável de ambiente 'USUÁRIO'.
    - ```os.getenv("SENHA")``` obtém o valor da variável de ambiente SENHA.
    - ```os.getenv("HOST")``` obtém o valor da variável de ambiente HOST.
    - ```os.getenv("BANCO_DE_DADOS")``` obtém o valor da variável de ambiente BANCO_DE_DADOS.
* Definindo as variáveis 'source' e 'target'
    - ```source = dados.json``` define o caminho do arquivo de dados JSON que será utilizado como fonte (*altere aqui a fonte dos dados que passará como fonte para sua população).
    - ```target``` constrói a f-string de conexão do banco de dados destino usando as variáveis de ambiente para se conectar ao Microsoft SQL Server via 'pymssql'.
* Instanciando o objeto ETL
    - ```etl = ETL(source, target)``` cria uma instância de classe 'ETL' com os respectivos 'source' e 'target' como argumentos.

#### Executando o processo ETL
```python
etl.extract()
etl.transform()
etl.load()
```

* ```etl.extract``` executa o método 'extract' do objeto 'ETL' que lê dados do arquivo JSON especificado em 'source'.
* ```etl.transform()``` executa o método 'transform' que transforma os dados extraídos em dataframes pandas.
* ```etl.load()``` executa o método 'load' que carrega os dados transformados no banco de dados de destino especificado em 'target'.

## Considerações
Considere o tratamento dos dados no arquivo JSON para que não haja inconsistência quanto aos dados que serão transformados durante o processo ETL, para isso, os dados deste arquivo devem estar padronizados de acordo com o esquema do banco de dados e das tabelas que serão populadas.
<br>