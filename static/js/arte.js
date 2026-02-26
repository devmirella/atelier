
document.addEventListener("DOMContentLoaded", () => {

    // BOTÃO VOLTAR
    document.querySelector("#btn-voltar").addEventListener("click", () => {
        window.location.href = "/home";
    });

    // ESTADO DE FAVORITOS (LOCALSTORAGE)
    let favoritos = JSON.parse(localStorage.getItem("atelier_favoritos")) || [];

    // FUNÇÃO: ATIVAR FAVORITO EM UM CARD
    function ativarFavorito(arte) {
        const id = arte.dataset.id;
        const estrela = arte.querySelector(".estrela");

        if (favoritos.includes(id)) {
            arte.classList.add("favorito");
            estrela.textContent = "★";
        }

        estrela.addEventListener("click", () => {
            if (favoritos.includes(id)) {
                favoritos = favoritos.filter(item => item !== id);
                arte.classList.remove("favorito");
                estrela.textContent = "☆";
            } else {
                favoritos.push(id);
                arte.classList.add("favorito");
                estrela.textContent = "★";
            }

            localStorage.setItem("atelier_favoritos", JSON.stringify(favoritos));
        });
    }

    // ATIVAR FAVORITOS NOS CARDS EXISTENTES   
    document.querySelectorAll(".arte").forEach(ativarFavorito);

    // FILTRO DE FAVORITOS
    document.querySelector("#filtro-favoritos").addEventListener("change", function () {
        document.querySelectorAll(".arte").forEach(arte => {
            if (this.checked && !arte.classList.contains("favorito")) {
                arte.style.display = "none";
            } else {
                arte.style.display = "block";
            }
        });
    });

    // FUNÇÃO: APAGAR ARTE    
    async function apagarArte(id, cardElemento) {
        if (!confirm("Deseja realmente apagar esta arte?")) {
            return;
        }

        try {
            const resposta = await fetch("/arte/apagar", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ id: Number(id) })
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                throw new Error(resultado.erro || "Erro ao apagar");
            }

            cardElemento.remove();

        } catch (erro) {
            console.error(erro);
            alert("Erro ao apagar a arte");
        }
    }
    
    // ATIVAR BOTÃO APAGAR NOS CARDS EXISTENTES
    document.querySelectorAll(".btn-apagar").forEach(botao => {
        botao.addEventListener("click", function () {
            const card = this.closest(".arte");
            apagarArte(this.dataset.id, card);
        });
    });

    // ADICIONAR ARTE (FORMULÁRIO)
    const form = document.getElementById("formArte");
    const inputImagem = document.getElementById("imagemArte");
    const gridArte = document.querySelector(".grid-arte");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const imagem = inputImagem.value.trim();

        if (!imagem) {
            alert("Informe a URL da imagem");
            return;
        }

        try {
            const resposta = await fetch("/arte/adicionar", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ imagem })
            });

            const novaArte = await resposta.json();

            if (!resposta.ok) {
                throw new Error(novaArte.erro || "Erro ao adicionar");
            }

            criarCardArte(novaArte);
            inputImagem.value = "";

        } catch (erro) {
            console.error(erro);
            alert("Erro ao adicionar a arte");
        }
    });

    // FUNÇÃO: CRIAR CARD DE ARTE NO DOM 
    function criarCardArte(arte) {
        const card = document.createElement("div");
        card.classList.add("arte");
        card.dataset.id = arte.id;

        card.innerHTML = `
            <span class="estrela">☆</span>
            <div class="imagem">
                <img src="${arte.imagem}" alt="Arte ${arte.id}">
            </div>
            <button class="btn-apagar" data-id="${arte.id}">Apagar</button>
        `;

        gridArte.prepend(card);

        ativarFavorito(card);

        card.querySelector(".btn-apagar").addEventListener("click", () => {
            apagarArte(arte.id, card);
        });
    }

});