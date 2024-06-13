from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.mysql import BIT

class Base(DeclarativeBase):
    pass


class Fresadora(Base):
    __tablename__ = "FRESADORA"
    
    numero = Column(Integer, ForeignKey("UNIDADE_PRODUCAO.numero"), primary_key=True, nullable=False, autoincrement=False)
    velocidade_rotacao = Column(Float, nullable=False)
    profundidade_corte = Column(Float, nullable=False)


class Impressora3D(Base):
    __tablename__ = "IMPRESSORA_3D"

    numero = Column(Integer, ForeignKey("UNIDADE_PRODUCAO.numero"),primary_key=True, nullable=True, autoincrement=False)
    espessura_camada = Column(Float, nullable=False)
    tipo_material = Column(String(30), nullable=False)


class Peca(Base):
    __tablename__ = "PECA"

    numero = Column(Integer, ForeignKey("UNIDADE_PRODUCAO.numero"), primary_key=True, nullable=True, autoincrement=False)
    status = Column(String(10), nullable=False)
    inicio_fabricacao = Column(Date)
    fim_fabricacao = Column(Date)
    numero_unidade_producao = Column(Integer, nullable=False)

class Registro_Falha(Base):
    __tablename__ = "REGISTRO_FALHA"

    id = Column(Integer, primary_key=True, nullable=True, autoincrement=False)
    severidade = Column(BIT) # A FAZER
    inicio = Column(Date)
    fim = Column(Date)
    numero_unidade_producao = Column(Integer, ForeignKey("UNIDADE_PRODUCAO.numero"))


class Sopradora(Base):
    __tablename__ = "SOPRADORA"

    numero = Column(Integer, ForeignKey("UNIDADE_PRODUCAO.numero"), primary_key=True, nullable=True, autoincrement=False)
    vazao_sopro = Column(Float, nullable=False)
    pressao_sopro = Column(Float, nullable=False)


class Torno_Cnc(Base):
    __tablename__ = "TORNO_CNC"

    numero = Column(Integer, ForeignKey("UNIDADE_PRODUCAO.numero"), primary_key=True, nullable=True, autoincrement=False)
    velocidade_rotacao = Column(Float, nullable=False)
    tolerancia = Column(Float, nullable=False)


class Unidade_Producao(Base):
    __tablename__ = "UNIDADE_PRODUCAO"

    numero = Column(Integer, primary_key=True, nullable=True, autoincrement=False)
    peca_hora_nominal = Column(Float, nullable=False)
  