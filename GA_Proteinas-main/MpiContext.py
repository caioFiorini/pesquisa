import mpi4py
mpi4py.rc.initialize = False
from mpi4py import MPI

class MPIContext:
    def ensure_mpi():
        if not MPI.Is_initialized():
            MPI.Init_thread()
        return MPI
