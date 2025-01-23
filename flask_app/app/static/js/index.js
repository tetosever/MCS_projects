document.getElementById("methodForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let formData = new FormData(this);
    document.getElementById("loading").style.display = "block";

    fetch("/api/apply", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            localStorage.setItem("solver_results", JSON.stringify(data));
            window.location.href = "/results";
        }
    })
    .catch(error => {
        console.error("Errore:", error);
        alert("Errore durante l'elaborazione!");
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const toleranceNumberInput = document.getElementById("tolerance-number");
    const toleranceScientificInput = document.getElementById("tolerance-scientific");
    const toleranceCheckbox = document.getElementById("tolerance-notation-checkbox");

    function toggleToleranceInput() {
        if (toleranceCheckbox.checked) {
            toleranceScientificInput.style.display = "inline";
            toleranceNumberInput.style.display = "none";
            toleranceScientificInput.value = toleranceNumberInput.value !== "" ? toleranceNumberInput.value : "1e-3";
        } else {
            toleranceScientificInput.style.display = "none";
            toleranceNumberInput.style.display = "inline";
            toleranceNumberInput.value = toleranceScientificInput.value !== "" ? parseFloat(toleranceScientificInput.value) : "0.0001";
        }
    }

    toleranceCheckbox.addEventListener("change", toggleToleranceInput);
});

