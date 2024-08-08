from abc import ABC, abstractmethod
import numpy as np

class IterSolverStrategy(ABC):
    @abstractmethod
    def _solve_iteration(self, A, b, x):
        pass

    def solve(self, A, b, tol=1e-10, max_iter=20000):
        # methods must start from the initial null vector
        x = np.zeros_like(b)
        for k in range(max_iter):
            x_new = self._solve_iteration(A, b, x)
            residue = np.linalg.norm(np.dot(A, x_new) - b)
            if residue < tol * np.linalg.norm(b):
                return x_new
            x = x_new
        raise Exception(f"Method did not convert to {max_iter} iterations")