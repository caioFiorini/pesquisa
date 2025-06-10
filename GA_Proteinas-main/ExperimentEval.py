import os
from Arquivo import Arquivo
from diretorio import Diretorio
from rankeamento import Rankeamento
from valida import valida_experimento

DIRETORIO_PATH = os.path.abspath(".outputs")
EXPERIMENTO_PATH_ = os.path.abspath("./Experimentos")
RESULTADOS_PATH = os.path.abspath("./Resultados_teste")

class ExperimentEval:
    def __init__(self,
                 class_name_test_file,
                 individual_size):
        self.class_name_test_file = class_name_test_file
        self.individual_size = individual_size
        
    def exec_final_ranking(self):
        rank = Rankeamento()
        arquivo = Arquivo()
        diretorio = Diretorio(DIRETORIO_PATH)
        diretorio.remove_arquivos(RESULTADOS_PATH)
        rank.junta_arquivos(EXPERIMENTO_PATH_, RESULTADOS_PATH)
        colunas = rank.processa_arquivos_teste(EXPERIMENTO_PATH_, RESULTADOS_PATH, self.individual_size)
        colunas_para_filtrar = [item[0] for item in colunas]  
        colunas_tratadas = [int(coluna.split(" ")[-1].strip()) for coluna in colunas_para_filtrar]
        validacao = valida_experimento()
        dataset = arquivo.retorna_dataset()
        validacao.valida_sem_salvar_modelo(dataset, self.class_name_test_file, colunas_tratadas)