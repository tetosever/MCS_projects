from abc import ABC, abstractmethod
import numpy as np
import time

class IterSolverStrategy(ABC):
    @abstractmethod
    def _solve_iteration(self, A, b, x):
        pass

    def solve(self, A, b, tol, max_iter):
        x = np.zeros_like(b)
        start_time = time.time()

        residuals = []  # Lista dei residui
        times = []  # Tempo accumulato
        solutions = []  # Andamento della soluzione

        for k in range(max_iter):
            x_new = self._solve_iteration(A, b, x)
            x_new = x_new.flatten()

            Ax_new = A.dot(x_new)

            if isinstance(Ax_new, np.ndarray):
                residue = np.linalg.norm(Ax_new - b)
            else:
                residue = np.linalg.norm(Ax_new.toarray() - b)

            residuals.append(residue)
            solutions.append(x_new.copy())
            times.append(time.time() - start_time)  # Tempo cumulativo
                        
            if residue < tol * np.linalg.norm(b):
                end_time = time.time()
                execution_time = end_time - start_time
                return x_new, execution_time, k + 1, residuals, times, solutions
            x = x_new
            
        end_time = time.time()
        execution_time = end_time - start_time
        raise Exception(f"Method did not converge in {max_iter} iterations. Time elapsed: {execution_time:.2f} seconds, Iterations: {max_iter}")

class IterSolverContext:
    def __init__(self, strategy=None):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def solve(self, A, b, tol, max_iter):
        if not self._strategy:
            raise Exception("No iteretion solver is selected")
        return self._strategy.solve(A, b, tol, max_iter)