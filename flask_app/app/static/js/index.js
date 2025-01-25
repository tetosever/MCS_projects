document.addEventListener("DOMContentLoaded", function () {
    const formContainer = document.getElementById("form-container");
    const addFormButton = document.getElementById("add-form");
    const removeFormButton = document.getElementById("remove-form");
    const submitButton = document.getElementById("apply-method-button");

    let formCount = 0;
    const maxForms = 4;
    const minForms = 1;

    function createForm(index) {
        const formDiv = document.createElement("div");
        formDiv.classList.add("form-instance");
        formDiv.setAttribute("id", `form-${index}`);
        formDiv.innerHTML = `
            <h3>Metodo ${index + 1}</h3>
            <div class="form-group">
                <label for="file-${index}">Scegli un file .mtx:</label>
                <input type="file" id="file-${index}" name="file-${index}" accept=".mtx">
            </div>
            <div class="form-group">
                <label for="tolerance-${index}">Valore della tolleranza:</label>
                <input type="number" id="tolerance-number-${index}" name="tolerance_number" step="any" value="0.0001">
                <input type="text" id="tolerance-scientific-${index}" name="tolerance_scientific"
                       pattern="^-?\\d+(\\.\\d+)?([eE][-+]?\\d+)?$"
                       title="Inserisci un numero in notazione scientifica (es. 1e-3, 2.5E6)"
                       style="display: none;" value="1e-3">
                <input type="checkbox" id="tolerance-notation-checkbox-${index}" name="scientific">
                <label for="tolerance-notation-checkbox-${index}">Usa notazione scientifica</label>
            </div>
            <div class="form-group">
                <label for="iteration-${index}">Numero massimo di iterazioni:</label>
                <input type="number" id="iteration-${index}" name="iteration" value="20000">
            </div>
            <div class="form-group">
                <label for="method-${index}">Metodo iterativo:</label>
                <select id="method-${index}" name="methodList">
                    <option value="jacobi">Jacobi</option>
                    <option value="gauss_seidel">Gauss-Seidel</option>
                    <option value="gradient">Gradient</option>
                    <option value="coniugate_gradient">Coniugate Gradient</option>
                </select>
            </div>
        `;
        return formDiv;
    }

    function updateButtons() {
        addFormButton.disabled = formCount >= maxForms;
        removeFormButton.disabled = formCount <= minForms;
    }

    function addForm() {
        if (formCount < maxForms) {
            const newForm = createForm(formCount);
            formContainer.appendChild(newForm);
            formCount++;
            updateButtons();
        }
    }

    function removeForm() {
        if (formCount > minForms) {
            formContainer.removeChild(formContainer.lastElementChild);
            formCount--;
            updateButtons();
        }
    }

    addFormButton.addEventListener("click", addForm);
    removeFormButton.addEventListener("click", removeForm);

    addForm();

    submitButton.addEventListener("click", function (event) {
        event.preventDefault();

        let formData = new FormData();
        let dataList = [];

        for (let i = 0; i < formCount; i++) {
            let fileInput = document.getElementById(`file-${i}`);
            let toleranceNumber = document.getElementById(`tolerance-number-${i}`).value;
            let toleranceScientific = document.getElementById(`tolerance-scientific-${i}`).value;
            let tolerance = toleranceNumber ? toleranceNumber : toleranceScientific;
            let iteration = document.getElementById(`iteration-${i}`).value;
            let method = document.getElementById(`method-${i}`).value;

            let obj = {
                index: i,  // Assicura che il backend sappia a quale form appartiene
                tolerance: tolerance,
                max_iterations: iteration,
                method: method
            };

            dataList.push(obj);

            if (fileInput.files.length > 0) {
                formData.append(`file-${i}`, fileInput.files[0]);  // Associa il file al form giusto
            } else {
                formData.append(`file-${i}`, new Blob(), "empty.txt");  // Segnaposto per evitare buchi
            }
        }

        formData.append("data", JSON.stringify(dataList));

        console.log("DEBUG - File inviati:", [...formData.entries()].map(([key, value]) => `${key}: ${value.name}`));
        console.log("DEBUG - Dati inviati:", dataList);

        document.getElementById("loading").style.display = "block";

        fetch("/api/apply", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("DEBUG - Risposta dal server:", data);
            if (data.message) {
                localStorage.setItem("solver_results", JSON.stringify(data));
                window.location.href = "/results";
            }
        })
        .catch(error => {
            console.error("DEBUG - Errore:", error);
            alert("Errore durante l'elaborazione!");
        });
    });
});