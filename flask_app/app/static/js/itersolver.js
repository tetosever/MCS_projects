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
            <div class="form-group tolerance-group">
                <div class="label-container">
                    <label for="tolerance-${index}">Valore della tolleranza:</label>
                    <span class="info-icon" data-tooltip="La tolleranza non deve essere un valore piú piccolo di 0.1">ℹ️</span>
                </div>
                <div class="tolerance-inputs">
                    <input type="number" id="tolerance-number-${index}" name="tolerance_number" step="any" value="1e-04">
                </div>
            </div>
            <div class="form-group">
                <div class="label-container">
                    <label for="iteration-${index}">Numero massimo di iterazioni:</label>
                    <span class="info-icon" data-tooltip="Il valore deve essere minimo 20000">ℹ️</span>
                </div>
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
            if (document.getElementById("add-form").disabled) {
                document.getElementById("add-form").disabled = false;
            }
            const newForm = createForm(formCount);
            formContainer.appendChild(newForm);
            formCount++;
            updateButtons();
        }
        else {
            document.getElementById("add-form").disabled = true;
        }
    }

    function removeForm() {
        if (formCount > minForms) {
            if (document.getElementById("remove-form").disabled) {
                document.getElementById("remove-form").disabled = false;
            }
            formContainer.removeChild(formContainer.lastElementChild);
            formCount--;
            updateButtons();
        }
        else {
            document.getElementById("remove-form").disabled = true;
        }
    }

    function validateForm(fileInput, toleranceInput, iterationInput, methodInput) {
        let valid = true;

        if (!fileInput || !toleranceInput || !iterationInput || !methodInput) {
            console.error("Errore: Uno o più campi non esistono nel DOM.");
            return false;
        }

        fileInput.classList.remove("invalid-input");
        toleranceInput.classList.remove("invalid-input");
        iterationInput.classList.remove("invalid-input");
        methodInput.classList.remove("invalid-input");

        if (!fileInput.files.length || !fileInput.files[0].name.endsWith(".mtx")) {
            valid = false;
            fileInput.classList.add("invalid-input");
        }

        let toleranceValue = parseFloat(toleranceInput.value);
        if (isNaN(toleranceValue) || toleranceValue >= 0.1) {
            valid = false;
            toleranceInput.classList.add("invalid-input");
        }

        let iterationValue = parseInt(iterationInput.value, 10);
        if (isNaN(iterationValue) || iterationValue < 20000) {
            valid = false;
            iterationInput.classList.add("invalid-input");
        }

        return valid;
    }

    addFormButton.addEventListener("click", addForm);
    removeFormButton.addEventListener("click", removeForm);

    addForm();

    submitButton.addEventListener("click", function (event) {
        event.preventDefault();

        let formData = new FormData();
        let dataList = [];
        let allValid = true;

        for (let i = 0; i < formCount; i++) {
            let fileInput = document.getElementById(`file-${i}`);
            let toleranceInput = document.getElementById(`tolerance-number-${i}`);
            let iterationInput = document.getElementById(`iteration-${i}`);
            let methodInput = document.getElementById(`method-${i}`);

            if (!fileInput || !toleranceInput || !iterationInput || !methodInput) {
                console.error(`Errore: Il form ${i + 1} ha campi mancanti.`);
                allValid = false;
                continue;
            }

            let isValid = validateForm(fileInput, toleranceInput, iterationInput, methodInput);
            if (!isValid) {
                allValid = false;
                continue;
            }

            let obj = {
                index: i,
                tolerance: toleranceInput.value,
                max_iterations: iterationInput.value,
                method: methodInput.value
            };

            dataList.push(obj);

            if (fileInput.files.length > 0) {
                formData.append(`file-${i}`, fileInput.files[0]);
            } else {
                formData.append(`file-${i}`, new Blob(), "empty.txt");
            }
        }

        if (!allValid) {
            return;
        }

        formData.append("data", JSON.stringify(dataList));

        console.log("DEBUG - File inviati:", [...formData.entries()].map(([key, value]) => `${key}: ${value.name}`));
        console.log("DEBUG - Dati inviati:", dataList);

        document.getElementById("loadingIndicator").style.display = "block";

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
        })
        .finally(() => {
        document.getElementById("loadingIndicator").style.display = "none";
    });
    });

    document.getElementById("backButton").addEventListener("click", function () {
        window.location.href = "/";
    });
});