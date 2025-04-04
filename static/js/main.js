document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("login-form");
    const registerButton = document.getElementById("register-button");

    // Ação do botão de login
    loginForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Evita o reload da página

        let formData = new FormData(this);

        fetch("/login", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirect) {
                window.location.href = data.redirect; // Redireciona para a dashboard
            } else if (data.error) {
                alert(data.error); // Exibe erro
            }
        })
        .catch(error => console.error("Erro:", error));
    });

    // Ação do botão de registro (vai direto para a página de cadastro)
    registerButton.addEventListener("click", function() {
        window.location.href = "/register";
    });
});
