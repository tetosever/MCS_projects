class IterSolverOutputDTO:
    def __init__(self, index, solutions, residue_absolute, residue_relative, tolerance, iterations, max_iterations, times, execution_time, method, converged):
        self.index = index
        self.solutions = solutions
        self.residue_absolute = residue_absolute
        self.residue_relative = residue_relative
        self.tolerance = float(tolerance)
        self.iterations = iterations
        self.max_iterations = int(max_iterations)
        self.times = times
        self.execution_time = execution_time
        self.method = method
        self.converged = converged

    def __repr__(self):
        return (f"IterSolverOutputDTO(index={self.index}, solutions={self.solutions}, residue_absolute={self.residue_absolute}, "
                f"residue_relative={self.residue_relative}, "f"tolerance={self.tolerance}, "f"iterations={self.iterations}, "
                f"max_iterations={self.max_iterations}, times={self.times}, "f"execution_time={self.execution_time}, method={self.method})"
                f"converged={self.converged}")

    def to_json(self):
        return {
            "index": self.index,
            "solutions": self.solutions,
            "residue_absolute": self.residue_absolute,
            "residue_relative": self.residue_relative,
            "tolerance": self.tolerance,
            "iterations": self.iterations,
            "max_iterations": self.max_iterations,
            "times": self.times,
            "execution_time": self.execution_time,
            "method": self.method,
            "converged": self.converged
        }