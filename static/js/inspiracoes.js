// Espera o HTML inteiro ser carregado antes de rodar qualquer JavaScript
document.addEventListener("DOMContentLoaded", () => {

    
    const imagens = document.querySelectorAll(".inspo-img"); // Seleciona todas as imagens renderizadas 
    const lightbox = document.getElementById("lightbox"); // Seleciona o lightbox
    const lightboxImg = lightbox.querySelector("img"); // Seleciona a imagem dentro do lightbox 

    // Adiciona um evento de clique para cada imagem, que ao ser clicada, exibe a imagem no lightbox
    imagens.forEach(img => {
        img.addEventListener("click", () => {
            lightboxImg.src = img.src;
            lightbox.style.display = "flex";
        });
    });

    // Fecha o lightbox ao clicar fora da imagem
    lightbox.addEventListener("click", () => {
        lightbox.style.display = "none";
        lightboxImg.src = "";
    });

    // Seleciona input onde o usuário digita o nome da imagem 
    const inputImagem = document.querySelector("#imagemInput");

    // Seleciona o botão que será clicado para adicionaar a inspiração
    const botaoAdicionar = document.querySelector("#btnAdicionar");

    // Seleciona o parágrafo onde vamos mostrar mensagens ao usuário
    const mensagem = document.querySelector("#mensagem");

    // Adiciona um ouvinte de evento ao botão
    // Esse código só roda quando o botão for clicado 
    botaoAdicionar.addEventListener("click", function () {
        const arquivo = inputImagem.files[0];

        if (!arquivo) {
            mensagem.textContent = "Por favor, Selecione uma imagem.";
            return;
        }

        const formData = new FormData();
        formData.append("imagem", arquivo);

        fetch("/inspiracoes/adicionar", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())  // Quando o backend responder, converte a resposta para JSON
        .then(data => {  // Quanddo o JSON estiver pronto, usamos os dados retornados
            mensagem.textContent = data.mensagem; // Mostra mensagem enviada pelo backend na página
            inputImagem.value = ""; 
            location.reload();  // Recarrega a página para mostrar a nova inpiração adicionada
        })
        
        .catch(() => {
            mensagem.textContent = "Erro ao adicionar inspiração. Tente novamente.";
        });
    });
    
    // Apagar inspiração 
    // querySelectorAll retorna uma lista (NodeList)
    document.querySelectorAll(".btn-apagar").forEach(botao => {
        botao.addEventListener("click", function () {
            // this aqui é o botão que foi clicado e closest(".paper") sobe no HTML até encontrar o card pai
            const card = this.closest(".paper");
            const id = Number(card.dataset.id); 
            console.log("ID ENVIADO:", id);

            // Abre uma confirmação no navegador e se o usuário clicar em "cancelar", tudo para aqui
            if (!confirm("Deseja apagar esta inspiração?")) {
                return;
            }
            // Envia uma requisição para o backend pedindo para apagar
            fetch("/inspiracoes/apagar", { 
                // Método POST (estamos enviando dados)
                method: "POST",
                headers: {
                    "Content-type": "application/json"
                },
                // Envia o id da inspiração que deve ser apagada
                body: JSON.stringify({
                    id: id
                })
            })
            // Esse .then recebe a Resposta do servidor (não os dados ainda)
            .then(res => {
                if(!res.ok) {
                    throw new Error("Erro ao apagar inspiração.");
                }
                return res.json() // Se chegou ate aqui, significa que o backend apagou com sucesso
            })
            // Esse .the só executa se o anterior não 
            .then(() => {
                card.remove();
            })
            
            // So entra aqui se algum erro aconteceu
            .catch(() => {
                alert("Erro ao apagar inspiração.");
            });
        });

    });

});



        