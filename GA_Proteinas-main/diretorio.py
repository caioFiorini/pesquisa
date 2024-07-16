import os

class Diretorio :
    def __init__(self, caminho) :
        self.caminho = caminho

    def create_folder(self, nome_diretorio):
        path = self.caminho + nome_diretorio
        os.mkdir(path)

    def create_folder_in_folder(self, nome_diretorio_destino, nome_novo_diretorio):
        path = nome_diretorio_destino + nome_novo_diretorio
        os.mkdir(path)