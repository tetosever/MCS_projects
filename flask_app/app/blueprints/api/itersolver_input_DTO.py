class IterSolverInputDTO:
    def __init__(self, index, file, tolerance, max_iterations, method):
        self.index = index
        self.file = file
        self.tolerance = float(tolerance)
        self.max_iterations = int(max_iterations)
        self.method = method

    def __repr__(self):
        return f"IterSolverInputDTO(index={self.index}, file={self.file.filename}, tolerance={self.tolerance}, max_iterations={self.max_iterations}, method={self.method})"
