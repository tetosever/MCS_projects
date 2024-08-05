from ._jacobi import JacobiStrategy
from ._gauss_seidel import GaussSeidelStrategy
from ._gradiente import GradienteStrategy
from ._gradiente_coniugato import GradienteConiugatoStrategy
from iter_solver_context import IterSolverContext
from iter_solver_validator import IterSolverValidator

class IterSolver:
    def __init__(self):
        self.context = IterSolverContext()

    def set_solver(self, solver_type):
        if solver_type == 'jacobi':
            self.context.set_strategy(JacobiStrategy())
        elif solver_type == 'gauss_seidel':
            self.context.set_strategy(GaussSeidelStrategy())
        elif solver_type == 'gradiente':
            self.context.set_strategy(GradienteStrategy())
        elif solver_type == 'gradiente_coniugato':
            self.context.set_strategy(GradienteConiugatoStrategy())
        else:
            raise ValueError("Tipo di solver non riconosciuto")

    def solve(self, A, b, tol=1e-10, max_iter=20000):
        IterSolverValidator.validate(A, b, max_iter)
        return self.context.solve(A, b, tol, max_iter)
