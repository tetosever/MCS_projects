function toggleInput() {
    var checkbox = document.getElementById("tolerance-notation-checkbox");
    var numberInput = document.getElementById("tolerance-number");
    var scientificInput = document.getElementById("tolerance-scientific");

    if (checkbox.checked) {
        numberInput.style.display = "none";
        scientificInput.style.display = "inline";
    } else {
        numberInput.style.display = "inline";
        scientificInput.style.display = "none";
    }
}