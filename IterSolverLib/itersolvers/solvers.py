import numpy as np
from IterSolverLib.itersolvers.iter_solver_strategy import IterSolverStrategy
from scipy.sparse import diags

class JacobiStrategy(IterSolverStrategy):
    def _solve_iteration(self, A, b, x):
        D = A.diagonal()
        R = A - diags(D)
        return (b - R.dot(x)) / D

class GaussSeidelStrategy(IterSolverStrategy):
    def _solve_iteration(self, A, b, x):
        x_new = np.copy(x)
        A = A.tocsc()
        
        for i in range(A.shape[0]):
            s1 = A[i, :i].dot(x_new[:i])
            s2 = A[i, i+1:].dot(x[i+1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        return x_new
    
class GradienteStrategy(IterSolverStrategy):
    def _solve_iteration(self, A, b, x):
        r = b - A.dot(x)
        alpha = np.dot(r, r) / np.dot(r, A.dot(r))
        return x + alpha * r

class GradienteConiugatoStrategy(IterSolverStrategy):
    def __init__(self):
        self.r = None
        self.p = None
        self.rs_old = None

    def _solve_iteration(self, A, b, x):
        if self.r is None:
            self.r = b - A.dot(x)
            self.p = self.r
            self.rs_old = np.dot(self.r, self.r)

        Ap = A.dot(self.p)
        alpha = self.rs_old / np.dot(self.p, Ap)
        x_new = x + alpha * self.p
        self.r = self.r - alpha * Ap
        rs_new = np.dot(self.r, self.r)
        self.p = self.r + (rs_new / self.rs_old) * self.p
        self.rs_old = rs_new
        return x_new
