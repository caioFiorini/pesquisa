import mpi4py
mpi4py.rc.initialize = False
from mpi4py import MPI

class MPIContext:
    @staticmethod
    def ensure_mpi():
        if not MPI.Is_initialized():
            MPI.Init()
        return MPI

    # opcional helper
    @staticmethod
    def finalize():
        if MPI.Is_initialized() and not MPI.Is_finalized():
            MPI.Finalize()

