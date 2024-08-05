from abc import ABC, abstractmethod
import numpy as np

class IterSolverStrategy(ABC):
    @abstractmethod
    def _solve_iteration(self, A, b, x):
        pass

    def solve(self, A, b, tol=1e-10, max_iter=20000):
        x = np.zeros_like(b)
        for k in range(max_iter):
            x_new = self._solve_iteration(A, b, x)
            if np.linalg.norm(x_new - x) / np.linalg.norm(b) < tol:
                return x_new
            x = x_new
        raise Exception(f"Metodo non ha converguto in {max_iter} iterazioni")