document.addEventListener("DOMContentLoaded", function () {
    let data = localStorage.getItem("solver_results");

    if (data) {
        data = JSON.parse(data);

        document.getElementById("message").innerText = data.message;
        document.getElementById("iterations").innerText = data.iterations;
        document.getElementById("execution_time").innerText = data.execution_time + " secondi";

        const imagesContainer = document.querySelector(".graphs"); // Trova il div dei grafici

        if (data.images && data.images.length > 0) {
            data.images.forEach((imgSrc, index) => {
                const img = document.createElement("img");
                img.src = imgSrc;  // ✅ Imposta il valore Base64 corretto
                img.style.display = "block";
                imagesContainer.appendChild(img);
            });
        }
    }
    localStorage.removeItem("solver_results");

    document.getElementById("back-button").addEventListener("click", function () {
        window.location.href = "/";
    });
});