document.addEventListener("DOMContentLoaded", function () {
    let data = localStorage.getItem("solver_results");

    if (!data) {
        console.error("Errore: Nessun dato trovato in localStorage.");
        alert("Nessun risultato disponibile. Torna alla pagina principale e avvia una nuova analisi.");
        window.location.href = "/";
        return;
    }

    try {
        data = JSON.parse(data);

        if (!data.results || data.results.length === 0) {
            console.error("Errore: Nessun risultato disponibile.");
            alert("I dati dei risultati non sono validi.");
            return;
        }

        const tableBody = document.querySelector("#resultsTable tbody");
        data.results.forEach(result => {
            let row = tableBody.insertRow();
            row.innerHTML = `
                <td>${result.method}</td>
                <td>${result.iterations}</td>
                <td>${(result.residuals.length > 0 ? result.residuals[result.residuals.length - 1].toExponential(2) : "N/A")}</td>
                <td>${result.execution_time.toFixed(4)}</td>
                <td>${result.tolerance}</td>
            `;
        });

        if (data.images && data.images.convergence_plot) {
            document.getElementById("convergencePlot").src = data.images.convergence_plot;
        } else {
            console.error("Grafico della convergenza non disponibile.");
        }

        if (data.images && data.images.execution_time_plot) {
            document.getElementById("executionTimePlot").src = data.images.execution_time_plot;
        } else {
            console.error("Grafico del tempo di esecuzione non disponibile.");
        }

    } catch (error) {
        console.error("Errore durante l'elaborazione dei dati:", error);
        alert("Si è verificato un errore nel recupero dei dati. Controlla la console.");
    }
});

document.getElementById("backButton").addEventListener("click", function () {
    window.location.href = "/";
});
