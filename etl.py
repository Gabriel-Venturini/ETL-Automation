from abstract_etl import AbstractETL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import json
from classes import *

class ETL(AbstractETL):
  def __init__(self, source, target):
    self.source = source
    self.target = target
  
  def extract(self):
    with open(self.source, 'r') as arquivo:
        dados_arquivo = json.load(arquivo)
        self.extracted = dados_arquivo
  
  def transform(self):
    dicionario_datas = {}
    for dicionario in self.extracted:
      nome_tabela=dicionario['tipo']
      atributos = dicionario['atributos']
      df = pd.DataFrame(atributos)
      dicionario_datas[nome_tabela]=df
    self.transformed = dicionario_datas

# Iterar sobre a lista principal

  def load(self):
    engine = create_engine(self.target)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    df_unidade = self.transformed['UNIDADE_PRODUCAO']
    lista_unidadePd = []
    for indice, linha in  df_unidade.iterrows():
      unidade_pd = Unidade_Producao(numero=linha['numero'], peca_hora_nominal=linha['peca_hora_nominal'])
      lista_unidadePd.append(unidade_pd)
      
    df_peca = self.transformed['PECA']
    lista_pecas = []
    for indice, linha in  df_peca.iterrows():
      unidade_pecas = Peca(numero=linha['numero'], status=linha['status'], inicio_fabricacao=linha['inicio_fabricacao'], fim_fabricacao=linha['fim_fabricacao'], numero_unidade_producao=linha['numero_unidade_producao'])
      lista_pecas.append(unidade_pecas)
    
    df_registroFalha = self.transformed['REGISTRO_FALHA']

    lista_registro = []
    for indice, linha in df_registroFalha.iterrows():
      registro_Falhas = Registro_Falha(id=linha['id'], severidade=linha['severidade'], inicio=linha['inicio'], fim=linha['fim'], numero_unidade_producao=linha['numero_unidade_producao'])
      lista_registro.append(registro_Falhas)
      
    df_sopradora = self.transformed['SOPRADORA']
    lista_sopradora = []
    for indice, linha in df_sopradora.iterrows():
      sopradora = Sopradora(numero=linha['numero'], vazao_sopro=linha['vazao_sopro'], pressao_sopro=linha['pressao_sopro'])
      lista_sopradora.append(sopradora)
    
    df_torno_cnc = self.transformed['TORNO_CNC']
    lista_torno_cnc = []
    for indice, linha in df_torno_cnc.iterrows():
      torno_cnc = Torno_Cnc(numero=linha['numero'], velocidade_rotacao=linha['velocidade_rotacao'], tolerancia=linha['tolerancia'])
      lista_torno_cnc.append(torno_cnc)
    
    df_impressora3d = self.transformed['IMPRESSORA_3D']
    lista_impressora3d = []
    for indice, linha in df_impressora3d.iterrows():
      impressora3d = Impressora3D(numero=linha['numero'], espessura_camada=linha['espessura_camada'], tipo_material=linha['tipo_material'])
      lista_impressora3d.append(impressora3d)
      
    df_fresadora = self.transformed['FRESADORA']
    lista_fresadora = []
    for indice, linha in df_fresadora.iterrows():
      fresadora = Fresadora(numero=linha['numero'], velocidade_rotacao=linha['velocidade_rotacao'], profundidade_corte=linha['profundidade_corte'])
      lista_fresadora.append(fresadora)
    
    
    session.add_all(lista_unidadePd)
    session.add_all(lista_pecas)
    session.add_all(lista_registro)
    session.add_all(lista_sopradora)
    session.add_all(lista_torno_cnc)
    session.add_all(lista_impressora3d)
    session.add_all(lista_fresadora)
    session.commit()
      
      
    
