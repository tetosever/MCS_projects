document.addEventListener("DOMContentLoaded", function() {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code") || "500";
    const message = params.get("message") || "Si è verificato un errore imprevisto";

    document.getElementById("errorCode").textContent = code;
    document.getElementById("errorMessage").textContent = decodeURIComponent(message);
});