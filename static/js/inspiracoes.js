// Espera o HTML inteiro ser carregado antes de rodar qualquer JavaScript
document.addEventListener("DOMContentLoaded", () => {

    // Seleciona input onde o usuário digita o nome da imagem 
    const inputImagem = document.querySelector("#imagemInput");

    // Seleciona o botão que será clicado para adicionaar a inspiração
    const botaoAdicionar = document.querySelector("#btnAdicionar");

    // Seleciona o parágrafo onde vamos mostrar mensagens ao usuário
    const mensagem = document.querySelector("#mensagem");

    // Adiciona um ouvinte de evento ao botão
    // Esse código só roda quando o botão for clicado 
    botaoAdicionar.addEventListener("click", function () {

        // Pega o valor digitado no input
        const imagemDigitada = inputImagem.value; 

        // Verifica se o usuário não digitou nada
        if (!imagemDigitada) {
            mensagem.textContent = "Por favor, digite o nome da imagem,";
            return;
        }

        // Envia os dados para o backend usando fetch
        fetch("/inspiracoes/adicionar", {

            //Define que o método da requisição é POST
            method: "POST",

            // Define que estamos enviando dados no formato JSON
            headers: {
                "Content-type": "application/json"
            },
            // Converte o objeto JavaScript em JSON
            body: JSON.stringify({
                imagem: imagemDigitada
            })
        })

        
        // Quando o backend responder, converte a resposta para JSON
        .then(res => res.json())
        // Quando o JSON estiver pronto, usamos os dados retornados
        .then(data => {
            // Mostra a mensagem enviada pelo backend na página
            mensagem.textContent = data.mensagem;
            // Limpa o campo de input após o envio
            inputImagem.value = "";
            // Recarrega a página para mostrar a nova inspiração adicionada
            location.reload();
        })
        // Se ocorrer qualquer erro na requisição
        .catch(() => {
            // Mostra mensagem de erro para o usuário
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

            .then(res => res.json())
            .then(() => {
                location.reload();
            })
            // Se acontecer qualquer erro no processo 
            .catch(() => {
                alert("Erro ao apagar inspiração.");
            });
        });

    });

});



        