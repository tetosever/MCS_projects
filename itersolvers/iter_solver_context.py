class IterSolverContext:
    def __init__(self, strategy=None):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def risolvi(self, A, b, tol=1e-10, max_iter=20000):
        if not self._strategy:
            raise Exception("No iteretion solver is selected")
        return self._strategy.solve(A, b, tol, max_iter)