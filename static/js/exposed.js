"use strict";

document.addEventListener("DOMContentLoaded", () => {

  // Seleção de elementos principais
  const grid = document.querySelector(".grid-exposed");
  const form = document.getElementById("formExposed");

  const inputImagem = document.getElementById("imagemExposed");
  const inputTitulo = document.getElementById("tituloExposed");
  const inputTag = document.getElementById("tagExposed");

  const lightbox = document.getElementById("lightboxArte");
  const lightboxImg = document.getElementById("lightboxImg");

  // ─── Ativar abertura/fechamento do card ───────────────────────────────────
  // O clique agora fica no .paper (article) inteiro.
  // Abre ao clicar no .titulo-fita ou no .sketch.
  // Fecha ao clicar no .fechar-card.
  function ativarCard(paper) {
    paper.addEventListener("click", e => {

      // Fechar card
      if (e.target.classList.contains("fechar-card")) {
        paper.classList.remove("aberto");
        return;
      }

      // Não propaga cliques nos botões internos
      if (e.target.closest(".adicionar") || e.target.closest(".btn-apagar")) return;
      if (e.target.closest(".artes")) return;

      // Abre ao clicar no título ou na imagem de capa
      if (
        e.target.classList.contains("titulo-fita") ||
        e.target.closest(".titulo-fita") ||
        e.target.classList.contains("sketch")
      ) {
        paper.classList.toggle("aberto");
      }
    });
  }

  // ─── Ativar botão "ADICIONAR ARTE" ───────────────────────────────────────
  function ativarAdicionarArte(paper) {
    const botao = paper.querySelector(".adicionar");
    if (!botao) return;

    botao.addEventListener("click", e => {
      e.stopPropagation();

      const url = prompt("Cole a URL da arte:");
      if (!url || !url.trim()) return;

      const artes = paper.querySelector(".artes");
      const arte = document.createElement("div");
      arte.className = "arte";

      arte.innerHTML = `
        <span class="fechar-arte">✕</span>
        <img src="${url.trim()}" alt="arte">
      `;
      artes.appendChild(arte);
    });
  }

  // ─── Controle de artes internas (remover + lightbox) ─────────────────────
  document.addEventListener("click", e => {

    // Remover arte
    if (e.target.classList.contains("fechar-arte")) {
      e.stopPropagation();
      const arte = e.target.closest(".arte");
      if (arte && confirm("Deseja remover esta arte?")) {
        arte.remove();
      }
      return;
    }

    // Abrir arte no lightbox (clique na imagem)
    const imagemArte = e.target.closest(".arte img");
    if (imagemArte && lightbox && lightboxImg) {
      lightboxImg.src = imagemArte.src;
      lightbox.style.display = "flex";
    }
  });

  // ─── Fechar lightbox ──────────────────────────────────────────────────────
  if (lightbox) {
    lightbox.addEventListener("click", () => {
      lightbox.style.display = "none";
      lightboxImg.src = "";
    });
  }

  if (lightboxImg) {
    lightboxImg.addEventListener("click", e => e.stopPropagation());
  }

  // ─── Ativar cards já existentes no HTML ───────────────────────────────────
  document.querySelectorAll(".paper").forEach(paper => {
    ativarCard(paper);
    ativarAdicionarArte(paper);
  });

  // ─── Apagar item ──────────────────────────────────────────────────────────
  async function apagarExposed(id, elemento) {
    if (!confirm("Deseja realmente apagar este item?")) return;

    try {
      const resposta = await fetch("/exposed/apagar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: Number(id) })
      });

      const resultado = await resposta.json();

      if (!resposta.ok) {
        throw new Error(resultado.erro || "Erro ao apagar");
      }
      elemento.remove();

    } catch (erro) {
      alert("Erro ao apagar item: " + erro.message);
    }
  }

  // Ativar botão apagar nos itens existentes
  document.querySelectorAll(".btn-apagar").forEach(botao => {
    botao.addEventListener("click", function (e) {
      e.stopPropagation();
      const paper = this.closest(".paper");
      const id = paper.dataset.id;
      apagarExposed(id, paper);
    });
  });

  // ─── Criar card no DOM ────────────────────────────────────────────────────
  function criarCardExposed(item) {
    const article = document.createElement("article");
    article.className = "paper";
    article.dataset.id = item.id;

    article.innerHTML = `
      <img class="sketch" src="${item.imagem}" alt="${item.titulo || ''}">
      <div class="titulo-fita">${item.titulo || ""}</div>

      <div class="card">
        <div class="fechar-card">✕</div>
        <div class="card-conteudo">
          <div class="tag">${item.tag || ""}</div>
          <div class="artes"></div>
          <button class="adicionar">+ Adicionar Arte</button>
        </div>
      </div>

      <button class="btn-apagar">Apagar</button>
    `;

    grid.prepend(article);

    // Ativa interações no novo card
    ativarCard(article);
    ativarAdicionarArte(article);

    // Ativa botão apagar no novo card
    article.querySelector(".btn-apagar").addEventListener("click", (e) => {
      e.stopPropagation();
      apagarExposed(item.id, article);
    });
  }

  // ─── Formulário: adicionar novo exposed ───────────────────────────────────
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
          body: JSON.stringify({ imagem, titulo, tag })
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