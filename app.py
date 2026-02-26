from flask import Flask, render_template, jsonify, request
import json
import os
from pathlib import Path

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/arte")
def arte():
    caminho = Path("data/arte.json")

    if caminho.exists():
        with open(caminho, encoding="utf-8") as f:
            artes = json.load(f)
    else: 
        artes = []
    return render_template("arte.html", artes=artes)

@app.route("/arte/adicionar", methods=["POST"])
def adicionar_arte():
    caminho = Path("data/arte.json") # Caminho relativo para o arquivo arte.json

    # Lê o corpo da requisição
    dados = request.get_json()

    # Validação básica
    if not dados or "imagem" not in dados or dados["imagem"].strip() == "":
        return jsonify({"erro": "URL da imagem é obrigatória"}), 400
    
    # Garante que o arquivo existe
    if not caminho.exists():
        artes = []
    else:
        with open(caminho, encoding="utf-8") as f:
            artes = json.load(f)

    # Gera novo ID
    novo_id = 1
    if artes:
        novo_id = max(item["id"] for item in artes ) + 1

    # Nova arte
    nova_arte = {
        "id": novo_id,
        "imagem": dados["imagem"]
    }

    artes.append(nova_arte)

    # Salva no JSON
    with open(caminho, "w", encoding="utf-8") as f: 
        json.dump(artes, f, ensure_ascii=False, indent=2)

    return jsonify(nova_arte), 201

@app.route("/arte/apagar", methods=["POST"])
def apagar_arte():
    caminho = Path("data/arte.json")

    dados = request.get_json()

    # Validação básica 
    if not dados or "id" not in dados:
        return jsonify({"erro": "ID é obrigatório"}), 400
    
    id_para_apagar = dados["id"]

    # Se o arquivo não existir, não há o que apagar
    if not caminho.exists():
        return jsonify({"erro": "Arquivo de arte não encontrado"}), 404
    
    # Lê o JSON 
    with open(caminho, encoding="utf-8") as f:
        artes = json.load(f)

    # Filtra removendo apenas o ID informado
    artes_filtradas = [arte for arte in artes if arte["id"] != id_para_apagar]

    # Se nada mudou, o ID não existia
    if len(artes) == len(artes_filtradas):
        return jsonify({"erro": "Arte não encontrada"}), 404
    
    # Salva o JSON atualizado
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(artes_filtradas, f, ensure_ascii=False, indent=2)

    return jsonify({"sucesso": True}), 200

@app.route("/exposed")
def exposed():
    caminho = Path("data/exposed.json")

    if caminho.exists():
        with open(caminho, encoding="utf-8") as f:
            exposed = json.load(f)
    else:
        exposed = []

    return render_template("exposed.html", exposed=exposed)

@app.route("/exposed/adicionar", methods=["POST"])
def adicionar_exposed():
    # Define o caminho do arquivo JSON onde as artes do exposed são salvas
    caminho = Path("data/exposed.json")

    dados = request.get_json()
    if not dados or "imagem" not in dados or dados["imagem"].strip() == "":
        return jsonify({"erro": "URL da imagem é obrigatoria"}), 400
    
    # Verifica se o arquivo exposed.json já existe
    if caminho.exists():
        with open(caminho, encoding="utf-8") as f:
            exposed = json.load(f)
    else:
        # Se não existir, inicia uma lista vazia
        exposed = []
    novo_id = 1
    if exposed:
        novo_id = max(item["id"] for item in exposed) + 1
    # Cria um novo item que será salvo no JSON
    novo_item = {
        "id": novo_id,
        "imagem": dados["imagem"],
        "titulo": dados.get("titulo", ""),
        "tag": dados.get("tag", "")
    }
    # Adicionar o novo item á lista existente
    exposed.append(novo_item)
    # Abre o arquivo JSON em modo escrita
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(exposed, f, ensure_ascii=False, indent=2) #  # indent=2 deixa o JSON legível
    # Retorna o item criado como resposta JSON
    return jsonify(novo_item), 201



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
    