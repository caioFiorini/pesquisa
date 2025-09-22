import os
import re
from MpiContext import MPI
from deap import creator
from ExperimentEval import ExperimentEval
from ExperimentExec import ExperimentExec
import os, time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, FIRST_COMPLETED

# ====== Constantes de Tags para comunicação ======
TAG_TASK = 1  # A mensagem contém uma tarefa
TAG_RESULT = 2 # A mensagem contém um resultado
TAG_STOP = 0   # Não há mais tarefas (sinal de parada)

DIRETORIO_PATH = os.path.abspath(".outputs")
EXPERIMENTO_PATH = os.path.abspath("./Experimentos")
    
class MultiParallelManager:    
    def __init__(
        self,
        comm_parallel,
        size_parallel,
        rank_parallel,
        experiments,
        name_test_file,
        class_name_test_file,
        individual_size,
        start_time
        
    ):
        self.comm_parallel = comm_parallel
        self.size_parallel = size_parallel
        self.rank_parallel = rank_parallel
        self.experiments = experiments
        self.name_test_file = name_test_file
        self.class_name_test_file = class_name_test_file
        self.individual_size = individual_size
        self.start_time = start_time
    
    def run(self):
        """Starts the master or slave logic based on the rank."""
        if self.size_parallel < 2:
            print("Erro: Requires at least 2 MPI processes.")
            self.comm_parallel.Abort(1)

        if self.rank_parallel == 0:
            self.master_parallel_loop()
        else:
            print(f"[Slave {self.rank_parallel}] Starting slave loop.")
            self.slave_parallel_loop()
        
            
    def exec_ranking(self):
        print("Mestre: Starting post-processing...")
        experiment_evaluator = ExperimentEval(self.name_test_file, self.class_name_test_file, self.individual_size)
        experiment_evaluator.exec_final_ranking()
    

    def read_best_individuals(self, experiments_folder):
        """
        Lê os arquivos que contenham 'melhores' no nome dentro da pasta experiments_folder,
        reconstrói os indivíduos com genótipo e fitness.
        """
        print(f"[DEBUG][Rank {self.rank_parallel}] Pasta atual: {os.getcwd()}")
        padrao = r"Individual\('i',\s*\[(.*?)\]\)\(np\.float64\((.*?)\),\s*(.*?)\)"
        individuos = []

        for nome_arquivo in os.listdir(experiments_folder):
            if "melhores" in nome_arquivo.lower() and nome_arquivo.endswith(".txt"):
                caminho_arquivo = os.path.join(experiments_folder, nome_arquivo)

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
        print("[DEBUG] Diretório base:", dir_base)
        print("[DEBUG] Pasta do experimento:", experiment_folder)
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
    
    def _compute_one(self, task_data):
        executor = ExperimentExec(task_data, self.start_time)
        executor.execute_experiment()

        experiment_folder_path = os.path.join(EXPERIMENTO_PATH,
                                              f"Experimento_{task_data.experiment_count}")
        melhores = self.read_best_individuals(experiment_folder_path)
        serialized = self.serialize_individuals(melhores)
        return {
            "task_id": task_data.experiment_count,
            "data": serialized if serialized else {"genotype": [], "fitness": []}
        }
        
    def compute_one_wrapper(args):
        """Função picklável chamada dentro do ProcessPoolExecutor."""
        self_obj, task_data = args
        return self_obj._compute_one(task_data)

        
    def slave_parallel_loop(self):
        ctx = mp.get_context("spawn")
        local_cores = int(os.environ.get("LOCAL_CORES", os.cpu_count()))

        pending_futures = {}   # future -> task_id
        stop_flag = False

        print(f"[Slave {self.rank_parallel}] starting pool with {local_cores} workers")
        with ProcessPoolExecutor(max_workers=local_cores, mp_context=ctx) as pool:
            # 1) receber primeiro lote (bloqueante, simples)
            status = MPI.Status()
            task_list = self.comm_parallel.recv(source=0, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()
            if tag == TAG_STOP:
                print(f"[Slave {self.rank_parallel}] STOP before start.")
                return
            if tag != TAG_TASK:
                print(f"[Slave {self.rank_parallel}] unexpected tag {tag}; exiting.")
                return

            # submete o primeiro lote
            for t in task_list:
                fut = pool.submit(self.compute_one_wrapper, (self, t))
                pending_futures[fut] = t.experiment_count

            # 2) loop principal: enviar resultados assim que prontos e aceitar novos trabalhos
            while pending_futures or not stop_flag:
                # 2.a) enviar resultados prontos (não bloqueia)
                done_set = [f for f in list(pending_futures) if f.done()]
                for f in done_set:
                    task_id = pending_futures.pop(f)
                    try:
                        payload = f.result()
                    except Exception as e:
                        payload = {"task_id": task_id, "data": {"genotype": [], "fitness": []}, "error": str(e)}
                    # envia UM resultado por mensagem (streaming)
                    self.comm_parallel.isend({"worker_rank": self.rank_parallel,
                                            "result": payload}, dest=0, tag=TAG_RESULT)

                # 2.b) drenar novas tarefas se o master topar (checa sem bloquear)
                st = MPI.Status()
                while self.comm_parallel.Iprobe(source=0, tag=MPI.ANY_TAG, status=st):
                    incoming = self.comm_parallel.recv(source=0, tag=MPI.ANY_TAG, status=st)
                    itag = st.Get_tag()
                    if itag == TAG_TASK and incoming:
                        for t in incoming:
                            fut = pool.submit(compute_one_wrapper, (self, t))
                            pending_futures[fut] = t.experiment_count
                    elif itag == TAG_STOP:
                        stop_flag = True
                    else:
                        pass

        print(f"[Slave {self.rank_parallel}] Finalizado.")
    
    def master_parallel_loop(self):
        """Master: agenda 1 tarefa por escravo e vai gravando os resultados assim que chegam."""
        tasks = list(self.experiments)
        num_tasks = len(tasks)
        num_workers = self.size_parallel - 1

        if num_workers <= 0 or num_tasks == 0:
            print("[Master] Nothing to do.")
            return

        # Config simples: lote inicial por worker (padrão: cores do nó)
        CHUNK_INICIAL = int(os.environ.get("LOCAL_CORES", os.cpu_count()))
        next_task_idx = 0
        completed = 0
        active_workers = set(range(1, self.size_parallel))
        
        print(f"[Master] Dispatching {num_tasks} tasks across {num_workers} workers (chunk inicial={CHUNK_INICIAL})")
        
        # 1) lote inicial por worker
        for w in range(1, self.size_parallel):
            if next_task_idx >= num_tasks:
                break
            batch = tasks[next_task_idx : min(next_task_idx + CHUNK_INICIAL, num_tasks)]
            next_task_idx += len(batch)
            print(f"[Master] Sending {len(batch)} tasks iniciais to slave {w}")
            self.comm_parallel.send(batch, dest=w, tag=TAG_TASK)

        inflight_by_worker = {w: 0 for w in range(1, self.size_parallel)}  # estatística leve (opcional)
        
        # 2) loop: recebe resultados 1 a 1 e mantém “top-up” de 1 tarefa por resultado
        while completed < num_tasks and active_workers:
            st = MPI.Status()
            # Espera algum resultado chegar (bloqueante)
            payload = self.comm_parallel.recv(source=MPI.ANY_SOURCE, tag=TAG_RESULT, status=st)
            worker_rank = st.Get_source()

            results_list = payload.get("result", [])
            if isinstance(results_list, dict):
                results_list = [results_list]

            for serialized_ind_data in results_list:
                task_id = serialized_ind_data.get("task_id")
                data = serialized_ind_data.get("data", [])

                # normaliza caso 'data' venha como dict vazio
                if isinstance(data, dict):
                    data = []

                # encontra config
                try:
                    experiment_config = next(exp for exp in self.experiments if exp.experiment_count == task_id)
                except StopIteration:
                    print(f"[WARN][Master] Experiment config not found for task_id={task_id}. Ignorando.")
                    continue

                # grava imediatamente
                print(f"[Master] Writing best individuals for experiment {experiment_config.experiment_count}")
                self.save_best_individuals(data, experiment_config)
                completed += 1
                inflight_by_worker[worker_rank] = max(0, inflight_by_worker[worker_rank] - 1)

                # top-up: para cada resultado, mande 1 nova tarefa se houver
                if next_task_idx < num_tasks:
                    next_task = tasks[next_task_idx]
                    next_task_idx += 1
                    self.comm_parallel.send([next_task], dest=worker_rank, tag=TAG_TASK)
                    inflight_by_worker[worker_rank] += 1
                else:
                    # se foi a última tarefa enviada a todos e este worker ficar ocioso, envia STOP quando esvaziar
                    # (o worker sai sozinho quando receber STOP e terminar o que está pendente)
                    if (completed + sum(inflight_by_worker.values())) >= num_tasks:
                        # todos os trabalhos já têm destino; podemos sinalizar encerramento
                        self.comm_parallel.send(None, dest=worker_rank, tag=TAG_STOP)
                        active_workers.discard(worker_rank)

            # opcional: prints periódicos de progresso
            if completed % 20 == 0:
                print(f"[Master] progresso: {completed}/{num_tasks}")

        # redundância: garante STOP a quem sobrou ativo
        for w in list(active_workers):
            self.comm_parallel.send(None, dest=w, tag=TAG_STOP)

        print(f"[Master] {completed}/{num_tasks} tasks processed.")
        self.exec_ranking()
        print("[Master] Finished.")
