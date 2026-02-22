"use strict";

// Protege a página
if (localStorage.getItem("atelier_logado") !== "true") {
    window.location.href = "/";
}

// Botão voltar
document.querySelector("#btn-voltar").addEventListener("click", function () {
    window.location.href = "/home";
});

const artes = document.querySelectorAll(".arte");
let favoritos = JSON.parse(localStorage.getItem("atelier_favoritos")) || [];

artes.forEach(arte => {
    const id = arte.dataset.id;

    if (favoritos.includes(id)) {
        arte.classList.add("favorito");
        arte.querySelector(".estrela").textContent = "★";
    }

    arte.querySelector(".estrela").addEventListener("click", function () {
        if (favoritos.includes(id)) {
            favoritos = favoritos.filter(item => item !== id);
            arte.classList.remove("favorito");
            this.textContent = "☆";
        } else {
            favoritos.push(id);
            arte.classList.add("favorito");
            this.textContent = "★";
        }

        localStorage.setItem("atelier_favoritos", JSON.stringify(favoritos));
    });
});

document.querySelector("#filtro-favoritos").addEventListener("change", function () {
    artes.forEach(arte => {
        if (this.checked && !arte.classList.contains("favorito")) {
            arte.style.display = "none";
        } else {
            arte.style.display = "block";
        }
    });
});


document.querySelectorAll(".btn-apagar").forEach(botao => {
    botao.addEventListener("click", function () {

        const idArte = this.dataset.id;

        if (!confirm("Deseja realmente apagar esta arte?")) {
            return;
        }

        fetch("/arte/apagar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: Number(idArte)
            })
        })
        .then(response => response.json())
        .then(resultado => {
            if (resultado.sucesso) {
                // remove o card inteiro da tela
                this.closest(".arte").remove();
            } else {
                alert(resultado.erro || "Erro ao apagar a arte");
            }
        })
        .catch(() => {
            alert("Erro de conexão com o servidor");
        });
    });
});