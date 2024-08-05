import numpy as np
from .iter_solvers_strategy import IterSolverStrategy

class GaussSeidelStrategy(IterSolverStrategy):
    def _solve_iteration(self, A, b, x):
        x_new = np.copy(x)
        for i in range(A.shape[0]):
            s1 = np.dot(A[i, :i], x_new[:i])
            s2 = np.dot(A[i, i+1:], x[i+1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        return x_new
