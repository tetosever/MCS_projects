class IterSolverOutputDTO:
    def __init__(self, index, solutions, residuals, tolerance, iterations, max_iterations, times, execution_time, method):
        self.index = index
        self.solutions = solutions
        self.residuals = residuals
        self.tolerance = float(tolerance)
        self.iterations = iterations
        self.max_iterations = int(max_iterations)
        self.times = times
        self.execution_time = execution_time
        self.method = method

    def __repr__(self):
        return (f"IterSolverOutputDTO(index={self.index}, solutions={self.solutions}, residuals={self.residuals}, "
                f"tolerance={self.tolerance}, "f"iterations={self.iterations}, max_iterations={self.max_iterations}, "
                f"times={self.times}, "f"execution_time={self.execution_time}, method={self.method})")

    def to_json(self):
        return {
            "index": self.index,
            "solutions": self.solutions,
            "residuals": self.residuals,
            "tolerance": self.tolerance,
            "iterations": self.iterations,
            "max_iterations": self.max_iterations,
            "times": self.times,
            "execution_time": self.execution_time,
            "method": self.method
        }