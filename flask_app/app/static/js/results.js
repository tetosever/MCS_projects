document.addEventListener("DOMContentLoaded", function () {
    let data = localStorage.getItem("solver_results");

    if (!data) {
        console.error("Errore: Nessun dato trovato in localStorage.");
        window.location.href = "/";
        return;
    }

    try {
        data = JSON.parse(data);

        console.log("DEBUG - Risultati:", data);

        if (!data.results || data.results.length === 0) {
            console.error("Errore: Nessun risultato disponibile.");
            return;
        }

        console.log("DEBUG - results:", data.results);

        const tableBody = document.querySelector("#resultsTable tbody");
        data.results.forEach(result => {
            let row = tableBody.insertRow();
            row.innerHTML = `
                <td>${result.method}</td>
                <td>${result.iterations}</td>
                <td>${result.execution_time.toFixed(4)}</td>
                <td>${(result.residue_absolute.length > 0 ? result.residue_absolute[result.residue_absolute.length - 1] : "N/A")}</td>
                <td>${(result.residue_relative.length > 0 ? result.residue_relative[result.residue_relative.length - 1] : "N/A")}</td>
                <td>${result.tolerance}</td>
                <td>${result.converged}</td>
            `;
        });

        if (data.images) {
            if (data.images.convergence_absolute_plot) {
                document.getElementById("convergenceAbsolutePlot").src = data.images.convergence_absolute_plot;
            } else {
                console.error("Grafico della convergenza assoluta non disponibile.");
            }

            if (data.images.convergence_relative_plot) {
                document.getElementById("convergenceRelativePlot").src = data.images.convergence_relative_plot;
            } else {
                console.error("Grafico della convergenza assoluta non disponibile.");
            }

            if (data.images.execution_time_plot) {
                document.getElementById("executionTimePlot").src = data.images.execution_time_plot;
            } else {
                console.error("Grafico del tempo di esecuzione non disponibile.");
            }

            if (data.images.iterations_barplot) {
                document.getElementById("iterationsBarPlot").src = data.images.iterations_barplot;
            } else {
                console.error("Grafico a barre numero di iterazioni non disponibile.");
            }

            if (data.images.execution_time_barplot) {
                document.getElementById("executionTimeBarPlot").src = data.images.execution_time_barplot;
            } else {
                console.error("Grafico a barre tempi di esecuzione non disponibile.");
            }
        } else {
            console.error("Immagini non disponibili.");
        }
    } catch (error) {
        console.error("Errore durante l'elaborazione dei dati:", error);
    }
});

document.getElementById("backButton").addEventListener("click", function () {
    window.location.href = "/itersolvers";
});
