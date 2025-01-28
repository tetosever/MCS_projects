document.getElementById("image").addEventListener("change", function(event) {
    let file = event.target.files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById("originalImg").src = e.target.result;
            document.getElementById("originalImg").style.display = "block";

            document.getElementById("originalSize").textContent =
                `Dimensione originale: ${(file.size / 1024).toFixed(2)} KB`;
        };
        reader.readAsDataURL(file);
    }
});

function uploadImage() {
    let formData = new FormData();
    let imageFile = document.getElementById("image").files[0];
    let blockSize = document.getElementById("block_size").value;
    let frequencyThreshold = document.getElementById("frequency_threshold").value;

    if (!imageFile || !blockSize || !frequencyThreshold) {
        alert("Compila tutti i campi!");
        return;
    }

    formData.append("image", imageFile);
    formData.append("block_size", blockSize);
    formData.append("frequency_threshold", frequencyThreshold);

    fetch("/api/process_image", {
        method: "POST",
        body: formData
    })
    .then(response => response.blob().then(blob => {
        let url = URL.createObjectURL(blob);
        document.getElementById("processedImg").src = url;
        document.getElementById("processedImg").style.display = "block";

        let compressedSizeKB = (blob.size / 1024).toFixed(2);
        document.getElementById("compressedSize").textContent =
            `Dimensione compressa: ${compressedSizeKB} KB`;
    }))
    .catch(error => console.error("Errore durante l'upload:", error));
}