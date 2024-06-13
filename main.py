# %%
# imports
import os
from etl import ETL
from dotenv import load_dotenv

load_dotenv()

# %%
# gera os parâmetros para instanciar o objeto ETL
usuario = os.getenv("USUARIO")
senha = os.getenv("SENHA")
host = os.getenv("HOST")
banco_de_dados = os.getenv("BANCO_DE_DADOS")

source = "dados.json"
target = f"mssql+pymssql://{usuario}:{senha}@{host}/{banco_de_dados}"
etl = ETL(source, target)
# %%
# testando
etl.extract()
etl.transform()
etl.load()