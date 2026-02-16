from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/arte")
def arte():
    return render_template("arte.html")

@app.route("/exposed")
def exposed():
    return render_template("exposed.html")

@app.route("/inspiracoes")
def inspiracoes():
    """
    Esta rota agora Não cria inspirações no código.
    Ela lê os dados de um arquivo JSON. 
    """
    # Caminho absoluto para o arquivo inspiracoes.json
    caminho_json = os.path.join(
        app.root_path,
        "data",
        "inspiracoes.json"
    )
    # Abre o arquivo JSON em modo leitura
    with open(caminho_json, "r", encoding="utf-8") as arquivo:
        inspiracoes = json.load(arquivo)

    # Envia a lista para o template inspiracoes.html
    return render_template("inspiracoes.html", inspiracoes=inspiracoes)

@app.route("/inspiracoes/adicionar", methods=["POST"])
def adicionar_inspiracao():
    """
    Rota responsável por adicionar
    uma nova inspiração ao JSON.
    (ainda sem interface)
    """

    # Caminho do arquivo JSON
    caminho_json = os.path.join(
        app.root_path,
        "data",
        "inspiracoes.json"
    )

    # Dados recebidos no Post (JSON)
    dados = request.get_json()

    # Validação simples
    if not dados or "imagem" not in dados:
        return jsonify({
            "erro": "Campo 'imagem' é obrigatório."
        }), 400
    
    # Abre o JSON atual
    with open(caminho_json, "r", encoding="utf-8") as arquivo:
        inspiracoes = json.load(arquivo)

    # Calcula o próximo ID
    if inspiracoes:
        ultimo_id = max(item["id"] for item in inspiracoes)
    else:
        ultimo_id = 0

    novo_id = ultimo_id + 1   

    # Adiciona a nova inspiração com id
    inspiracoes.append({
        "id": novo_id,
        "imagem": dados["imagem"]
    })

    # Salva de volta no arquivo JSON
    with open(caminho_json, "w", encoding="utf-8") as arquivo:
        json.dump(inspiracoes, arquivo, ensure_ascii=False, indent=2)

    # Resposta simples de sucesso
    return jsonify({
        "mensagem": "Inspiração adicionada com sucesso!"
    }), 201

@app.route("/inspiracoes/apagar", methods=["POST"])
def apagar_inspiracao():
    """
    Rota responsável por apagar uma inspiração
          existente pelo id
    """
    # Caminho do arquivo JSON
    caminho_json = os.path.join(
        app.root_path,
        "data",
        "inspiracoes.json"
    )

    # Dados recebidos no POST (JSON)
    dados = request.get_json()
    # Validação básica: precisa ter id 
    if not dados or "id" not in dados:
        return jsonify({
            "erro": "Campo 'id' é obrigatório."
        }), 400
    id_para_apagar = dados["id"]

    # Abre o JSON atual
    with open(caminho_json, "r", encoding="utf-8") as arquivo:
        inspiracoes = json.load(arquivo)
    # Filtra removendo apenas o item com o id fornecido
    novas_inspiracoes = [
        item for item in inspiracoes if item["id"] != id_para_apagar
    ]
    # Se nada foi removido, o id não existia
    if len(novas_inspiracoes) == len(inspiracoes):
        return jsonify({
            "erro": "Inspiração não encontrada."
        }), 404
    # Salva o JSON atualizado
    with open(caminho_json, "w", encoding="UTF-8") as arquivo:
        json.dump(novas_inspiracoes, arquivo, ensure_ascii=False, indent=2)
    
    # Resposta de sucesso
    return jsonify({
        "mensagem": "Inspiração apagada com sucesso!"
    }), 200

#Execução do App
if __name__ == "__main__":
    app.run(debug=True)
    