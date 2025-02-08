from abc import ABC, abstractmethod
import numpy as np
import time

def to_dense(x):
    return np.ravel(x.toarray()) if hasattr(x, "toarray") else np.ravel(x)

class IterSolverStrategy(ABC):
    def precompute(self, A, b):
        """
        Metodo opzionale per effettuare precomputazioni sui dati.
        Ad esempio: conversione della matrice in un formato specifico, estrazione della diagonale, ecc.
        Per impostazione predefinita non fa nulla.
        """
        return A, b

    @abstractmethod
    def iterate(self, A, b, x):
        """
        Metodo astratto che, dato il sistema (A, b) e l'iterato corrente x,
        calcola e restituisce il nuovo iterato.
        """
        pass

    def solve(self, A, b, tol, max_iter):
        """
        Metodo comune che gestisce il ciclo iterativo:
          - Esegue eventuali precomputazioni
          - Calcola la norma di b
          - Esegue il ciclo iterativo controllando il criterio di convergenza
          - Registra residui, tempi ed iterati ad ogni passo
        """
        # Precomputazioni opzionali
        A, b = self.precompute(A, b)

        norm_b = np.linalg.norm(b)
        if norm_b == 0:
            norm_b = 1.0

        x = np.zeros_like(b)
        start_time = time.perf_counter()
        residue_absolute = []
        residue_relative = []
        times = []
        solutions = []
        iterations = 0

        for k in range(max_iter):
            x_new = self.iterate(A, b, x)
            x_new = to_dense(x_new)
            Ax_new = to_dense(A.dot(x_new))
            residue = np.linalg.norm(Ax_new - b)
            residue_absolute.append(residue)
            residue_relative.append(residue / norm_b)
            solutions.append(x_new.copy())
            times.append(time.perf_counter() - start_time)
            iterations += 1

            if residue / norm_b < tol:
                execution_time = time.perf_counter() - start_time
                return (x_new, execution_time, iterations,
                        residue_absolute, residue_relative, times, solutions, True)
            x = x_new

        execution_time = time.perf_counter() - start_time
        return (x, execution_time, iterations,
                residue_absolute, residue_relative, times, solutions, False)

    # Esempio di classe context che utilizza il solver (strategy)


class IterSolverContext:
    def __init__(self, strategy: IterSolverStrategy = None):
        self._strategy = strategy

    def set_strategy(self, strategy: IterSolverStrategy):
        self._strategy = strategy

    def solve(self, A, b, tol, max_iter):
        if self._strategy is None:
            raise Exception("Nessun solver iterativo selezionato.")
        return self._strategy.solve(A, b, tol, max_iter)
