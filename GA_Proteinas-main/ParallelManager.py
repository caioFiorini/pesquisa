import os
import re
from mpi4py import MPI
from deap import creator
from ExperimentEval import ExperimentEval
from ExperimentExec import ExperimentExec


# ====== Constantes de Tags para comunicação ======
TAG_TASK = 1  # A mensagem contém uma tarefa
TAG_RESULT = 2 # A mensagem contém um resultado
TAG_STOP = 0   # Não há mais tarefas (sinal de parada)

DIRETORIO_PATH = os.path.abspath(".outputs")
EXPERIMENTO_PATH = os.path.abspath("./Experimentos")
    
class ParallelManager:    
    def __init__(
        self,
        comm_parallel,
        size_parallel,
        rank_parallel,
        experiments,
        class_name_test_file,
        individual_size,
        start_time
        
    ):
        self.comm_parallel = comm_parallel
        self.size_parallel = size_parallel
        self.rank_parallel = rank_parallel
        self.experiments = experiments
        self.class_name_test_file = class_name_test_file
        self.individual_size = individual_size
        self.start_time = start_time
    
    def run(self):
        """Starts the master or slave logic based on the rank."""
        if self.size_parallel < 2:
            print("Erro: Requer pelo menos 2 processos MPI.")
            self.comm_parallel.Abort(1)

        if self.rank_parallel == 0:
            self.master_parallel_loop()
        else:
            self.slave_parallel_loop()
        
            
    def exec_ranking(self):
        print("Mestre: Iniciando pós-processamento...")
        experiment_evaluator = ExperimentEval(self.class_name_test_file, self.individual_size)
        experiment_evaluator.exec_final_ranking()
    

    def read_best_individuals(self, experiments_folder):
        """
        Lê os arquivos que contenham 'melhores' no nome dentro da pasta experiments_folder,
        reconstrói os indivíduos com genótipo e fitness.
        """
        print(f"[DEBUG][Rank {self.rank_parallel}] Pasta atual: {os.getcwd()}")
        padrao = r"Individual\('i',\s*\[(.*?)\]\)\(np\.float64\((.*?)\),\s*(.*?)\)"
        individuos = []

        for subpasta in os.listdir(experiments_folder):
            caminho_subpasta = os.path.join(experiments_folder, subpasta)
            if os.path.isdir(caminho_subpasta):
                for nome_arquivo in os.listdir(caminho_subpasta):
                    if "melhores" in nome_arquivo.lower() and nome_arquivo.endswith(".txt"):
                        caminho_arquivo = os.path.join(caminho_subpasta, nome_arquivo)

                        with open(caminho_arquivo, 'r') as f:
                            for linha in f:
                                match = re.search(padrao, linha)
                                if match:
                                    bits = list(map(int, match.group(1).split(',')))
                                    fit1 = float(match.group(2))
                                    fit2 = float(match.group(3))
                                    fitness = (fit1, fit2)

                                    ind = creator.Individual(bits)
                                    ind.fitness.values = fitness
                                    individuos.append(ind)

                        print(f"[INFO] Leu {len(individuos)} indivíduos de '{nome_arquivo}'")
                        return individuos  # Para o primeiro arquivo encontrado

        print("[WARN] Nenhum arquivo com 'melhores' encontrado em:", experiments_folder)
        return []

    def serialize_individuals(self, individuals):
        serialized = []
        for ind in individuals:
            serialized.append({
                "genotype": list(ind),  # O vetor binário
                "fitness": list(ind.fitness.values)
            })
        return serialized
    
    def deserialize_individuals(self, serialized_individuals):
        reconstructed = []
        for data in serialized_individuals:
            ind = creator.Individual(data["genotype"])
            ind.fitness.values = tuple(data["fitness"])
            reconstructed.append(ind)
        return reconstructed
    
    def save_best_individuals(self, individuals, experiment_config):
        file_name = f"seed_{experiment_config.seed}_pop_{experiment_config.pop_size}_gen_{experiment_config.num_gen}_cross_{experiment_config.cross_rate}_muta_{experiment_config.mut_rate}"
        file_name_final = f"Melhores_{file_name}.txt"

        dir_base = experiment_config.output_base_dir
        experiment_folder = f"Experimento_{experiment_config.experiment_count}"
        full_path = os.path.join(dir_base, experiment_folder)

        # Cria diretório se não existir
        os.makedirs(full_path, exist_ok=True)

        caminho_final = os.path.join(full_path, file_name_final)

        with open(caminho_final, "w") as f: 
            for ind in individuals:
                genotype = ind["genotype"]
                fitness = tuple(ind["fitness"])
                f.write(f"Individual('i', {genotype})({fitness})\n")

        print(f"[Mestre] Arquivo '{file_name_final}' salvo em '{full_path}'")
        
    def slave_parallel_loop(self):
        while True:
            status = MPI.Status()
            task_list = self.comm_parallel.recv(source=0, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()

            if tag == TAG_TASK:
                all_serialized = []
                for task_data in task_list:
                    print(f"[Slave {self.rank_parallel}] Executing experiment {task_data.experiment_count}")
                    executor = ExperimentExec(task_data, self.start_time)
                    executor.execute_experiment()
                    
                    experiment_folder_path = os.path.join("./Experimentos", f"Experimento_{task_data.experiment_count}")
                    melhores = self.read_best_individuals(experiment_folder_path)
                    serialized = self.serialize_individuals(melhores)
                    print(f"Escravo {self.rank_parallel}: Enviando resultado para tarefa {task_data}: {serialized}")
                    all_serialized.append({
                        "task_id": task_data.experiment_count,
                        "data": serialized[0] if serialized else {"genotype": [], "fitness": []}
                    })
                    self.comm_parallel.send({"worker_rank": self.rank_parallel, "result": all_serialized}, dest=0, tag=TAG_RESULT)

                # Envia todos os resultados de uma vez
                self.comm_parallel.send({"worker_rank": self.rank_parallel, "result": all_serialized}, dest=0, tag=TAG_RESULT)

            elif tag == TAG_STOP:
                print(f"Escravo {self.rank_parallel}: Recebeu sinal de parada. Encerrando.")
                break
            else:
                print(f"Escravo {self.rank_parallel}: Recebeu tag inesperada {tag}. Ignorando.")

        print(f"Escravo {self.rank_parallel}: Finalizado.")
    
    def master_parallel_loop(self):
        """Função executada pelo processo mestre."""
        num_workers = self.size_parallel - 1
        tasks = self.experiments
        num_tasks = len(tasks)
        print(f"[Master] Dividindo {num_tasks} tarefas entre {num_workers} workers")

        # Divisão equilibrada de tarefas entre os escravos
        task_chunks = [[] for _ in range(num_workers)]
        for i, task in enumerate(tasks):
            worker_index = i % num_workers
            task_chunks[worker_index].append(task)

        # Envia todas as tarefas para cada escravo
        for i, worker_rank in enumerate(range(1, self.size_parallel)):
            print(f"Mestre: Enviando {len(task_chunks[i])} tarefas para escravo {worker_rank}")
            self.comm_parallel.send(task_chunks[i], dest=worker_rank, tag=TAG_TASK)

        # Recebe os resultados de cada escravo
        for _ in range(num_workers):
            status = MPI.Status()
            serialized_results = self.comm_parallel.recv(source=MPI.ANY_SOURCE, tag=TAG_RESULT, status=status)
            worker_rank = status.Get_source()
            print(f"Mestre: Recebeu resultado do escravo {worker_rank}")
            print(f"O conteúdo retornado foi: ", serialized_results["result"])

            for serialized_ind in serialized_results["result"]:
                best_individuals = self.deserialize_individuals(serialized_ind)
                experiment_config = next(exp for exp in self.experiments if exp.experiment_count == serialized_ind["task_id"])
                self.save_best_individuals(best_individuals, experiment_config)

            # Envia sinal de parada
            self.comm_parallel.send(None, dest=worker_rank, tag=TAG_STOP)
    
        print(f"Mestre: Todas as tarefas concluídas.")
        self.exec_ranking()

        print("Mestre: Finalizado.")
