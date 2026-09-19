document.addEventListener("DOMContentLoaded", () => {
    // Load saved options
    if (localStorage.getItem("dice")) {
        document.getElementById("dice").value = localStorage.getItem("dice");
    }
    if (localStorage.getItem("extra")) {
        document.getElementById("extra").value = localStorage.getItem("extra");
    }
    if (localStorage.getItem("aantal")) {
        document.getElementById("aantal").value = localStorage.getItem("aantal");
    }
    if (localStorage.getItem("modifier")) {
        document.getElementById("modifier").value = localStorage.getItem("modifier");
    }

    // Save options on form submit
    document.querySelector("form").addEventListener("submit", () => {
        localStorage.setItem("dice", document.getElementById("dice").value);
        localStorage.setItem("extra", document.getElementById("extra").value);
        localStorage.setItem("aantal", document.getElementById("aantal").value);
        localStorage.setItem("modifier", document.getElementById("modifier").value);
    });
});