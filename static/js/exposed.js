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
  // Expandir / fechar arte
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

  // Integração com BACKEND
  document.addEventListener("DOMContentLoaded", () => {

    // Seleção de elementos principais
    const grid = document.querySelector(".grid-exposed");
    const form = document.getElementById("formExposed");
    const inputImagem = document.getElementById("imagemExposed");

    // Apagar Exposed
    async function apagarExposed(id, cardElemento) {
      if (!confirm("Deseja realmente apagar este item?")) return;
  
      try {
        const resposta = await fetch("/exposed/apagar", {
          method: "POST", 
          headers: { "Content-type": "application/json" },
          body: JSON.stringify({ id: Number(id)})
        });

        // Converte a resposta do servidor em JSON
        const resultado = await resposta.json();
        if (!resposta.ok) {
          throw new Error(resultado.erro || "Erro ao apagar");
        }
        cardElemento.remove();
      } catch (erro) {
        console.log(erro);
        alert("Erro ao apagar item do Exposed");
      }
    }

    // Ativar botão APAGAR nos itens existentes
    document.querySelectorAll(".btn-apagar").forEach(botao => {
      botao.addEventListener("click", function () {
        const card = this.closest("[data-id]"); // Encontra o card mais próximo que possui data-id
        apagarExposed(this.dataset.id, card)
      });
    });

    // Adiciona novo item ao exposed
    if (form) {
        form.addEventListener("submit", async e => {
          e.preventDefault();   // Impede o reload da página

          const imagem = inputImagem.value.trim();
          if (!imagem) {
            alert("Informe a URL da imagem");
            return;
          }
          try {
            // Envia requisição POST para adicionar novo item
            const resposta = await fetch("/exposed/adicionar", {
              method: "POST",
              headers: {"Content-type": "application/json"},
              body: JSON.stringify({ imagem }) // Envia apena a imagem
            });
            const novoItem = await resposta.json(); // Converte a resposta do backend em JSON
            if (!resposta.ok) {
              throw new Error(novoItem.erro || "Erro ao adicionar");
            }
            criarCardExposed(novoItem);
            inputImagem.value = ""

          } catch (erro) {
            console.error(erro); // Loga o erro no console
            alert("Erro ao adicionar item no Exposed");
          }
     });
   }
   // Função: criar CARD no DOM 
   function criarCardExposed(item) {
    const article = document.createElement("article");
    article.classList.add("paper");
    article.dataset.id = item.id;

    article.innerHTML = `
    <img class="sketch" src="${item.imagem}">

    <div class="cap">
      <span>${item.titulo || ""}</span>
      <span class="tag">${item.tag || ""}</span>
    </div> 

    <div class="card">
      <div class="fechar-card">X</div>
      <div class="card-capa">${item.titulo || ""}</div>

      <div class="card-conteudo">
        <div class="artes"></div>
        <button class="adicionar">Adicionar Artes</button>
      </div>
    </div>

    <button class="btn-apagar" data-id="${item.id}">Apagar</button>
    `;
    grid.prepend(article); // Insere o novo card no top do grid

    article.querySelector(".btn-apagar").addEventListener("click", () => {
      apagarExposed(item.id, article);
    });
   }
});