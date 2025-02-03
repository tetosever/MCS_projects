document.getElementById("backButton").addEventListener("click", function () {
        window.location.href = "/";
    });

document.addEventListener('DOMContentLoaded', function () {
    // Riferimenti agli elementi della pagina
    const executeButton = document.getElementById('apply-method-button');
    const imageElement = document.getElementById('manualImplementationDCT');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const backButton = document.getElementById('backButton');

    executeButton.addEventListener('click', function () {
        loadingIndicator.style.display = 'block';
        imageElement.style.display = 'none';

        fetch('/api/test_dct2')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Errore nella risposta dal server');
                }
                return response.json();
            })
            .then(data => {
                const base64Image = data.manualImplementationDCT;
                imageElement.src = 'data:image/bmp;base64,' + base64Image;
                imageElement.style.display = 'block';
            })
            .catch(error => {
                console.error('Errore durante il recupero dell\'immagine:', error);
            })
            .finally(() => {
                loadingIndicator.style.display = 'none';
            });
    });

    backButton.addEventListener('click', function () {
        window.location.href = "/";
    });
});