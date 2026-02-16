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
