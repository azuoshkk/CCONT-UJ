document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("login-form").addEventListener("submit", function(event) {
        event.preventDefault(); // Evita o reload da página

        let formData = new FormData(this);

        fetch("/login", {
            method: "POST",
            body: formData
        })
        .then(response => response.text())
        .then(data => alert(data))  // Exibe a resposta do Flask
        .catch(error => console.error("Error:", error));
    });
});
