import time

import numpy as np
from IterSolverLib.itersolvers.iter_solver_strategy import IterSolverStrategy
from scipy.sparse import diags, issparse

def to_dense(x):
    """Utility per convertire in array denso, se necessario."""
    return np.ravel(x.toarray()) if hasattr(x, "toarray") else np.ravel(x)

class JacobiStrategy(IterSolverStrategy):
    def precompute(self, A, b):
        if issparse(A):
            A = A.tocsr()  # Conversione in formato CSR per estrarre la diagonale
        self.D = A.diagonal()
        self.R = A - diags(self.D)
        return A, b

    def iterate(self, A, b, x):
        # Calcola il nuovo iterato: x_new = (b - R.dot(x)) / D
        return (b - self.R.dot(x)) / self.D


class GaussSeidelStrategy(IterSolverStrategy):
    def precompute(self, A, b):
        if issparse(A):
            A = A.tocsr()
        return A, b

    def iterate(self, A, b, x):
        x_new = x.copy()
        n = A.shape[0]
        for i in range(n):
            row_start = A.indptr[i]
            row_end = A.indptr[i+1]
            s = 0.0
            diag = None
            for idx in range(row_start, row_end):
                j = A.indices[idx]
                a_ij = A.data[idx]
                if j == i:
                    diag = a_ij
                else:
                    # Per j < i usa x_new (già aggiornato), altrimenti x
                    s += a_ij * (x_new[j] if j < i else x[j])
            if diag is None or diag == 0:
                raise ValueError(f"Zero or missing diagonal element at A[{i},{i}].")
            x_new[i] = (b[i] - s) / diag
        return x_new
    
class GradienteStrategy(IterSolverStrategy):
    def iterate(self, A, b, x):
        Ax = to_dense(A.dot(x))
        r = b - Ax
        Ar = to_dense(A.dot(r))
        alpha = np.dot(r, r) / np.dot(r, Ar)
        return x + alpha * r

class GradienteConiugatoStrategy(IterSolverStrategy):
    def __init__(self):
        self.r = None
        self.p = None
        self.rs_old = None

    def iterate(self, A, b, x):
        if self.r is None:
            Ax = to_dense(A.dot(x))
            self.r = b - Ax
            self.p = self.r.copy()
            self.rs_old = np.dot(self.r, self.r)
        Ap = to_dense(A.dot(self.p))
        alpha = self.rs_old / np.dot(self.p, Ap)
        x_new = x + alpha * self.p
        self.r = self.r - alpha * Ap
        rs_new = np.dot(self.r, self.r)
        self.p = self.r + (rs_new / self.rs_old) * self.p
        self.rs_old = rs_new
        return x_new
