"use strict";

  document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("click", e => {
      if (e.target.classList.contains("fechar-card")) {
        card.classList.remove("aberto");
        return;
      }
      if (!e.target.closest(".card-capa")) return;
      card.classList.toggle("aberto");
    });
  });

  document.querySelectorAll(".adicionar").forEach(botao => {
    botao.addEventListener("click", e => {
      e.stopPropagation();
      const card = e.target.closest(".card");
      const artes = card.querySelector(".artes");

      const arte = document.createElement("div");
      arte.className = "arte";
      arte.innerHTML = `
        <span class="fechar-arte">X</span>
        <img src="https://via.placeholder.com/600x800">
      `;

      artes.appendChild(arte);
    });
  });

  document.addEventListener("click", e => {
    const arte = e.target.closest(".arte");
    if (!arte) return;

    if (e.target.classList.contains("fechar-arte")) {
      arte.classList.remove("expandida");
      return;
    }

    document.querySelectorAll(".arte").forEach(a =>
      a.classList.remove("expandida")
    );

    arte.classList.add("expandida");
  });