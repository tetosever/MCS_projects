import numpy as np
from itersolvers.iter_solvers_strategy import IterSolverStrategy

'''
Il metodo __init__ è stato implementato per GradienteConiugatoStrategy perché il metodo del gradiente coniugato 
richiede l'inizializzazione di alcune variabili (ad esempio, r, p, rs_old) che devono mantenere il loro stato tra 
le iterazioni. Queste variabili sono specifiche dell'algoritmo del gradiente coniugato e non sono necessarie per 
gli altri algoritmi.
'''
class GradienteConiugatoStrategy(IterSolverStrategy):
    def __init__(self):
        self.r = None
        self.p = None
        self.rs_old = None

    def _solve_iteration(self, A, b, x):
        if self.r is None:
            self.r = b - np.dot(A, x)
            self.p = self.r
            self.rs_old = np.dot(self.r, self.r)

        Ap = np.dot(A, self.p)
        alpha = self.rs_old / np.dot(self.p, Ap)
        x_new = x + alpha * self.p
        self.r = self.r - alpha * Ap
        rs_new = np.dot(self.r, self.r)
        self.p = self.r + (rs_new / self.rs_old) * self.p
        self.rs_old = rs_new
        return x_new