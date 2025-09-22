import os
import logging
from SerializationUtils import SerializationUtils
from ExperimentEval import ExperimentEval
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor

# ====== Constantes de Tags para comunicação ======
TAG_TASK = 1  # A mensagem contém uma tarefa
TAG_RESULT = 2 # A mensagem contém um resultado
TAG_STOP = 0   # Não há mais tarefas (sinal de parada)

DIRETORIO_PATH = os.path.abspath(".outputs")
EXPERIMENTO_PATH = os.path.abspath("./Experimentos")

def compute_one_module(task_data_serialized, start_time, exper_path, mpi_rank=None):
    import traceback
    from ExperimentExec import ExperimentExec
    serializer = SerializationUtils()
    task_cfg = task_data_serialized
    logger = setup_logger(task_cfg.experiment_count, os.getpid())

    worker_info = f"[Worker local | MPI rank {mpi_rank} | pid {os.getpid()} | exper {task_cfg.experiment_count}]"
    logger.info(f"{worker_info} Iniciando experimento...")

    worker_info = f"[Worker local | MPI rank {mpi_rank} | pid {os.getpid()} | exper {task_cfg.experiment_count}]"

    print(f"{worker_info} Iniciando experimento...")

    try:
        executor = ExperimentExec(task_cfg, start_time)
        
        # Log a cada passo do experimento, se o seu executor tiver etapas
        for step, step_name in enumerate(executor.get_steps()):  # exemplo fictício
            logger.info(f"{worker_info} Step {step}: {step_name} iniciando")
            executor.run_step(step)
            logger.info(f"{worker_info} Step {step}: {step_name} finalizado")

        # Se não houver steps detalhados, apenas log no começo/fim
        executor.execute_experiment()
        logger.info("Experimento finalizado com sucesso")

    except Exception as e:
        log_file = os.path.join(exper_path, f"Experimento_{task_cfg.experiment_count}", f"error_pid_{os.getpid()}.log")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, "a") as lf:
            lf.write("Exception in child:\n")
            lf.write(traceback.format_exc())
        print(f"{worker_info} ERRO: {e}")
        logger.error(f"Erro: {e}", exc_info=True)
        return {"task_id": task_cfg.experiment_count, "data": {"genotype": [], "fitness": []}, "error": str(e)}

    # Ler melhores indivíduos
    experiment_folder_path = os.path.join(exper_path, f"Experimento_{task_cfg.experiment_count}")
    melhores = serializer.read_best_individuals(experiment_folder_path)
    serialized = serializer.serialize_individuals(melhores)

    print(f"{worker_info} Experimento finalizado")
    return {"task_id": task_cfg.experiment_count, "data": serialized if serialized else {"genotype": [], "fitness": []}}

def setup_logger(experiment_count, pid):
    log_file = f"./logs/experiment_{experiment_count}_pid_{pid}.log"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger(f"Exp{experiment_count}_PID{pid}")
    logger.setLevel(logging.DEBUG)
    
    if not logger.hasHandlers():
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger
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

    def slave_parallel_loop(self):
        from MpiContext import MPI
        ctx = mp.get_context("fork")
        local_cores = 2

        pending_futures = {}   # future -> task_id
        stop_flag = False

        status = MPI.Status()
        print(f"[Slave {self.rank_parallel}] starting pool with {local_cores} workers", flush=True)
        
        with ThreadPoolExecutor(max_workers=local_cores, mp_context=ctx) as pool:
            # recebe primeiro lote de tarefas do master (via MPI)
            task_list = self.comm_parallel.recv(source=0, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()
            if tag == TAG_STOP:
                print(f"[Slave {self.rank_parallel}] STOP before start.", flush=True)
                return
            if tag != TAG_TASK:
                print(f"[Slave {self.rank_parallel}] unexpected tag {tag}; exiting.", flush=True)
                return

            for t in task_list:
                fut = pool.submit(compute_one_module, t, self.start_time, EXPERIMENTO_PATH, self.rank_parallel)
                pending_futures[fut] = t.experiment_count
                print(f"[Slave {self.rank_parallel}] Tarefa {t.experiment_count} enviada para o pool | Pending: {len(pending_futures)}", flush=True)

            while pending_futures or not stop_flag:
                # checa futuros prontos e envia resultado para master
                done_set = [f for f in list(pending_futures) if f.done()]
                for f in done_set:
                    task_id = pending_futures.pop(f)
                    try:
                        payload = f.result()
                    except Exception as e:
                        payload = {"task_id": task_id, "data": {"genotype": [], "fitness": []}, "error": str(e)}

                    print(f"[Slave {self.rank_parallel}] Tarefa {task_id} concluída | Pending: {len(pending_futures)}", flush=True)

                    self.comm_parallel.isend({"worker_rank": self.rank_parallel,
                                            "result": payload}, dest=0, tag=TAG_RESULT)

                # checa novas tarefas (via MPI) sem bloquear
                while self.comm_parallel.Iprobe(source=0, tag=MPI.ANY_TAG, status=status):
                    incoming = self.comm_parallel.recv(source=0, tag=MPI.ANY_TAG, status=status)
                    itag = status.Get_tag()
                    if itag == TAG_TASK and incoming:
                        for t in incoming:
                            fut = pool.submit(compute_one_module, t, self.start_time, EXPERIMENTO_PATH, self.rank_parallel)
                            pending_futures[fut] = t.experiment_count
                            print(f"[Slave {self.rank_parallel}] Nova tarefa {t.experiment_count} enviada | Pending: {len(pending_futures)}", flush=True)
                    elif itag == TAG_STOP:
                        stop_flag = True
                        print(f"[Slave {self.rank_parallel}] Recebeu STOP sinal.", flush=True)

        print(f"[Slave {self.rank_parallel}] Finalizado.", flush=True)

    
    def master_parallel_loop(self):
        from MpiContext import MPI
        """Master: agenda 1 tarefa por escravo e vai gravando os resultados assim que chegam."""
        tasks = list(self.experiments)
        num_tasks = len(tasks)
        num_workers = self.size_parallel - 1

        if num_workers <= 0 or num_tasks == 0:
            print("[Master] Nothing to do.")
            return

        # Config simples: lote inicial por worker (padrão: cores do nó)
        CHUNK_INICIAL = 2
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
