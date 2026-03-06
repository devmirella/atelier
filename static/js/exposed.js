"use strict";

 document.addEventListener("DOMContentLoaded", () => {
  
  // Seleção de elementos principais
  const grid = document.querySelector(".grid-exposed");
  const form = document.getElementById("formExposed");

  const inputImagem = document.getElementById("imagemExposed");
  const inputTitulo = document.getElementById("tituloExposed");
  const inputTag = document.getElementById("tagExposed");

  function ativarCard(card) {
    card.addEventListener("click", e => {
      // Fechar card
      if (e.target.classList.contains("fechar-card")) {
          card.classList.remove("aberto");
        return;
      }
      // Só abre se clicar na capa
      if (!e.target.closest(".card-capa") && !e.target.classList.contains("sketch")) return; // Permite clique apenas na capa do card ou no sketch

      card.classList.toggle("aberto");
    });
  }

  // Função: Ativar botão "ADICIONAR ARTE"
  function ativarAdicionarArte(card) {
    const botao = card.querySelector(".adicionar");

    if (!botao) return;

    botao.addEventListener("click", e => {
      e.stopPropagation();

      const url = prompt("Cole a URL da arte");

      if (!url) return;

      const artes = card.querySelector(".artes");
      const arte = document.createElement("div");
      arte.className = "arte";

      arte.innerHTML = `
        <span class="fechar-arte">X</span>
        <img src="${url}">
      `;
      artes.appendChild(arte);
    });
  }

  // Função: Ativar expandir arte / fechar arte
  document.addEventListener("click", e => {

    // Clica no X
    if (e.target.classList.contains("fechar-arte")) {
      e.stopPropagation();

      const arte = e.target.closest(".arte");

      if (confirm("Deseja remover esta arte?")) {
        arte.remove();
      }
      return;
    }
    const arte = e.target.closest(".arte");

    if (!arte) return;

    document.querySelectorAll(".arte").forEach(a =>
      a.classList.remove("expandida")
    );

    arte.classList.add("expandida");
  });

  // Ativar interação dos cards existentes
  document.querySelectorAll(".card").forEach(card => {
    ativarCard(card);
    ativarAdicionarArte(card);
  });

  // Função apagar item do exposed
  async function apagarExposed(id, elemento) {
    if (!confirm("Deseja realmente apagar este item?")) return;

    try {
      const resposta = await fetch("/exposed/apagar", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ id: Number(id) })
      });

      const resultado = await resposta.json();

      if (!resposta.ok) {
        throw new Error(resultado.erro || "Erro ao apagar");
      }
      elemento.remove();
    } catch (erro) {
      alert("Erro ao apagar item");
    }
  }

  // Ativar botão apagar nos itens existentes
  document.querySelectorAll(".btn-apagar").forEach(botao => {
    botao.addEventListener("click", function () {

      const card = this.closest(".paper");
      const id = card.dataset.id;

      apagarExposed(id, card);
    });
  });

  // Função: Criar card exposed no DOM
  function criarCardExposed(item) {
    const article = document.createElement("article");

    article.className = "paper";
    article.dataset.id = item.id;

    article.innerHTML = `
    <img class="sketch" src="${item.imagem}" >

    <div class="cap">
      <span>${item.titulo || ""}</span>
    </div>

    <div class="card">
      <div class="fechar-card">X</div>
      <div class="card-capa">${item.tag || ""}</div>

      <div class="card-conteudo">
        <div class="artes"></div>
        <button class="adicionar">Adicionar arte</button>
      </div>
    </div>  

    <button class="btn-apagar" data-id="${item.id}">Apagar</button>
    `;
    grid.prepend(article); 

    // Ativa interações no novo card
    const cardInterno = article.querySelector(".card");

    ativarCard(cardInterno);
    ativarAdicionarArte(cardInterno);

    // Ativa botão apagar no novo card
    article.querySelector(".btn-apagar").addEventListener("click", () => {
      apagarExposed(item.id, article);
    });
  }

   // FORMULÁRIO – ADICIONAR NOVO EXPOSED
  if (form) {
    form.addEventListener("submit", async e => {
      e.preventDefault();

      const titulo = inputTitulo.value.trim();
      const imagem = inputImagem.value.trim();
      const tag = inputTag.value.trim();

      if (!imagem) {
        alert("Informe a URL da imagem");
        return;
      }

      try {
        const resposta = await fetch("/exposed/adicionar", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            imagem,
            titulo,
            tag
           })
        });

        const novoItem = await resposta.json();

        if (!resposta.ok) {
          throw new Error(novoItem.erro || "Erro ao adicionar");
        }

        criarCardExposed(novoItem);
        form.reset();

      } catch (erro) {
        console.error(erro);
        alert("Erro ao adicionar item no Exposed");
      }
    });
  }

});
