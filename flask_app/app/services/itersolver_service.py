import numpy as np
import io
import base64
import matplotlib.pyplot as plt
from IterSolverLib.itersolvers import IterSolverFacade
from flask_app.app.utils.mtx_utils import read_mtx_file


class IterSolverService:
    def solve(self, file, tolerance, iteration, method):
        A = read_mtx_file(file)
        b = A.dot(np.ones(A.shape[1]))

        solver = IterSolverFacade()
        solver.set_solver(method)
        solution, execution_time, iterations, residuals, times, solutions = solver.solve(A, b, tolerance, iteration)
        print(f'File processed successfully with solution {solution}')

        images = self.generate_plots(residuals, times, solutions, method)

        return {
            "solution": solution.tolist(),
            "execution_time": execution_time,
            "iterations": iterations,
            "images": images
        }

    def generate_plots(self, residuals, times, solutions, method):
        return [self.plot_convergence(residuals, method),
                self.plot_execution_time(times),
                self.plot_solution_evolution(solutions)]

    def plot_convergence(self, residuals, method):
        """Generate a convergence plot (Residual vs Iterations)"""
        fig, ax = plt.subplots()
        ax.semilogy(residuals, marker='o', linestyle='-', label=method)
        ax.set_xlabel("Iterations")
        ax.set_ylabel("||Ax - b||")  # Residuo
        ax.set_title("Method Convergence")
        ax.legend()
        return self.save_plot_as_image(fig)

    def plot_execution_time(self, times):
        """Generates graph of execution time per iteration"""
        fig, ax = plt.subplots()
        ax.plot(times, marker='o', linestyle='-', label="Tempo per iterazione")
        ax.set_xlabel("Iterazioni")
        ax.set_ylabel("Tempo (s)")
        ax.set_title("Tempo di Esecuzione")
        ax.legend()
        return self.save_plot_as_image(fig)

    def plot_solution_evolution(self, solutions):
        """Generates the graph of the trend of the approximate solution"""
        fig, ax = plt.subplots()
        for i in range(len(solutions[0])):  # Plotta ogni componente della soluzione
            ax.plot([sol[i] for sol in solutions], marker='o', linestyle='-', alpha=0.5)
        ax.set_xlabel("Iterazioni")
        ax.set_ylabel("Valori delle Componenti della Soluzione")
        ax.set_title("Evoluzione della Soluzione")
        return self.save_plot_as_image(fig)

    def save_plot_as_image(self, fig):
        """Saves the graph to a buffer and returns it in base64 format"""
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
