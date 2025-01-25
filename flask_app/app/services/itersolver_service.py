import numpy as np
import io
import base64
import matplotlib.pyplot as plt
from matplotlib import cm

from IterSolverLib.itersolvers import IterSolverFacade
from flask_app.app.blueprints.api.itersolvers_output_DTO import IterSolverOutputDTO
from flask_app.app.utils.mtx_utils import read_mtx_file


class IterSolverService:
    def solve(self, solver_inputs):
        results = []
        for solver_input in solver_inputs:
            A = read_mtx_file(solver_input.file)
            b = A.dot(np.ones(A.shape[1]))

            solver = IterSolverFacade()
            solver.set_solver(solver_input.method)
            solution, execution_time, iterations, residuals, times, solutions = (
                solver.solve(A, b, solver_input.tolerance, solver_input.max_iterations))
            print(f'File processed successfully with solution {solution}')

            results.append(IterSolverOutputDTO(solver_input.index,
                                               solution.tolist(),
                                               residuals,
                                               solver_input.tolerance,
                                               iterations,
                                               solver_input.max_iterations,
                                               times,
                                               execution_time,
                                               solver_input.method))

        return results

    def generate_plots(self, results):
        methods = [result.method for result in results]
        residuals = [result.residuals for result in results]
        times = [result.times for result in results]

        return {
            "convergence_plot": self.plot_convergence(methods, residuals),
            "execution_time_plot": self.plot_total_execution_time(methods, times)
        }

    def plot_convergence(self, methods, residuals):
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = self.get_colors(len(methods))

        for i, method in enumerate(methods):
            iterations = range(1, len(residuals[i]) + 1)
            ax.plot(iterations, residuals[i], marker='o', linestyle='-', color=colors[i],
                    label=method, linewidth=2, markersize=6)

        ax.set_xlabel("Step Iterativo")
        ax.set_ylabel("Numero di Iterazioni")
        ax.set_title("Convergenza dei Metodi Iterativi")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.5)

        return self.save_plot_as_image(fig)

    def plot_total_execution_time(self, methods, times):
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = self.get_colors(len(methods))

        for i, method in enumerate(methods):
            iterations = range(1, len(times[i]) + 1)  # Iterazioni 1, 2, ..., N
            ax.plot(iterations, times[i], marker='o', linestyle='-', color=colors[i],
                    label=method, linewidth=2, markersize=6)

        ax.set_xlabel("Step di Calcolo")
        ax.set_ylabel("Tempo di Esecuzione (s)")
        ax.set_title("Confronto dei Tempi di Esecuzione")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.5)

        return self.save_plot_as_image(fig)

    def get_colors(self, num_colors):
        cmap = cm.get_cmap("tab10", num_colors)  # Usa la palette 'tab10' di Matplotlib
        return [cmap(i) for i in range(num_colors)]

    def save_plot_as_image(self, fig):
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
