document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("login-form").addEventListener("submit", function(event) {
        event.preventDefault(); // Evita o reload da página

        let formData = new FormData(this);

        fetch("/login", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())  // Converte a resposta para JSON
        .then(data => {
            if (data.redirect) {
                window.location.href = data.redirect;  // Redireciona corretamente
            } else if (data.error) {
                alert(data.error);  // Exibe erro
            }
        })
        .catch(error => console.error("Erro:", error));
    });
});
