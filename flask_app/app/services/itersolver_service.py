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
            solution, execution_time, iterations, residue_absolute, residue_relative, times, solutions, converged = (
                solver.solve(A, b, solver_input.tolerance, solver_input.max_iterations))
            print(f'File processed successfully with solution {solution}')

            results.append(IterSolverOutputDTO(solver_input.index,
                                               solution.tolist(),
                                               residue_absolute,
                                               residue_relative,
                                               solver_input.tolerance,
                                               iterations,
                                               solver_input.max_iterations,
                                               times,
                                               execution_time,
                                               solver_input.method,
                                               converged))

        return results

    def generate_plots(self, results):
        methods = [result.method for result in results]
        residue_absolute = [result.residue_absolute for result in results]
        residue_relative = [result.residue_relative for result in results]
        times = [result.times for result in results]
        iterations = [result.iterations for result in results]
        execution_times = [result.execution_time for result in results]

        return {
            "convergence_absolute_plot": self.plot_absolute_convergence(methods, residue_absolute),
            "convergence_relative_plot": self.plot_relative_convergence(methods, residue_relative),
            "execution_time_plot": self.plot_total_execution_time(methods, times),
            "iterations_barplot": self.plot_iterations_barplot(methods, iterations),
            "execution_time_barplot": self.plot_execution_time_barplot(methods, execution_times)
        }

    def plot_absolute_convergence(self, methods, residue_absolute):
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = self.get_colors(len(methods))

        for i, method in enumerate(methods):
            iterations = range(1, len(residue_absolute[i]) + 1)
            ax.plot(iterations, residue_absolute[i], marker='o', linestyle='-', color=colors[i],
                    label="Metodo " + str(i+1) + ": " + method, linewidth=2, markersize=6)

        ax.set_xlabel("Numero di Iterazioni")
        ax.set_ylabel("Residuo assoluto")
        ax.set_yscale("log")
        ax.set_title("Convergenza dei Metodi Iterativi")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.5)

        return self.save_plot_as_image(fig)

    def plot_relative_convergence(self, methods, residue_relative):
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = self.get_colors(len(methods))

        for i, method in enumerate(methods):
            iterations = range(1, len(residue_relative[i]) + 1)
            ax.plot(iterations, residue_relative[i], marker='o', linestyle='-', color=colors[i],
                    label="Metodo " + str(i+1) + ": " + method, linewidth=2, markersize=6)

        ax.set_xlabel("Numero di Iterazioni")
        ax.set_ylabel("Residuo relativo")
        ax.set_yscale("log")
        ax.set_title("Convergenza dei Metodi Iterativi")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.5)

        return self.save_plot_as_image(fig)

    def plot_total_execution_time(self, methods, times):
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = self.get_colors(len(methods))

        for i, method in enumerate(methods):
            iterations = range(1, len(times[i]) + 1)
            ax.plot(iterations, times[i], marker='o', linestyle='-', color=colors[i],
                    label="Metodo " + str(i+1) + ": " + method, linewidth=2, markersize=6)

        ax.set_xlabel("Step di Calcolo")
        ax.set_ylabel("Tempo di Esecuzione (s)")
        ax.set_yscale("log")
        ax.set_title("Confronto dei Tempi di Esecuzione")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.5)

        return self.save_plot_as_image(fig)

    def plot_iterations_barplot(self, methods, iterations):
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = self.get_colors(len(methods))

        x = np.arange(len(methods))
        bar_width = 0.25

        ax.bar(x, iterations, color=colors, alpha=0.8, width=bar_width)

        xticklabels = [f"Metodo {i + 1}: {method}" for i, method in enumerate(methods)]

        ax.set_xticks(x)
        ax.set_xticklabels(xticklabels)
        ax.set_xlim(-0.5, len(methods) - 0.5)
        ax.set_xlabel("Metodi Iterativi")
        ax.set_ylabel("Numero di Iterazioni")
        ax.set_title("Confronto del Numero di Iterazioni tra i Metodi")
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        return self.save_plot_as_image(fig)

    def plot_execution_time_barplot(self, methods, execution_times):
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = self.get_colors(len(methods))

        x = np.arange(len(methods))
        bar_width = 0.25

        ax.bar(x, execution_times, color=colors, alpha=0.8, width=bar_width)

        xticklabels = [f"Metodo {i + 1}: {method}" for i, method in enumerate(methods)]

        ax.set_xticks(x)
        ax.set_xticklabels(xticklabels)
        ax.set_xlim(-0.5, len(methods) - 0.5)
        ax.set_xlabel("Metodi Iterativi")
        ax.set_ylabel("Tempo di Esecuzione (s)")
        ax.set_title("Confronto dei Tempi di Esecuzione tra i Metodi")
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        return self.save_plot_as_image(fig)

    def get_colors(self, num_colors):
        cmap = cm.get_cmap("tab10", num_colors)  # Usa la palette 'tab10' di Matplotlib
        return [cmap(i) for i in range(num_colors)]

    def save_plot_as_image(self, fig):
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
