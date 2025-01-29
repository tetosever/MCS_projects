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

function uploadImage() {
    let formData = new FormData();
    let imageFile = document.getElementById("image").files[0];
    let blockSize = document.getElementById("block_size").value;
    let frequencyThreshold = document.getElementById("frequency_threshold").value;

    if (!imageFile || !blockSize || !frequencyThreshold) {
        console.error("Compila tutti i campi!");
        return;
    }

    formData.append("image", imageFile);
    formData.append("block_size", blockSize);
    formData.append("frequency_threshold", frequencyThreshold);

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
    .catch(error => console.error("Errore durante l'upload:", error));
}