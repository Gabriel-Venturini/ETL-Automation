from abc import ABC,abstractmethod


class AbstractETL(ABC):
    def __init__(self,source:str,target:str):
        self.source = source
        self.target = target
        self.extracted = None
        self.transformed = None

    @abstractmethod
    def extract(self):
        # TODO: lê os dados a serem inseridos a partir do caminho do arquivo (source)
        pass

    @abstractmethod
    def transform(self):
        # TODO: transforma os dados extraídos em um formato mais adequado para inserção
        pass

    @abstractmethod
    def load(self):
        # TODO: cria uma engine a partir do destino (target) e insere os dados transformados
        pass