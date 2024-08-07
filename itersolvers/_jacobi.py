import numpy as np
from itersolvers.iter_solvers_strategy import IterSolverStrategy

class JacobiStrategy(IterSolverStrategy):
    def _solve_iteration(self, A, b, x):
        D = np.diag(A)
        R = A - np.diagflat(D)
        return (b - np.dot(R, x)) / D
