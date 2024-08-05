import numpy as np
from .iter_solvers_strategy import IterSolverStrategy

class GradienteStrategy(IterSolverStrategy):
    def _solve_iteration(self, A, b, x):
        r = b - np.dot(A, x)
        alpha = np.dot(r, r) / np.dot(r, np.dot(A, r))
        return x + alpha * r
