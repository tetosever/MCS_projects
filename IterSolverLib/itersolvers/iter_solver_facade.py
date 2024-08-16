from itersolvers.solvers import JacobiStrategy, GaussSeidelStrategy, GradienteStrategy, GradienteConiugatoStrategy
from itersolvers.iter_solver_strategy import IterSolverContext
from itersolvers.iter_solver_validator import IterSolverValidator

class IterSolverFacade:
    def __init__(self):
        self.context = IterSolverContext()

    def set_solver(self, solver_type):
        if solver_type == 'jacobi':
            self.context.set_strategy(JacobiStrategy())
        elif solver_type == 'gauss_seidel':
            self.context.set_strategy(GaussSeidelStrategy())
        elif solver_type == 'gradient':
            self.context.set_strategy(GradienteStrategy())
        elif solver_type == 'coniugate_gradient':
            self.context.set_strategy(GradienteConiugatoStrategy())
        else:
            raise ValueError("Tipo di solver non riconosciuto")

    def solve(self, A, b, tol, max_iter):
        IterSolverValidator.validate(A, b, max_iter)
        return self.context.solve(A, b, tol, max_iter)
