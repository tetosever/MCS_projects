document.getElementById("image").addEventListener("change", function(event) {
    let file = event.target.files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById("originalImg").src = e.target.result;
            document.getElementById("originalImg").style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});

function validateForm(imageFile, blockSize, frequencyThreshold) {
    let valid = true;

    document.getElementById("image").classList.remove("invalid-input");
    document.getElementById("block_size").classList.remove("invalid-input");
    document.getElementById("frequency_threshold").classList.remove("invalid-input");

    if (!imageFile) {
        console.error("Non é stata inserita nessuna immagine!");
        valid = false;
        document.getElementById("image").classList.add("invalid-input");
    }

    if (!blockSize || blockSize < 1) {
        console.error("Valore della dimensione del blocco non valido");
        valid = false;
        document.getElementById("block_size").classList.add("invalid-input");
    }

    if (!frequencyThreshold || frequencyThreshold < 0 || frequencyThreshold > (2 * blockSize) - 2) {
        console.error("Il valore della frequenza inserita non é valido!");
        valid = false;
        document.getElementById("frequency_threshold").classList.add("invalid-input");
    }

    return valid;
}

function uploadImage() {
    let formData = new FormData();
    let imageFile = document.getElementById("image").files[0];
    let blockSize = document.getElementById("block_size").value;
    let frequencyThreshold = document.getElementById("frequency_threshold").value;

   if (!validateForm(imageFile, blockSize, frequencyThreshold)) {
        return;
   }

    formData.append("image", imageFile);
    formData.append("block_size", blockSize);
    formData.append("frequency_threshold", frequencyThreshold);

    document.getElementById("processedImg").style.display = "none";
    document.getElementById("loadingIndicator").style.display = "block";

    fetch("/api/process_image", {
        method: "POST",
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                window.location.href = `/error?code=${errorData.status_code}&message=${encodeURIComponent(errorData.message)}`;
                throw new Error(`Errore ${errorData.status_code}: ${errorData.message}`);
            });
        }
        return response.blob();
    })
    .then(blob => {
        let url = URL.createObjectURL(blob);
        document.getElementById("processedImg").src = url;
        document.getElementById("processedImg").style.display = "block";
    })
    .catch(error => console.error("Errore durante l'upload:", error))
    .finally(() => {
        document.getElementById("loadingIndicator").style.display = "none";
    });
}

document.getElementById("apply-method-button").addEventListener("click", uploadImage);

document.getElementById("backButton").addEventListener("click", function () {
        window.location.href = "/";
    });