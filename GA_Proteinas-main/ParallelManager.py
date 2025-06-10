import re
import os
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
        Busca automaticamente o primeiro arquivo contendo 'melhores' no nome dentro da experiments_folder,
        lê os indivíduos e os reconstrói com genótipo e fitness.
        """
        padrao = r"Individual\('i',\s*\[(.*?)\]\)\((.*?)\)"
        individuos = []

        # Busca arquivo com "melhores" no nome
        for nome_arquivo in os.listdir(experiments_folder):
            if "melhores" in nome_arquivo.lower() and nome_arquivo.endswith(".txt"):
                caminho_arquivo = os.path.join(experiments_folder, nome_arquivo)

                with open(caminho_arquivo, 'r') as f:
                    for linha in f:
                        match = re.search(padrao, linha)
                        if match:
                            bits = list(map(int, match.group(1).split(',')))
                            fitness = tuple(map(float, match.group(2).split(',')))

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
                f.write(str(ind) + str(ind.fitness.values) + "\n")

        print(f"[Mestre] Arquivo '{file_name_final}' salvo em '{full_path}'")

            
    def slave_parallel_loop(self):

        while True:
            status = MPI.Status()
            task_data = self.comm_parallel.recv(source=0, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()
            
            if tag == TAG_TASK:
                print(f"[Slave {self.rank_parallel}] Executing experiment {task_data.experiment_count}")
                executor = ExperimentExec(task_data, self.start_time)
                executor.execute_experiment()
                
                melhores = self.read_best_individuals("./Experimentos")
                serialized = self.serialize_individuals(melhores)
                                
                # Cria um resultado
                result = {"task_id": task_data.experiment_count, "result": serialized, "worker_rank": self.rank_parallel}
                print(f"Escravo {self.rank_parallel}: Enviando resultado para tarefa {task_data}: {serialized}")
                # Envia o resultado para o mestre
                self.comm_parallel.send(result, dest=0, tag=TAG_RESULT)
            elif tag == TAG_STOP:
                print(f"Escravo {self.rank_parallel}: Recebeu sinal de parada. Encerrando.")
                break
            else:
                print(f"Escravo {self.rank_parallel}: Recebeu tag inesperada {tag}. Ignorando.")
            
        print(f"Escravo {self.rank_parallel}: Finalizado.")
    
    def master_parallel_loop(self):
        """Função executada pelo processo mestre."""
        num_workers = self.size_parallel - 1

        # 1. Gerar a lista de tarefas
        tasks = self.experiments
        num_tasks = len(tasks)
        task_index = 0
        results = []
        active_workers = 0 # Contador de escravos atualmente trabalhando

        print(f"[Master] Enviando {num_tasks} tarefas para {num_workers} workers")

        # 2. Distribuição inicial de tarefas para todos os escravos disponíveis
        # Envia uma tarefa para cada escravo (se houver tarefas suficientes)
        for worker_rank in range(1, min(self.size_parallel, num_tasks + 1)):
            if task_index < num_tasks:
                task_to_send = tasks[task_index]
                print(f"Mestre: Enviando tarefa inicial {task_to_send} para escravo {worker_rank}")
                self.comm_parallel.send(task_to_send, dest=worker_rank, tag=TAG_TASK)
                task_index += 1
                active_workers += 1
            else:
                # Caso haja mais escravos que tarefas iniciais
                pass

        # 3. Loop principal: receber resultados e enviar novas tarefas
        while active_workers > 0:
            status = MPI.Status()
            # Mestre espera por um resultado de QUALQUER escravo
            serialized_results = self.comm_parallel.recv(source=MPI.ANY_SOURCE, tag=TAG_RESULT, status=status)
            worker_rank = status.Get_source() # Descobre qual escravo enviou
            print(f"Mestre: Recebeu resultado da tarefa {serialized_results['task_id']} do escravo {worker_rank}")
            print(f"\nO conteúdo retornado foi: ", serialized_results["result"])
            best_individuals = self.deserialize_individuals(serialized_results["result"])
            task_id = serialized_results["task_id"]
            experiment_config = next(exp for exp in self.experiments if exp.experiment_count == task_id)

            self.save_best_individuals(best_individuals, experiment_config)
            active_workers -= 1 # Escravo terminou uma tarefa

            # Verificar se ainda há tarefas para enviar
            if task_index < num_tasks:
                # Enviar a próxima tarefa para o escravo que acabou de ficar livre
                task_to_send = tasks[task_index]
                print(f"Mestre: Enviando próxima tarefa {task_to_send} para escravo {worker_rank}")
                self.comm_parallel.send(task_to_send, dest=worker_rank, tag=TAG_TASK)
                task_index += 1
                active_workers += 1 # Escravo começou uma nova tarefa
            else:
                # Não há mais tarefas, enviar sinal de parada para este escravo
                print(f"Mestre: Não há mais tarefas. Enviando sinal de parada para escravo {worker_rank}")
                self.comm_parallel.send(None, dest=worker_rank, tag=TAG_STOP)
                
        print(f"Mestre: Todas as tarefas concluídas.")
        self.exec_ranking(results)

        print("Mestre: Finalizado.")
